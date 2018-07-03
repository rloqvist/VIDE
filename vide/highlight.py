from vide.utils import load_config
import uuid

kws = ["VAR", "OUT", "INP", "INC", "DEC", "WHL", "END"]

types = ["INT", "STR"]

def create_tag_name():
    return str(uuid.uuid4()).split('-')[0]


def line_keyword_positions(line, keyword, line_number):
    positions = list()
    i = line.find(keyword)
    while i >= 0:
        pos = {
            'start': "%s.%s" % ( line_number+1, i ),
            'stop': "%s.%s" % ( line_number+1, i+len(keyword) ),
            'word': keyword,
        }
        positions.append(pos)
        i = line.find(keyword, i + 1)
    return positions

def keywords_positions(string):
    positions = list()
    for kw in kws:
        for n, line in enumerate(string.split("\n")):
            positions += line_keyword_positions(line, kw, n)
    return positions

def comments_positions(string):
    positions = list()
    for n, line in enumerate(string.split("\n")):
        i = line.find("//")
        if i >= 0:
            pos = {
                'start': "%s.%s" % ( n+1, i ),
                'stop': "%s.%s" % ( n+1, len(line) ),
            }
            positions.append(pos)
    return positions

def reserved_positions(string):
    positions = list()
    for rw in types:
        for n, line in enumerate(string.split("\n")):
            positions += line_keyword_positions(line, rw, n)
    return positions


class Highlighter:

    def __init__(self, text=None):
        load_config(self)
        self.text_widget = text
        self.tag_names = list()
        self.color()

    def color(self):
        for tag in self.tag_names:
            self.text_widget.tag_remove(tag, '1.0')
            self.tag_names = list()

        self.text_widget.configure(background=self.BACKGROUND)
        self.text_widget.tag_add("text",  "1.0", 'end')
        self.text_widget.tag_configure("text", foreground=self.NORMAL_TEXT)
        self.tag_names.append('text')

        string = self.text_widget.get("1.0", "end")[:-1]
        self.color_positions(string, keywords_positions, self.KEY_WORD)
        self.color_positions(string, reserved_positions, self.RESERVED_WORD)
        self.color_positions(string, comments_positions, self.COMMENT)

    def color_positions(self, string, fetch_positions, color):
        positions = fetch_positions(string)
        for position in positions:
            tag_name = create_tag_name()
            self.text_widget.tag_add(tag_name,  position['start'], position['stop'])
            self.text_widget.tag_configure(tag_name, foreground=color)
            self.tag_names.append(tag_name)
