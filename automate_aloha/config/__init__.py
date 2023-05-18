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