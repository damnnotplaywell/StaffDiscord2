import os
import discord
from datetime import time
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
time1 = time(20, 0)

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

async def carousel_content():
  # Create the carousel message
  cur_caster, cur_hour, cur_title, cur_img = current()
  
  embed = discord.Embed(title="ウェザーニュース L!VE", description="番組表（タイムテーブル）", url="https://www.youtube.com/watch?v=zAdWzjab1B8")
  embed.set_thumbnail(url=cur_img)
  embed.add_field(name="Caster", value=caster_kanji(caster_trans(cur_caster)))
  embed.add_field(name="Time", value=cur_hour)
  embed.add_field(name="Program", value=cur_title)

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
  msg, hour2 = message(casters)
  time2 = [time.fromisoformat(t) for t in hour2]

  tasks = []
  for t in time2:
    @loop(time=t)
    async def task_2():
      await carousel_content()
    tasks.append(task_2)
  
  # Start the scheduled_task loop
  task_1.start()
  for task in tasks:
    task.start()

client_thread = Thread(target=run_client)
client_thread.start()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)