#this is the code for this schedule system
#from sysprompt import get_prompt
from sysprompt import get_prompt
from tools import from_frontend

get_prompt(SYSTEM_PROMPTS,"add_planner")
############################trigger one:user demand

def get_prompt(prompt_name):
    """Get a specific prompt by name"""
    result=[("system", SYSTEM_PROMPTS.get(prompt_name, "Prompt not found"))]
    return result


def from_frontend():
    return input("please enter: ")

def to_frontend(text):
    print(text)
#the workflow could be 
# 1.listening 
# 2.get user input ,start dialouge 
# 3.excurte 
# 4.stop and wait 5 minutes 
# 5. save dialouge to memory, clear memory and hault the program




user_input='i will swim tommorow at 10 am,20250303,1 hour'
#start dialougue
floor_messages=[]
#user input
user_input = from_frontend()
#floor messages does not have agent syspromt
floor_messages.append(("user",user_input))

#router
router_msg=chater_prompt()
router_msg.append(("user",user_input))
response = type_agent("chater",router_msg,llm)

action = response.split("User needs:")[1].strip()

#add
if action=='add':
    #call extractor
    add_msg=add_extractor_prompt()
    add_msg.append(("user",user_input))
    response = type_agent("add_extractor",add_msg,llm)
    add_msg.append(("assistant",response))
    if "turns: 1" in response and "Status: completed" in  response:
        new_data=json.loads(response.split("Collected events:")[1].strip())
        feteched_data =get_add_event(new_data)
       # new_data =json.loads(response.split("```json")[1].strip().split("```")[0].strip())
        check_conflict = check_time_conflicts(existed_event,new_data)
        if len(check_conflict)>0:
            conflict_output="found conflicts, how can I help you solve it? \n "+str(check_conflict)
            add_msg.append(("assistant",f'[conflict checker]: {conflict_output}'))
            to_frontend(conflict_output) # report conflict
            user_input = from_frontend()
            add_msg.append(("user",user_input))
            router_msg.append(("user",user_input)) # this will check what user want to do with the conflict
            conflict_action = type_agent("chater",router_msg,llm)
            #if cancel, end the dialogue
            if "delete" in conflict_action:
                floor_messages.append(add_msg[1:])
                return "user delete the new events"
            else:
                #send it to add planner
                addplan_msg=add_planner_prompt()
                get_confirm=False # has to be confirmed by user 
                while not get_confirm:
                    response = type_agent("add_planner",addplan_msg,llm)
                    addplan_msg.append(("assistant",response))
                    try:
                        conflict_res= response.split("Conflict explanation:")[1].split("Would this")[0].strip()
                        to_frontend(conflict_res)
                        user_input = from_frontend()
                        addplan_msg.append(("user",user_input))
                    except:    
                        solved_plan= response.split("Suggested Schedule")[1].split("----separate line----")[0].strip()
                        to_frontend("OK! conflict solved \n"+solved_plan+"\n Would you confirm?")
                        user_input = from_frontend()
                        addplan_msg.append(("user",user_input))
                        confirm_msg=get_prompt('confirm_agent')
                        get_confirm = type_agent("confirm_agent",confirm_msg,llm)
                        if get_confirm.split('[confirm_agent]:')[1].strip()=="agree":
                            get_confirm=True

                final_schedule=json.loads(response.split("Suggested Schedule:")[1].split("----separate line----")[0].strip())
                write_event(final_schedule)#need to delete the event in the new event listed first
                floor_messages.append(add_msg[1:])
                floor_messages.append(addplan_msg[1:])
                return "new event has been added"
    else:
        to_frontend(extract_message(response,"grounded message:")) # ask for more infor 
        user_input = from_frontend()
        add_msg.append(("user",user_input))
        response = type_agent("add_extractor",add_msg,llm)
        add_msg.append(("assistant",response))

    if "turns:2" in response and "status:completed" in  response: #similar to round 1
        new_data=json.loads(response.split("Collected events:")[1].strip())
        feteched_data =get_add_event(new_data)
       # planned_event =json.loads(response.split("```json")[1].strip().split("```")[0].strip())
        check_conflict = check_time_conflicts(existed_event,new_data)
        if len (check_conflict)>0:
            conflict_output="found conflicts, how can I help you solve it? \n "+str(check_conflict)
            add_msg.append(("assistant",f'[conflict checker]: {conflict_output}'))
            to_frontend(conflict_output) # report conflict
            user_input = from_frontend()
            add_msg.append(("user",user_input))
            router_msg.append(("user",user_input)) # this will check what user want to do with the conflict
            conflict_action = type_agent("chater",router_msg,llm)
            #if cancel, end the dialogue
            if "delete" in conflict_action:
                floor_messages.append(add_msg[1:])
                return "user delete the new events"
            else:
                #send it to add planner
                addplan_msg=add_planner_prompt()
                get_confirm=False # has to be confirmed by user 
                while not get_confirm:
                    response = type_agent("add_planner",addplan_msg,llm)
                    addplan_msg.append(("assistant",response))
                    try:
                        conflict_res= response.split("Conflict explanation:")[1].split("Would this")[0].strip()
                        to_frontend(conflict_res)
                        user_input = from_frontend()
                        addplan_msg.append(("user",user_input))
                    except:    
                        solved_plan= response.split("Suggested Schedule")[1].split("----separate line----")[0].strip()
                        to_frontend("OK! conflict solved \n"+solved_plan+"\n Would you confirm?")
                        user_input = from_frontend()
                        addplan_msg.append(("user",user_input))
                        confirm_msg=get_prompt('confirm_agent')
                        get_confirm = type_agent("confirm_agent",confirm_msg,llm)
                        if get_confirm.split('[confirm_agent]:')[1].strip()=="agree":
                            get_confirm=True

                final_schedule=json.loads(response.split("Suggested Schedule:")[1].split("----separate line----")[0].strip())
                write_event(final_schedule)#need to delete the event in the new event listed first
                floor_messages.append(add_msg[1:])
                floor_messages.append(addplan_msg[1:])
                return "new event has been added"

    else: # information is not enough , call add planner
        #planner need new_data, and fetched data 
       # new_data =json.loads(response.split("```json")[1].strip().split("```")[0].strip())
        new_data=json.loads(response.split("Collected events:")[1].strip())
        feteched_data =get_add_event(new_data)
        user_input=None# now user does not have feedback yet
        addplan_msg=add_planner_prompt()

        get_confirm=False # has to be confirmed by user 
        while not get_confirm:
            response = type_agent("add_planner",addplan_msg,llm)
            addplan_msg.append(("assistant",response))
            try:
                conflict_res= response.split("Conflict explanation:")[1].split("Would this")[0].strip()
                addplan_msg.append(("assistant",f'[conflict checker]: {conflict_output}'))
                to_frontend(conflict_res)
                user_input = from_frontend()
                addplan_msg.append(("user",user_input))
                confirm_msg= confirm_agent_prompt()
                get_confirm = type_agent("confirm_agent",confirm_msg,llm)
                if get_confirm.split('[confirm_agent]:')[1].strip()=="agree":
                    get_confirm=True
            except:    
                if(len(conflict_res))==0:
                    # never have conflict
                    solved_plan= response.split("Suggested Schedule")[1].split("Would this")[0].strip()
                    to_frontend("OK! Here is the suggested schedule \n"+solved_plan+"\n Would you confirm?")
                    user_input = from_frontend()
                    addplan_msg=addplan_msg.append(("user",user_input))
                    confirm_msg= confirm_agent_prompt()
                    get_confirm = type_agent("confirm_agent",confirm_msg,llm)
                    if get_confirm.split('[confirm_agent]:')[1].strip()=="agree":
                        get_confirm=True
                else:
                    #conflict has solved
                    solved_plan= response.split("Suggested Schedule")[1].split("Would this")[0].strip()
                    to_frontend("OK! conflict solved \n"+solved_plan+"\n Would you confirm?")
                    user_input = from_frontend()
                    addplan_msg.append(("user",user_input))
                    confirm_msg=get_prompt('confirm_agent')
                    get_confirm = type_agent("confirm_agent",confirm_msg,llm)
                    if get_confirm.split('[confirm_agent]:')[1].strip()=="agree":
                        get_confirm=True


        final_schedule=json.loads(response.split("Suggested Schedule:")[1].split("Would this")[0].strip())
        write_event(final_schedule)#need to delete the event in the new event listed first

#add all messages to floor at last
#the first one is the system prompt, do not add to floor
floor_messages.append(add_msg[1:])
floor_messages.append(addplan_msg[1:])
return "new event has been added"





#delete


#check



#modify




#end of dialogue, when no one speak for 5 mins

#save the dialogue to memory

########################trigger two:system clock


#event notice clock

#period event plan clock

#summary and analysis clock




SYSTEM_PROMPTS = {
    "chater": f'''

Role: I am a scheduling assistant focused on understanding your calendar needs.

My task is to identify if you want to:
1. Add a new event
2. Check existing schedule
3. Modify an event
4. delete an event
 
Output:
I will respond with "User needs: (add/check/modify/delete)" followed by relevant questions.
no other words are allowed

Examples:
User: "I need to schedule a meeting tomorrow"
Response: "User needs: add"

User: "What's on my calendar for next week?"
Response: "User needs: check"

User: "Can you change the time of my dentist appointment?"
Response: "User needs: modify"
'''
,


"add_extractor":f"""
Role: I am an event information collector. I will:

1. Extract event details from user message in this format:
when implicite time give(e.g. tommorow), you may use current time{time} to infer.
Do not hallucinate if the information is not given in users response.
Auto-infer category (Work/Personal/Health).
You should auto gen an eventid over 20 digits that impossible to repeat
{{
    "event_id": "random_alphanumeric", 
    "start_time": "YYYY-MM-DD HH:MM", (required)
    "end_time": "YYYY-MM-DD HH:MM",   
    "category": "Work/Personal/Health",
    "description": "user input",
    "priority": "1-5"
}}

2. 
grounded message: "your grounded message"
when fields are missing from user statement (fields include start_time,end_time,category,description, priority):
- First Response: respond with "Would you provide more information about [list missing fields]?"
- Second Response: "Since you haven't given all info, I shall try it based on your preference"

When all fields provided: "Ok, I shall help you arrange it"

If any field is missing, you may ground "would you provide more information about (missing fileds) ?" Do not infer.
If  all field is provided, you may ground "ok i shall help you arrange it ". Do not infer.
If after your inquire the fields are still missing , you may ground "since you haven't give all info, i shall try it based on your preference " .In this case, the status should be partially completed.


3. Output format:
turns:1-2(this is showing the number of turns that you are anwsering)
Status: completed/partially completed
grounded message: "your grounded message"
Collected events: list of newly scheduled events


Example:
User: "Schedule a meeting tomorrow at 2pm"
Response: "I need the following details:
- Meeting duration/end time
- Priority (1-5)
- Category (Work/Personal/Health)

Status: partially completed
Events: [{{
    "event_id": "mt123xyz",
    "start_time": "2025-02-26 14:00",
    "description": "meeting"
}}]
""",
"add_planner":f"""Role: I am a Schedule Planning Specialist that optimizes event scheduling.
    I need to follow the rules and the output format strictly.

Input:
- Existing Events: Current scheduled events list
- New Requirements: Events to be scheduled (may have missing fields)
- User Preferences: Optional scheduling preferences

Process:
1. For incomplete events, I will:
   - Set default meeting duration: 1 hour
   - Assign appropriate priority (1-5)
   - Consider category-based optimal timing

2. For scheduling, I will:
   - Avoid time conflicts,Avoid time conflicts
   - Follow scheduling best practices
   - Consider event categories and priorities

Output Format:
(follow this sequence)
1.Suggested Schedule:
2.----separate line----(make sure always output this line)
3.Conflict explaination:(optional when there is no conflict)
4.would this work for you?

Suggested Schedule:
(below should be a list of new scheduled event [{{}},{{}}])
{{
    "event_id": [original],
    "start_time": [original or suggested],
    "end_time": [original or suggested],
    "category": [original],
    "description": [original],
    "priority": [original or suggested]
}}


Would this schedule work for you?"

Conflict explaination:
Only explain why you give the suggestion when you found conflict, and only explain about the conflict using event names or descriptions,
do not use event id ,do not include others.

After user feedback:
- If changes needed: Provide new suggestion
- If confirmed: Output final format:
status: confirmed
plan: a list final schedule details [{{}},{{}}]

Your input is listed here:
existed_events:{feteched_data}, 
new_requirement:{new_data},
 user preference:{user_input}

rules:
1.if no conflict found, do not explain conflict in the output.
2.if the users change the existed events, then the existed events will be consider new scheduled showing in output.
3.if found conflict, you should use your knowledge to adjust the new_requirement or existed_events.
4.in the Suggested Schedule, only show new add event or the existed event that is adjusted by you.

""",
"confirm_agent":f"""
role:
you are a sensitive agent that good at judging the user's agreement to the plan.

output:
if the user agree, return "agree"
if the user disagree, return "disagree"
if the user is using a statement, not showing any intention, return "none"

this is user input:{user_input}
"""
}

def confirm_agent_prompt():
    return f"""
role:
you are a sensitive agent that good at judging the user's agreement to the plan.

output:
if the user agree, return "agree"
if the user disagree, return "disagree"
if the user is using a statement, not showing any intention, return "none"

this is user input:{user_input}
"""

def chater_prompt():
    return f'''

Role: I am a scheduling assistant focused on understanding your calendar needs.

My task is to identify if you want to:
1. Add a new event
2. Check existing schedule
3. Modify an event
4. delete an event
 
Output:
I will respond with "User needs: (add/check/modify/delete)" followed by relevant questions.
no other words are allowed

Examples:
User: "I need to schedule a meeting tomorrow"
Response: "User needs: add"

User: "What's on my calendar for next week?"
Response: "User needs: check"

User: "Can you change the time of my dentist appointment?"
Response: "User needs: modify"
'''

def add_extractor_prompt():
    return f"""
Role: I am an event information collector. I will:

1. Extract event details from user message in this format:
when implicite time give(e.g. tommorow), you may use current time{time} to infer.
Do not hallucinate if the information is not given in users response.
Auto-infer category (Work/Personal/Health).
You should auto gen an eventid over 20 digits that impossible to repeat
{{
    "event_id": "random_alphanumeric", 
    "start_time": "YYYY-MM-DD HH:MM", (required)
    "end_time": "YYYY-MM-DD HH:MM",   
    "category": "Work/Personal/Health",
    "description": "user input",
    "priority": "1-5"
}}

2. 
grounded message: "your grounded message"
when fields are missing from user statement (fields include start_time,end_time,category,description, priority):
- First Response: respond with "Would you provide more information about [list missing fields]?"
- Second Response: "Since you haven't given all info, I shall try it based on your preference"

When all fields provided: "Ok, I shall help you arrange it"

If any field is missing, you may ground "would you provide more information about (missing fileds) ?" Do not infer.
If  all field is provided, you may ground "ok i shall help you arrange it ". Do not infer.
If after your inquire the fields are still missing , you may ground "since you haven't give all info, i shall try it based on your preference " .In this case, the status should be partially completed.


3. Output format:
turns:1-2(this is showing the number of turns that you are anwsering)
Status: completed/partially completed
grounded message: "your grounded message"
Collected events: list of newly scheduled events


Example:
User: "Schedule a meeting tomorrow at 2pm"
Response: "I need the following details:
- Meeting duration/end time
- Priority (1-5)
- Category (Work/Personal/Health)

Status: partially completed
Events: [{{
    "event_id": "mt123xyz",
    "start_time": "2025-02-26 14:00",
    "description": "meeting"
}}]
"""

def add_planner_prompt():
    return f"""Role: I am a Schedule Planning Specialist that optimizes event scheduling.
    I need to follow the rules and the output format strictly.

Input:
- Existing Events: Current scheduled events list
- New Requirements: Events to be scheduled (may have missing fields)
- User Preferences: Optional scheduling preferences

Process:
1. For incomplete events, I will:
   - Set default meeting duration: 1 hour
   - Assign appropriate priority (1-5)
   - Consider category-based optimal timing

2. For scheduling, I will:
   - Avoid time conflicts,Avoid time conflicts
   - Follow scheduling best practices
   - Consider event categories and priorities

Output Format:
(follow this sequence)
1.Suggested Schedule:
2.----separate line----(make sure always output this line)
3.Conflict explaination:(optional when there is no conflict)
4.would this work for you?

Suggested Schedule:
(below should be a list of new scheduled event [{{}},{{}}])
{{
    "event_id": [original],
    "start_time": [original or suggested],
    "end_time": [original or suggested],
    "category": [original],
    "description": [original],
    "priority": [original or suggested]
}}


Would this schedule work for you?"

Conflict explaination:
Only explain why you give the suggestion when you found conflict, and only explain about the conflict using event names or descriptions,
do not use event id ,do not include others.

After user feedback:
- If changes needed: Provide new suggestion
- If confirmed: Output final format:
status: confirmed
plan: a list final schedule details [{{}},{{}}]

Your input is listed here:
existed_events:{feteched_data}, 
new_requirement:{new_data},
 user preference:{user_input}

rules:
1.if no conflict found, do not explain conflict in the output.
2.if the users change the existed events, then the existed events will be consider new scheduled showing in output.
3.if found conflict, you should use your knowledge to adjust the new_requirement or existed_events.
4.in the Suggested Schedule, only show new add event or the existed event that is adjusted by you.

"""


user_input="ddd"
print(confirm_agent_prompt())
user_input='hhh'
print(confirm_agent_prompt())
user_input="aaa"
print(confirm_agent_prompt())