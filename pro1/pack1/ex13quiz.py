def find_max(a, n):
    if n == 1:
        return a[0]
    max_n_1 = find_max(a, n - 1)
    print(max_n_1)
    if a[n - 1] > max_n_1:
        return a[n - 1]
    else:
        return max_n_1

v = [7, 9, 15, 43, 32, 21]
print(find_max(v, len(v)))