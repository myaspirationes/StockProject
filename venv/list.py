import numpy as np

list_one=[1,2,3,4,6,8,9,12]
list_two=[1,2,3,4,6,8,9,9,9,12]

print(list_one[list_one[0] == list_two[0]])


str="shang,lang"
print(list(str))
print(list_two)
print(list_two.pop(6))
list_two.insert(-2, 30)
print(list_two)



#list append 在list后面添加“一个”元素或对象，括号内是一个整体添加进入
list_one.append(["1","2"])
print(list_one)
list_one.append(1)
print(list_one)
list_one.append((2,5,8))
print(list_one)
#extend  拆分未单个后添加
list_one.extend("shanghai")
list_one.extend((2,4,8))
print(list_one)
#提取list中嵌套的元素
print(list_one[8][1])
print(list_one[10][1])

#统计某个元素在列表中出现的次数
print(list_one.count("h"))

#显示元素的位置,只显示第一个出现的位置
print(list_one.index(8))

#b = a[i:j]   #表示复制a[i]到a[j-1]，以生成新的list对象
#a[:]就相当于完整复制一份a
#b = a[i:j:s]  #表示：i,j与上面的一样，但s表示步进，缺省为1.
#所以a[::-1]   #相当于 a[-1:-len(a)-1:-1]，也就是从最后一个元素到第一个元素复制一遍，即倒序。
temp = [('a', 1, 1.5),
        ('b', 2, 5.1),
        ('c', 9, 4.3)]
print(temp)

# temp.sort(key)
#找到其中是 ('b', XX, XX) 这样的元素
temp.sort(key=lambda x: x[0]!= 'b')
print(temp[0])


students  =  [( 'john' ,  'A' ,  15 ), ( 'jane' ,  'B' ,  20 ), ( 'dave' ,  'B' ,  10 )]
sorted (students, key = lambda  student : student[ 0 ])
print(students)

a = np.random.rand(5)
print("-------------->")
print(a)
#[0.64061262 0.8451399  0.965673  0.89256687 0.48518743]

print(a[-1])  ###取最后一个元素
#[0.48518743]

print(a[:-1])  ### 除了最后一个取全部
#[0.64061262 0.8451399  0.965673  0.89256687]

print(a[::-1])  ### 取从后向前（相反）的元素
#[0.48518743 0.89256687 0.965673  0.8451399  0.64061262]

print(a[2::-1])  ### 取从下标为2的元素翻转读取
#[0.965673 0.8451399  0.64061262]

x  = [ 4 ,  6 ,  2 ,  1 ,  7 ,  9 ]
y  =  x.copy()
y.sort()
print(y)  #[1, 2, 4, 6, 7, 9]
print (x)   #[4, 6, 2, 1, 7, 9]


alist  =  [( '2' ,  '3' ,  '10' ), ( '1' ,  '2' ,  '3' ), ( '5' ,  '6' ,  '7' ), ( '2' ,  '5' ,  '10' ), ( '2' ,  '4' ,  '10' )]
# 多级排序，先按照第3个元素排序，然后按照第2个元素排序：
sorted (alist, key  =  lambda  x:( int (x[ 2 ]),  int (x[ 1 ])), reverse  =  False )
print(alist)

#字典根据键从小到大排序
dic={"name":"zs","age":18,"city":"深圳","tel":"1362626627"}
lis=sorted(dic.items(),key=lambda x:x[0],reverse=False)
print(lis)
print(dict(lis))

def twoSum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """

    for i in range(len(nums)):
        for j in range(i,len(nums)):
            if (nums[i] + nums[j] == 9):
                print(i, j)


if __name__ == '__main__':
    twoSum( nums = [2, 5,4,7, 11, 15,7],
        target = 9)


