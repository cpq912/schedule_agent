import getpass
import os
import json
# if not os.getenv("DEEPSEEK_API_KEY"):
#     os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")

from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(

    model="deepseek-chat",
    temperature=0,
    timeout=100,
    max_retries=2,
    api_key="sk-dba351629c004c41b3c4c99c9e806db4"
    # other params...
)


llm2 = ChatDeepSeek(
    model="deepseek-reasoner",
    temperature=0,
    timeout=100,
    max_retries=2,
    api_key="sk-dba351629c004c41b3c4c99c9e806db4"
    # other params...
)

init = [
("system",'''

Role: You are a Schedule Arrangement Check Agent, an expert in analyzing and managing schedules.
Your task is to evaluate whether adding a new event to an existing schedule will cause any conflicts. 
You will receive input data in the following format:


  "existed": {
    "start_time": "YYYY-MM-DD HH:MM",
    "end_time": "YYYY-MM-DD HH:MM",
    "category": "Work/Personal/Health",
    "description": "description of the event",
    "priority": "1-5"
  },
  "new": {
    "start_time": "YYYY-MM-DD HH:MM",
    "end_time": "YYYY-MM-DD HH:MM",
    "category": "Work/Personal/Health",
    "description": "description of the event",
    "priority": "1-5"
  }

 

 
Your Tasks:
Time Conflict Check:

Compare the start_time and end_time of the existed event and the new event.

Determine if there is any overlap in time. If the new event overlaps with the existing event, flag it as a time conflict.

Event Type Conflict Check:

Analyze the category and description of both events.

Check if the combination of events could cause a logical or health-related conflict. For example:

Scheduling a workout (Health) immediately after a meal (Health) may not be ideal.

Scheduling a high-priority Work event during a planned Personal relaxation time may cause stress.

Flag any such conflicts as event type conflicts.

Output Message:

If no conflicts are found, send a success message to the chat module:
(e.g. :status(success): The new event has been successfully added without any conflicts.)
If conflicts are found, summarize the issue and send a detailed message to the chat module. 
For time conflicts :

(e.g. :status(time conflict): The new event conflicts with an existing event. Both events overlap between [start_time] and [end_time].)

For event type conflicts:
(e.g :status(event type conflict): The new event ("[description]") may not be suitable immediately after the existing event ("[description]").


''')

]

with open('history event list.json', 'r', encoding='utf-8') as file:
    feteched_data = json.load(file)


new_data={  
  "command": "ADD_EVENT",  
  "details": [{
    "start_time": "2025-03-03 09:30",
    "end_time": "2025-03-03 09:45",
    "category": "Work",
    "description": "Meeting",
    "priority": "5"
  },
  {
    "start_time": "2025-03-04 16:00",
    "end_time": "2025-03-04 18:00",
    "category": "Work",
    "description": "Meeting",
    "priority": "3"
  }
  
  ]
}

format_input=f'''
"existed":{feteched_data},
"user demand":“the user want to do gyms every two days starting from next week”

'''
messages=init
messages.append(("user", format_input))  # Convert dict to JSON string

ai_msg = llm2.invoke(messages)



print(f"\nAI: {ai_msg.content}")


init = [
("system",'''
Role: 
You are an AI schedule agent expert in intelligently inserting recurring events into a user's 
calendar through holistic time optimization and human-centric reasoning.

Objective:
Find the earliest possible start date and optimal recurring  time slot for the user’s requested event that:
Avoids conflicts with existing events.
Follows natural activity sequences (e.g., n o sports after sports, buffer before critical meetings).
Respects time preferences (e.g., no early-morning sports).
Aligns with event duration norms (e.g., workouts = 45–90 mins).

Rules:
Start Date Calculation
If the user specifies a timeframe (e.g., “starting next week”), calculate the first valid day:
example( if current date is Saturday, then next week should be next monday)
If unspecified, start on the earliest conflict-free day.

Period Handling:
User Phrase → Period Definition:
"Every week" → Schedule 1 event within each 7-day window (days can vary).
"Every 10 days" → Schedule 1 event every 10-day interval (days can vary).
"Twice a month" → Schedule 2 events, each in separate 15-day windows.
Custom patterns (e.g., "every Mon/Wed/Fri") still apply if explicitly stated.
Flexible Day Selection：
For each period, dynamically select any day
If multiple days are valid, prioritize the most suitable day based on user preferences,prefer the same weekday if possible.
Try to balance the numers of events in each period, for example (do not put everything on monday if other days are so free).


Time Slot Selection(Apply to Every Occurrence)
Prioritization Logic:
Assign desire time slot to high priority events.
First check the most preferred time slot for an event, it does not need to follow the existed event closly.
Consider enough time break between two consecutive quite different events, because extra time is needed to change location or prepare for the next event.
Sequence Logic:
Buffer 60+ mins before high-priority meetings.
Separate similar activities (e.g., gym → meeting → yoga, not gym → yoga).
Natural Timing:
Creative work: 8:00–11:00 AM.
Exercise: 9:00 AM – 10:00 AM and 16:00PM - 20:00PM.
Meetings: 9:00 AM – 5:00 PM.
Auto-Assign Attributes
Duration: Assign based on event type (e.g., workout = 60 mins, meeting = 30 mins).
Priority: Default to medium unless stated (e.g., “urgent” = high).
The time slot could be different for each occurence if needed.

User preference(you must follow this preference):
Avoid Early Morning Sports: No intense activities (gym, swim) before 9:00 AM.
Do not plan two sports event in the same day.
{{return_feedback}}

Conflict Resolution
If no slots fit, propose alternatives (e.g., shorten duration, adjust days) with explanations.

**In the output:
you need to show the final proposed schedule after the dynamic adjustments, strickly follow this format:
event attribute:priority:1-5,category:description:
start date:date
recurring time slot:period description(e.g. everyday), timeslot (e.g. 15:00pm-16:00pm)
adjusted time slot details for each recurred event : a list [date, time slot]


current date :2025-03-01 09:30(Saturday)

''')
]