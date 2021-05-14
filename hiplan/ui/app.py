from hiplan.base.task import Task
from kivymd.app import MDApp as App
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextFieldRound
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
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
        self.screen_manager = App.get_running_app().screen_manager
        records = self.board.records
        for record in records:
            record_list = RecordList(
                            record=record,
                        )
            self.ids.record_layout.add_widget(record_list)
            # record_list.height = record_list.parent.height
        self.ids.board_label.text = self.board.name

        self.ids.back.icon = "close"
        self.ids.back.size_hint_x = None
        self.ids.back.bind(on_press = self.back_callback)

        self.ids.home.icon = 'home'
        self.ids.home.size_hint_x = None
        self.ids.home.col = 1
        self.ids.home.theme_text_color = 'Custom'
        self.ids.home.icon_color = 1, 0, 0, 1
        self.ids.home.bind(on_press = self.home_callback)

    def home_callback(self, instance):
        self.screen_manager.current = 'board-screen'

    def back_callback(self, instance):
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = self.screen_manager.previous()
            

class RecordLayout(RectangularElevationBehavior, BaseShadowWidget, MDGridLayout):
    pass

class RecordList(StackLayout):
    def __init__(self, **kwargs):
        self.record = kwargs.pop('record')
        super().__init__(**kwargs)
        self.screen_manager = App.get_running_app().screen_manager
        self.size_hint = (None, None)
        self.size_hint_x = 1
        self.size_hint_y = 1
        self.ids.list_title.add_widget(
            Label(
                text=self.record.name + '  -  priority: ' + str(self.record.priority.name),
            )
        )
        tasks = self.record.tasks
        for task in tasks:
            task_btn = TaskLayout(
                    text = task.title,
                    secondary_text = task.description,
                    task = task
                )
            self.ids.task_layout.add_widget(task_btn)
            task_btn.bind(on_press = self.callback)
        new_task_btn = MDIconButton(
                icon='plus',
                size_hint= (0.9, None)
            )
        self.ids.task_layout.add_widget(new_task_btn)
        new_task_btn.bind(on_press=self.record.add_tasks)
        # new_board_btn.bind(on_press = lambda *args: BackendApp.get_instance().add_board())

    def callback(self, instance):
        self.screen_manager.add_widget(screen=TaskScreen(task=instance.task, name=instance.task.title))
        self.screen_manager.current = instance.task.title

class TaskLayout(TwoLineListItem):
    def __init__(self, **kwargs):
        self.task = kwargs.pop('task')
        super().__init__(**kwargs)

class TaskDeadline(MDTextFieldRound):
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
        self.text ="Deadline: on " + str(picked_date)+ " at " + str (picked_time)
        # print(picked_date, picked_time)
        # self.callback(date_time.combine(picked_date, picked_time))

class TaskScreen(Screen):
    def __init__(self, **kwargs):
        self.task = kwargs.pop('task')
        super().__init__(**kwargs)
        self.screen_manager = App.get_running_app().screen_manager
        self.ids.task_label.text = self.task.title

        self.ids.task_deadline.multiline = False
        self.ids.task_deadline.hint_text = 'Deadline'
        self.ids.task_deadline.text = str("Deadline: on " + self.task.deadline.strftime("%d/%m/%Y") +" at "+ self.task.deadline.strftime("%H:%M:%S"))
        self.ids.task_deadline.callback = self.update_deadline
        self.ids.task_deadline.size_hint_y = None

        self.ids.task_progress_status.multiline = True
        self.ids.task_progress_status.hint_text = 'Progress: SOLVED / UNSOLVED ?'
        self.ids.task_progress_status.text = self.task.progress_status.name
        self.ids.task_progress_status.size_hint_y = None

        self.ids.task_title.multiline = False
        self.ids.task_title.hint_text = 'Task title'
        self.ids.task_title.text = self.task.title
        self.ids.task_title.size_hint_y = None

        self.ids.task_description.multiline = True
        self.ids.task_description.hint_text = 'Task description'
        self.ids.task_description.text = self.task.description
        self.ids.task_description.size_hint_y = None

        self.ids.task_members.multiline = True
        self.ids.task_members.hint_text = 'task_member@email.example'
        self.ids.task_members.size_hint_y = None

        self.ids.open_goals.icon = "login"
        self.ids.open_goals.text = "Open goal list to see your goals"
        self.ids.open_goals.width = dp(280)
        self.ids.open_goals.theme_text_color = "Custom"
        self.ids.open_goals.text_color = (1, 1, 1, 1)
        self.ids.open_goals.md_bg_color = (0.3, 0.56, 1, 1)
        self.ids.open_goals.bind(on_press = self.goal_callback)

        self.ids.open_attachments.icon = "attachment"
        self.ids.open_attachments.text = "Open your list of attachments"
        self.ids.open_attachments.width = dp(280)
        self.ids.open_attachments.theme_text_color = "Custom"
        self.ids.open_attachments.text_color = (1, 1, 1, 1)
        self.ids.open_attachments.md_bg_color = (0.3, 0.56, 1, 1)
        self.ids.open_attachments.bind(on_press = self.attachment_callback)

        self.ids.back.icon = "close"
        self.ids.back.size_hint_x = None
        self.ids.back.bind(on_press = self.back_callback)

        self.ids.home.icon = 'home'
        self.ids.home.size_hint_x = None
        self.ids.home.col = 1
        self.ids.home.theme_text_color = 'Custom'
        self.ids.home.icon_color = 1, 0, 0, 1
        self.ids.home.bind(on_press = self.home_callback)

    def home_callback(self, instance):
        self.screen_manager.current = 'board-screen'

    def back_callback(self, instance):
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = self.screen_manager.previous()

    def update_deadline(self, picked_deadline):
        self.task.deadline = picked_deadline

    def goal_callback(self, instance):
        self.screen_manager.add_widget(screen=GoalScreen(name="Goals"))
        self.screen_manager.current = "Goals"

    def attachment_callback(self, instance):
        self.screen_manager.add_widget(screen=AttachmentScreen(name="Attachments"))
        self.screen_manager.current = "Attachments"

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class GoalLayout(OneLineAvatarIconListItem):
    pass

class GoalScreen(Screen):
    def __init__(self, **kwargs):
        # self.task = kwargs.pop('goal')
        super().__init__(**kwargs)
        self.screen_manager = App.get_running_app().screen_manager
        self.ids.goal_label.text = "Goals: "
        
        self.ids.back.icon = "close"
        self.ids.back.size_hint_x = None
        self.ids.back.bind(on_press = self.back_callback)

        self.ids.home.icon = 'home'
        self.ids.home.size_hint_x = None
        self.ids.home.col = 1
        self.ids.home.theme_text_color = 'Custom'
        self.ids.home.icon_color = 1, 0, 0, 1
        self.ids.home.bind(on_press = self.home_callback)

    def home_callback(self, instance):
        self.screen_manager.current = 'board-screen'

    def back_callback(self, instance):
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = self.screen_manager.previous() 

class AttachmentLayout(OneLineAvatarIconListItem):
    pass

class AttachmentScreen(Screen):
    def __init__(self, **kwargs):
        # self.task = kwargs.pop('goal')
        super().__init__(**kwargs)
        self.screen_manager = App.get_running_app().screen_manager
        self.ids.attachment_label.text = "Attachments: "

        self.ids.back.icon = "close"
        self.ids.back.size_hint_x = None
        self.ids.back.bind(on_press = self.back_callback)

        self.ids.home.icon = 'home'
        self.ids.home.size_hint_x = None
        self.ids.home.col = 1
        self.ids.home.theme_text_color = 'Custom'
        self.ids.home.icon_color = 1, 0, 0, 1
        self.ids.home.bind(on_press = self.home_callback)

    def home_callback(self, instance):
        self.screen_manager.current = 'board-screen'

    def back_callback(self, instance):
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = self.screen_manager.previous()

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
