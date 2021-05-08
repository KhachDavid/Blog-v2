from io import StringIO
from html.parser import HTMLParser

__author__ = "David Khachatryan"
__copyright__ = "Copyright 2021, Mat Ognutyun"
__credits__ = "https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python"
__license__ = "GPL"
__version__ = "2.0.0"
__maintainer__ = "David Khachatryan"
__email__ = "dkhachatryan@wisc.edu"
__status__ = "Production"

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()