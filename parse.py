import requests
from datetime import datetime

def data_parse():
    """
    Get data from the API
    """
    url = "http://smtgvs.cdn.weathernews.jp/a/solive_timetable/timetable.json"
    response = requests.get(url)
    data = response.json()
    
    return data

  
def caster_kanji(caster):
  """
  Caster name in kanji
  """
  
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

def caster_trans(caster):
  """
  Caster name alternative
  """

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
          
  return alt_caster


def title_trans(title):
  """
  Program title alternative
  """
  
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

def data(casters):
  """
  Function to print all available casters
  """
  
  caster = []
  hour = []
  title = []

  for item in data_parse():
    for key, value in item.items():
      for name in casters:
        if name in value:
          caster.append(item['caster'])

          program = item['title'].split("・")[1]
          title.append(program)

          time = datetime.strptime(item['hour'], '%H:%M') - datetime.strptime("2:00", '%H:%M')
          hour.append((datetime.min + time).strftime("%H:%M"))

  return caster, hour, title

# Function to print the message
def message(caster, hour, title):
  """
  Function to print the message
  """
  
  line = "今日も1日 Have a good day.\n\n"

  if len(caster) != 0:
    for idx in range(len(caster)):
      line = line + f"本日の{caster_kanji(caster_trans(caster[idx]))}の出演予定：{title[idx]} {hour[idx]}〜 (Indonesia time)\n\n"

  else:
    line = line + "No casters are available."

  return line