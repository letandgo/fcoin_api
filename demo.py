from apis.trader import Trader

site='fcoin' #'fcoin_margin'
tradeapi=Trader(site).tradeapi

balance=tradeapi.balance()
print(balance)
wallet=tradeapi.wallet()
print(wallet)
