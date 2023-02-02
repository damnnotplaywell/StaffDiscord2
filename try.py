import requests
from datetime import datetime

# Function to parse the json data from URL
def data_parse():
    url = "http://smtgvs.cdn.weathernews.jp/a/solive_timetable/timetable.json"
    response = requests.get(url)
    data = response.json()
    
    return data

# If statement for kanji caster name         
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

# Function to print all available casters
def data(casters):
    caster = []
    hour = []
    title = []

    for item in data_parse():
        for key, value in item.items():
            for name in casters:
                if name in value:
                    caster.append(item['caster'])
                    hour.append(item['hour'])
                    title.append(item['title'])
    
    return caster, hour, title

def message(casters):
    caster, hour, title = data(casters)
    
    line = "今日も1日 Have a good day.\n\n"
    
    for idx in range(len(casters)):
        program = title[idx].split("・")

        # Timezone different
        time = datetime.strptime(hour[idx], '%H:%M') - datetime.strptime("2:00", '%H:%M')
        line = line + f"本日の{caster_kanji(caster_trans(caster[idx]))}の出演予定：{program[1]} {str(time)[:-3]}〜 (Indonesia time)\n\n"

    return line
        

casters = ["hiyama2018", "kobayashi", "komaki2018"]
print(message(casters))