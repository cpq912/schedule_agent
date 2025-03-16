#this is the code for this schedule system
from sysprompt import get_prompt
############################trigger one:user demand


#the workflow could be 
# 1.listening 
# 2.get user input ,start dialouge 
# 3.excurte 
# 4.stop and wait 5 minutes 
# 5. save dialouge to memory, clear memory and hault the program





#start dialougue
floor_messages=[]
#user input
user_input = from_frontend
#floor messages does not have agent syspromt
floor_messages.append(("user",user_input))

#router
router_msg=get_prompt('chater')
router_msg=router_msg.append(("user",user_input))
response = type_agent("chater",router_msg,llm)

action = response.split("User needs:")[1].strip()

#add
if action=='add':
    #call extractor
    add_msg=get_prompt('add_extractor')
    add_msg=add_msg.append(("user",user_input))
    response = type_agent("add_extractor",add_msg,llm)
    add_msg=add_msg.append(("assistant",response))
    if "turns:1" in response and "status:completed" in  response:
        feteched_data =get_event()
        new_data =json.loads(response.split("```json")[1].strip().split("```")[0].strip())
        check_conflict = check_time_conflicts(existed_event,planned_event)
        if check_conflict==True:
            add_msg=add_msg.append(("assistant",'[conflict checker]: output'))
            output.to_frontend # report conflict
            user_input = from_frontend
            add_msg=add_msg.append(("user",user_input))
            router_msg=router_msg.append(("user",user_input)) # this will check what user want to do with the conflict
            conflict_action = type_agent("chater",router_msg,llm)
            #if cancel, end the dialogue
            if "delete" in conflict_action:
                floor_messages.append(add_msg[1:])
                return "user delete the new events"
            else:
                #send it to add planner
                addplan_msg=get_prompt('add_planner')
                get_confirm=False # has to be confirmed by user 
                while get_confirm:
                    response = type_agent("add_planner",addplan_msg,llm)
                    addplan_msg=addplan_msg.append(("assistant",response))
                    try:
                        conflict_res= response.split("Conflict explanation:")[1].split("Would this")[0].strip()
                        conflict_res.to_frontend
                        user_input = from_frontend
                        addplan_msg=addplan_msg.append(("user",user_input))
                    except:    
                        "Would this schedule work for you?".to_frontend
                        user_input = from_frontend
                        addplan_msg=addplan_msg.append(("user",user_input))
                        confirm_msg=get_prompt('confirm_agent')
                        get_confirm = type_agent("confirm_agent",confirm_msg,llm)

                final_schedule=json.loads(response.split("Suggested Schedule:")[1].split("Would this")[0].strip())
                write_event()#need to delete the event in the new event listed first
                floor_messages.append(add_msg[1:])
                floor_messages.append(addplan_msg[1:])
                return "new event has been added"
    else:
        extract_message(response,"grounded message:").to_frontend # ask for more infor 
        user_input = from_frontend
        add_msg=add_msg.append(("user",user_input))
        response = type_agent("add_extractor",add_msg,llm)
        add_msg=add_msg.append(("assistant",response))

    if "turns:2" in response and "status:completed" in  response: #similar to round 1
        existed_event =get_event()
        planned_event =json.loads(response.split("```json")[1].strip().split("```")[0].strip())
        check_conflict = check_time_conflicts(existed_event,planned_event)
        if check_conflict==True:
            add_msg=add_msg.append(("assistant",'[conflict checker]: output'))
            output.to_frontend # report conflict
            user_input = from_frontend
            add_msg=add_msg.append(("user",user_input))
            router_msg=router_msg.append(("user",user_input)) # this will check what user want to do with the conflict
            conflict_action = type_agent("chater",router_msg,llm)
            #if cancel, end the dialogue
            if "delete" in conflict_action:
                floor_messages.append(add_msg[1:])
                return "user delete the new events"
            else:
                #send it to add planner
                addplan_msg=get_prompt('add_planner')
                get_confirm=False # has to be confirmed by user 
                while get_confirm:
                    response = type_agent("add_planner",addplan_msg,llm)
                    addplan_msg=addplan_msg.append(("assistant",response))
                    try:
                        conflict_res= response.split("Conflict explanation:")[1].split("Would this")[0].strip()
                        conflict_res.to_frontend
                        user_input = from_frontend
                        addplan_msg=addplan_msg.append(("user",user_input))
                    except:    
                        "Would this schedule work for you?".to_frontend
                        user_input = from_frontend
                        addplan_msg=addplan_msg.append(("user",user_input))
                        confirm_msg=get_prompt('confirm_agent')
                        get_confirm = type_agent("confirm_agent",confirm_msg,llm)

                final_schedule=json.loads(response.split("Suggested Schedule:")[1].split("Would this")[0].strip())
                write_event()#need to delete the event in the new event listed first
                floor_messages.append(add_msg[1:])
                floor_messages.append(addplan_msg[1:])
                return "new event has been added"

    else: # information is not enough , call add planner
        #planner need new_data, and fetched data 
        feteched_data =get_event()
        new_data =json.loads(response.split("```json")[1].strip().split("```")[0].strip())
        addplan_msg=get_prompt('add_planner')

        get_confirm=False # has to be confirmed by user 
        while get_confirm:
            response = type_agent("add_planner",addplan_msg,llm)
            addplan_msg=addplan_msg.append(("assistant",response))
            try:
                conflict_res= response.split("Conflict explanation:")[1].split("Would this")[0].strip()
                conflict_res.to_frontend
                user_input = from_frontend
                addplan_msg=addplan_msg.append(("user",user_input))
            except:    
                "Would this schedule work for you?".to_frontend
                user_input = from_frontend
                addplan_msg=addplan_msg.append(("user",user_input))
                confirm_msg=get_prompt('confirm_agent')
                get_confirm = type_agent("confirm_agent",confirm_msg,llm)

        final_schedule=json.loads(response.split("Suggested Schedule:")[1].split("Would this")[0].strip())
        write_event()#need to delete the event in the new event listed first

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
