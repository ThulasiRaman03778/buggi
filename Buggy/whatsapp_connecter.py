import asyncio
import websockets
import threading
import time
import json 
from asgiref.sync import sync_to_async

from Home.models import Profile,Reminder
WS_URI = "wss://messageapi.dchans.com/whatsapp/api"


stop_event = threading.Event()
ws = None               
loop = None             
async def listen(ws_conn):
    try:
        async for message in ws_conn:
            try:
                data=json.loads(message)
                print(data)
                if(data.get("type")==3):
                    try:
                        user=await get_user(data.get("phone"))
                        await create_reminder(user,data.get("description"),data.get("time"))
                        send_message({"to":user.profile.phone_number,"userdata":{"name":user.username,"age":user.profile.age,"time":data.get("time"),"prompt":4,"language":user.profile.language}})
                        print("saved")
                    except Exception as e:
                        print(e)
                        send_message({"to":data.get("phone"),"prompt":-1})
                    print("Setting Remainder For Phone:",data.get("phone"))
                if(data.get("type")==4):
                    try:
                        user=await get_user(data.get("phone"))
                        if(data.get("to_check")):
                            send_message({"to":user.profile.phone_number,"userdata":{"name":user.username,"age":user.profile.age,"language":user.profile.language,"prompt":1,"bpm":user.profile.heart_rate}})
                        else: 
                            await change_language(user,data.get("language"))
                            send_message({"to":user.profile.phone_number,"userdata":{"name":user.username,"age":user.profile.age,"language":data.get("language"),"prompt":5,}})
                    except Exception as e:
                        print(e)
                        send_message({"to":data.get("phone"),"prompt":-1})
                    print("Setting Remainder For Phone:",data.get("phone"))
            except Exception as e:
                print(e)
           
    except websockets.ConnectionClosed as e:
        print(f"⚠️ Connection closed: {e.code} - {e.reason}")

async def websocket_handler():
    global ws
    while not stop_event.is_set():
        try:
            async with websockets.connect(
                WS_URI,
                ping_interval=20,
                ping_timeout=10
            ) as ws_conn:
                print("✅ Connected to Whatsapp Api Server!")
                ws = ws_conn
                await listen(ws_conn)
        except Exception as e:
            print(f"❌ Connection error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

def start_websocket_thread():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_handler())
thread = threading.Thread(target=start_websocket_thread, daemon=True)
thread.start()
def send_message(message):
    print(message)
    global ws, loop
    if  ws :
        future = asyncio.run_coroutine_threadsafe(ws.send(json.dumps(message)), loop)
        try:
            future.result(timeout=5)
            print(f"📤 Sent from trigger: {message}")
        except Exception as e:
            print(f"❌ Send failed: {e}")
    else:
        print("⚠️ WebSocket not connected.")
def cleanup():
    global ws, loop
    print("🧹 Cleaning up WebSocket...")

    stop_event.set()  # Signal thread to stop

    if ws and ws.open and loop and loop.is_running():
        try:
            future = asyncio.run_coroutine_threadsafe(ws.close(), loop)
            future.result(timeout=5)
            print("✅ WebSocket closed cleanly.")
        except Exception as e:
            print(f"❌ Failed to close WebSocket: {e}")

    if thread.is_alive():
        thread.join(timeout=5)
        print("🧵 Background thread joined.")
@sync_to_async
def get_user(phone):
    return Profile.objects.get(phone_number=phone).user

@sync_to_async
def create_reminder(user, desc, time):
    return Reminder.objects.create(
        user=user,
        description=desc,
        time=time,
        recurrence="daily",
        is_active=True
    )
@sync_to_async
def change_language(user,language):
    user.profile.language=language
    user.profile.save()





   
  
      
   