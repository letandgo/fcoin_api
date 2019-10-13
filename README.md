# fcoin_api

使用方法：
from apis.trader import Trader

website='fcoin'  #'fcoin_margin'
tradeapi=Trader(website).tradeapi

balance=tradeapi.balance()
print(balance)
wallet=tradeapi.wallet()
print(wallet)

其余直接调用tradeapi的函数就可以了。
