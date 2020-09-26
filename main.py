from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.logger import Logger

from taskpanel import TaskPanel
from circuit import Circuit
from truthtable import TruthTable
import boolean as boolean


class Title(Label):
    def __init__(self, **kwargs):
        super(Title, self).__init__(**kwargs)
        self.text = 'LC Draw'
        self.bold = True
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class BtnProceed(Button):
    def __init__(self, **kwargs):
        super(BtnProceed, self).__init__(**kwargs)
        self.text = "Proceed"
        self.pos_hint = {'x': .7, 'y': .15}
        self.size_hint = (.2, .5)


class LogicInput(FloatLayout):
    def __init__(self, **kwargs):
        super(LogicInput, self).__init__(**kwargs)
        self.error = Label(pos_hint={'x': .5, 'y': .6}, size_hint=(.05, .4), color=(1, 0, 0, 1))
        self.label = Label(text='Y = ', pos_hint={'x': .06, 'y': .15}, size_hint=(.05, .5), color=(1, 1, 1, 1))
        self.textinput = TextInput(pos_hint={'x': .1, 'y': .15}, size_hint=(.6, .5), multiline=False)
        self.proceed = BtnProceed()
        self.add_widget(self.error)
        self.add_widget(self.label)
        self.add_widget(self.textinput)
        self.add_widget(self.proceed)
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class Simp(BoxLayout):
    def __init__(self, text, **kwargs):
        super(Simp, self).__init__(**kwargs)
        self.text = text
        self.label = Label(text=self.text, text_size=self.size, pos=self.pos, color=(0, 0, 0, 1), halign='center', valign='middle')
        self.label.font_size = 40
        self.add_widget(self.label)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.label.pos = instance.pos
        self.label.text_size = instance.size


class BoardCanvas(ScrollView):
    def __init__(self, **kwargs):
        super(BoardCanvas, self).__init__(**kwargs)
        self.size_hint = (.9, .95)
        self.pos_hint = {'x': .03, 'y': .05}
        self.effect_cls = "ScrollEffect"
        self.bar_width = 10
        self.scroll_type = ["bars", "content"]
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.do_scroll_x: True
        self.do_scroll_y: True

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class BoardSlider(Slider):
    def __init__(self, **kwargs):
        super(BoardSlider, self).__init__(**kwargs)
        self.size_hint = (.05, .95)
        self.pos_hint = {'x': .93, 'y': .05}
        self.min = 0.5
        self.max = 2
        self.value = 1
        self.orientation = 'vertical'


class Board(FloatLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.board_canvas = BoardCanvas()
        self.slider = BoardSlider()
        self.add_widget(self.board_canvas)
        self.add_widget(self.slider)
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
        self.logic_input = LogicInput(size_hint_y=None, height=60)
        self.board = Board()
        self.add_widget(self.title)
        self.add_widget(self.taskpanel)
        self.add_widget(self.logic_input)
        self.add_widget(self.board)
        self.logic_input.proceed.bind(on_press=self._perform_task)
        self.board.slider.bind(value=self._zoom_canvas)

    # zoom board canvas using slider
    def _zoom_canvas(self, instance, value):
        if not self.board.board_canvas.children:
            return
        else:
            self.board.board_canvas.children[0].width = self.board.board_canvas.width * value
            self.board.board_canvas.children[0].height = self.board.board_canvas.height * value

    # sets task to perform on input expression
    def _perform_task(self, instance):
            task = self.taskpanel.panel.task
            expr = self.logic_input.textinput.text
            self.logic_input.error.text = ""
            if expr == "":
                self.logic_input.error.text = "Input is Empty"
                raise ValueError("Input is Empty")
            try:
                if task == "Simplify":
                    self.simplify(expr)
                elif task == "Circuit":
                    self.draw_circuit(expr)
                elif task == "Truthtable":
                    self.draw_truthtable(expr)
                else:
                    raise TypeError("Unknowwn Task or not a task {}".format(task))
            except:
                self.logic_input.error.text = "Invalid input expression"
                raise ValueError("Invalid input expression")

    # simplify a boolean expression
    def simplify(self, expr):
        sim_exp = boolean.parse(expr)
        exp = Simp(text=str(sim_exp), pos=self.pos, size=self.size)
        self.board.board_canvas.clear_widgets()
        self.board.board_canvas.add_widget(exp)

    # draw logic circuit for boolean expression
    def draw_circuit(self, expr):
        expr = "Y = " + expr
        circuit = Circuit(expr, size=self.board.board_canvas.size)
        self.board.board_canvas.clear_widgets()
        self.board.board_canvas.add_widget(circuit)

    # draw truth table for boolean expression
    def draw_truthtable(self, expr):
        truthtable = TruthTable(expr, "Y", size=self.board.board_canvas.size)
        self.board.board_canvas.clear_widgets()
        self.board.board_canvas.add_widget(truthtable)


# Error handler for app
class E(ExceptionHandler):
    def handle_exception(self, inst):
        Logger.exception('Exception catched by ExceptionHandler')
        return ExceptionManager.PASS


ExceptionManager.add_handler(E())


class LCDrawApp(App):
    def build(self):
        root = LCDrawWidget()
        return root


if __name__ == "__main__":
    LCDrawApp().run()
