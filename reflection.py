#periodically analysis each user message and event list



#test qwen performance
import os
from openai import OpenAI
import json
client = OpenAI(
    # If environment variables are not configured, replace the following line with: api_key="sk-xxx",
    api_key="sk-d0d414ae60c04b569db14cd502eeb8bc", 
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)




def get_dialouge(user_id,start,end):

    db=dialogueDatabase()
    dialogue= db.get_by_id(user_id,start,end)
        
    return dialogue

# message

dialogue_prompt=f"""

you are an expert in infer user preference by reading the dialogue.
you will be given some conversations,and you need to identify the user's preference when they clearly state. 
for example in the conversation
user: i do not do sports before 10 am
then you should generate a json like this

user_id is given as {user_id} 
make sure this is a valid json format
{{
'user_id': userid,
'preference':"[ this is a list of preference]"
}}

"""

user_id = 'exampleid123' 
db=dialogueDatabase()
query_result = db.get_by_id(user_id, '2025-04-10 08:30', '2025-04-13 22:30')
dia_hist = list(query_result)


dialogue_text = ""
for record in dia_hist:
    for k in record['message']:
       # print(k)
        dialogue_text += f"role: {k[0]}\n"
        dialogue_text += f"content: {k[1]}\n"




completion = client.chat.completions.create(
    model="qwen2.5-7b-instruct", # This example uses qwen-plus. You can change the model name as needed. Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': dialogue_prompt},
        {'role': 'user', 'content': dialogue_text}],
)
    
#print(completion.model_dump_json()['messages']['content'])
reflection_result=  json.loads(completion.choices[0].message.content)
reflection_json = json.loads(reflection_result.replace("'", '"').replace("\n", ""))
prefer_doc = {
    "type":'dialogue'
    "user_id": reflection_json["user_id"],
    "content": reflection_json["preference"]
}



rf_db=prefereceDatabase()
rf_db.add_prefer(prefer_doc)


#list of preference 
collected_prefer = list(rf_db.get_by_id(user_id))[-1]['content']

# events

event_db=EventDatabase()
start='2025-03-01 08:30'
end='2025-05-01 08:30'
events_list = list( event_db.get_events_by_time_range(start, end))


# Group events by category
from collections import defaultdict
import pandas as pd
from datetime import timedelta

def analyze_events(events):
    # Group events by category
    categories = defaultdict(list)
    for event in events:
        categories[event['category']].append(event)
    
    analysis_results = {}
    
    for category, category_events in categories.items():
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(category_events)
        
        # 1. Average duration
        df['duration'] = (df['end_time'] - df['start_time']).apply(lambda x: x.total_seconds() / 3600)  # in hours
        avg_duration = df['duration'].mean()
        
        # 2. Weekday distribution
        weekday_dist = df['start_time'].apply(lambda x: x.strftime('%A')).value_counts().to_dict()
        
        # 3. Average priority
        avg_priority = df['priority'].astype(float).mean()
        
        # 4. Min and max duration
        min_duration = df['duration'].min()
        max_duration = df['duration'].max()
        
        # 5. Top 3 most frequent hours
        hour_counts = df['start_time'].apply(lambda x: x.hour).value_counts()
        # Convert hour (integer) keys to strings
        top_hours = {str(k): v for k, v in hour_counts.nlargest(3).to_dict().items()}
        
        analysis_results[category] = {
            'average_duration_hours': round(avg_duration, 2),
            'weekday_distribution': weekday_dist,
            'average_priority': round(avg_priority, 2),
            'min_duration_hours': round(min_duration, 2),
            'max_duration_hours': round(max_duration, 2),
            'top_hours': top_hours
        }
    
    return analysis_results

# Perform analysis
analysis_results = analyze_events(events_list)

# Print results
for category, stats in analysis_results.items():
    print(f"\nAnalysis for category: {category}")
    print(f"Average duration: {stats['average_duration_hours']} hours")
    print(f"Weekday distribution: {stats['weekday_distribution']}")
    print(f"Average priority: {stats['average_priority']}")
    print(f"Duration range: {stats['min_duration_hours']} to {stats['max_duration_hours']} hours")
    print(f"Most frequent hours: {stats['top_hours']}")


prefer_doc = {
    "type":'events',
    "user_id": user_id,
    "content": analysis_results
}



rf_db=prefereceDatabase()
rf_db.add_prefer(prefer_doc)



compute for each category
1.average duration
2.weekday distribution
3.average priority
4. min and max duration
5.top 3 most frequent hours sections
