import os
import json
import csv


def check_file_exist(filename, required=False):
    if not os.path.exists(filename):
        if required:
            print('filename is required!', filename)
            exit(1)
        # print('file not exist:', filename)
        return False
    # ('file exist:', filename)
    return True


def check_dir_exist(dirname, create=False, required=False):
    if not os.path.exists(dirname):
        if required:
            print('dir is required!', dirname)
            exit(1)
        if create:
            os.makedirs(dirname)
            print('create dir:', dirname)
            return True
        return False
    return True


def load(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


def store(data, filename):
    with open(filename, 'w') as json_file:
        # json_file.write(json.dumps(data, indent=2))
        json_file.write(json.dumps(data, indent=2, ensure_ascii=False))


def load_text_lines(filename):
    with open(filename) as txt_file:
        lines = txt_file.readlines()
        return lines


def write_text_lines(lines, filename):
    with open(filename, 'w', encoding='utf-8') as txt_file:
        txt_file.writelines(lines)


def load_text(filename):
    with open(filename, 'r') as txt_file:
        lines = txt_file.read()
        return lines


def write_text(text, filename):
    with open(filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)


def load_csv_lines(filename, encoding='ISO-8859-1'):
    with open(filename, 'r', newline='', encoding=encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = []
        for row in csv_reader:
            data.append(row)
        return data


def write_csv_lines(lines, filename, encoding='ISO-8859-1'):
    with open(filename, 'w', newline='', encoding=encoding) as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(lines)