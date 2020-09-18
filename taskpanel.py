from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle


class Task(Button):

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
        self.text = "Task"
        self.font_size = 16
        self.background_color = (0.4, 0.4, 0.4, 1)


class TaskPanel(BoxLayout):

    def __init__(self, **kwargs):
        super(TaskPanel, self).__init__(**kwargs)
        self.btn1 = Button(text="btn1")
        self.btn2 = Button(text="btn2")
        self.btn3 = Button(text="btn3")
        self.btn4 = Button(text="btn3")
        self.task = Task()
        self.add_widget(self.task)
        self.task = Task()
        self.add_widget(self.task)
        self.add_widget(self.btn4)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.btn3)


if __name__ == '__main__':
    class TestApp(App):

        def build(self):
            root = TaskPanel()
            return root


    TestApp().run()