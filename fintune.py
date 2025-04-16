# 微调Qwen2.5-7b-instruct模型，使其能够完成多任务处理

import os
import json
import torch
import logging
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from data_processor import process_training_data
import pandas as pd



# 加载处理后的数据
with open('./event_collector_training_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


messages = pd.DataFrame()
for i in data:
    # Handle both list and non-list items
    items = i if isinstance(i, list) else [i]
    
    for j in items:
        dialogue=[]
        if j.get('round') == 1:
            dialogue.append({'role':'user','content':j.get('user')})
            dialogue.append({'role':'assistant','content':json.dumps(j.get('assistant'))})
        elif j.get('round')==2:
            dialogue.append({'role':'user','content':j.get('round1_context').get('user')})
            dialogue.append({'role':'assistant','content':json.dumps(j.get('round1_context').get('assistant'))})
            dialogue.append({'role':'user','content':j.get('user')})
            dialogue.append({'role':'assistant','content':json.dumps(j.get('assistant'))})
        messages=messages._append({'messages':dialogue},ignore_index=True)

sysprompt="""you are a event information collector. you will follow the steps below:

1.extract  start_time, end_time,priority, category,description of the event from user input
- if related time given, you may use current time to infer. 
(example: user:i will swim next Friday , if current time is 2025-2-25 Tuesday, next Friday should be 2025-2-28 )
-Note: the current time is  {time}, infer based on this time 
- the format for start_time and end_time is YYYY-MM-DD HH:MM

2.identify which fields are missing start_time, end_time,priority, category,description, show them in a list

3.you may infer priority (1-5, 1 is most important), category(Work/Personal/Health) and description by your self
- you may infer the end_time given start_time and possible period of this event

4.show the information collected in a json format

"""
# LINE_BREAK = "<|break|>"
# processed_sysprompt = sysprompt.replace('\n', LINE_BREAK)


from datasets import Dataset
dataset_records=Dataset.from_pandas(pd.DataFrame(messages))
def format_chat_template(row):
    dialogue_list = []
    # 重新排序系统提示的键
    system_prompt = {
        'role': 'system',
        'content': sysprompt.format(time="2025-03-01 21:00")
    }
    dialogue_list.append(system_prompt)
    
    # 重新排序对话消息的键
    for msg in row['messages']:
        ordered_msg = {
            'role': msg['role'],
            'content': msg['content']
        }
        dialogue_list.append(ordered_msg)
    
    row["text"] = tokenizer.apply_chat_template(dialogue_list, tokenize=False) #this will turn json to pure text with special token to separate the roles.
    return row

from transformers import AutoModelForCausalLM, AutoTokenizer
# Load tokenizer
base_model = "Qwen/Qwen2.5-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
# Set pad_token to be the same as eos_token
tokenizer.pad_token = tokenizer.eos_token



dataset_train = dataset_records.map(
    format_chat_template,
    num_proc= 4,
)


from transformers import (
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
)
from peft import (
    LoraConfig,
    PeftModel,
    prepare_model_for_kbit_training,
    get_peft_model,
)
import os, torch, wandb
from datasets import load_dataset
from trl import SFTTrainer, setup_chat_format


new_model = "qwen-2.5-7b-it-scheduler"

if torch.cuda.get_device_capability()[0] >= 8:
    !pip install -qqq flash-attn
    torch_dtype = torch.bfloat16
    attn_implementation = "flash_attention_2"
else:
    torch_dtype = torch.float16
    attn_implementation = "eager"


# QLoRA config

base_model = "Qwen/Qwen2.5-7B-Instruct"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch_dtype,
    bnb_4bit_use_double_quant=True,
)
# Load model
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=bnb_config,
    device_map="auto",
    attn_implementation=attn_implementation
)


import bitsandbytes as bnb
# this part???? if just use k ,q, v
def find_all_linear_names(model):
    cls = bnb.nn.Linear4bit
    lora_module_names = set()
    for name, module in model.named_modules():
        if isinstance(module, cls):
            names = name.split('.')
            lora_module_names.add(names[0] if len(names) == 1 else names[-1])
    if 'lm_head' in lora_module_names:  # needed for 16 bit
        lora_module_names.remove('lm_head')
    return list(lora_module_names)

modules = find_all_linear_names(model)

# LoRA config
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=modules
)
#model, tokenizer = setup_chat_format(model, tokenizer)
model = get_peft_model(model, peft_config)
#Hyperparamter
training_arguments = TrainingArguments(
    output_dir=new_model,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=2,
    optim="paged_adamw_32bit",
    num_train_epochs=1,
    eval_strategy="no",
    eval_steps=0.2,
    logging_steps=1,
    warmup_steps=10,
    logging_strategy="steps",
    learning_rate=2e-4,
    fp16=False,
    bf16=False,
    group_by_length=True,
    report_to="wandb",
    do_eval=False 
)

# Setting sft parameters
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset_train,
   # eval_dataset=dataset_test,
    peft_config=peft_config,
  #  max_seq_length= 1024,  # it is not listed in TrainingArguments, could be set in model or tokenizer
   # dataset_text_field="text",
    #tokenizer=tokenizer,
  #
    args=training_arguments,
   # packing= False,  ## if some input is short pack them to one to more efficient
)

trainer.train()