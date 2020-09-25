from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.clock import Clock

from taskpanel import TaskPanel
from circuit import Circuit
from truthtable import TruthTable
import boolean as boolean


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


class BtnProceed(Button):

    def __init__(self, **kwargs):
        super(BtnProceed, self).__init__(**kwargs)
        self.text = "Proceed"
        self.pos_hint = {'x': .7, 'y': .2}
        self.size_hint = (.2, .6)


class LogicInput(FloatLayout):
    def __init__(self, **kwargs):
        super(LogicInput, self).__init__(**kwargs)
        self.label = Label(text='Y = ', pos_hint={'x': .06, 'y': .2}, size_hint=(.05, .6), color=(1,1,1,1))
        self.textinput = TextInput(pos_hint={'x': .1, 'y': .2}, size_hint=(.6, .6))
        self.proceed = BtnProceed()
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
        # self.size = (Window.width, Window.height)
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
        self.logic_input = LogicInput(size_hint_y=None, height=50)
        self.board = Board()
        self.add_widget(self.title)
        self.add_widget(self.taskpanel)
        self.add_widget(self.logic_input)
        self.add_widget(self.board)
        self.logic_input.proceed.bind(on_press=self._perform_task)
        self.board.slider.bind(value=self._zoom_canvas)

    def _zoom_canvas(self, instance, value):
        if not self.board.board_canvas.children:
            return
        else:
            self.board.board_canvas.children[0].width = self.board.board_canvas.width * value
            self.board.board_canvas.children[0].height = self.board.board_canvas.height * value

    def _perform_task(self, instance):
            task = self.taskpanel.panel.task
            expr = self.logic_input.textinput.text
            if task == "Simplify":
                self.simplify(expr)
            elif task == "Circuit":
                self.draw_circuit(expr)
            elif task == "Truthtable":
                self.draw_truthtable(expr)
            else:
                print("Unknown task: ", task)

    def simplify(self, expr):
        sim_exp = boolean.parse(expr)
        exp = Label(text=str(sim_exp), pos=self.pos, size=self.size, font_size=75, color=[0, 0, 0, 1])
        self.board.board_canvas.clear_widgets()
        self.board.board_canvas.add_widget(exp)

    def draw_circuit(self, expr):
        expr = "Y = " + expr
        circuit = Circuit(expr, size=self.board.board_canvas.size)
        self.board.board_canvas.clear_widgets()
        self.board.board_canvas.add_widget(circuit)
        # Clock.schedule_once(circuit.run_sim, 0.1)

    def draw_truthtable(self, expr):
        truthtable = TruthTable(expr, "Y", size=self.board.board_canvas.size)
        self.board.board_canvas.clear_widgets()
        self.board.board_canvas.add_widget(truthtable)


class LCDrawApp(App):

    def build(self):
        root = LCDrawWidget()
        return root


if __name__ == "__main__":
    LCDrawApp().run()
