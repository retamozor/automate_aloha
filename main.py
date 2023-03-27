
import pandas as pd
from app.Aloha import Aloha
from decouple import config
import os

aloha_path = config('ALOHA_PATH', default=r'C:\Program Files (x86)\ALOHA\ALOHA.EXE')
run_case = config('ALOHA_CASE', default=2, cast=int)
data_path = config('ALOHA_DATA', default='Cyclohexanone_tank_case1.csv')
print(run_case)

# read .csv file

df = pd.read_csv(data_path)
data = df.to_dict(orient='records')

# set up the foder
if not os.path.exists(r'caso_{}'.format(run_case)):
  print('no existe')
  os.makedirs(r'caso_{}'.format(run_case))

colors_path = r'caso_{}\Colors.csv'.format(run_case)

# set up the colors file
  
try:
  with open(colors_path, 'r') as f:
    pass
except:
  colors = {
    'index' : [],
    'Red'   : [],
    'Orange': [],
    'Yellow': [],
  }
  pd.DataFrame.from_dict(colors, orient='columns').to_csv(colors_path, mode='w')

# open Aloha 5.4.7

alohaApp = Aloha(aloha_path)
alohaApp.setup()

# run simulation

for i, x in enumerate(data):
  try:
    print('run {i}'.format(i=i))
    with open(r'caso_{run_case}\{i}.kml'.format(run_case = run_case, i = i), 'r') as f:
      print('Already done {i}'.format(i=i))
  except:
    # read Color.csv and find index i in column 'index'
    df = pd.read_csv(colors_path)
    if (i in df['index'].values):
      print('Already done {i}'.format(i=i))
      continue
    if (x['Liquid level'] == 0):
      print('Liquid level = 0')
      continue
    if x['Liquid level'] <= x['Height of the Tank opening']:
      print('Liquid level <= Height of the Tank opening')
      continue
    alohaApp.run(x, i, run_case)
    print('Done {i}'.format(i=i))
  print('----------------------------------')

# close Aloha 5.4.7

alohaApp.close()
