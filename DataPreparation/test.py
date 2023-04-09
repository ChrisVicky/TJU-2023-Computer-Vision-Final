import os
nums = os.listdir("./results")
nums = [int(i) for i in nums]
print(nums)
print(max(nums))
