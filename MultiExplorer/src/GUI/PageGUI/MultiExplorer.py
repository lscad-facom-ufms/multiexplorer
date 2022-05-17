import Tkinter as Tk
import ttk

from Tkconstants import CENTER
from ..Menus import DefaultMenu
from ..Styles import DefaultStyle


class TelaInicial:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        self.style = DefaultStyle()

        top.geometry("1024x768")
        top.minsize(640, 480)
        top.maxsize(1920, 1080)
        top.resizable(1, 1)
        top.title("MultiExplorer")
        top.configure(highlightcolor="black")

        self.Label_Execution = Tk.LabelFrame(top)
        self.Label_Execution.place(relx=0.5, rely=0.5, anchor=CENTER, height=120, width=600)
        self.Label_Execution.configure(relief='groove')
        self.Label_Execution.configure(labelanchor='n')
        self.Label_Execution.configure(text='''Execution Flow''')

        self.Button_fluxoDeExe = Tk.Button(self.Label_Execution)
        self.Button_fluxoDeExe.place(relx=0.599, rely=0.405, height=33, width=55
                                     , bordermode='ignore')
        self.Button_fluxoDeExe.configure(activebackground="#f9f9f9")
        self.Button_fluxoDeExe.configure(borderwidth="2")
        self.Button_fluxoDeExe.configure(text='''Run''')

        self.Combobox_ExecutionFlow = ttk.Combobox(self.Label_Execution)
        self.Combobox_ExecutionFlow.place(relx=0.177, rely=0.405, relheight=0.405
                                          , relwidth=0.392, bordermode='ignore')
        self.value_list = ['Gpu', 'Cpu', 'Outros', ]
        self.Combobox_ExecutionFlow.configure(values=self.value_list)
        self.Combobox_ExecutionFlow.configure(textvariable=Tk.StringVar())
        self.Combobox_ExecutionFlow.configure(takefocus="")

        self.menubar = DefaultMenu(top)

        self.Image_ME = Tk.Label(top)
        self.Image_ME.place(relx=0.302, rely=0.043, height=138, width=239)
        self.Image_ME.configure(activebackground="#f9f9f9")
        self.Image_ME.configure(text='''MultiExplorer.png''')
