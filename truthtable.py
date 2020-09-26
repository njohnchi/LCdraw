from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout

import boolean as boolean


class Cell(BoxLayout):
    def __init__(self, text, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.text = text
        self.label = Label(text=self.text, size=self.size, pos=self.pos, color=(0, 0, 0, 1))
        self.label.font_size = 30
        self.add_widget(self.label)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.label.pos = instance.pos
        self.label.size = instance.size


class TruthTable(GridLayout):
    def __init__(self, expression, output, **kwargs):
        super(TruthTable, self).__init__(**kwargs)
        self.output = output
        self.expression = self.expression(expression)
        self.table = self.table(self.expression)
        self.draw_table(self.table)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.bind(size=self.update_cell, pos=self.update_cell)
        self.bind(minimum_height=self.setter('height'))
        self.bind(minimum_width=self.setter('width'))
        self.size_hint_x=None
        self.size_hint_y=None

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def expression(self, expression):
        if isinstance(expression, str):
            expression = boolean.parse(expression, False)
        if not isinstance(expression, boolean.Expression):
            raise TypeError(
                "Argument must be str or Expression but it is {}"
                .format(expression.__class__))
        return expression

    def table(self, table):
        if isinstance(table, str):
            table = boolean.parse(table, False)
        if isinstance(table, boolean.Expression):
            table = boolean.truth_table(table)
        else:
            raise TypeError(
                "Argument must be Expression but it is {}"
                .format(table.__class__))
        # Table should not be directly modified
        return tuple(table)

    def no_cols(self, table):
        no = 0
        for sym in sorted(table[0].keys()):
            if isinstance(sym, boolean.Symbol):
                no += 1
        no += 1
        return no

    def draw_table(self, table):
        self.cols = self.no_cols(table)
        if len(table[0]) <= 1:
            self.cols -= 1
        for sym in sorted(table[0].keys()):
            if isinstance(sym, boolean.Symbol):
                self.cell = Cell(text=str(sym))
                self.add_widget(self.cell)
        if len(table[0]) > 1:
            self.cell = Cell(text=self.output)
            self.add_widget(self.cell)
        for dic in table:
            n = 0
            for key in sorted(dic.keys()):
                if n == self.no_cols(table)-1:
                    self.cell = Cell(text=str(dic[key]))
                    self.add_widget(self.cell)
                n += 1
                if isinstance(key, boolean.Symbol):
                    self.cell = Cell(text=str(dic[key]))
                    self.add_widget(self.cell)

    def update_cell(self, instance, value):
        for child in self.children:
            child.size = instance.size
            child.pos = instance.pos


if __name__ == '__main__':
    class TruthTableApp(App):

        def build(self):
            root = TruthTable("a+b", "Y")
            return root

    TruthTableApp().run()

