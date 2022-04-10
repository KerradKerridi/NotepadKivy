import os

def save_note(self, header, body):
    Body = body.text
    Header = header.text
    os.chdir('/opt/python/PycharmProjects/NotepadForLinux/notebooks')
    f = open(f'{Header}.txt', 'w', encoding='utf-8')
    f.write(Body)
    f.close()
    print(Header)
    print(Body)

def delete_note(self, header):
    Header = header.text
    root_path = '/opt/python/PycharmProjects/NotepadForLinux/notebooks/'
    pathtodel = os.path.join(os.path.abspath(root_path), f'{Header}.txt')
    os.remove(pathtodel)
    print('Success')