from kivymd.app import MDApp as App
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
# from kivymd.config import Config
from kivy.core.window import Window
from datetime import date, timedelta
from functools import partial
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivy.graphics import Line, Color


from hiplan.base.board import Background, Board
from hiplan.base.app import App as BackendApp

# Config.set('graphics', 'width', '90')
# Config.set('graphics', 'height', '600')
Window.size = (350, 600)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = App.get_running_app().screen_manager
        boards = App.get_running_app().app.boards
        for board in boards:
            button = BoardIcon(
                    text=board.name,
                    background=board.background,
                    board=board
                )
            self.ids.boards_layout.add_widget(button)
            button.bind(on_press = self.callback)

        new_board_btn = BoardIcon(
                            text = '+ New Board',
                            background = Background(color=(0.321, 0.254, 0.424))
                        )
        self.ids.boards_layout.add_widget(new_board_btn)
        new_board_btn.bind(on_press = lambda *args: BackendApp.get_instance().add_board())
    
    def callback(self, instance):
        self.screen_manager.add_widget(screen=BoardScreen(board=instance.board, name=instance.board.name))
        self.screen_manager.current = instance.board.name

def add_gradient(widget, palette):
    alpha_channel_rate = 0
    increase_rate = 1 / widget.width

    palette_values = []
    for i in range(widget.width):
        palette_values.append([max(value+i/30.0, 1) for value in palette])

    for sep, pos in zip(palette_values, range(widget.width)):
        widget.canvas.add(Color(rgba=(*sep, 1)))
        widget.canvas.add(Line(points=[pos, 0, pos, widget.height], width=1))

class BaseShadowWidget(Widget):
    pass

class BoardIcon(Button):
    def __init__(self, **kwargs):
        background = kwargs.pop('background')
        self.board = kwargs.pop('board', None)
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        # self.size = (dp(160), dp(90)) 
        # self.height = dp(90)
        self.size_hint_x = 0.5
        self.size_hint_y = 0.2
        if background.type == Background.BackgroundType.COLOR:
            self.background_color = (*background.color, 1)
            self.background_normal = 'white.png'
        else:
            self.background_normal = background.image

class BoardScreen(Screen):
    def __init__(self, **kwargs):
        self.board = kwargs.pop('board')
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()
        records = self.board.records
        for record in records:
            record_list = RecordList(
                            record=record,
                        )
            self.ids.record_layout.add_widget(record_list)
            # record_list.height = record_list.parent.height
        self.ids.board_label.text = self.board.name
            

class RecordLayout(RectangularElevationBehavior, BaseShadowWidget, MDGridLayout):
    pass

class RecordList(StackLayout):
    def __init__(self, **kwargs):
        self.record = kwargs.pop('record')
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size_hint_x = 1
        self.size_hint_y = 1
        self.ids.list_title.add_widget(
            Label(
                text=self.record.name,
            )
        )
        tasks = self.record.tasks
        for task in tasks:
            self.ids.task_layout.add_widget(
                TwoLineListItem(
                    text = task.title,
                    secondary_text = task.description,
                )
            )
        new_task_btn = MDIconButton(
                icon='plus',
                size_hint= (0.9, None)
            )
        self.ids.task_layout.add_widget(new_task_btn)
        new_task_btn.bind(on_press=self.record.add_tasks)


class TaskDeadline(TextInput):
    def __init__(self, **kwargs):
        # self.callback = kwargs.pop('callback')
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        calendar = MDDatePicker(callback=self.open_clock)
        calendar.open()
    
    def open_clock(self, picked_date):
        callback = partial(self.update_deadline, picked_date)
        clock = MDTimePicker()
        clock.bind(time=callback)
        clock.open()

    def update_deadline(self, picked_date, instance, picked_time):
        print(picked_date, picked_time)
        # self.callback(date_time.combine(picked_date, picked_time))

class TaskScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # layout.add_widget(TaskDeadline(multiline=False, callback=self.update_deadline))

    def update_deadline(self, picked_deadline):
        self.task.deadline = picked_deadline

class HiPlanApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()
        self.app = BackendApp.read_from_file()

    def build(self):
        self.screen_manager.add_widget(screen=HomeScreen(name='board-screen'))
        self.screen_manager.current = 'board-screen'
        
        return self.screen_manager

    
    
HiPlanApp().run()