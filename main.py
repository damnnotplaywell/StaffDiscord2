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
time = time(16, 32)

# Casters
casters = ["hiyama","kobayashi", "komaki"]
data = Data(casters)

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
def send_message():
  # Parsing process
  msg = data.print_caster()

  return msg
  # # Send message to Discord
  # channel = client.get_channel(staff_channel_id)
  # await channel.send('@everyone\n' + msg)

def carousel_content():
  # Create the carousel message
  cur_caster, cur_hour, cur_title, cur_img = data.current()
  
  embed = discord.Embed(title="ウェザーニュース L!VE", description="番組表（タイムテーブル）", url="https://www.youtube.com/watch?v=zAdWzjab1B8")
  embed.set_thumbnail(url=cur_img)
  embed.add_field(name="Caster", value=caster_kanji(cur_caster))
  embed.add_field(name="Time", value=cur_hour)
  embed.add_field(name="Program", value=cur_title)

  return embed
  
####################################################
##################### TASKS ########################

@client.event
async def on_ready():
  @loop(time=time)
  async def task():
    await send_message()
  # Start the scheduled_task loop
  task.start()

@client.event
async def on_message(message):
  if message.content.startswith("!send"):
    channel = client.get_channel(botdump_channel_id)
    await channel.send(embed=carousel_content())
  elif message.content.startswith("!try"):
    channel = client.get_channel(botdump_channel_id)
    await channel.send(send_message())

client_thread = Thread(target=run_client)
client_thread.start()

#if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=8080)