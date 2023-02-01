# Import requests module
import requests
from datetime import datetime

def data_parse():
  # URL
  url = "http://smtgvs.cdn.weathernews.jp/a/solive_timetable/timetable.json"  

  # Making a get request
  response = requests.get(url)
  
  # Parse the json
  data = response.json()
  
  return data

def print_caster(casters):
  found = False
  msg = "今日も1日 Have a good day.\n\n"
  # img_url = []
  # hour = []

  # IMPORTANT: use the data as the first iteration to check whether the caster is in the data or not in order to get the correct order of the time
  
  # Iterate every item in json
  for item in data_parse():
    # Iterate every caster in casters
    for caster in casters:
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
          
          # Append image URL and time
          """img_url.append(f"https://smtgvs.cdn.weathernews.jp/wnl/img/caster/M1_{program(title[1])}_{caster}.jpg?1")
hour.append(str(time))"""

          msg = msg + f"本日の{kanji(caster)}の出演予定：{title[1]} {str(time)[:-3]}〜 (Indonesia time)\n\n"

          break
          
      if found:
        break
  
  # Check if there's no casters
  if found == False:
    msg = "No caster today."

  return msg
    
# If statement for converting to kanji
def kanji(caster):
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

# If statement for program title
def program(title):
  program_title = ""
  if title == "モーニング":
    program_title = "morning"

  elif title == "サンシャイン":
    program_title = "sunshine"

  elif title == "コーヒータイム":
    program_title = "coffeetime"

  elif title == "アフタヌーン":
    program_title = "afternon"

  elif title == "イブニング":
    program_title = "evening"

  elif title == "ムーン" or title == "ムーン ":
    program_title = "moon"

  return program_title