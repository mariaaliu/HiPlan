from kivymd.app import MDApp as App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout


class BoardScreen(Screen):
    pass

class BoardIcon(StackLayout):
    pass


class HiPlanApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()

    def build(self):
        self.screen_manager.add_widget(screen=BoardScreen(name='board-screen'))
        self.screen_manager.current = 'board-screen'
        return self.screen_manager

    
    
HiPlanApp().run()
