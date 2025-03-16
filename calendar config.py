import os
import speech_recognition as sr
from autogen import AssistantAgent, UserProxyAgent

# 语音识别模块
def listen_and_transcribe():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("请说出您的指令...")
        audio = r.listen(source)
        
    try:
        return r.recognize_google(audio, language='zh-CN')
    except Exception as e:
        print(f"识别错误: {e}")
        return ""
    
#text=listen_and_transcribe()

#print(text)
# import win32com.client
# from datetime import datetime, timedelta
# outlook = win32com.client.Dispatch("Outlook.Application")
# namespace = outlook.GetNamespace("MAPI")

# 在代码开头添加系统检查
# 修改原来的open_calendar函数
# import os
# import subprocess

# def open_calendar():
#     try:
#         # 方案1：直接调用Outlook的日历界面
#         outlook_path = os.path.expanduser(
#             "~\\AppData\\Local\\Microsoft\\Office\\OUTLOOK.EXE"
#         )
#         if os.path.exists(outlook_path):
#             subprocess.Popen([outlook_path, "/select", "outlook:calendar"])
#             print( "正在打开Outlook日历...")
#         else:
#             # 方案2：通过注册表查找安装路径
#             try:
#                 import winreg
#                 key = winreg.OpenKey(
#                     winreg.HKEY_LOCAL_MACHINE,
#                     r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\OUTLOOK.EXE"
#                 )
#                 outlook_path = winreg.QueryValue(key, None)
#                 subprocess.Popen([outlook_path, "/select", "outlook:calendar"])
#                 print( "正在通过注册表路径打开日历...")
#             except:
#                 # 方案3：通用打开方式
#                # os.startfile("outlook:calendar")
#                 print( "已尝试打开默认日历")
#     except Exception as e:
#         print(f"打开失败，请手动检查Outlook安装。技术细节: {str(e)}")
#         return "无法打开日历，请确保Outlook已正确安装"
# open_calendar()

# import psutil
# [p.exe() for p in psutil.process_iter() if "outlook.exe" in p.name().lower()]

# 安装依赖
#pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

# 示例代码：创建日历事件
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build



from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(
    'client.json',  # 确保这是从控制台下载的文件名
    scopes=SCOPES
)

# 在本地浏览器完成授权流程
flow.run_local_server(port=0)

# 自动生成token.json
with open('token.json', 'w') as f:
    f.write(flow.credentials.to_json())


def google_calendar_create_event():
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar'])
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': '团队会议',
        'start': {'dateTime': '2025-03-20T09:00:00+08:00'},
        'end': {'dateTime': '2025-03-20T10:00:00+08:00'},
    }
    
    created_event = service.events().insert(
        calendarId='primary',
        body=event
    ).execute()
    print('yes')
    return f"事件已创建：{created_event.get('htmlLink')}"

google_calendar_create_event()