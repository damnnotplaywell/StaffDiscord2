from datetime import time, timedelta
from threading import Thread
from discord import Client
from discord.ext.tasks import loop
from flask import Flask
from parse import *
import os
import discord
import json
import asyncio

# Set up Flask
app = Flask(__name__)

# Bot class
class Bot:
    def __init__(self):
        # Client set up
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=self.intents)

        # Channel ID
        self.staff_channel_id = 1049414474274189333

        # Caster
        self.casters = ["hiyama2018", "kobayashi", "komaki2018"]

        # Time set up
        self.offset = timedelta(hours=7)
        self.time1 = time(2, 0)
        self.time1 = (datetime.combine(datetime.today(), self.time1) - self.offset).time()
    
    # Run the bot
    def run_client(self):
        try:
            self.client.run(os.environ['TOKEN'])
        except:
            print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
            os.system("kill 1")
            os.system("python restarter.py")

    @app.route('/')
    def index():
        return "I'm alive!"
    
    # Function to send the message
    async def send_message(self, caster, hour, title):
        msg = message(caster, hour, title)
        channel = self.client.get_channel(self.staff_channel_id)

        try:
            await channel.send("@everyone\n" + msg)
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after)
                await self.send_message(caster, hour, title)

    # Function to send the carousel message
    async def carousel_content(self, caster, hour, title, idx):
        embed = discord.Embed(
            title="ウェザーニュース LiVE",
            description="番組表（タイムテーブル）",
            url="https://www.youtube.com/watch?v=zAdWzjab1B8"
        )
        img=f'https://smtgvs.cdn.weathernews.jp/wnl/img/caster/M1_{title_trans(title[idx])}_{caster_trans(caster[idx])}.jpg'

        embed.set_thumbnail(url=img)
        embed.add_field(name="Caster", value=caster_kanji(caster_trans(caster[idx])))
        embed.add_field(name="Time", value=hour[idx])
        embed.add_field(name="Program", value=title[idx])

        channel = self.client.get_channel(self.staff_channel_id)

        try:
            await channel.send(embed=embed)
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after)
                await self.carousel_content(caster, hour, title, idx)

    async def on_ready(self):
        tasks = []

        # Task 1: Send the message every day at 2 AM
        @loop(time=self.time1)
        async def task_1():
            caster, hour, title = data(self.casters)
            message = {
                "caster": caster,
                "hour": hour,
                "title": title
            }
            json_message = json.dumps(message, indent=4, ensure_ascii=False)

            with open("data.json", "w") as outfile:
                outfile.write(json_message)
            
            await self.send_message(caster, hour, title)

            try:
                with open("data.json", "r") as openfile:
                    json_object = json.load(openfile)
                    caster2 = json_object["caster"]
                    hour2 = json_object["hour"]
                    title2 = json_object["title"]

                    time2 = [time.fromisoformat(t) for t in hour2]

                    for t_idx, t in enumerate(time2):
                        t = (datetime.combine(datetime.today(), t) - self.offset).time()
                        
                        # Task 2: Send the carousel message every day at the time specified in the data.json file
                        async def task_2(t_idx=t_idx):
                            await self.carousel_content(caster2, hour2, title2, t_idx)
                        task_2_loop = loop(time=t)(task_2)
                        tasks.append(task_2_loop)

                # Start the tasks
                task_1.start()
                for task in tasks:
                    task.start()

            except:
                print("Data not found. Creating new data.json file.")
                task_1.start()

bot = Bot()
client_thread = Thread(target=bot.run_client)
client_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)