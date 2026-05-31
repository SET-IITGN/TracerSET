def find_lucky_index(nums):
    total_sum = sum(nums)
    left_sum = 0

    for i in range(len(nums)):
        total_sum -= nums[i]

        if left_sum == total_sum:
            return i

        left_sum += nums[i]

    return -1
input_list=list(map(int, input().strip("[]").split()))

result = find_lucky_index(input_list)
print(result)