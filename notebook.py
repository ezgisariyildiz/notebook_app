import tornado.ioloop
import tornado.web
from datetime import datetime

class Note:
    def __init__(self, title, content, date):
        self.title = title
        self.content = content
        self.date = date

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, notebook):
        self.notebook = notebook

    def get(self):
        notes = self.notebook
        self.render("notebook.html", notes=notes)

    def post(self):
        title = self.get_argument("title")
        content = self.get_argument("content")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note = Note(title, content, date)
        self.notebook.append(note)
        self.redirect("/")

class DeleteHandler(tornado.web.RequestHandler):
    def initialize(self, notebook):
        self.notebook = notebook

    def post(self):
        index = int(self.get_argument("index"))
        del self.notebook[index]
        self.redirect("/")

def make_app():
    notebook = []
    return tornado.web.Application([
        (r"/", MainHandler, dict(notebook=notebook)),
        (r"/delete", DeleteHandler, dict(notebook=notebook)),
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    print("Web server started at http://localhost:8000")
    tornado.ioloop.IOLoop.current().start()


