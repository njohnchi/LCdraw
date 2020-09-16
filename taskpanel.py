from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty


kv = '''
BoxLayout:
    orientation: 'vertical'
    Widget:
        canvas:
            Color: 
                rgb: 0, 0, 1
            Mesh:
                vertices: app.vertices
                indices: app.indices
                mode: app.mode
        on_touch_down:
            if self.collide_point(*args[1].pos): app.add_point(args[1].pos)
    BoxLayout:
        size_hint_y: None
        height: '20sp'
        Spinner:
            text: app.mode
            values:
                'points', 'line_strip', 'line_loop', 'lines',\
                'triangle_strip', 'triangle_fan'
            on_text: app.mode = args[1]
        Button:
            text: 'clear'
            on_press: app.clear()
'''


class TriangleApp(App):
    vertices = ListProperty([])
    indices = ListProperty([])
    mode = StringProperty('points')

    def build(self):
        return Builder.load_string(kv)

    def add_point(self, pos):
        self.vertices.extend([pos[0], pos[1], 0, 0])
        self.indices.append(len(self.indices))
        print(self.vertices)
        print(self.indices)

    def clear(self):
        self.vertices = []
        self.indices = []


if __name__ == '__main__':
    TriangleApp().run()