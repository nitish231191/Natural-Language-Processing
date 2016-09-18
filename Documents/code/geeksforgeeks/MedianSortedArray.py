class Solution(object):
    def findMiddle(self,low,high):
        return int(low+(high-low)/2)
    def binarySearch(self,num1,target):
        low=0
        high=len(num1)-1
        if(num1[high]<target):
            return high
        if(num1[low]>target):
            return -1
        while(high-low>1):
            mid = int(low+(high-low)/2)
            if(num1[mid]<target):
                low=mid
            elif(num1[mid]>target):
                high=mid-1
            else:
                return mid-1
        if(num1[high]==target):
            return high
        if(num1[high]<target):
            return high
        return low
    def findMedianSortedArrays(self, nums1, nums2):
        low =0
        high = len(nums1)-1
        size_array1=len(nums1)
        size_array2=len(nums2)
        if( size_array1 ==0 and size_array2==0):
            return -1
        i = int(size_array1/2)
        j=  int(size_array2/2)

        if(size_array1==0):
            if(size_array2%2==0):
                return (float(nums2[j-1]+nums2[j])/2)
            else:
                return float(nums2[j])
        if(size_array2==0):
            if(size_array1%2==0):
                return (float(nums1[i-1]+nums1[i])/2)
            else:
                return float(nums1[i])
        if(nums1==nums2):
            if(size_array1%2==0):
                return (float(nums1[i-1]+nums1[i])/2)
            else:
                return float(nums1[i])
        target = (size_array1+size_array2)/2
        target =int(target)
        counter =0
        potential_result=-1
        first_loop=0
        second_loop=0
       # print target
        while(i<size_array1 and i>=0 and low<=high):
            result_index=Solution().binarySearch(nums2,nums1[i])
            print i,result_index,i+1+result_index
            if(i+1+result_index==target):
                potential_result=i
                first_loop=1
                break
            '''
            if counter ==10:
                break
                '''
            if(i+1+result_index>target or i==high):
                high=i-1
                i= Solution().findMiddle(low,high)
                #print low,high
            if( i+1+result_index<target):
                low=i+1
                i= Solution().findMiddle(low,high)
            counter=counter+1

        print "Second search Array Starts"
        low=0
        high= len(nums2)-1
        counter =0
        while(j<size_array2 and j>=0 and low<=high and first_loop==0):
            result_index=Solution().binarySearch(nums1,nums2[j])
            print j,result_index,j+1+result_index
            '''
            if counter ==10:
                break
                '''
            if(j+1+result_index == target):
                potential_result=j
                second_loop=1
                break
            if(j+1+result_index>target or j==high):
                high=j-1
                j=Solution().findMiddle(low,high)
                print "low and high",low,high,j

            if( j+1+result_index<target):
                low=j+1
                j= Solution().findMiddle(low,high)
            counter =counter+1
        print "potential_Result",potential_result
        if second_loop ==1:
            temp=nums1
            nums1=nums2
            nums2=temp
        if (size_array1+size_array2)%2==0 and potential_result >=0:
            index = Solution().binarySearch(nums2,nums1[potential_result])
            print index
            if index>=0 and potential_result==0:
                return (float(nums2[index]+nums1[potential_result])/2)
            if index >=0 and nums2[index]>nums1[potential_result-1] and potential_result>=1:
                return (float(nums2[index]+nums1[potential_result])/2)
            if index>=0 and nums2[index]<=nums1[potential_result-1] and potential_result>=1:
                return (float(nums1[potential_result-1]+nums1[potential_result])/2)
            if index==-1:
                return (float(nums1[potential_result-1]+nums1[potential_result])/2)
        if((size_array1+size_array2)%2!=0) and potential_result>=0:
            return float (nums1[potential_result])
        return -1




        
