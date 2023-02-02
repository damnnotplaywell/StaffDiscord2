def data_parse():
  """
  Function to parse the json data from URL.
  """
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

          msg = msg + f"本日の{caster_kanji(caster)}の出演予定：{title[1]} {str(time)[:-3]}〜 (Indonesia time)\n\n"

          break
          
      if found:
        break
  
  # Check if there's no casters
  if found == False:
    msg = "No caster today."

  return msg

def current():
  current = data_parse()[0]
  caster = caster_trans(current['caster'])
  hour = current['hour']
  title = current['title'].split("・")[1]
  img = f'https://smtgvs.cdn.weathernews.jp/wnl/img/caster/M1_{title_trans(title)}_{caster}.jpg'

  return caster, hour, title, img