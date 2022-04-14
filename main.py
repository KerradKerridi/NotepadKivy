from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window
import crud_operations, style


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
            #TODO: Создать через kivy элемент, и докинуть ему аргумент on_press
            button = Button(size_hint_y=None, background_color=[0, .8235, .5255, 1])
            button.text = f'{head_notes[i - 1]}'
            self.ids.grid.add_widget(button)
            button.bind(on_press=self.pressed)  # when the button is clicked

    def pressed(self, button):
        print('successPressedButton')
        sm.get_screen('edit').ids.HeaderNote.text = button.text
        sm.current = 'edit'

    def on_leave(self):  # Будет вызвана в момент закрытия экрана
        self.ids.grid.clear_widgets()

class NewButton(Button):
    pass

class EditTextWidget(Screen):
    # TODO: LATER: Если заметка пустая(заголовок и текст), не давать ее сохранять, выводить модалку об ошибке
    # TODO: Если заходим в заметку, начинаем ее корректировать, ТО удалять старую заметку
    head = ObjectProperty()
    body = ObjectProperty()
    back_button = ObjectProperty()
    delete_button = ObjectProperty()
    save_button = ObjectProperty()

    def on_pre_enter(self, *args):
        if Window.clearcolor == [0.18, 0.18, 0.18, 1]:
            self.head.background_color = style.input_color_dark()
            self.body.background_color = style.input_color_dark()
            self.back_button.background_color = style.button_color_dark()
            self.delete_button.background_color = style.button_color_dark()
            self.save_button.background_color = style.button_color_dark()
            print('light_color')
        else:
            self.head.background_color = style.input_color_light()
            self.body.background_color = style.input_color_light()
            self.back_button.background_color = style.button_color_light()
            self.delete_button.background_color = style.button_color_light()
            self.save_button.background_color = style.button_color_light()
            print('dark_color')

    def __init__(self, **kw):
        super(EditTextWidget, self).__init__(**kw)

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
    back_button = ObjectProperty()

    def change_theme(self):
        #TODO: Switch при прокрутке колесика мыши пытается переключаться.
        #Дефолтная тема, светлая
        if self.switch.active == False:
            Window.clearcolor = style.main_theme_dark()
            self.back_button.background_color = style.button_color_dark()
            print(Window.clearcolor)
            print('dark_color')
        else:
            Window.clearcolor = style.main_theme_light()
            self.back_button.background_color = style.button_color_light()
            print(Window.clearcolor)
            print('light_color')

class NewTextWidget(Screen):
    back_button = ObjectProperty()
    save_button = ObjectProperty()
    head = ObjectProperty()
    body = ObjectProperty()

    def on_pre_enter(self, *args):
        if Window.clearcolor == [0.18, 0.18, 0.18, 1]:
            self.head.background_color = style.input_color_dark()
            self.body.background_color = style.input_color_dark()
            self.back_button.background_color = style.button_color_dark()
            self.save_button.background_color = style.button_color_dark()
            print('light_color')
        else:
            self.head.background_color = style.input_color_light()
            self.body.background_color = style.input_color_light()
            self.back_button.background_color = style.button_color_light()
            self.save_button.background_color = style.button_color_light()
            print('dark_color')

    def save_new(self, head, body):
        crud_operations.save_new_note(head, body)

    def on_leave(self):
        self.head.text = ''
        self.body.text = ''

class NotepadApp(App):
    def build(self):
        sm.add_widget(FirstWindow(name='first'))
        sm.add_widget(MainWidget(name='main'))
        sm.add_widget(EditTextWidget(name='edit'))
        sm.add_widget(EmptyPage(name='empty'))
        sm.add_widget(NewTextWidget(name='new'))
        sm.add_widget(SettingsWidget(name='settings'))
        #TODO: В конфиги нужно сохранить параметры цветов
        NotepadApp.main_theme(.9, .9, .9, 1)
        return sm

    def main_theme(r, g, b, a):
        Window.clearcolor = (r, g, b, a)

if __name__ == '__main__':
    NotepadApp().run()