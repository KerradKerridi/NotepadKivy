import os

root_path = '/opt/python/PycharmProjects/NotepadForLinux/notebooks/'

def save_note(self, header, body):
    Body = body.text
    Header = header.text
    #TODO: Добавить проверку на необходимость создания папки, если нет такой папки у пользователя
    #TODO: Добавить реализацию через относительные пути
    os.chdir(root_path)
    f = open(f'{Header}.txt', 'w', encoding='utf-8')
    f.write(Body)
    f.close()
    print(Header)
    print(Body)

def delete_note(self, header):
    Header = header.text
    pathtodel = os.path.join(os.path.abspath(root_path), f'{Header}.txt')
    os.remove(pathtodel)
    print('Success')

def read_notes(self):
    #TODO: Сделать через один массив массивов или json
    files = os.listdir(root_path)
    headers = []
    strings = []

    for file in files:
        headers.append(file)

    lenMassive = len(headers)

    for file in files:
        f = open(f'{root_path}{file}', 'r', encoding='utf-8')
        string = f.read()
        strings.append(string)
        f.close()

    print(headers)
    print(strings)
    print(lenMassive)