from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, BorderImage


class Task(Button):

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
        self.text = "Task"
        self.font_size = 16
        self.background_down = ''
        self.background_normal = ''
        self.size_hint = (1, .9)
        self.pos_hint = {'x': 1, 'y': .05}
        self.background_color = (0.2, 0.2, 0.2, 1)


class Icon(Label):

    def __init__(self, **kwargs):
        super(Icon, self).__init__(**kwargs)
        with self.canvas.before:
            Color(.2, .2, .2, 1)
            self.image = BorderImage(size=self.size, pos=self.pos, source="img/not_on.png")
        self.bind(size=self._update_image, pos=self._update_image)

    def _update_image(self, instance, value):
        self.image.pos = instance.pos
        self.image.size = instance.size


class TaskPanel(BoxLayout):

    def __init__(self, **kwargs):
        super(TaskPanel, self).__init__(**kwargs)
        self.icon = Icon()
        self.add_widget(self.icon)
        self.task = Task()
        self.add_widget(self.task)
        self.task = Task()
        self.add_widget(self.task)
        self.task = Task()
        self.add_widget(self.task)
        self.task = Task()
        self.add_widget(self.task)
        self.task = Task()
        self.add_widget(self.task)


if __name__ == '__main__':
    class TestApp(App):

        def build(self):
            root = TaskPanel()
            return root


    TestApp().run()