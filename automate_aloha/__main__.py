
import pandas as pd
from config import ALOHA_PATH, ALOHA_DATA, ALOHA_CASE, OUT_DATA
from aloha_bot import Aloha
import os
import re
import sys

print('Running Case: ', ALOHA_CASE)

# read .csv file
print(r'automate_aloha\out\caso_{}'.format(ALOHA_CASE), os.path.exists(r'out\caso_{}'.format(ALOHA_CASE)))

df = pd.read_csv(ALOHA_DATA)
data = df.to_dict(orient='records')

# set up the foder
if not os.path.exists(r'automate_aloha\out\caso_{}'.format(ALOHA_CASE)):
  print('the folder does not exist, making a new one')
  os.makedirs(r'automate_aloha\out\caso_{}'.format(ALOHA_CASE))

colors_path = r'automate_aloha\out\caso_{}\Colors.csv'.format(ALOHA_CASE)

# set up the colors file
  
try:
  with open(colors_path, 'r') as f:
    pass
except:
  colors = OUT_DATA[ALOHA_CASE]
  pd.DataFrame.from_dict(colors, orient='columns').to_csv(colors_path, mode='w')

close = True
sys.stdout = open(r'automate_aloha\logs\logs.txt', 'w')

# open Aloha 5.4.7

alohaApp = Aloha(ALOHA_PATH, ALOHA_CASE, close)

# run simulation
if close:
  for i, x in enumerate(data):
    try:
      print('run {i}'.format(i=i))
      with open(r'automate_aloha\data\caso_{run_case}\{i}.kml'.format(run_case = ALOHA_CASE, i = i), 'r') as f:
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
      alohaApp.run(x, i)
      print('Done {i}'.format(i=i))
    print('----------------------------------')

# close Aloha 5.4.7
  alohaApp.close()
else:
  try:
    alohaApp.print_self()
  except:
    print('No se pudo imprimir')


sys.stdout.close()