import requests, math

key = "99aac01c-0625-4ed8-9ea4-5d13b88c787d"
bz_api = "https://api.hypixel.net/skyblock/bazaar"
id_api = "https://api.mojang.com/users/profiles/minecraft/"
pf_api = "https://api.hypixel.net/skyblock/profiles"

username = input("Username?\n-> ")
profile = input("Which profile? (USES PURSE)\n-> ")

def fetch_player_data(username, profile_name):
    raw_player_data = requests.get(id_api + username)
    uuid = raw_player_data.json()["id"]

    raw_profile_data = requests.get(pf_api + "?key=%s&&uuid=%s" % (key, uuid))
    player_data = raw_profile_data.json()["profiles"]
    for profile in player_data:
        if profile["cute_name"] == profile_name:
            return profile["members"][uuid]
    print("Critical Error: Player has no profile [%s]" % profile_name)

def fetch_bazaar_data():
    raw_bazaar_data = requests.get(bz_api)
    return raw_bazaar_data.json()["products"]

def find_flippable_items(player_purse, bazaar_items, min_price, max_price, min_margin, max_margin, min_moving_week):
    flippable_items = []

    for item in bazaar_items:
        data = bazaar_items[item]
        invalid = False
        try:
            top_buy_order = data["sell_summary"][0]["pricePerUnit"]
            top_sell_order = data["buy_summary"][0]["pricePerUnit"]
        except: invalid = True

        if not invalid:
            if top_buy_order < top_sell_order and top_buy_order >= min_price and top_buy_order <= max_price:
                margin = top_sell_order / top_buy_order * 100 - 100
                moved_in_a_week = (data["quick_status"]["sellMovingWeek"] + data["quick_status"]["sellMovingWeek"]) / 2
                if margin >= min_margin and margin <= max_margin and moved_in_a_week >= min_moving_week:
                    flippable_items.append([
                        item,
                        top_buy_order,
                        margin,
                        moved_in_a_week
                        ])

    return flippable_items

while True:
    player_purse = int(fetch_player_data(username, profile)["coin_purse"])
    bazaar_items = fetch_bazaar_data()
    
    min_item_price = int(input("Minimum Price Per Item? (PUT -1 IF NOT SURE)\n-> "))
    max_item_price = int(input("Maximum Price Per Item? (PUT -1 IF NOT SURE)\n-> "))
    min_margin = int(input("Minimum Margin? (PUT -1 IF NOT SURE)\n-> "))
    max_margin = int(input("Maximum Margin? (PUT -1 IF NOT SURE)\n-> "))
    min_moved_in_week = int(input("Minimum Bought/Sold in a week? (PUT -1 IF NOT SURE)\n-> "))

    if min_item_price == -1:
        min_item_price = 1000

    if max_item_price == -1:
        man_item_price = player_purse - 10

    if min_margin == -1:
        min_margin = 30

    if max_margin == -1:
        max_margin = 100
        
    if min_moved_in_week == -1:
        min_moved_in_week = 1000000
    
    flippable_items = find_flippable_items(player_purse, bazaar_items, min_item_price, max_item_price, min_margin, max_margin, min_moved_in_week)

    best_item = "None"
    best_margin = 0

    for name, price, margin, weekly in flippable_items:
        if margin > best_margin:
            best_item = name
            best_margin = margin

    print("ITEM: %s\nMARGIN: %s percent." % (best_item, math.floor(best_margin)))
    

        
    

