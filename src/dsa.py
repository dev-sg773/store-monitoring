
def maximumProfit(prices:list) -> int:
    prices_dict = {} 
    for i, val in enumerate(prices):
        prices_dict[val]=i
    '''
    {
        7:0,
        1:1,
        5:2,
        3:3,
        6:4, 
        4:5,
    }
    '''
    prices.sort() # [1,3,4,5,6,7]
    left = 0
    right = len(prices) -1
    profit = []

    while left <= right: #left = 1 , right = 4
        if prices_dict[prices[left]] < prices_dict[prices[right]]: #left index value = 3, right index = 2
            profit.append(prices[right] - prices[left])
            left+=1
        else:
            right -=1
        print('left--, right', left, right)
    return max(profit)

if __name__ == "__main__":
    prices = [7,1,5,3,6,4]
    print(maximumProfit(prices=prices))
    # pass