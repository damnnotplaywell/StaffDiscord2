import os
import discord
from datetime import time, timedelta
from threading import Thread
from discord import Client
from discord.ext.tasks import loop
from parse import *
from flask import Flask

# Set up Flask app
app = Flask(__name__)

# Set up Discord client
intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Channel ID
staff_channel_id = 1049414474274189333
botdump_channel_id = 1040908494297120808

# Set up time
offset = timedelta(hours=7)
time1 = time(2, 0)
time1 = (datetime.combine(datetime.today(), time1) - offset).time()

# Casters
casters = ["hiyama2018", "kobayashi", "komaki2018"]

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

####################################################
################# MESSAGE CONTENT ##################
async def send_message():
  # Parsing process
  msg = message(casters)
  
  # # Send message to Discord
  channel = client.get_channel(staff_channel_id)
  await channel.send('@everyone\n' + msg)

async def carousel_content(caster, hour, title):
  # Create the carousel message
  
  embed = discord.Embed(title="ウェザーニュース L!VE", description="番組表（タイムテーブル）", url="https://www.youtube.com/watch?v=zAdWzjab1B8")
  img = f'https://smtgvs.cdn.weathernews.jp/wnl/img/caster/M1_{title_trans(title[0])}_{caster_trans(caster[0])}.jpg'

  embed.set_thumbnail(url=img)
  embed.add_field(name="Caster", value=caster_kanji(caster_trans(caster[0])))
  embed.add_field(name="Time", value=hour[0])
  embed.add_field(name="Program", value=title[0])

  channel = client.get_channel(staff_channel_id)
  await channel.send(embed = embed)
  
####################################################
##################### TASKS ########################
@client.event
async def on_ready():
  @loop(time=time1)
  async def task_1():
    await send_message()

    # Update time2
    caster, hour, title = data(casters)
    time2 = [time.fromisoformat(t) for t in hour]

    tasks = []
    for t in time2:
      t = (datetime.combine(datetime.today(), t) - offset).time()
      @loop(time=t)
      async def task_2():
        await carousel_content(caster, hour, title)
      tasks.append(task_2)

    for task in tasks:
      task.start()
      
  task_1.start()
    

# @client.event
# async def on_message(message):
#   if message.content.startswith("!send"):
#     await carousel_content()

client_thread = Thread(target=run_client)
client_thread.start()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)