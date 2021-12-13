"""
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Output: Because nums[0] + nums[1] == 9, we return [0, 1].
"""

def twoSum(nums, target):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[j] == target - nums[i]:
                    print(i,nums[i],j,nums[j])
                    return [i, j]

sol = twoSum([1,2,3,4],5)
print(sol)


## Sample Output 
root@localhost:/home/test# python3 test.py 
0 1 3 4
[0, 3]
root@localhost:/home/test# 
