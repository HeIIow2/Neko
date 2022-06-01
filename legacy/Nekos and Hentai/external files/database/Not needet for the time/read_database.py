import urllib
import os
import requests

class ReadDatabase:
    def __init__(self, url_table, external_path, like_name='likes', config_name='config.txt'):
        with open(os.path.expandvars(external_path + config_name), 'r') as config_file:
            keywords = 'new neko keys = ', 'prev neko keys = ', 'like_keys = ', 'blacklist = ', 'activate_blacklist = '
            for line in config_file:
                for i in range(len(keywords)):
                    if keywords[i] in line:
                        if i == 0:
                            self.right = line[len(keywords[i]):].split(', ')
                        elif i == 1:
                            self.left = line[len(keywords[i]):].split(', ')
                        elif i == 2:
                            self.like_keys = line[len(keywords[i]):].split(', ')
                        elif i == 3:
                            blacklist = line[len(keywords[i]):].split(', ')
                        elif i == 4:
                            if line[len(keywords[i]):].rstrip('\n') == 'True':
                                activate_blacklist = True
                            else:
                                activate_blacklist = False

        self.tags = ['all', 'liked']
        globals()[self.tags[0]] = []
        globals()[self.tags[1]] = []

        with urllib.request.urlopen(url_table) as table_file:
            for row in table_file:
                row = row.decode('utf-8').rstrip('\n')
                if any(blocked in row for blocked in blacklist) is False or activate_blacklist is False:
                    row_list = row.split('; ')

                    # index
                    row_list[0] = int(row_list[0])

                    # tags
                    row_list[2] = row_list[2].replace('(', '')
                    row_list[2] = row_list[2].replace(')', '')

                    row_list[2] = row_list[2].split(', ')
                    row_list[2] = row_list[2][:-1]

                    print(row_list)
                    for tag in row_list[2]:
                        if tag not in self.tags:
                            self.tags.append(tag)
                            globals()[tag] = []
                        globals()[tag].append(row_list[0])
                    globals()[self.tags[0]].append(row_list[0])

        with open(os.path.expandvars(external_path + like_name), 'r') as likes_file:
            likes_string = likes_file.readline()
            likes_string = likes_string.rstrip('\n')

            globals()[self.tags[1]] = likes_string.split(', ')

        print(self.tags)
        for tag in self.tags:
            print(tag)
            print(globals()[tag])

    def add_lists(self, list1, list2, mode):
        mode_keywords = 0, 1, 2

        if isinstance(list1, str):
            tuple1 = globals()[list1]
        else:
            tuple1 = list1
        if isinstance(list2, str):
            tuple2 = globals()[list2]
        else:
            tuple2 = list2

        print(tuple1, tuple2)

        final_list = []
        if mode == mode_keywords[0]:
            final_list = tuple1
            for element in tuple2:
                if element not in final_list:
                    final_list.append(element)
        elif mode == mode_keywords[1]:
            for element in tuple1:
                if element in tuple2:
                    final_list.append(element)
        elif mode == mode_keywords[2]:
            for element in tuple1:
                if element not in tuple2:
                    final_list.append(element)

        return final_list

    def string_to_list(self, filter_string):
        # final_list = self.add_lists('emo', globals()['epic'], 'or')
        operator_keywords = ' or ', ' and ', ' and not '
        if any(operator in filter_string for operator in operator_keywords) is False:
            final_list = globals()[filter_string]
        else:
            for u in range(len(operator_keywords)):
                if operator_keywords[u] in filter_string:
                    filter_strings = filter_string.split(operator_keywords[u])
                    print(filter_strings)
                    final_list = self.add_lists(filter_strings[0], filter_strings[1], u)

        return final_list


    '''
       

    def tag_and_tag(self, _start, include, _include):
        final_list = []

        if _include is True:
            for _element in _start:
                if _element in include:
                    final_list.append(_element)
        else:
            for element in _start:
                # start = list(_start)
                if element not in include:
                    final_list.append(element)

        return final_list

    def tag_or_tag(self, start, include):
        final_list = start

        for element in include:
            if element not in final_list:
                final_list.append(element)

        return final_list

    def substring_to_list(self, string):
        and_ = ' and '
        and_not = ' and not '
        or_ = ' or '

        final_list = []

        is_tuple = isinstance(string, tuple)
        # print('is tuple: ' + str(is_tuple))
        # print('string: ' + str(string))

        if is_tuple is True:
            liste = [[], []]

            string_list = list(string)
            if or_ in string_list[0] or or_ in string_list[1]:
                for i in range(len(liste)):
                    if isinstance(string_list[i], list):
                        liste[i] = string[i]
                    else:
                        string_list[i] = string_list[i].replace(or_, '')
                        liste[i] = globals()[string_list[i]]
                final_list = tag_or_tag(liste[0], liste[1])

            if and_not in string_list[0] or and_not in string_list[1]:
                for i in range(len(liste)):
                    if isinstance(string_list[i], list):
                        liste[i] = string[i]
                    else:
                        string_list[i] = string_list[i].replace(' and not ', '')
                        # print(string_list)
                        liste[i] = globals()[string_list[i]]
                final_list = tag_and_tag(liste[0], liste[1], False)

            if and_ in string_list[0] or and_ in string_list[1]:
                for i in range(len(liste)):
                    if isinstance(string_list[i], list):
                        liste[i] = string[i]
                    else:
                        string_list[i] = string_list[i].replace(and_, '')
                        liste[i] = globals()[string_list[i]]
                final_list = self.tag_and_tag(liste[0], liste[1], True)
        else:
            if or_ in string:
                string = string.split(or_)
                final_list = self.tag_or_tag(globals()[string[0]], globals()[string[1]])

            if and_not in string:
                string = string.split(and_not)
                final_list = self.tag_and_tag(globals()[string[0]], globals()[string[1]], False)

            if and_ in string:
                string = string.split(and_)
                final_list = self.tag_and_tag(globals()[string[0]], globals()[string[1]], True)

        return final_list

    def string_to_list(self, string):
        if ' or ' not in string and ' and ' not in string and ' and not ' not in string:
            final_list = globals()[string]
        else:
            final_list = []
            string = '(' + string + ')'

            if '(' in string:
                depth = 0
                brackets = []

                for i in range(len(string)):
                    if string[i] == '(':
                        brackets.append([depth, i])
                        depth += 1

                    if string[i] == ')':
                        depth -= 1
                        for element in reversed(brackets):
                            if depth == element[0]:
                                u = brackets.index(element)
                                brackets[u].append(i)
                                break

            brackets = sorted(brackets, key=lambda l: l[0], reverse=True)
            # print(brackets)

            temp_list = [[], []]
            prev_element = brackets[0]
            for i in range(len(brackets)):
                element = brackets[i]
                # print(element)
                # print(prev_element)
                if element[0] != 0:
                    if brackets[i - 1][1] == element[1]:
                        u = 0
                    else:
                        u = 1
                    if element[0] == prev_element[0]:
                        temp_list[u] = self.substring_to_list(string[element[1] + 1:element[2]])
                    else:
                        # print('ok')
                        temp_list[1 - last_u] = string[element[1] + 1:prev_element[1]]
                        temp_list[u] = self.substring_to_list(tuple(temp_list))
                    last_u = u
                else:
                    if prev_element[0] != 0:
                        temp_list[1 - last_u] = string[element[1] + 1:prev_element[1]]
                        final_list = self.substring_to_list(tuple(temp_list))
                    else:
                        final_list = self.substring_to_list(string[element[1] + 1:element[2]])

                prev_element = element

        return final_list
        '''


data = ReadDatabase('https://ln.topdf.de/img/table', '%appdata%/neko/')
current_list = data.string_to_list('emo or epic')
print('current list:')
print(current_list)