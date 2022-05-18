import Tkinter as Tk
import ttk

from Tkconstants import CENTER
from ..Styles import DefaultStyle, DefaultStyleSettings


class LaunchScreen:
    def __init__(self, top=None):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        self.style = DefaultStyle()

        self.me_logo_image = Tk.Label(top)
        self.me_logo_image.place(relx=0.5, anchor="n", height=150, width=250)
        self.me_logo_image.configure(activebackground=DefaultStyleSettings.bg_color)
        self.me_logo_image.configure(text='''MultiExplorer.png''')

        self.execution_flow_label_frame = Tk.LabelFrame(top)
        self.execution_flow_label_frame.place(relx=0.5, rely=0.5, anchor=CENTER, height=120, width=600)
        self.execution_flow_label_frame.configure(relief='groove')
        self.execution_flow_label_frame.configure(labelanchor='n')
        self.execution_flow_label_frame.configure(text='''Execution Flow''')

        self.execute_button = Tk.Button(self.execution_flow_label_frame)
        self.execute_button.place(
            relx=0.599,
            rely=0.405,
            height=33,
            width=55,
            bordermode='ignore'
        )
        self.execute_button.configure(activebackground="#f9f9f9")
        self.execute_button.configure(borderwidth="2")
        self.execute_button.configure(text='''Run''')

        self.select_execution_flow_combobox = ttk.Combobox(self.execution_flow_label_frame)
        self.select_execution_flow_combobox.place(
            relx=0.177,
            rely=0.405,
            relheight=0.405,
            relwidth=0.392,
            bordermode='ignore'
        )
        self.value_list = ['Gpu', 'Cpu', 'Outros', ]
        self.select_execution_flow_combobox.configure(values=self.value_list)
        self.select_execution_flow_combobox.configure(textvariable=Tk.StringVar())
        self.select_execution_flow_combobox.configure(takefocus="")
