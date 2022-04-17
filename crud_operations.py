import os

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = f'{PARENT_DIR}/notebooks/'

def save_edit_note(header, body):
    body = body.text
    header = header.text
    #TODO: Добавить проверку на необходимость создания папки, если нет такой папки у пользователя
    #TODO: Добавить реализацию через относительные пути
    #TODO: Если нет окончания txt то добавлять, либо сохранять в config, как в test.py
    print(ROOT_PATH)
    os.chdir(ROOT_PATH)
    f = open(f'{header}', 'w', encoding='utf-8')
    f.write(body)
    f.close()


def delete_edit_note(header):
    head = header.text
    path_for_delete = os.path.join(os.path.abspath(ROOT_PATH), f'{head}')
    os.remove(path_for_delete)
    print('SuccessDelete')


def save_new_note(header, body):
    body = body.text
    header = header.text
    os.chdir(ROOT_PATH)
    f = open(f'{header}.txt', 'w', encoding='utf-8')
    f.write(body)
    f.close()


def read_notes():
    #TODO: Сделать через один массив массивов или json
    try:
        files = os.listdir(ROOT_PATH)
    except FileNotFoundError:
        new_dir = os.mkdir(f'{PARENT_DIR}{ROOT_PATH}')
        files = os.listdir(new_dir)
    headers = []
    strings = []
    first_strings = []

    for file in files:
        headers.append(file)

    for file in files:
        f = open(f'{ROOT_PATH}{file}', 'r', encoding='utf-8')
        string = f.read()
        strings.append(string)
        f.close()

    for file in files:
        f = open(f'{ROOT_PATH}{file}', 'r', encoding='utf-8')
        first_string = f.readline()
        first_strings.append(first_string)
        f.close()

    return headers, strings, first_strings


def count_notes():
    try:
        files = os.listdir(ROOT_PATH)
    except FileNotFoundError:
        new_dir = os.mkdir(f'{ROOT_PATH}')
        files = os.listdir(new_dir)
    headers = []
    for file in files:
        headers.append(file)

    len_massive = len(headers)
    return len_massive
