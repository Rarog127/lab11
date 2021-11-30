import os
import zipfile
import hashlib
import requests
import re
import csv

arch_file = os.path.abspath("tiff-4.2.0_lab1.zip")
arch_file = zipfile.ZipFile(arch_file)

print('Задание 1')
print('Извлечение файлов из архива в директорию')
directory_to_extract_to = 'C:\\Users\\1\\PycharmProjects\\lab11\\folder'
arch_file.extractall(directory_to_extract_to)
print('Архив был распакован')
arch_file.close()
test = os.listdir(directory_to_extract_to)
print(test)

print('Задание 2')
print('Поиск всех файлов формата txt')
txt_files = []
for dirpath, dirnames, filenames in os.walk('.'):
    directory_to_extract_to = 'C:\\Users\\1\\PycharmProjects\\lab11'
    for filename in filenames:
        if filename.endswith('.txt'):
            txt_files.append(directory_to_extract_to + (os.path.join(dirpath, filename))[1::])

for filename in txt_files:
    target_file_data = open(filename, 'rb').read()
    result = hashlib.md5(target_file_data).hexdigest()
    print('{:100s}'.format(filename), result)

print('Задание 3')
print('Поиск файла по заданному хешу')
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = " "
target_file_data = " "
for dirpath, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        path = dirpath + '/' + filename
        tmp = open(path, "rb").read()
        tmp_data = hashlib.md5(tmp).hexdigest()
        if tmp_data == target_hash:
            target_file_data = tmp
            target_file_hash = tmp_data
            break
print(target_file)
print(target_file_data)
print('\n Полученный хеш: \t' + target_file_hash)
print('\n Искомый хеш: \t\t' + target_hash)

print('Задание 4')
print('Парсинг страницы по полученному хешу')
r = requests.get(target_file_data)
result_dct = {}
counter = 0
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    if counter == 0:
        headers = re.sub("<.*?>", " ", line)
        headers = re.findall("Заболели|Умерли|Вылечились|Активные случаи", headers)
    temp = re.sub("<.*?>", ';', line)
    temp = re.sub(r'\(.*?\)', '', temp)
    temp = re.sub(r'\xa0', '', temp)
    temp = re.sub(r'\s', ';', temp)
    temp = re.sub(r'\;;+', '!', temp)
    temp = re.sub(';', ' ', temp)
    temp = re.sub(r'^\!+|\s+$', '', temp)
    temp = re.sub(r'^\W+', '', temp)
    temp = re.sub(r'^\!', '', temp)
    temp = re.sub('_', '-1', temp)
    temp = re.sub(r'[*]', '', temp)
    tmp_split = re.split(r'\!', temp)
    if tmp_split != headers:
        country_name = tmp_split[0]
        result_dct[country_name] = [0, 0, 0, 0]
        for i in range(4):
            result_dct[country_name][i] = int(tmp_split[i+1])
    counter += 1
print(headers)
for key, value in result_dct.items():
    print('{:30s}'.format(key), ':', value)

print('Задание 5')
print('Запись данных из словаря в файл')
output = open('data.csv', 'w')
file_writer = csv.writer(output, delimiter=";")
file_writer.writerow(headers)
for key in result_dct.keys():
    file_writer.writerow([key, result_dct[key][0], result_dct[key][1], result_dct[key][2], result_dct[key][3]])
output.close()

print('Задание 6')
print('Вывод данных таблицы по ключу')
target_country = input("Введите название страны: ")
print(headers)
print(result_dct[target_country])
