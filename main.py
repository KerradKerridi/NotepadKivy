from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
import crud_operations

kv = Builder.load_file("windows.kv")
sm = ScreenManager()

class MainWidget(Screen):
    pass

class EditTextWidget(Screen):
    #TODO: Если заметка пустая(заголовок и текст), не давать ее сохранять, выводить модалку об ошибке
    def save(self, head, body):
        crud_operations.save_note(self, head, body)

    def delete(self, head):
        crud_operations.delete_note(self,head)

class EmptyPage(Screen):
    pass

class FirstWindow(Screen):
    pass

class MainApp(App):

    def build(self):
        sm.add_widget(FirstWindow(name='first'))
        sm.add_widget(MainWidget(name='main'))
        sm.add_widget(EditTextWidget(name='edit'))
        sm.add_widget(EmptyPage(name='empty'))
        return sm

if __name__ == '__main__':
    MainApp().run()