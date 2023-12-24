filename = 'resources/text_2_var_43'
with open(filename) as file:
    stroka = file.readlines()

count = 0
summ_number = 0
average_value = 0
mylist = []

for i in stroka:
    new_str = i.strip().replace("/", " ").strip().split(" ")
    len_str = len(new_str)
    for j in new_str:
        summ_number += int(j)
        count += 1
        if len_str == count:
            average_value = summ_number / count
            mylist.append(average_value)
            count = 0
            len_str = 0
            summ_number = 0

with open('results/text_2_var_43_result.txt', 'w') as result:
    for number in mylist:
        result.write(str(number) + "\n")
