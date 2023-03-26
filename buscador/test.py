
def a(x):
    price_list = [10, x, 10, 10]

    if len(set(price_list)) == 1:
        print("All prices in the list are the same.")
        return False
    else:
        print("Not all prices in the list are the same.")
        return True


a("sfas")