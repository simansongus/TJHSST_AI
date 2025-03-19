CACHECHANGE = {}
def change(n, coinLst):
    key = (n, tuple(coinLst))

    if key in CACHECHANGE:
        return CACHECHANGE[key]

    if n == 0:
        return 1  # Found a combination
    if n < 0 or not coinLst:
        return 0  # No valid combination

    # Calculate combinations by including and excluding the current coin
    include_current = change(n - coinLst[0], coinLst)
    exclude_current = change(n, coinLst[1:])

    # Update the cache and return the result
    CACHECHANGE[key] = include_current + exclude_current
    return CACHECHANGE[key]

temp = change(1000, [100,50,25,10,5,1])
print(temp)