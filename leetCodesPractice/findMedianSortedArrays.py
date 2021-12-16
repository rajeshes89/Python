"""
Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
"""

class Solution(object):

    def findMedianSortedArrays(self, num1, num2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        import math
        a = sorted(num1+num2)
        if len(a)%2 == 0:
            return (a[int(len(a)/2) ] + (a[int(len(a)/2)- 1])) / 2.0
        else:
            return a[int(math.floor(len(a)/2))]
