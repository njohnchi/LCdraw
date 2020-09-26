from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.properties import BooleanProperty, StringProperty


class Task(Button):
    # true if task is selected
    is_active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
        self.text = "Task"
        self.font_size = 16
        self.background_down = ''
        self.background_normal = ''
        self.size_hint = (None, .9)
        self.width = 80
        self.pos_hint = {'x': 1, 'y': .05}
        self.background_color = (0.2, 0.2, 0.2, 1)

    def on_is_active(self, instance, value):
        if self.is_active:
            self.color = (0, 0, 1, 1)
        else:
            self.color = (1, 1, 1, 1)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self.is_active:
                self.is_active = True
                self.parent.task = self.text


class Icon(BoxLayout):
    def __init__(self, **kwargs):
        super(Icon, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 50
        self.image = Image(source="img/icon.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.image)


class Simplify(Task):
    def __init__(self, **kwargs):
        super(Simplify, self).__init__(**kwargs)
        self.text = "Simplify"
        self.is_active = True


class DrawCircuit(Task):
    def __init__(self, **kwargs):
        super(DrawCircuit, self).__init__(**kwargs)
        self.text = "Circuit"


class DrawTruthtable(Task):
    def __init__(self, **kwargs):
        super(DrawTruthtable, self).__init__(**kwargs)
        self.text = "Truthtable"


class Help(Task):
    def __init__(self, **kwargs):
        super(Help, self).__init__(**kwargs)
        self.text = "Help"


class Panel(BoxLayout):
    task = StringProperty("Simplify")

    def __init__(self, **kwargs):
        super(Panel, self).__init__(**kwargs)
        self.size_hint = (1, .9)
        self.pos_hint = {'x': 1, 'y': .05}
        self.icon = Icon()
        self.add_widget(self.icon)
        self.simplify = Simplify()
        self.drawcircuit = DrawCircuit()
        self.drawtruthtable = DrawTruthtable()
        self.help = Help()
        self.add_widget(self.simplify)
        self.add_widget(self.drawcircuit)
        self.add_widget(self.drawtruthtable)
        self.add_widget(self.help)
        with self.canvas.before:
            Color(.2, .2, .2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # select and set task to perform
    def on_task(self, instance, value):
        self.simplify.is_active = False
        self.drawcircuit.is_active = False
        self.drawtruthtable.is_active = False
        self.help.is_active = False
        if self.task == "Simplify":
            self.simplify.is_active = True
        elif self.task == "Circuit":
            self.drawcircuit.is_active = True
        elif self.task == "Truthtable":
            self.drawtruthtable.is_active = True
        elif self.task == "Help":
            self.help.is_active = True
        else:
            raise TypeError("Unknowwn Task or not a task: {}".format(self.task))


class TaskPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(TaskPanel, self).__init__(**kwargs)
        self.panel = Panel()
        self.add_widget(self.panel)


if __name__ == '__main__':
    class TestApp(App):

        def build(self):
            root = TaskPanel()
            return root


    TestApp().run()
