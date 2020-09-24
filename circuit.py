from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, StringProperty, ReferenceListProperty, ListProperty, BooleanProperty
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.clock import Clock

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

    def update_node(self, instance, value):
        x = instance.x + instance.xIncr / 2 + (self.node["x"] * instance.xIncr)
        y = instance.y + 20 + self.node["y"] * instance.yWin
        print(instance.yWin)
        size = (instance.xWin / 20, instance.yWin / 12)
        self.pos = (x, y)
        self.size = size

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

    def update_node(self, instance, value):
        x = instance.x + instance.xIncr / 2 + (self.node["x"] * instance.xIncr)
        y = instance.y + 20 + self.node["y"] * instance.yWin
        size = (instance.xWin / 20, instance.yWin / 12)
        self.pos = (x, y)
        self.size = (size[0] + (size[0] / 5) * (self.node["inputs"] - 2), size[1] + (size[1] / 5) * (self.node["inputs"] - 2))

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

    def update_node(self, instance, value):
        x = instance.x + instance.xIncr / 2 + (self.node["x"] * instance.xIncr)
        y = instance.y + 20 + self.node["y"] * instance.yWin
        size = (instance.xWin / 20, instance.yWin / 12)
        self.pos = (x, y)
        self.size = (size[0] + (size[0] / 5) * (self.node["inputs"] - 2), size[1] + (size[1] / 5) * (self.node["inputs"] - 2))

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

    def update_node(self, instance, value):
        x = instance.x + instance.xIncr / 2 + (self.node["x"] * instance.xIncr)
        y = instance.y + 20 + self.node["y"] * instance.yWin
        size = (instance.xWin / 20, instance.yWin / 12)
        self.pos = (x, y)
        self.size = (size[0] + (size[0] / 5) * (self.node["inputs"] - 2), size[1] + (size[1] / 5) * (self.node["inputs"] - 2))

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

    def update_node(self, instance, value):
        x = instance.x + instance.xIncr / 2 + (self.node["x"] * instance.xIncr)
        y = instance.y + 20 + self.node["y"] * instance.yWin
        size = (instance.xWin / 20, instance.yWin / 12)
        self.pos = (x, y)
        self.size = (size[0] + (size[0] / 5) * (self.node["inputs"] - 2), size[1] + (size[1] / 5) * (self.node["inputs"] - 2))

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

    def update_node(self, instance, value):
        x = instance.x + instance.xIncr / 2 + (self.node["x"] * instance.xIncr)
        y = instance.y + 20 + self.node["y"] * instance.yWin
        size = (instance.xWin / 20, instance.yWin / 12)
        self.pos = (x, y)
        self.size = (size[0] + (size[0] / 5) * (self.node["inputs"] - 2), size[1] + (size[1] / 5) * (self.node["inputs"] - 2))

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

    def update_node(self, instance, value):
        x = instance.x + instance.xIncr / 2 + (self.node["x"] * instance.xIncr)
        y = instance.y + 20 + self.node["y"] * instance.yWin
        size = (instance.xWin / 20, instance.yWin / 12)
        self.pos = (x, y)
        self.size = (size[0] + (size[0] / 5) * (self.node["inputs"] - 2), size[1] + (size[1] / 5) * (self.node["inputs"] - 2))

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

    def __init__(self, node, x, y, size, yWin, index, **kwargs):
        super(Input, self).__init__(**kwargs)
        self.node = node
        self.index = index
        self.pos = (x, y)
        self.size = size
        self.on_image = Image(source="img/port_on.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.off_image = Image(source="img/port_off.png", size=self.size, pos=self.pos, allow_stretch=True)
        self.add_widget(self.off_image)
        self.bind(size=self._update_image, pos=self._update_image)
        self.name = Label(text=self.node["name"], size=self.size, pos=[self.x, (self.y-self.size[1]/1.2)], color=[0,0,0,1])
        self.add_widget(self.name)
        with self.canvas.before:
            Color(0, 0, 0)
            self.line1 = Line(points=(x+self.size[0]/2, y+self.size[1]/1.3, x+self.size[0]/2, y + yWin+50), width=1.2)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def update_node(self, instance, value):
        x = instance.x - self.index * instance.width / 15
        y = instance.y - 20
        size = (instance.xWin / 20, instance.yWin / 12)
        self.pos = (x, y)
        self.size = size
        self.line1.points = (x + self.size[0] / 2, y + self.size[1] / 1.3, x + self.size[0] / 2, y + instance.yWin + 50)
        self.name.size = self.size
        self.name.pos = [self.x, (self.y - self.size[1] / 1.2)]

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
        self.name = Label(text=self.node["name"], size=self.size, pos=[self.x, (self.y - self.size[1] / 1.3)],
                          color=[0, 0, 0, 1])
        self.add_widget(self.name)

    def _update_image(self, instance, value):
        self.on_image.pos = instance.pos
        self.on_image.size = instance.size
        self.off_image.pos = instance.pos
        self.off_image.size = instance.size

    def update_node(self, instance, value):
        x = instance.x + instance.xIncr / 2 + (self.node["x"] * instance.xIncr)
        y = instance.y + 20 + self.node["y"] * instance.yWin
        size = (instance.xWin / 20, instance.yWin / 12)
        self.pos = (x, y)
        self.size = size
        self.name.size = self.size
        self.name.pos = [self.x, (self.y - self.size[1] / 1.3)]

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
    start = ListProperty([])
    stop = ListProperty([])

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

    def update_wire(self, instance, value):
        parent = instance.parent_node
        # print("p ", parent.nodes)
        # print("w ", instance)
        print("se", self)
        print("wi", instance)
        for i in range(len(parent.nodes)):
            print("ps ", parent.nodes[i])
            if parent.nodes[i] == instance:
                inst = parent.nodes[i]
                print("true")
                o = i
                if i >= len(parent.nodes) / 2:
                    o = len(parent.nodes) - i - 1
                b = parent.out_pin()[i]
                if instance.node["kind"] == "input":
                    _x = self.parent.x + self.parent.xIncr / 2 + (instance.node["x"] * self.parent.xIncr)
                    y = self.parent.y + 20 + instance.node["y"] * self.parent.yWin
                    a = self.parent.inputs[instance.node["name"]].in_pin(y)
                    x = _x - (o * 15) + (b[0] - _x) / 2
                    _a = (x, a[1])
                    _b = (x, b[1])
                    self.line1.points = (a, _a)
                    self.line2.points = (_a, _b)
                    self.line3.points = (_b, b)
                else:
                    a = instance.in_pin()
                    x = a[0] - (o * 15) + (b[0] - a[0]) / 2
                    _a = (x, a[1])
                    _b = (x, b[1])
                    self.line1.points = (a, _a)
                    self.line2.points = (_a, _b)
                    self.line3.points = (_b, b)
            elif parent.nodes[i].node["name"] == instance.node["name"]:
                print("prr ", parent)
            else:
                print(False)


class Cir(Widget):
    xIncr = NumericProperty(0)
    yIncr = NumericProperty(0)
    xWin = NumericProperty(0)
    yWin = NumericProperty(0)

    def __init__(self, tree, **kwargs):
        super(Cir, self).__init__(**kwargs)
        self.tree = tree
        self.inputs = {}
        self.build_tree()
        self.bind(size=self._update_win, pos=self._update_win)

    def _update_win(self, instance, value):
        self.xWin = instance.size[0]
        self.yWin = instance.size[1] * 0.9
        self.xIncr = self.xWin / self.tree["depth"]
        self.yIncr = self.yWin / self.tree["weight"]
        # self.clear_widgets()
        # self.inputs = {}
        # self.build_tree()

    def build_tree(self):
        for i in self.tree["nodes"]:
            self.draw_node(i, False, 0, False)

    def draw_node(self, node, outpin, o, parent):
        widget = self.build_node(node)
        wid = widget
        if node["kind"] == "input":
            if node["name"] not in self.inputs.keys():
                self.inputs[node["name"]] = widget
                self.add_widget(widget)
            else:
                widget = self.inputs[node["name"]]
            print(wid.node["y"])
            x = self.x + self.xIncr / 2 + (node["x"] * self.xIncr)
            y = self.y + 20 + node["y"] * self.yWin
            wire = Wire((x, y), outpin, o)
            print("wire ", wire)
            print("wid", wid)
            # self.add_widget(wire)
            # widget.bind(pos=wire.update_wire)
            # wire = Wire((x, y), widget.in_pin(y), o)
            self.add_widget(wire)
            wid.bind(pos=wire.update_wire, size=wire.update_wire)
        else:
            self.add_widget(widget)
            if outpin:
                wire = Wire(widget.in_pin(), outpin, o)
                print("wire n ,", wire)
                self.add_widget(wire)
                wid.bind(pos=wire.update_wire, size=wire.update_wire)
        if parent:
            parent.nodes.append(wid)
            # widget.parent_node = parent
            wid.parent_node = parent

        for i in range(node["inputs"]):
            o = i
            if i >= node["inputs"] / 2:
                o = node["inputs"] - i - 1
            self.draw_node(node["nodes"][i], widget.out_pin()[i], o, wid)

    def build_node(self, node):
        x = self.x + self.xIncr / 2 + (node["x"] * self.xIncr)
        y = self.y + 20 + node["y"] * self.yWin
        size = (self.xWin / 20, self.yWin / 12)
        widget = ""
        if node["kind"] == "not":
            widget = Not(node, x, y, size)
            self.bind(size=widget.update_node, pos=widget.update_node)
        elif node["kind"] == "and":
            widget = And(node, x, y, size)
            self.bind(size=widget.update_node, pos=widget.update_node)
        elif node["kind"] == "nand":
            widget = Nand(node, x, y, size)
            self.bind(size=widget.update_node, pos=widget.update_node)
        elif node["kind"] == "or":
            widget = Or(node, x, y, size)
            self.bind(size=widget.update_node, pos=widget.update_node)
        elif node["kind"] == "nor":
            widget = Nor(node, x, y, size)
            self.bind(size=widget.update_node, pos=widget.update_node)
        elif node["kind"] == "xor":
            widget = Xor(node, x, y, size)
            self.bind(size=widget.update_node, pos=widget.update_node)
        elif node["kind"] == "nxor":
            widget = Nxor(node, x, y, size)
            self.bind(size=widget.update_node, pos=widget.update_node)
        elif node["kind"] == "input":
            x = self.x - len(self.inputs) * self.width / 15
            y = self.y - 20
            index = len(self.inputs)
            widget = Input(node, x, y, size, self.yWin, index)
            self.bind(size=widget.update_node, pos=widget.update_node)
        elif node["kind"] == "output":
            widget = Output(node, x, y, size)
            self.bind(size=widget.update_node, pos=widget.update_node)
        else:
            print("unknown node object")
            print(node)
        return widget


class Circuit(Widget):

    def __init__(self, expr, **kwargs):
        super(Circuit, self).__init__(**kwargs)
        self.tree = run.compiler(expr, False)
        self.tree = json.loads(self.tree)
        self.circuit = Cir(self.tree)
        self.add_widget(self.circuit)
        self.size_hint = (None, None)
        self.bind(size=self._update_win, pos=self._update_win)
        Clock.schedule_once(self.run_sim, 0.1)

    def _update_win(self, instance, value):
        self.circuit.width = instance.width * 0.55
        self.circuit.height = instance.height * 0.9
        self.circuit.x = instance.x + len(self.circuit.inputs) * self.circuit.width / 15
        self.circuit.y = instance.y + 50

    def run_sim(self, dt):
        for i in self.circuit.inputs:
            self.circuit.inputs[i].state = True
        return


if __name__ == "__main__":
    class CircuitApp(App):
        def build(self):
            root = Circuit(expr)
            return root


    expr = "f = a * (b OR (NOT (c * (NOT i)))) xor (d | c | g) xor (s OR t) xor (NOT (a OR (NOT (u and p)))) and f"
    # tree = run.compiler(expr, True)
    # tree = json.loads(tree)
    # print(tree)
    CircuitApp().run()
