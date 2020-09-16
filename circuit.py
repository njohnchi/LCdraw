from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, StringProperty, ReferenceListProperty, ListProperty, BooleanProperty
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.image import Image
from kivy.properties import ObjectProperty

from compiler import run
import json


class Not(Widget):
    state = BooleanProperty(False)
    nodes = ListProperty([])

    def __init__(self, node, x, y, size, **kwargs):
        super(Not, self).__init__(**kwargs)
        self.node = node
        self.pos = (x, y)
        self.size = size
        self.on_image = Image(source="img/not_on.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.off_image = Image(source="img/not_off.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.off_image)
        self.bind(size=self._update_image, pos=self._update_image)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def on_state(self, instance, value):
        if self.state:
            self.clear_widgets()
            self.add_widget(self.on_image)
        else:
            self.clear_widgets()
            self.add_widget(self.off_image)

    def in_pin(self):
        return self.pos[0] + self.size[0], self.pos[1] + self.size[1] / 2

    def out_pin(self):
        return [(self.pos[0], self.pos[1] + self.size[1] / 2)]

    def on_nodes(self, instance, value):
        for i in self.nodes:
            i.bind(state=self.up_nod)

    def up_nod(self, instance, value):
        self.state = not self.nodes[0].state


class And(Widget):
    state = BooleanProperty(False)
    nodes = ListProperty([])

    def __init__(self, node, x, y, size, **kwargs):
        super(And, self).__init__(**kwargs)
        self.node = node
        self.pos = (x, y)
        self.size = (size[0]+(size[0]/5)*(self.node["inputs"] - 2), size[1]+(size[1]/5)*(self.node["inputs"] - 2))
        self.on_image = Image(source="img/and_on.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.off_image = Image(source="img/and_off.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.off_image)
        self.bind(size=self._update_image, pos=self._update_image)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def on_state(self, instance, value):
        if self.state:
            self.clear_widgets()
            self.add_widget(self.on_image)
        else:
            self.clear_widgets()
            self.add_widget(self.off_image)

    def in_pin(self):
        return self.pos[0] + self.size[0], self.pos[1] + self.size[1] / 2

    def out_pin(self):
        points = []
        offset = self.size[1] / (self.node["inputs"] + 1)
        for i in range(self.node["inputs"] + 1):
            points.extend([(self.pos[0], self.pos[1] + offset * (i + 1))])
        return points

    def on_nodes(self, instance, value):
        for i in self.nodes:
            i.bind(state=self.up_nod)

    def up_nod(self, instance, value):
        s = self.nodes[0].state
        for i in range(len(self.nodes) - 1):
            s = s and self.nodes[i + 1].state
        self.state = s


class Nand(Widget):
    state = BooleanProperty(False)
    nodes = ListProperty([])

    def __init__(self, node, x, y, size, **kwargs):
        super(Nand, self).__init__(**kwargs)
        self.node = node
        self.text = "Or"
        self.pos = (x, y)
        self.size = (size[0]+(size[0]/5)*(self.node["inputs"] - 2), size[1]+(size[1]/5)*(self.node["inputs"] - 2))
        self.on_image = Image(source="img/nand_on.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.off_image = Image(source="img/nand_off.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.off_image)
        self.bind(size=self._update_image, pos=self._update_image)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def on_state(self, instance, value):
        if self.state:
            self.clear_widgets()
            self.add_widget(self.on_image)
        else:
            self.clear_widgets()
            self.add_widget(self.off_image)

    def in_pin(self):
        return self.pos[0] + self.size[0], self.pos[1] + self.size[1] / 2

    def out_pin(self):
        points = []
        offset = self.size[1] / (self.node["inputs"] + 1)
        for i in range(self.node["inputs"] + 1):
            points.extend([(self.pos[0], self.pos[1] + offset * (i + 1))])
        return points

    def on_nodes(self, instance, value):
        for i in self.nodes:
            i.bind(state=self.up_nod)

    def up_nod(self, instance, value):
        s = self.nodes[0].state
        for i in range(len(self.nodes) - 1):
            s = s and self.nodes[i + 1].state
        self.state = not s


class Or(Widget):
    state = BooleanProperty(False)
    nodes = ListProperty([])

    def __init__(self, node, x, y, size, **kwargs):
        super(Or, self).__init__(**kwargs)
        self.node = node
        self.text = "Or"
        self.pos = (x, y)
        self.size = (size[0]+(size[0]/5)*(self.node["inputs"] - 2), size[1]+(size[1]/5)*(self.node["inputs"] - 2))
        self.on_image = Image(source="img/or_on.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.off_image = Image(source="img/or_off.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.off_image)
        self.bind(size=self._update_image, pos=self._update_image)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def on_state(self, instance, value):
        if self.state:
            self.clear_widgets()
            self.add_widget(self.on_image)
        else:
            self.clear_widgets()
            self.add_widget(self.off_image)

    def in_pin(self):
        return self.pos[0] + self.size[0] , self.pos[1] + self.size[1] / 2

    def out_pin(self):
        points = []
        offset = self.size[1] / (self.node["inputs"] + 1)
        for i in range(self.node["inputs"] + 1):
            points.extend([(self.pos[0] + (self.size[0]/4.8), self.pos[1] + offset * (i + 1))])
        return points

    def on_nodes(self, instance, value):
        for i in self.nodes:
            i.bind(state=self.up_nod)

    def up_nod(self, instance, value):
        s = self.nodes[0].state
        for i in range(len(self.nodes) - 1):
            s = s or self.nodes[i + 1].state
        self.state = s


class Nor(Widget):
    state = BooleanProperty(False)
    nodes = ListProperty([])

    def __init__(self, node, x, y, size, **kwargs):
        super(Nor, self).__init__(**kwargs)
        self.node = node
        self.pos = (x, y)
        self.size = (size[0]+(size[0]/5)*(self.node["inputs"] - 2), size[1]+(size[1]/5)*(self.node["inputs"] - 2))
        self.on_image = Image(source="img/nor_on.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.off_image = Image(source="img/nor_off.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.off_image)
        self.bind(size=self._update_image, pos=self._update_image)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def on_state(self, instance, value):
        if self.state:
            self.clear_widgets()
            self.add_widget(self.on_image)
        else:
            self.clear_widgets()
            self.add_widget(self.off_image)

    def in_pin(self):
        return self.pos[0] + self.size[0], self.pos[1] + self.size[1] / 2

    def out_pin(self):
        points = []
        offset = self.size[1] / (self.node["inputs"] + 1)
        for i in range(self.node["inputs"] + 1):
            points.extend([(self.pos[0] + (self.size[0]/4.8), self.pos[1] + offset * (i + 1))])
        return points

    def on_nodes(self, instance, value):
        for i in self.nodes:
            i.bind(state=self.up_nod)

    def up_nod(self, instance, value):
        s = self.nodes[0].state
        for i in range(len(self.nodes) - 1):
            s = s or self.nodes[i + 1].state
        self.state = not s


class Xor(Widget):
    state = BooleanProperty(False)
    nodes = ListProperty([])

    def __init__(self, node, x, y, size, **kwargs):
        super(Xor, self).__init__(**kwargs)
        self.node = node
        self.text = "Or"
        self.pos = (x, y)
        self.size = (size[0]+(size[0]/5)*(self.node["inputs"] - 2), size[1]+(size[1]/5)*(self.node["inputs"] - 2))
        self.on_image = Image(source="img/xor_on.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.off_image = Image(source="img/xor_off.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.off_image)
        self.bind(size=self._update_image, pos=self._update_image)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def on_state(self, instance, value):
        if self.state:
            self.clear_widgets()
            self.add_widget(self.on_image)
        else:
            self.clear_widgets()
            self.add_widget(self.off_image)

    def in_pin(self):
        return self.pos[0] + self.size[0], self.pos[1] + self.size[1] / 2

    def out_pin(self):
        points = []
        offset = self.size[1] / (self.node["inputs"] + 1)
        for i in range(self.node["inputs"] + 1):
            points.extend([(self.pos[0] + (self.size[0]/5), self.pos[1] + offset * (i + 1))])
        return points

    def on_nodes(self, instance, value):
        for i in self.nodes:
            i.bind(state=self.up_nod)

    def up_nod(self, instance, value):
        s = self.nodes[0].state
        for i in range(len(self.nodes) - 1):
            s = s ^ self.nodes[i + 1].state
        self.state = s


class Nxor(Widget):
    state = BooleanProperty(False)
    nodes = ListProperty([])

    def __init__(self, node, x, y, size, **kwargs):
        super(Nxor, self).__init__(**kwargs)
        self.node = node
        self.pos = (x, y)
        self.size = (size[0]+(size[0]/5)*(self.node["inputs"] - 2), size[1]+(size[1]/5)*(self.node["inputs"] - 2))
        self.on_image = Image(source="img/nxor_on.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.off_image = Image(source="img/nxor_off.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.off_image)
        self.bind(size=self._update_image, pos=self._update_image)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def on_state(self, instance, value):
        if self.state:
            self.clear_widgets()
            self.add_widget(self.on_image)
        else:
            self.clear_widgets()
            self.add_widget(self.off_image)

    def in_pin(self):
        return self.pos[0] + self.size[0], self.pos[1] + self.size[1] / 2

    def out_pin(self):
        points = []
        offset = self.size[1] / (self.node["inputs"] + 1)
        for i in range(self.node["inputs"] + 1):
            points.extend([(self.pos[0] + (self.size[0]/5), self.pos[1] + offset * (i + 1))])
        return points

    def on_nodes(self, instance, value):
        for i in self.nodes:
            i.bind(state=self.up_nod)

    def up_nod(self, instance, value):
        s = self.nodes[0].state
        for i in range(len(self.nodes) - 1):
            s = s ^ self.nodes[i + 1].state
        self.state = not s


class Input(Widget):
    state = BooleanProperty(False)
    nodes = ListProperty([])

    def __init__(self, node, x, y, size, yWin, **kwargs):
        super(Input, self).__init__(**kwargs)
        self.node = node
        self.pos = (x, y)
        self.size = size
        self.on_image = Image(source="img/port_on.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.off_image = Image(source="img/port_off.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.off_image)
        self.bind(size=self._update_image, pos=self._update_image)
        self.name = Label(text=self.node["name"], size=self.size, pos=[self.x, (self.y-self.size[1]/2)], color=[0,0,0,1])
        self.add_widget(self.name)
        with self.canvas:
            Color(0, 0, 0)
            self.line1 = Line(points=(x+self.size[0]/2, y+self.size[1]/1.3, x+self.size[0]/2, yWin + 70), width=1.2)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def on_state(self, instance, value):
        if self.state:
            self.clear_widgets()
            self.add_widget(self.on_image)
            self.add_widget(self.name)
        else:
            self.clear_widgets()
            self.add_widget(self.off_image)
            self.add_widget(self.name)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.state = not self.state

    def in_pin(self, y):
        return self.pos[0] + self.size[0]/2, y


class Output(Widget):
    state = BooleanProperty(False)
    nodes = ListProperty([])

    def __init__(self, node, x, y, size, **kwargs):
        super(Output, self).__init__(**kwargs)
        self.node = node
        self.pos = (x, y)
        self.size = size
        self.on_image = Image(source="img/port_on.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.off_image = Image(source="img/port_off.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.off_image)
        self.bind(size=self._update_image, pos=self._update_image)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def on_state(self, instance, value):
        if self.state:
            self.clear_widgets()
            self.add_widget(self.on_image)
        else:
            self.clear_widgets()
            self.add_widget(self.off_image)

    def out_pin(self):
        return [(self.pos[0], self.pos[1] + self.size[1] / 2)]

    def on_nodes(self, instance, value):
        for i in self.nodes:
            i.bind(state=self.up_nod)

    def up_nod(self, instance, value):
        self.state = self.nodes[0].state


class Wire(Widget):

    def __init__(self, a, b, o, **kwargs):
        super(Wire, self).__init__(**kwargs)
        x = a[0] - (o*15) + (b[0] - a[0]) / 2
        _a = (x, a[1])
        _b = (x, b[1])
        with self.canvas:
            Color(0, 0, 0)
            self.line1 = Line(points=(a, _a), width=1.2)
            self.line2 = Line(points=(_a, _b), width=1.2)
            self.line3 = Line(points=(_b, b), width=1.2)


class Circuit(Widget):
    xIncr = NumericProperty(0)
    yIncr = NumericProperty(0)
    xWin = NumericProperty(0)
    yWin = NumericProperty(0)
    inputs = {}

    def __init__(self, tree, **kwargs):
        super(Circuit, self).__init__(**kwargs)
        self.tree = tree
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.bind(size=self._update_win, pos=self._update_win)

    def _update_win(self, instance, value):
        self.xWin = instance.size[0]
        self.yWin = instance.size[1] * 0.9
        self.clear_widgets()
        self.inputs = {}
        self.build_tree()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def build_tree(self):
        self.xIncr = self.xWin / self.tree["depth"]
        self.yIncr = self.yWin / self.tree["weight"]
        for i in self.tree["nodes"]:
            self.draw_node(i, False, 0, False)

    def draw_node(self, node, outpin, o, parent):
        widget = self.build_node(node)
        if node["kind"] == "input":
            if node["name"] not in self.inputs.keys():
                self.inputs[node["name"]] = widget
                self.add_widget(widget)
            else:
                widget = self.inputs[node["name"]]
            x = self.x + self.xIncr / 2 + (node["x"] * self.xIncr)
            y = self.y + 20 + node["y"] * self.yWin
            wire = Wire((x, y), outpin, o)
            self.add_widget(wire)
            wire = Wire((x, y), widget.in_pin(y), o)
            self.add_widget(wire)
        else:
            self.add_widget(widget)
            if outpin:
                wire = Wire(widget.in_pin(), outpin, o)
                self.add_widget(wire)
        if parent:
            parent.nodes.append(widget)

        for i in range(node["inputs"]):
            o = i
            if i >= node["inputs"] / 2:
                o = node["inputs"] - i - 1
            self.draw_node(node["nodes"][i], widget.out_pin()[i], o, widget)

    def build_node(self, node):
        x = self.x + self.xIncr / 2 + (node["x"] * self.xIncr)
        y = self.y + 20 + node["y"] * self.yWin
        size = (self.xWin / 25, self.yWin / 12)
        widget = ""
        if node["kind"] == "not":
            widget = Not(node, x, y, size)
        elif node["kind"] == "and":
            widget = And(node, x, y, size)
        elif node["kind"] == "nand":
            widget = Nand(node, x, y, size)
        elif node["kind"] == "or":
            widget = Or(node, x, y, size)
        elif node["kind"] == "nor":
            widget = Nor(node, x, y, size)
        elif node["kind"] == "xor":
            widget = Xor(node, x, y, size)
        elif node["kind"] == "nxor":
            widget = Nxor(node, x, y, size)
        elif node["kind"] == "input":
            x = self.x - len(self.inputs) * self.width / 15
            y = self.y - 20
            widget = Input(node, x, y, size, self.yWin)
        elif node["kind"] == "output":
            widget = Output(node, x, y, size)
        else:
            print("unknown node object")
            print(node)
        return widget


class Cir(Widget):

    def __init__(self, tree, **kwargs):
        super(Cir, self).__init__(**kwargs)
        self.circuit = Circuit(tree)
        self.add_widget(self.circuit)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.bind(size=self._update_win, pos=self._update_win)

    def _update_win(self, instance, value):
        self.circuit.width = instance.width * 0.55
        self.circuit.height = instance.height * 0.9
        self.circuit.x = instance.x + len(self.circuit.inputs) * self.circuit.width / 15
        self.circuit.y = instance.y + 50

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == "__main__":
    class TaskPanelApp(App):
        def build(self):
            root = Cir(tree)
            return root


    expr = "f = a * (b OR (NOT (c * (NOT i)))) xor (d | c | g) xor (s OR t) xor (NOT (a OR (NOT (u and p)))) and f"
    tree = run.compiler(expr, False)
    tree = json.loads(tree)
    print(tree)
    TaskPanelApp().run()
