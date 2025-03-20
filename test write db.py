#write event list to mongodb
from pymongo import MongoClient

from datetime import datetime, timedelta 

class EventDatabase:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://chrispeng912:hdKhfSgWYWSCcqvf@agent.aosmv.mongodb.net/?retryWrites=true&w=majority&appName=agent')
        self.db = self.client['schedule_db']
        self.events = self.db['events'] # collectioin
        
        # Create indexes for efficient querying
        self.events.create_index("event_id")
        self.events.create_index("start_time")
        self.events.create_index("category")

    def add_event(self, event):
        # Convert string dates to datetime objects
        event['start_time'] = datetime.strptime(event['start_time'], "%Y-%m-%d %H:%M")
        event['end_time'] = datetime.strptime(event['end_time'], "%Y-%m-%d %H:%M")
        return self.events.insert_one(event)

    def get_event_by_id(self, event_id):
        
        return self.events.find_one({"event_id": event_id})

    def get_event_by_date(self,event_date):

        start_of_day = datetime(event_date.year, event_date.month, event_date.day)
        end_of_day = start_of_day + timedelta(days=1)
        return self.events.find({
            "start_time": {
                "$gte": start_of_day,
                "$lt": end_of_day
            }
        })


    def get_events_by_time_range(self, start_time, end_time):
        return self.events.find({
            "start_time": {
                "$gte": datetime.strptime(start_time, "%Y-%m-%d %H:%M"),
                "$lte": datetime.strptime(end_time, "%Y-%m-%d %H:%M")
            }
        })

    def get_events_by_category(self, category):
        return self.events.find({"category": category})

    def get_events_by_criteria(self, criteria=None):
        """
        Combined search with multiple conditions
        """
        if criteria is None:
            criteria = {}
            
        query = {}
        # Handle time range
        if 'start_time' in criteria :
            query['start_time'] = {}
            query['end_time'] = {}
            query['start_time']['$gte'] = criteria['start_time']
            query['end_time']['$lte'] = criteria['end_time']
                
        # Handle other criteria
        for field in ['category', 'priority', 'event_id']:
            if field in criteria:
                query[field] = criteria[field]
        #content search
        if 'description' in criteria:
            query['description'] = {'$regex': criteria['description'], '$options': 'i'}
 
        return self.events.find(query)

    # Add events
with open('history event list.json', 'r', encoding='utf-8') as file:
    events = json.load(file)

dates = [event['start_time'] for event in events]

db = EventDatabase()
# for event in events:
#     db.add_event(event)

# Query examples
event = db.get_event_by_id("et32d42")
event = db.get_event_by_date(dates[2])
event = db.get_events_by_criteria({'description': 'meeting'})
health_events = db.get_events_by_category("Health")


