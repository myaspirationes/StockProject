# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/1 19:13
@Auth ： Tiger
@File ：leeCodes.py
@IDE ：PyCharm
@Motto:
"""



class Solution:
    """
    问题描述：
    给定一个整数数组和一个目标值，找出数组中和为目标值的两个数。
    你可以假设每个输入只对应一种答案，且同样的元素不能被重复利用。
    示例:
    给定 nums = [2, 7, 11, 15], target = 9
    因为 nums[0] + nums[1] = 2 + 7 = 9
    所以返回 [0, 1]
    """
    def twoSum(self, nums, target):
        i = 0
        while i < len(nums):
            if i == len(nums) - 1:
                return "No solution here!"
            r = target - nums[i]
            # Can't use a num twice
            num_follow = nums[i + 1:]
            if r in num_follow:
                return [i, num_follow.index(r) + i + 1]
            i = i + 1

    """
    问题描述：
    给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有和为 0 且不重复的三元组。
    注意：答案中不可以包含重复的三元组。
    示例 1：
    输入：nums = [-1,0,1,2,-1,-4]
    输出：[[-1,-1,2],[-1,0,1]]
    """
    def threeSum(self,nums):
        # 先排序
        nums.sort()
        res = []

        for i in range(len(nums) - 2):
            # 如果当前的数等于前面的数，continue
            if (i > 0) and (nums[i] == nums[i - 1]):
                continue
            # 双指针
            left = i + 1
            right = len(nums) - 1
            # 跳出条件
            while left < right:
                sum = nums[i] + nums[left] + nums[right]
                # 如果三数之和小于0，那么左指针右移
                if sum < 0:
                    left += 1
                # 如果三数之和大于0，那么右指针左移
                if sum > 0:
                    right -= 1
                # 如果三数之和等于0
                if sum == 0:
                    # 把三个数添加到结果中
                    res.append([nums[i], nums[left], nums[right]])
                    # 去除重复的左边元素
                    while (left < right) and (nums[left] == nums[left + 1]):
                        left += 1
                    # 去除重复的右边元素
                    while (left < right) and (nums[right] == nums[right - 1]):
                        right -= 1
                    # 更新指针
                    left += 1
                    right -= 1

        return res



if __name__ == '__main__':

        souluton=Solution()

        list=[1,4,67,2,4,56,66,6]
        print(souluton.twoSum(list,89))

        nums = [3,-1, 0, 1, 2, -1, -4]
        print(souluton.threeSum(nums))