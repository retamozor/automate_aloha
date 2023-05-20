from dotenv import load_dotenv
import os

load_dotenv()

path = os.environ.get('ALOHA_PATH')
ALOHA_PATH = ""

if not path:
    raise EnvironmentError('la variable de entorno ALOHA_PATH no esta definida')

ALOHA_PATH = path

caso = os.environ.get('ALOHA_CASE')
ALOHA_CASE=""

if not caso:
    raise EnvironmentError('la variable de entorno ALOHA_CASE no esta definida')
ALOHA_CASE = caso

data = os.environ.get('ALOHA_DATA')
ALOHA_DATA = ""

if not data:
    raise EnvironmentError('la variable de entorno ALOHA_DATA no esta definida')

ALOHA_DATA = data

OUT_DATA = {}

# caso 1
OUT_DATA['1'] = {
    'index' : [],
    'Red'   : [],
    'Orange': [],
    'Yellow': [],
}

# caso 2
OUT_DATA['2'] = {
    'index' : [],
    'Red'   : [],
    'Orange': [],
    'Yellow': [],
    'Max Flame Length': [],
    'Burn Duration': [],
    'Max Burn Rate': [],
    'Total Amount Burned': [],
}