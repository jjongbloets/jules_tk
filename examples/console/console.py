
from julesTk import app, controller, view
from julesTk.utils.console import LogView
from julesTk.controller import poller
import logging

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class LogApp(app.Application):

    def __init__(self):
        super(LogApp, self).__init__()

    def _prepare(self):
        self.title('Console')
        self.geometry('500x500+200+200')
        self.minsize(500, 300)
        self.add_controller("main", MainController(self))

    @property
    def main(self):
        return self.get_controller("main")

    def _start(self):
        self.main.start()


class MainView(view.View):

    def _prepare(self):
        # pack this view
        self.pack(fill=view.tk.BOTH, expand=1)
        frmb = view.ttk.Frame(self, relief=view.tk.RAISED, borderwidth=1)
        frmb.pack(side=view.tk.TOP, fill=view.tk.BOTH, expand=1)
        self._prepare_body(frmb)
        frmt = view.ttk.Frame(self, relief=view.tk.RAISED, borderwidth=1)
        frmt.pack(side=view.tk.BOTTOM, fill=view.tk.X, expand=1)
        self._prepare_tools(frmt)

    def _prepare_body(self, parent=None):
        if parent is None:
            parent = self
        log = LogView(parent)
        self.add_widget("log", log)
        log.pack(fill=view.tk.BOTH, expand=1)

    def _prepare_tools(self, parent=None):
        if parent is None:
            parent = self
        log = self.get_widget("log")
        btc = view.ttk.Button(parent, text="Clear", command=log.clear)
        btc.pack(side=view.tk.LEFT)


class MainController(poller.Poller, controller.ViewController):

    VIEW_CLASS = MainView

    def __init__(self, parent):
        super(MainController, self).__init__(parent=parent)
        self._log = logging.getLogger()
        self._log.setLevel(20)
        self._count = 0

    def _prepare(self):
        return controller.ViewController._prepare(self)

    def _start(self):
        controller.ViewController._start(self)
        handler = logging.StreamHandler(self.view.get_widget("log"))
        handler.level = 20
        self._log.addHandler(handler)
        self.run()

    def execute(self):
        self._log.info("Cycle {}".format(self._count))
        self._count += 1


if __name__ == "__main__":

    app = LogApp()
    app.run()
