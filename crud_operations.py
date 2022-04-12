import os

ROOT_PATH = '/opt/python/PycharmProjects/NotepadForLinux/notebooks/'

def save_edit_note(header, body):
    body = body.text
    header = header.text
    # TODO: Добавить проверку на необходимость создания папки, если нет такой папки у пользователя
    # TODO: Добавить реализацию через относительные пути
    # TODO: Если нет окончания txt то добавлять, либо сохранять в config, как в test.py
    os.chdir(ROOT_PATH)
    f = open(f'{header}', 'w', encoding='utf-8')
    f.write(body)
    f.close()
    print(header)
    print(body)

def delete_edit_note(header):
    head = header.text
    path_for_delete = os.path.join(os.path.abspath(ROOT_PATH), f'{head}')
    os.remove(path_for_delete)
    print('SuccessDelete')

def save_new_note(header, body):
    body = body.text
    header = header.text
    # TODO: Добавить проверку на необходимость создания папки, если нет такой папки у пользователя
    # TODO: Добавить реализацию через относительные пути
    os.chdir(ROOT_PATH)
    f = open(f'{header}.txt', 'w', encoding='utf-8')
    f.write(body)
    f.close()
    print(header)
    print(body)

def read_notes():
    # TODO: Сделать через один массив массивов или json
    files = os.listdir(ROOT_PATH)
    headers = []
    strings = []

    for file in files:
        headers.append(file)

    for file in files:
        f = open(f'{ROOT_PATH}{file}', 'r', encoding='utf-8')
        string = f.read()
        strings.append(string)
        f.close()

    return headers, strings

def count_notes():
    files = os.listdir(ROOT_PATH)
    headers = []
    for file in files:
        headers.append(file)

    len_massive = len(headers)
    return len_massive
