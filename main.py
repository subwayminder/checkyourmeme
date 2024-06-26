from typing import Union
from loguru import logger
from concurrent.futures import ProcessPoolExecutor
from config import ACCOUNTS, PROXIES
from settings import USE_PROXY, CHECK_PROXY, MEME_INFO_ENDPOINT, RPC, QUANTITY_THREADS
import requests
import csv
from web3 import Web3

def getWallets():
    if USE_PROXY:
        account_with_proxy = dict(zip(ACCOUNTS, PROXIES))

        wallets = [
            {
                "id": _id,
                "address": key,
                "proxy": account_with_proxy[key]
            } for _id, key in enumerate(account_with_proxy, start=1)
        ]
    else:
        wallets = [
            {
                "id": _id,
                "address": key,
                "proxy": None
            } for _id, key in enumerate(ACCOUNTS, start=1)
        ]
    return wallets

def check_proxy(proxy):
    request_kwargs = {"proxies": {"https": f"http://{proxy}"}}
    w3 = Web3(Web3.HTTPProvider(RPC, request_kwargs=request_kwargs))
    if w3.is_connected():
        logger.info(f"Прокси [http://{proxy}] работает")
        return True
    raise ValueError(f"Прокси [http://{proxy}] не работает")

def run_check(address: str, proxy: Union[str, None]):
    url = MEME_INFO_ENDPOINT
    headers = {}
    if USE_PROXY:
        headers = {"proxy": f"http://{proxy}"}
    r = requests.get(url=url + address)
    if r.status_code == 200:
        body = r.json()
        return [address, body['steaks']['total'], body['steaks']['perWeek']]

def run(account):
    return run_check(account.get('address'), account.get('proxy'))

def main():
    if(CHECK_PROXY):
        with ProcessPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
            for _id, key in enumerate(PROXIES):
                executor.submit(check_proxy, key)

    wallets = getWallets()

    with ProcessPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        res = list(executor.map(run, wallets))

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Address", "Total", "Per week"])
        writer.writerows(row for row in res)
            
# logger.add("output.log")
main()