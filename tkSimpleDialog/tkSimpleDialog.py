import Tkinter


class Dialog(Tkinter.Toplevel):
    def __init__(self, parent, callback=None, title=None):

        Tkinter.Toplevel.__init__(self, parent)
        self.transient(parent)

        self.callback = callback

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Tkinter.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Tkinter.Frame(self)

        w = Tkinter.Button(box, text="OK", width=10, command=self.ok, default=Tkinter.ACTIVE)
        w.pack(side=Tkinter.LEFT, padx=5, pady=5)
        w = Tkinter.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=Tkinter.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        if self.callback:
            self.callback(self.apply())
        else:
            self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1  # override

    def apply(self):

        pass  # override
