from os import path

from kivy.app import App
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

import crud_operations
import style
from uix.edit_panel import *
from uix.buttons import *

kv = Builder.load_file("windows.kv")
sm = ScreenManager()


class MainWidget(Screen):
    box_layout = ObjectProperty()
    anchor_layout = ObjectProperty()
    grid = ObjectProperty()

    def __init__(self, **kw):
        super(MainWidget, self).__init__(**kw)

    def on_pre_enter(self):
        self.app = App.get_running_app()
        if self.app.config.get('default', 'theme_application') == 'light_theme':
            self.ids.anchor_layout.add_widget(
                BottomButton(text='Создать запись', size_hint=(.5, 1), on_press=self.new_post,
                             background_color=style.button_color_light()))
            self.ids.box_layout.add_widget(DefaultImage(source='src/logo.png'))
            self.ids.box_layout.add_widget(
                SortButton(on_press=self.pressed_sort, background_color=style.button_color_light()))
            self.ids.box_layout.add_widget(
                NotepadButton(on_press=self.pressed_notepad, background_color=style.button_color_light()))
            self.ids.box_layout.add_widget(
                SettingButton(on_press=self.pressed_settings, background_color=style.button_color_light()))
        else:
            self.ids.anchor_layout.add_widget(
                BottomButton(text='Создать запись', size_hint=(.5, 1), on_press=self.new_post,
                             background_color=style.button_color_dark()))
            self.ids.box_layout.add_widget(DefaultImage(source='src/logo.png'))
            self.ids.box_layout.add_widget(
                SortButton(on_press=self.pressed_sort, background_color=style.button_color_dark()))
            self.ids.box_layout.add_widget(
                NotepadButton(on_press=self.pressed_notepad, background_color=style.button_color_dark()))
            self.ids.box_layout.add_widget(
                SettingButton(on_press=self.pressed_settings, background_color=style.button_color_dark()))

        count_notes = crud_operations.count_notes()
        head_notes, strings_notes, first_strings = crud_operations.read_notes()
        # WARNING: Костыль. Считаем количество заметок и делим на 4.5(сколько входит по дефолту в экран)
        self.ids.grid.size_hint_y = count_notes / 4.5
        print(count_notes / 4.5)
        try:
            for i in range(0, count_notes):
                button = AnotherButton()
                button.id = i
                button.head = head_notes[i]
                button.body = first_strings[i]
                if self.app.config.get('default', 'theme_application') == 'light_theme':
                    button.rgba_color = (247 / 255, 239 / 255, 212 / 255, 1)
                    button.font_color = (.1, .1, .1, 1)
                else:
                    button.rgba_color = (89 / 255, 68 / 255, 14 / 255, 1)
                    button.font_color = (.7, .7, .7, 1)
                self.ids.grid.add_widget(button)
                button.bind(on_press=self.pressed)
        except IndexError:
            pass

    @staticmethod
    def new_post(button):
        sm.current = 'new'

    @staticmethod
    def pressed(button):
        print('successPressedButton')
        sm.get_screen('edit').ids.HeaderNote.text = button.head
        sm.current = 'edit'

    @staticmethod
    def pressed_sort(button):
        sm.current = 'empty'

    @staticmethod
    def pressed_notepad(button):
        sm.current = 'empty'

    @staticmethod
    def pressed_settings(button):
        sm.current = 'settings'

    def on_leave(self):  # Будет вызвана в момент закрытия экрана
        self.ids.grid.clear_widgets()
        self.ids.box_layout.clear_widgets()


class EditTextWidget(Screen):
    # TODO: LATER: Если заметка пустая(заголовок и текст), не давать ее сохранять, выводить модалку об ошибке
    # TODO: Нет реализации ctrl+c и ctrl+v
    head = ObjectProperty()
    body = ObjectProperty()

    def on_pre_enter(self, *args):
        self.open_files()
        self.app = App.get_running_app()
        if self.app.config.get('default', 'theme_application') == 'light_theme':
            self.ids.box_layout.add_widget(
                SaveButton(on_press=self.save_edit, background_color=style.button_color_light()))
            self.ids.box_layout.add_widget(
                DeleteButton(on_press=self.delete_edit, background_color=style.button_color_light()))
            self.ids.box_layout.add_widget(
                BackButton(on_press=self.pressed_back, background_color=style.button_color_light()))
            self.head.background_color = style.input_color_light()
            self.body.background_color = style.input_color_light()
        else:
            self.ids.box_layout.add_widget(
                SaveButton(on_press=self.save_edit, background_color=style.button_color_dark()))
            self.ids.box_layout.add_widget(
                DeleteButton(on_press=self.delete_edit, background_color=style.button_color_dark()))
            self.ids.box_layout.add_widget(
                BackButton(on_press=self.pressed_back, background_color=style.button_color_dark()))
            self.head.background_color = style.input_color_dark()
            self.body.background_color = style.input_color_dark()

    def __init__(self, **kw):
        super(EditTextWidget, self).__init__(**kw)

    @staticmethod
    def pressed_back(button):
        sm.current = 'main'

    def open_files(self):
        parent_dir = path.dirname(path.abspath(__file__))
        file_path = f'{parent_dir}/notebooks/'
        header = self.ids.HeaderNote.text
        f = open(f'{file_path}{header}', 'r')
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
        self.app = App.get_running_app()
        if self.app.config.get('default', 'theme_application') == 'light_theme':
            self.add_widget(
                BottomButton(text='Вернуться', on_press=self.press_main, background_color=style.button_color_light()))
        else:
            self.add_widget(
                BottomButton(text='Вернуться', on_press=self.press_main, background_color=style.button_color_dark()))

    @staticmethod
    def press_main(button):
        sm.current = 'main'


class FirstWindow(Screen):
    box = ObjectProperty


class SettingsWidget(Screen):
    back_button = ObjectProperty()
    switch = ObjectProperty()

    def change_theme(self):
        # TODO: Switch при прокрутке колесика мыши пытается переключаться.
        if self.switch.active is False:
            self.app = App.get_running_app()
            self.app.config.set('default', 'theme_application', 'dark_theme')
            Window.clearcolor = style.main_theme_dark()
            self.back_button.background_color = style.button_color_dark()
        else:
            self.app = App.get_running_app()
            self.app.config.set('default', 'theme_application', 'light_theme')
            Window.clearcolor = style.main_theme_light()
            self.back_button.background_color = style.button_color_light()


class NewTextWidget(Screen):
    head = ObjectProperty()
    body = ObjectProperty()

    def on_pre_enter(self, *args):
        self.app = App.get_running_app()
        if self.app.config.get('default', 'theme_application') == 'light_theme':
            self.head.background_color = style.input_color_light()
            self.body.background_color = style.input_color_light()
            self.ids.box_layout.add_widget(
                SaveButton(on_press=self.save_new, background_color=style.button_color_light()))
            self.ids.box_layout.add_widget(
                BackButton(on_press=self.back_button, background_color=style.button_color_light()))
        else:
            self.head.background_color = style.input_color_dark()
            self.body.background_color = style.input_color_dark()
            self.ids.box_layout.add_widget(
                SaveButton(on_press=self.save_new, background_color=style.button_color_dark()))
            self.ids.box_layout.add_widget(
                BackButton(on_press=self.back_button, background_color=style.button_color_dark()))

    def save_new(self, button):
        head = self.head
        body = self.body
        crud_operations.save_new_note(head, body)
        sm.current = 'main'
        print('Success')

    @staticmethod
    def back_button(button):
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
        config.setdefault('default', 'theme_application', 'light_theme')

    def build(self):
        sm.add_widget(FirstWindow(name='first'))
        sm.add_widget(MainWidget(name='main'))
        sm.add_widget(EditTextWidget(name='edit'))
        sm.add_widget(EmptyPage(name='empty'))
        sm.add_widget(NewTextWidget(name='new'))
        sm.add_widget(SettingsWidget(name='settings'))
        style.main_theme(.9, .9, .9, 1)
        return sm


if __name__ == '__main__':
    NotepadApp().run()
