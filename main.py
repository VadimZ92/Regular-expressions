from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    for var in contacts_list:
        if len(var) > 7:
            ## убираем лишний элемент
            var.pop(-1)
        if var == ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']:
            continue
        if var[1] == var[2] == '':
            ## делаем список из строки и обратно переводим в строку с разделением по запятой
            var[0] = ','.join(
                var[0].split())
            ## делаем список из строк с разделением по запятой
            var[0] = var[0].split(",")
            var[1] = var[0][1]
            var[2] = var[0][-1]
            var[0] = var[0][0]
        elif var[2] == '':
            var[1] = ','.join(var[1].split())
            var[1] = var[1].split(",")
            var[2] = var[1][-1]
            var[1] = var[1][0]

    contacts_list_new = []
    for value in contacts_list:
        ## переводим в строку для работы с регулярными выражениями
        text = ','.join(value)
        pattern = r"(\+7|8)?\s*.?(\d{3}).?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})([-\s]*.{5}[-\s](\d{4}))?"
        if "доб" in text:
            substitution = r"+7(\2)\3-\4-\5 доб.\7"
        else:
            substitution = r"+7(\2)\3-\4-\5"
        result = re.sub(pattern, substitution, text)
        ## переводим обратно в список
        contacts_list_var = result.split(",")
        ## измененный список
        contacts_list_new.append(contacts_list_var)

    count = -1
    list_norepeat = []
    phonebook_list = []
    for value1 in contacts_list_new:
        ##считаем номер элемента списка contacts_list_new
        count += 1
        ##проверка наличия имени в списке неповторяемых имен
        if value1[0] in list_norepeat:
            norepeat_count = -1
            for name in list_norepeat:
                ##считаем номер элемента списка неповторяемых имен
                norepeat_count += 1
                ##проверка совпадения имени в списке неповторяемых имен и списка contacts_list_new
                if name == value1[0]:
                    position_count = -1
                    for position in contacts_list_new[norepeat_count]:
                        ##считаем номер элемента списка конкретного человека
                        position_count += 1
                        if position == '':
                            ## замена пустого элемента в списке на заполненный из повтора
                            contacts_list_new[norepeat_count][position_count] = contacts_list_new[count][position_count]
                            if position_count == 6:
                                ## добавление элемента в спикок неповторяющихся имен, чтобы не нарушить порядок
                                ## так как повторный элемент пропадает
                                list_norepeat.append(contacts_list_new[norepeat_count][position_count])

        else:
            list_norepeat.append(value1[0])
            phonebook_list.append(value1)

    print(phonebook_list)

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(phonebook_list)
