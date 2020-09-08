from kivy.app import App
from kivy.uix.widget import Widget


class LCDrawWidget(Widget):
    pass


class LCDrawApp(App):

    def build(self):
        root = LCDrawWidget()
        return root


if __name__ == "__main__":
    LCDrawApp().run()
