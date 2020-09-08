from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class TaskPanel(BoxLayout):

    def __init__(self, **kwargs):
        super(TaskPanel, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.title = Label(text="LC Draw")

if __name__ == "__main__":
    class TaskPanelApp(App):
        def build(self):
            root = TaskPanel()
            return root


    TaskPanelApp().run()
