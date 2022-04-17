from kivy.config import ConfigParser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
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
        self.app = App.get_running_app()
        if self.app.config.get('default', 'theme_application') == 'light_theme':
            self.ids.anchor_layout.add_widget(BottomButton(text='Создать запись', size_hint=(.5, 1), on_press=self.new_post, background_color=style.button_color_light()))
            self.ids.box_layout.add_widget(DefaultImage(source='src/logo.png'))
            self.ids.box_layout.add_widget(SortButton(on_press=self.pressed_sort, background_color=style.button_color_light()))
            self.ids.box_layout.add_widget(NotepadButton(on_press=self.pressed_notepad, background_color=style.button_color_light()))
            self.ids.box_layout.add_widget(SettingButton(on_press=self.pressed_settings, background_color=style.button_color_light()))
        else:
            self.ids.anchor_layout.add_widget(BottomButton(text='Создать запись', size_hint=(.5, 1), on_press=self.new_post, background_color=style.button_color_dark()))
            self.ids.box_layout.add_widget(DefaultImage(source='src/logo.png'))
            self.ids.box_layout.add_widget(SortButton(on_press=self.pressed_sort, background_color=style.button_color_dark()))
            self.ids.box_layout.add_widget(NotepadButton(on_press=self.pressed_notepad, background_color=style.button_color_dark()))
            self.ids.box_layout.add_widget(SettingButton(on_press=self.pressed_settings, background_color=style.button_color_dark()))

        count_notes = crud_operations.count_notes()
        head_notes, strings_notes, first_strings = crud_operations.read_notes()
        for i in range(0, count_notes):
            button = AnotherButton()
            button.id = i
            button.head = head_notes[i]
            button.body = first_strings[i]
            #TODO: Добавить расцветку
            if self.app.config.get('default', 'theme_application') == 'light_theme':
                button.rgba_color = (37/255, 178/255, 0/255, 1)
            else:
                button.rgba_color = (15/255, 73/ 255, 0/255, 1)
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
    # TODO: Нет реализации ctrl+c и ctrl+v
    head = ObjectProperty()
    body = ObjectProperty()

    def on_pre_enter(self, *args):
        self.open_files()
        self.app = App.get_running_app()
        if self.app.config.get('default', 'theme_application') == 'light_theme':
            self.ids.box_layout.add_widget(SaveButton(on_press=self.save_edit, background_color = style.button_color_light()))
            self.ids.box_layout.add_widget(DeleteButton(on_press=self.delete_edit, background_color = style.button_color_light()))
            self.ids.box_layout.add_widget(BackButton(on_press=self.pressed_back, background_color = style.button_color_light()))
            self.head.background_color = style.input_color_light()
            self.body.background_color = style.input_color_light()
        else:
            self.ids.box_layout.add_widget(SaveButton(on_press=self.save_edit, background_color = style.button_color_dark()))
            self.ids.box_layout.add_widget(DeleteButton(on_press=self.delete_edit, background_color = style.button_color_dark()))
            self.ids.box_layout.add_widget(BackButton(on_press=self.pressed_back, background_color = style.button_color_dark()))
            self.head.background_color = style.input_color_dark()
            self.body.background_color = style.input_color_dark()

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
        self.app = App.get_running_app()
        if self.app.config.get('default', 'theme_application') == 'light_theme':
            self.add_widget(BottomButton(text='Вернуться', on_press=self.press_main, background_color=style.button_color_light()))
        else:
            self.add_widget(BottomButton(text='Вернуться', on_press=self.press_main, background_color=style.button_color_dark()))

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
            self.app = App.get_running_app()
            self.app.config.set('default', 'theme_application', 'dark_theme')
            Window.clearcolor = style.main_theme_dark()
            self.back_button.background_color = style.button_color_dark()
            #return 'Dark_theme'
        else:
            self.app = App.get_running_app()
            self.app.config.set('default', 'theme_application', 'light_theme')
            Window.clearcolor = style.main_theme_light()
            self.back_button.background_color = style.button_color_light()
            #return 'Light_theme'

class NewTextWidget(Screen):
    head = ObjectProperty()
    body = ObjectProperty()
    def on_pre_enter(self, *args):
        self.app = App.get_running_app()
        # Тут тестируем другой блок
        if self.app.config.get('default', 'theme_application') == 'light_theme':
            self.head.background_color = style.input_color_light()
            self.body.background_color = style.input_color_light()
            self.ids.box_layout.add_widget(SaveButton(on_press=self.save_new, background_color=style.button_color_light()))
            self.ids.box_layout.add_widget(BackButton(on_press=self.back_button, background_color=style.button_color_light()))
            #SaveButton().background_color = style.button_color_light()
            print(self.ids.box_layout.children)
            #Back_button = self.ids.box_layout.__doc__
            #Back_button.background_color = style.button_color_light()
            #self.ids.box_layout.SaveButton.background_color = style.button_color_light()
            #BackButton().background_color = style.button_color_light()
        else:
            self.head.background_color = style.input_color_dark()
            self.body.background_color = style.input_color_dark()
            self.ids.box_layout.add_widget(SaveButton(on_press=self.save_new, background_color=style.button_color_dark()))
            self.ids.box_layout.add_widget(BackButton(on_press=self.back_button, background_color=style.button_color_dark()))
        #Тут все работало
        #if Window.clearcolor == [0.18, 0.18, 0.18, 1]:
            #self.head.background_color = style.input_color_dark()
            #self.body.background_color = style.input_color_dark()
            #print('light_color')
        #else:
            #self.head.background_color = style.input_color_light()
            #self.body.background_color = style.input_color_light()
            #print('dark_color')

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
        config.setdefault('default', 'theme_application', 'light_theme')

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