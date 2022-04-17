from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

import style

kv = Builder.load_file("uix/buttons.kv")

class DefaultButton(Button):
    pos_hint = {'x': .1, 'y': 0}
    font_size = 20
    background_color = (125 / 255, 0 / 255, 194 / 255, 1)


class BottomButton(Button):
    font_size = 20
    background_color = (125 / 255, 0 / 255, 194 / 255, 1)
    size_hint = .5, .1
    pos_hint = {'x': .25, 'y': 0}

class AnotherButton(ButtonBehavior, BoxLayout):
    id = ObjectProperty()
    head = StringProperty('')
    body = StringProperty('')
    rgba_color = ListProperty([.1, .1, .1, 1])
    #events_callback = ObjectProperty(None)


class DefaultImage(Image):
    pos_hint = {'x': 0, 'y': 0}
    size_hint = (.3, 1)

class SortButton(DefaultButton):
    text = 'Сортировка'

class SettingButton(DefaultButton):
    text = 'Настройки'

class NotepadButton(DefaultButton):
    text = 'Записные книжки'

class BackButton(DefaultButton):
    text = 'Назад'

class DeleteButton(DefaultButton):
    text = 'Удалить'

class SaveButton(DefaultButton):
    text = 'Сохранить'