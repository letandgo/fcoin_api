# fcoin_api
1，将api-key放到apis/trader.py下


2，使用方法：
from apis.trader import Trader

website='fcoin'  #'fcoin_margin'

tradeapi=Trader(website).tradeapi

balance=tradeapi.balance()

print(balance)

wallet=tradeapi.wallet()

print(wallet)

其余直接调用tradeapi的函数就可以了。
