count = {1:0,
               10:0,
               100:0,
               1000:0}

def coin_dropped(dropped_coins):
    coins = dropped_coins

    while coins > 0:
        count[check(coins)] += 1
        coins -= check(coins)
 

    print(count)
    return count
def check(dropped_coins):
    
    coins = dropped_coins
    if coins >= 1000:
        return 1000
    elif coins >= 100:
        return 100
    elif coins >= 10:
        return 10
    elif coins >= 1:
        return 1
