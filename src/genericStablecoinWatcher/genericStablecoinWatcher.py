# Imports
import time
import datetime
import os
import numpy as np
import brownie
import telegram
import helper
from dotenv import load_dotenv
load_dotenv()


# GLOBAL VARIABLES
# Token for the telegram bot
TOKEN = os.getenv('token')
# The group ID for where messages will be sent from the BOT
CHATID = os.getenv('chat_id')

#Functions
def send(msg, chat_id, token):
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)


"""Network & Account Management"""
# Connect to the avax network

#print(
#    "Ethereum (Infura) = mainnet, ropsten, rinkeby, goerli, kovan \nEthereum Classic = etc, kotti \nArbitrum = arbitrum-main \nAvalanche=avax-main,avax-test \nAurora = aurora-main, aurora-test \nBinance Smart Chain=bsc-test, bsc-main \nBoba=boba-test, boba-main \nFantom Opera=ftm-test, ftm-main \nHarmony=harmony-main, \nMoonbeam=moonbeam-main, moonbeam-test \nMoonriver=moonriver-main \nPolygon(Infura): polygon-main, polygon-test \nxDAI=xdai-main, xdai-test"
#)

#brownie.network.connect(input("Enter the chain you want to connect to name: "))

brownie.network.connect(input("avax-main")

# Check if user account exists and load user account
try:
    user = brownie.accounts.load(input("Enter your account name: "))
except Exception as err:
    print(err)

"""Contracts & Tokens Setup"""
# the token we are putting in - eg. dai = 0xd586e7f844cea2f87f50152665bcbc2c279d8d70
token0 = helper.Erc20Token(input("Enter your first token:")) 
# the token we want out  - eg. usdc = 0xa7d7079b0fead91f3e65f86e8915cb59c1a4c664
token1 = helper.Erc20Token(input("Enter your second token:")) 
"""
    the token which belongs to the blockchain we are connected to
    Eg. Native token for the avalanche chain, wavax = 0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7
"""
nativeToken = helper.Erc20Token(input("Enter your blockchain's native token:"))
"""
    router - this manages the swapping between 2 assets
    eg. router contract for traderjoe = 0x60aE616a2155Ee3d9A68541Ba4544862310933d4
"""
router_contract = brownie.Contract.from_explorer(input("Enter your DEXs router:")) 

while brownie.network.is_connected():
    qty_out = (
            router_contract.getAmountsOut( # the router contract
                1 * (10 ** token0.decimals), # the total amount you want swapped
                [
                    token0.address, # the token you put in to swap
                    nativeToken.address, # the intermediary native token contract address
                    token1.address, # the token you will recieve
                ],
            ) [-1] / (10 ** token1.decimals) # [-1] only returns the last value / by the decimals to make it human readable
        )
    send(f"1 {token0.symbol} = {qty_out} {token1.symbol}", CHATID, TOKEN)
    if qty_out in np.arange(1.01,2.00,0.01):
    # generic output  content to track if there has been a successful arbitrage opportunity
            send(f"{datetime.datetime.now().strftime('[%I:%M:S %p]')} {token0.symbol} -> {token1.symbol}: ({qty_out:.3f})", CHATID, TOKEN)
    time.sleep(1)
