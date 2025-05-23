import pytest

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


def binary_search_recursive(num_list, low, high, num):
    while low <= high:
        mid = low + (high-low) // 2

        if num_list[mid] == num:
            return mid
        
        elif num_list[mid] > num:
            return binary_search_recursive(num_list, low, mid-1, num)

        else:
            return binary_search_recursive(num_list, mid+1, high, num)
    return -1




class TestBinarySearch:
    def test_binary_search_iterative(self):
        num_list = [2, 3, 4, 10, 40]
        num = 10

        assert binary_search_iterative(num_list, num) == 3

    def test_binary_search_iterative_first(self):
        num_list = [2, 3, 4, 10, 40]
        num = 2

        assert binary_search_iterative(num_list, num) == 0

    def test_binary_search_iterative_last(self):
        num_list = [2, 3, 4, 10, 40]
        num = 40

        assert binary_search_iterative(num_list, num) == 4

    def test_binary_search_iterative_empty_list(self):
        num_list = []
        num = 10

        assert binary_search_iterative(num_list, num) == -1

    def test_binary_search_recursive(self):
        num_list = [2, 3, 4, 10, 40]
        num = 10

        assert binary_search_recursive(num_list, 0, len(num_list)-1, num) == 3

    def test_binary_search_recursive_first(self):
        num_list = [2, 3, 4, 10, 40]
        num = 2

        assert binary_search_recursive(num_list, 0, len(num_list)-1, num) == 0

    def test_binary_search_recursive_last(self):
        num_list = [2, 3, 4, 10, 40]
        num = 40

        assert binary_search_recursive(num_list, 0, len(num_list)-1, num) == 4

    def test_binary_search_recursive_empty_list(self):
        num_list = []
        num = 10

        assert binary_search_recursive(num_list, 0, len(num_list)-1, num) == -1
