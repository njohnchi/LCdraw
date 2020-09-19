from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

from taskpanel import TaskPanel


class Title(Label):

    def __init__(self, **kwargs):
        super(Title, self).__init__(**kwargs)
        self.text = '[color=ff3333]L[/color][color=3333ff]C[/color] Draw'
        self.markup = True
        self.bold = True
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class LogicInput(FloatLayout):
    def __init__(self, **kwargs):
        super(LogicInput, self).__init__(**kwargs)
        self.label = Label(text='Y = ', pos_hint={'x': .06, 'y': .2}, size_hint=(.05, .6), color=(1,1,1,1))
        self.textinput = TextInput(text="Enter Expression", pos_hint={'x': .1, 'y': .2}, size_hint=(.6, .6))
        self.process = Button(text="Process", pos_hint={'x': .7, 'y': .2}, size_hint=(.2, .6))
        self.add_widget(self.label)
        self.add_widget(self.textinput)
        self.add_widget(self.process)
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class BoardCanvas(BoxLayout):
    def __init__(self, **kwargs):
        super(BoardCanvas, self).__init__(**kwargs)
        self.size_hint = (.94, .95)
        self.pos_hint = {'x': .03, 'y': .05}
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class Board(FloatLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.board_canvas = BoardCanvas()
        self.add_widget(self.board_canvas)
        with self.canvas.before:
            Color(.2, .2, .2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class LCDrawWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(LCDrawWidget, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.title = Title(size_hint_y = None, height = 30)
        self.taskpanel = TaskPanel(size_hint_y = None, height = 30)
        self.logic_input = LogicInput(size_hint_y=None, height=50)
        self.board = Board()
        self.add_widget(self.title)
        self.add_widget(self.taskpanel)
        self.add_widget(self.logic_input)
        self.add_widget(self.board)


class LCDrawApp(App):

    def build(self):
        root = LCDrawWidget()
        return root


if __name__ == "__main__":
    LCDrawApp().run()
