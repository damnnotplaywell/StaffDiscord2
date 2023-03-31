import os
import discord
import pickle
import json
from datetime import time, timedelta
from threading import Thread
from discord import Client
from discord.ext.tasks import loop
from flask import Flask
from parse import *

# Set up Flask app
app = Flask(__name__)

# Set up Discord client
intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Channel ID
staff_channel_id = 1049414474274189333
botdump_channel_id = 1040908494297120808

# Initialization
casters = ["hiyama2018", "kobayashi", "komaki2018"]

# Set up time for send loop tasks
offset = timedelta(hours=7)
time1 = time(2, 0)
time1 = (datetime.combine(datetime.today(), time1) - offset).time()

def run_client():
  try:
    client.run(os.environ['TOKEN'])
  except:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system('kill 1')
    os.system("python restarter.py")

@app.route("/")
def index():
  return "I'm alive!"

################# MESSAGE CONTENT ##################
async def send_message(caster, hour, title):
  # Parsing process
  msg = message(caster, hour, title)
  
  # Send message to Discord
  channel = client.get_channel(staff_channel_id)
  await channel.send('@everyone\n' + msg)

async def carousel_content(caster, hour, title, idx):
  # Create the carousel message
  embed = discord.Embed(title="ウェザーニュース L!VE", description="番組表（タイムテーブル）", url="https://www.youtube.com/watch?v=zAdWzjab1B8")
  img = f'https://smtgvs.cdn.weathernews.jp/wnl/img/caster/M1_{title_trans(title[idx])}_{caster_trans(caster[idx])}.jpg'

  embed.set_thumbnail(url=img)
  embed.add_field(name="Caster", value=caster_kanji(caster_trans(caster[idx])))
  embed.add_field(name="Time", value=hour[idx])
  embed.add_field(name="Program", value=title[idx])

  channel = client.get_channel(staff_channel_id)
  await channel.send(embed=embed)

##################### TASKS ########################
@client.event
async def on_ready():
  tasks = []
      
  @loop(time=time1)
  async def task_1():
    caster, hour, title = data(casters)
    
    message = {
              "caster": caster,
              "hour": hour,
              "title": title
    }
  
    # Serializing json
    json_message = json.dumps(message, indent=4, ensure_ascii=False)
     
    # Writing to json
    with open("data.json", "w") as outfile:
      outfile.write(json_message)

    await send_message(caster, hour, title)
  
  with open("data.json", "r") as openfile:
    json_object = json.load(openfile)
    caster2 = json_object['caster']
    hour2 = json_object['hour']
    title2 = json_object['title']

    time2 = [time.fromisoformat(t) for t in hour2]
    for t_idx, t in enumerate(time2):
      t = (datetime.combine(datetime.today(), t) - offset).time()
      async def task_2(t_idx=t_idx):
        await carousel_content(caster2, hour2, title2, t_idx)
      task_2_loop = loop(time=t)(task_2)
      tasks.append(task_2_loop)

  task_1.start()
  for task in tasks:
    task.start()

################# MAIN ####################
client_thread = Thread(target=run_client)
client_thread.start()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)