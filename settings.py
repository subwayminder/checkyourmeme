import dotenv

QUANTITY_THREADS = int(dotenv.get_key('.env', 'QUANTITY_THREADS')) if dotenv.get_key('.env', 'QUANTITY_THREADS') != None else 5
USE_PROXY = dotenv.get_key('.env', 'USE_PROXY') == 'True' if dotenv.get_key('.env', 'USE_PROXY') != None else False
CHECK_PROXY = dotenv.get_key('.env', 'CHECK_PROXY') == 'True' if dotenv.get_key('.env', 'CHECK_PROXY') != None else False
RPC = str(dotenv.get_key('.env', 'RPC'))
MEME_INFO_ENDPOINT = str(dotenv.get_key('.env', 'MEME_INFO_ENDPOINT'))
