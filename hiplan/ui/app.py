from kivymd.app import MDApp as App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.metrics import dp
# from kivymd.config import Config
from kivy.core.window import Window

from hiplan.base.board import Background
from hiplan.base.app import App as BackendApp

# Config.set('graphics', 'width', '90')
# Config.set('graphics', 'height', '600')
Window.size = (350, 600)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        boards = App.get_running_app().app.boards
        for board in boards:
            self.ids.boards_layout.add_widget(
                BoardIcon(
                    text=board.name,
                    background=board.background
                )
            )
        
        self.ids.boards_layout.add_widget(
            BoardIcon(
                text = '+ New Board',
                background = Background(color=(0.321, 0.254, 0.424))
            )
        )



class BoardIcon(Button):
    def __init__(self, **kwargs):
        background = kwargs.pop('background')
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(160), dp(90)) 
        if background.type == Background.BackgroundType.COLOR:
            self.background_color = (*background.color, 1)
            self.background_normal = 'white.png'
        else:
            self.background_normal = background.image

class BoardScreen(Screen):
    pass

class RecordList(StackLayout):
    pass

class HiPlanApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()
        self.app = BackendApp.read_from_file()

    def build(self):
        self.screen_manager.add_widget(screen=BoardScreen(name='board-screen'))
        self.screen_manager.current = 'board-screen'
        return self.screen_manager

    
    
HiPlanApp().run()
