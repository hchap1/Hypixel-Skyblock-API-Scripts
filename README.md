# Hypixel-Skyblock-API-Scripts
Python scripts utilizing the hypixel api (mainly skyblock), docs at api.hypixel.net. 

bazaar_flip_assistant.py is a customizable program that pulls down the API data for the bazaar (a stock market type item trading system), and sorts through the items, finding flippable items, where the buy order (create an order at a low price, so when people instantly sell the items at a low price, you can get them for cheap) is lower than the sell order (selling items at a high price waiting for someone to pay a higher price to get items instantly), by a significant amount, resulting in fairly high margins. The program takes into account the amount of coins in the players purse, a min price, a max price, same for margins, and includes a sell/buy volume (bought/sold in a week) check, to claculate how fast items will sell, and takes that into account in the calculation of the best flips.
