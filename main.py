import ast
import os

from kivy.config import Config, ConfigParser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.core.window import Window
import crud_operations, style
from uix.buttons import *

kv = Builder.load_file("windows.kv")
sm = ScreenManager()

class MainWidget(Screen):
    box_layout = ObjectProperty()
    anchor_layout = ObjectProperty()

    def __init__(self, **kw):
        super(MainWidget, self).__init__(**kw)

    def on_pre_enter(self):
        self.ids.anchor_layout.add_widget(BottomButton(text='Создать запись', size_hint=(.5, 1), on_press=self.new_post))
        self.ids.box_layout.add_widget(DefaultImage(source='src/logo.png'))
        self.ids.box_layout.add_widget(SortButton(on_press=self.pressed_sort))
        self.ids.box_layout.add_widget(NotepadButton(on_press=self.pressed_notepad))
        self.ids.box_layout.add_widget(SettingButton(on_press=self.pressed_settings))
        count_notes = crud_operations.count_notes()
        head_notes, strings_notes, first_strings = crud_operations.read_notes()
        print(count_notes)
        for i in range(0, count_notes):
            button = AnotherButton()
            button.id = i
            button.head = head_notes[i]
            button.body = first_strings[i]
            button.rgba_color = (37/255, 178/255, 0/255, 1)
            self.ids.grid.add_widget(button)
            button.bind(on_press=self.pressed)

    def new_post(self, button):
        sm.current = 'new'

    def pressed(self, button):
        print('successPressedButton')
        sm.get_screen('edit').ids.HeaderNote.text = button.head
        sm.current = 'edit'

    def pressed_sort(self, button):
        sm.current = 'empty'

    def pressed_notepad(self, button):
        sm.current = 'empty'

    def pressed_settings(self, button):
        sm.current = 'settings'

    def on_leave(self):  # Будет вызвана в момент закрытия экрана
        self.ids.grid.clear_widgets()
        self.ids.box_layout.clear_widgets()


class EditTextWidget(Screen):
    # TODO: LATER: Если заметка пустая(заголовок и текст), не давать ее сохранять, выводить модалку об ошибке
    # TODO: Если заходим в заметку, начинаем ее корректировать, ТО удалять старую заметку
    # TODO: Нет реализации ctrl+c и ctrl+v
    head = ObjectProperty()
    body = ObjectProperty()

    def on_pre_enter(self, *args):
        self.open_files()
        #TODO: LAST IMPORTANT Подумать над тем как выдать им идентификаторы чтобы можно было их перекрашить и к ним обращаться.
        self.ids.box_layout.add_widget(SaveButton(on_press=self.save_edit))
        self.ids.box_layout.add_widget(DeleteButton(on_press=self.delete_edit))
        self.ids.box_layout.add_widget(BackButton(on_press=self.pressed_back))

        if Window.clearcolor == [0.18, 0.18, 0.18, 1]:
            self.head.background_color = style.input_color_dark()
            self.body.background_color = style.input_color_dark()
            print('light_color')
        else:
            self.head.background_color = style.input_color_light()
            self.body.background_color = style.input_color_light()
            print('dark_color')

    def __init__(self, **kw):
        super(EditTextWidget, self).__init__(**kw)

    def pressed_back(self, button):
        sm.current = 'main'


    def open_files(self):
        ROOT_PATH = '/opt/python/PycharmProjects/NotepadForLinux/notebooks/'
        header = self.ids.HeaderNote.text
        f = open(f'{ROOT_PATH}{header}', 'r')
        s = f.read()
        self.head.text = header
        self.body.text = s
        f.close()

    def save_edit(self, button):
        head = self.head
        body = self.body
        crud_operations.save_edit_note(head, body)
        sm.current = 'main'

    def delete_edit(self, button):
        header = self.head
        crud_operations.delete_edit_note(header)
        sm.current = 'main'


    def on_leave(self):
        self.head.text = ''
        self.body.text = ''
        self.ids.box_layout.clear_widgets()


class EmptyPage(Screen):

    def on_pre_enter(self, *args):
        self.add_widget(BottomButton(text='Вернуться', on_press=self.press_main))

    def press_main(self, button):
        sm.current = 'main'


class FirstWindow(Screen):
    box = ObjectProperty

    def on_pre_enter(self, *args):
        pass

class SettingsWidget(Screen):
    back_button = ObjectProperty()
    switch = ObjectProperty()

    def change_theme(self):
        #TODO: Switch при прокрутке колесика мыши пытается переключаться.
        #TODO: Если switch.active == False, то в Config писать dark_theme. Далее опираясь на это выставлять тему приложения
        if self.switch.active == False:
            Window.clearcolor = style.main_theme_dark()
            self.back_button.background_color = style.button_color_dark()
            return 'Dark_theme'
        else:
            Window.clearcolor = style.main_theme_light()
            self.back_button.background_color = style.button_color_light()
            return 'Light_theme'

class NewTextWidget(Screen):
    head = ObjectProperty()
    body = ObjectProperty()
    def on_pre_enter(self, *args):
        self.ids.box_layout.add_widget(SaveButton(on_press=self.save_new))
        self.ids.box_layout.add_widget(BackButton(on_press=self.back_button))
        if Window.clearcolor == [0.18, 0.18, 0.18, 1]:
            self.head.background_color = style.input_color_dark()
            self.body.background_color = style.input_color_dark()
            print('light_color')
        else:
            self.head.background_color = style.input_color_light()
            self.body.background_color = style.input_color_light()
            print('dark_color')

    def save_new(self, button):
        head = self.head
        body = self.body
        crud_operations.save_new_note(head, body)
        sm.current = 'main'
        print('Success')

    def back_button(self, button):
        sm.current = 'main'

    def on_leave(self):
        self.head.text = ''
        self.body.text = ''
        self.ids.box_layout.clear_widgets()


class NotepadApp(App):
    def __init__(self, **kvargs):
        super(NotepadApp, self).__init__(**kvargs)
        self.config = ConfigParser()

    def build_config(self, config):
        config.adddefaultsection('default')
        config.setdefault('default', 'theme_application', 'white')

    #def get_application_config(self):
        #return super(NotepadApp, self).get_application_config(
        #'{}/%(appname)s.ini'.format(self.directory))

    #def set_value_from_config(self):
        #self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        #self.user_data = ast.literal_eval(self.config.get(
        #'main_theme', 'white_theme'))

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