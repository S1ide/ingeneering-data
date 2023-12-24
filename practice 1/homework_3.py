import math

filename = 'resources/text_3_var_43'
with open(filename) as file:
    lines = file.readlines()

mylist = []

for j in lines:
    nums = j.strip().split(",")
    for i in range(len(nums)):
        if nums[i] == 'NA':
            nums[i] = str((int(nums[i - 1]) + int(nums[i + 1])) / 2)

    filtred = list()
    for j in nums:
        number = float(j)
        if math.sqrt(number) > 70:
            mylist.append(number)

with open('results/text_3_var_43_result.txt', 'w') as result:
    for number in mylist:
        result.write(str(number) + "\n")