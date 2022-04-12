from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
import crud_operations

kv = Builder.load_file("windows.kv")
sm = ScreenManager()

class MainWidget(Screen):
    def __init__(self, **kw):
        super(MainWidget, self).__init__(**kw)

    def on_pre_enter(self):
        # TODO: LATER: Добавить вывод текста в кнопке, не только заголовка
        count_notes = crud_operations.count_notes()
        head_notes, strings_notes = crud_operations.read_notes()
        print(count_notes)
        for i in range(0, count_notes):
            button = Button()
            button.text = f'{head_notes[i - 1]}'
            self.ids.grid.add_widget(button)
            button.bind(on_press=self.pressed)  # when the button is clicked

    def pressed(self, button):
        print('successPressedButton')
        sm.get_screen('edit').ids.HeaderNote.text = button.text
        sm.current = 'edit'

    def on_leave(self):  # Будет вызвана в момент закрытия экрана
        self.ids.grid.clear_widgets()


class EditTextWidget(Screen):
    # TODO: LATER: Если заметка пустая(заголовок и текст), не давать ее сохранять, выводить модалку об ошибке
    # TODO: Если заходим в заметку, начинаем ее корректировать, ТО удалять старую заметку
    def __init__(self, **kw):
        super(EditTextWidget, self).__init__(**kw)

    head = ObjectProperty()
    body = ObjectProperty()

    def open_files(self):
        ROOT_PATH = '/opt/python/PycharmProjects/NotepadForLinux/notebooks/'
        header = self.ids.HeaderNote.text
        f = open(f'{ROOT_PATH}{header}', 'r')
        s = f.read()
        self.head.text = header
        self.body.text = s
        f.close()

    def save_edit(self, head, body):
        crud_operations.save_edit_note(head, body)

    def delete_edit(self, head):
        crud_operations.delete_edit_note(head)

    def on_leave(self):
        self.head.text = ''
        self.body.text = ''


class EmptyPage(Screen):
    pass

class FirstWindow(Screen):
    pass

class SettingsWidget(Screen):
    pass

class NewTextWidget(Screen):
    def save_new(self, head, body):
        crud_operations.save_new_note(head, body)

    def on_leave(self):
        self.head.text = ''
        self.body.text = ''

class MainApp(App):
    def build(self):
        sm.add_widget(FirstWindow(name='first'))
        sm.add_widget(MainWidget(name='main'))
        sm.add_widget(EditTextWidget(name='edit'))
        sm.add_widget(EmptyPage(name='empty'))
        sm.add_widget(NewTextWidget(name='new'))
        sm.add_widget(SettingsWidget(name='settings'))
        return sm

if __name__ == '__main__':
    MainApp().run()