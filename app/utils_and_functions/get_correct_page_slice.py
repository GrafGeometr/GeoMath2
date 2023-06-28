def get_correct_page_slice(num_of_pages, len_of_slice, index_of_current_page):
    n = num_of_pages
    k = len_of_slice
    i = index_of_current_page
    print(n, k, i)
    # look how google search works to understand
    # in a nutshell, it returns a slice with len = k, where i is the middle (except for when i is close to the borders)
    # everything is 1-indexed

    if k >= n:
        return [x for x in range(1, n + 1)]
    half = k // 2
    if i <= half + 1:
        return [x for x in range(1, k + 1)]
    elif n - (i - 1) <= (k - half):
        return [x for x in range(n - k + 1, n + 1)]
    else:
        return [x for x in range(i - half, i + (k - half))]
