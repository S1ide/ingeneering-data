filename = 'resources/text_1_var_43'
with open(filename) as file:
    s = file.readlines()

word_stat = dict()

for text in s:
    new_str = (text.strip()
               .replace("!", " ")
               .replace("?", " ")
               .replace(".", " ")
               .replace(",", " ")
               .strip()).split(" ")
    for new_word in new_str:
        if new_word in word_stat:
            word_stat[new_word] += 1
        else:
            word_stat[new_word] = 1

word_stat = (dict(sorted(word_stat.items(), reverse=True, key=lambda item: item[1])))
print(word_stat)

res_file_name = 'results/text_1_var_43_result.txt'

with open(res_file_name, 'w') as result:
    for key, value in word_stat.items():
        result.write(key + ":" + str(value) + "\n")