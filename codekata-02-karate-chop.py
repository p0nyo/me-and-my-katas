def binary_search_iterative(num_list, num):
    low = 0
    high = len(num_list) - 1
    while low <= high:
        mid = low + (high-low) // 2

        if num_list[mid] == num:
            return mid
        
        elif num_list[mid] > num:
            high = mid - 1

        else:
            low = mid + 1
    
    return -1


num_list = [2, 3, 4, 10, 40]
num = 10

print(binary_search_iterative(num_list, num))