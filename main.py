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

channel_id = 1049414474274189333

# Set up time
time = time(19, 0)

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

async def scheduled_task():
  # Parsing process
  casters = ["hiyama", "kobayashi", "komaki"]
  msg = print_caster(casters)
  
  # Send message to Discord
  channel = client.get_channel(channel_id)
  await channel.send('@everyone\n' + msg)
  
@client.event
async def on_ready():
  @loop(time=time)
  async def task():
    await scheduled_task()
  # Start the scheduled_task loop
  task.start()

client_thread = Thread(target=run_client)
client_thread.start()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


"""async def img_send(img_url):
  # Send image to Discord
  channel = client.get_channel(channel_id)
  await channel.send(file=File(BytesIO(img_url.content), filename='image.png'))

@client.event
async def on_ready():
  msg, img_url, hour = print_caster(casters)
  hour = time(14,7)
  for i in range(len(img_url)):
    @loop(time=hour)
    async def task():
      await img_send(i)
      task.start()"""