# Import requests module
import requests
from datetime import datetime

class Data:
  def __init__(self, casters):
    self.casters = casters
    self.data = self.data_parse()

  def data_parse(self):
    """
    Function to parse the json data from URL.
    """
    
    # URL
    url = "http://smtgvs.cdn.weathernews.jp/a/solive_timetable/timetable.json"  

    # Making a get request
    response = requests.get(url)

    # Parse the json
    self.data = response.json()

    return self.data

  def print_caster(self):
    """
    Function to print all available casters.
    """
    
    found = False
    line = "今日も1日 Have a good day.\n\n"
  
    # IMPORTANT: use the data as the first iteration to check whether the caster is in the data or not in order to get the correct order of the time
    
    # Iterate every item in json
    for item in self.data_parse():
      # Iterate every caster in casters
      for caster in self.casters:
        # Iterate every values in json
        for value in item.values():
          # Check whether the caster is in the values
          if caster in value:
            # Set found to True
            found = True
            # Split the title to get the program title
            title = item['title'].split("・")
            # Timezone different
            time = datetime.strptime(item['hour'], '%H:%M') - datetime.strptime("2:00", '%H:%M')
            line = line + f"本日の{caster_kanji(caster)}の出演予定：{title[1]} {str(time)[:-3]}〜 (Indonesia time)\n\n"
  
            break
            
        if found:
          break
    
    # Check if there's no casters
    if found == False:
      line = "No caster today."
  
    return line

  def current(self):
    self.data = self.data_parse()[0]
    self.caster = caster_trans(self.data['caster'])
    self.hour = self.data['hour']
    self.title = self.data['title'].split("・")[1]
    self.img = f'https://smtgvs.cdn.weathernews.jp/wnl/img/caster/M1_{title_trans(self.title)}_{self.caster}.jpg'
    
    return (self.caster, self.hour, self.title, self.img)

# If statement for converting to kanji
def caster_kanji(caster):
  kanji_caster = ""
  if caster == "kobayashi":
    kanji_caster = "小林 李衣奈"

  elif caster == "hiyama":
    kanji_caster = "檜山 沙耶"

  elif caster == "komaki":
    kanji_caster = "駒木 結衣"

  else:
    kanji_caster = caster
    
  return kanji_caster

# If statement for caster name alternative
def caster_trans(caster):
  alt_caster = caster
  
  if caster == "ailin":
    alt_caster = "yamagishi"
    
  elif caster == "hiyama2018":
    alt_caster = "hiyama"
  
  elif caster == "izumin":
    alt_caster = "maie"
  
  elif caster == "komaki2018":
    alt_caster = "komaki"
  
  elif caster == "matsu":
    alt_caster = "matsuyuki"
    
  elif caster == "ohshima":
    alt_caster = "oshima"

  elif caster == "sayane":
    alt_caster = "egawa"

  elif caster == "yuki":
    alt_caster = "uchida"
          
  return alt_caster;

# If statement for program title
def title_trans(title):
  alt_title = ""

  if title == "モーニング":
    alt_title = "morning"

  elif title == "サンシャイン":
    alt_title = "sunshine"

  elif title == "コーヒータイム":
    alt_title = "coffeetime"

  elif title == "アフタヌーン":
    alt_title = "afternoon"

  elif title == "イブニング":
    alt_title = "evening"

  elif title == "ムーン" or title == "ムーン ":
    alt_title = "moon"

  return alt_title


############################
@client.event
async def on_message(message):
  if message.content.startswith("!send"):
    channel = client.get_channel(botdump_channel_id)
    await channel.send(embed=carousel_content())
  elif message.content.startswith("!try"):
    channel = client.get_channel(botdump_channel_id)
    await channel.send(send_message())

##############################

@client.event
async def on_ready():
  @loop(time=time)
  async def task():
    await send_message()
  # Start the scheduled_task loop
  task.start()