#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 6.2
#  in conjunction with Tcl version 8.6
#    May 13, 2022 01:35:20 AM UTC  platform: Linux

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import Input_cpu_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    Input_cpu_support.set_Tk_var()
    top = Input_cpu (root)
    Input_cpu_support.init(root, top)
    root.mainloop()

w = None
def create_Input_cpu(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Input_cpu(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    Input_cpu_support.set_Tk_var()
    top = Input_cpu (w)
    Input_cpu_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Input_cpu():
    global w
    w.destroy()
    w = None

class Input_cpu:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1060x575+2295+323")
        top.minsize(1, 1)
        top.maxsize(3825, 1055)
        top.resizable(1,  1)
        top.title("MultiExplorer")
        top.configure(highlightcolor="black")

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.menubar.add_command(
                label="Edit as Json")

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.066, rely=0.07, relheight=0.278
                , relwidth=0.434)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''Preferences''')

        self.TCombobox1 = ttk.Combobox(self.Labelframe1)
        self.TCombobox1.place(relx=0.285, rely=0.25, relheight=0.169
                , relwidth=0.489, bordermode='ignore')
        self.value_list = ['Sniper','Verilator','Outro',]
        self.TCombobox1.configure(values=self.value_list)
        self.TCombobox1.configure(takefocus="")

        self.Checkbutton1 = tk.Checkbutton(self.Labelframe1)
        self.Checkbutton1.place(relx=0.283, rely=0.563, relheight=0.144
                , relwidth=0.146, bordermode='ignore')
        self.Checkbutton1.configure(activebackground="#f9f9f9")
        self.Checkbutton1.configure(justify='left')
        self.Checkbutton1.configure(text='''Yes''')
        self.Checkbutton1.configure(variable=Input_cpu_support.che53)
        self.tooltip_font = "TkDefaultFont"
        self.Checkbutton1_tooltip = \
        ToolTip(self.Checkbutton1, self.tooltip_font, '''Yes''')

        self.Label1 = tk.Label(self.Labelframe1)
        self.Label1.place(relx=0.065, rely=0.25, height=21, width=89
                , bordermode='ignore')
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Simulator''')

        self.Checkbutton2 = tk.Checkbutton(self.Labelframe1)
        self.Checkbutton2.place(relx=0.459, rely=0.563, relheight=0.144
                , relwidth=0.146, bordermode='ignore')
        self.Checkbutton2.configure(activebackground="#f9f9f9")
        self.Checkbutton2.configure(justify='left')
        self.Checkbutton2.configure(text='''No''')
        self.Checkbutton2.configure(variable=Input_cpu_support.che57)

        self.Label2 = tk.Label(self.Labelframe1)
        self.Label2.place(relx=0.087, rely=0.563, height=21, width=79
                , bordermode='ignore')
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(text='''DSE''')

        self.TCombobox3 = ttk.Combobox(self.Labelframe1)
        self.TCombobox3.place(relx=0.285, rely=0.813, relheight=0.131
                , relwidth=0.496, bordermode='ignore')
        self.value_list = ['clock','test1','outro1',]
        self.TCombobox3.configure(values=self.value_list)
        self.TCombobox3.configure(textvariable=Input_cpu_support.combobox)
        self.TCombobox3.configure(takefocus="")

        self.Label9 = tk.Label(self.Labelframe1)
        self.Label9.place(relx=0.065, rely=0.813, height=21, width=79
                , bordermode='ignore')
        self.Label9.configure(activebackground="#f9f9f9")
        self.Label9.configure(text='''Benchmark''')

        self.Labelframe2 = tk.LabelFrame(top)
        self.Labelframe2.place(relx=0.538, rely=0.07, relheight=0.838
                , relwidth=0.382)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(text='''General Modeling''')
        self.Labelframe2.configure(cursor="fleur")

        self.TLabel1 = ttk.Label(self.Labelframe2)
        self.TLabel1.place(relx=0.074, rely=0.122, height=19, width=42
                , bordermode='ignore')
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(relief="flat")
        self.TLabel1.configure(anchor='w')
        self.TLabel1.configure(justify='left')
        self.TLabel1.configure(text='''Core''')

        self.TLabel2 = ttk.Label(self.Labelframe2)
        self.TLabel2.place(relx=0.074, rely=0.224, height=19, width=82
                , bordermode='ignore')
        self.TLabel2.configure(background="#d9d9d9")
        self.TLabel2.configure(foreground="#000000")
        self.TLabel2.configure(relief="flat")
        self.TLabel2.configure(anchor='w')
        self.TLabel2.configure(justify='left')
        self.TLabel2.configure(text='''Frequency''')

        self.TLabel3 = ttk.Label(self.Labelframe2)
        self.TLabel3.place(relx=0.074, rely=0.326, height=18, width=82
                , bordermode='ignore')
        self.TLabel3.configure(background="#d9d9d9")
        self.TLabel3.configure(foreground="#000000")
        self.TLabel3.configure(relief="flat")
        self.TLabel3.configure(anchor='w')
        self.TLabel3.configure(justify='left')
        self.TLabel3.configure(text='''Memory''')

        self.TLabel4 = ttk.Label(self.Labelframe2)
        self.TLabel4.place(relx=0.074, rely=0.446, height=19, width=72
                , bordermode='ignore')
        self.TLabel4.configure(background="#d9d9d9")
        self.TLabel4.configure(foreground="#000000")
        self.TLabel4.configure(relief="flat")
        self.TLabel4.configure(anchor='w')
        self.TLabel4.configure(justify='left')
        self.TLabel4.configure(text='''Network''')

        self.TLabel5 = ttk.Label(self.Labelframe2)
        self.TLabel5.place(relx=0.074, rely=0.55, height=18, width=72
                , bordermode='ignore')
        self.TLabel5.configure(background="#d9d9d9")
        self.TLabel5.configure(foreground="#000000")
        self.TLabel5.configure(relief="flat")
        self.TLabel5.configure(anchor='w')
        self.TLabel5.configure(justify='left')
        self.TLabel5.configure(text='''Power''')

        self.TCombobox2 = ttk.Combobox(self.Labelframe2)
        self.TCombobox2.place(relx=0.321, rely=0.122, relheight=0.044
                , relwidth=0.435, bordermode='ignore')
        self.TCombobox2.configure(textvariable=Input_cpu_support.combobox)
        self.TCombobox2.configure(takefocus="")

        self.TEntry1 = ttk.Entry(self.Labelframe2)
        self.TEntry1.place(relx=0.321, rely=0.224, relheight=0.044, relwidth=0.43
                , bordermode='ignore')
        self.TEntry1.configure(takefocus="")
        self.TEntry1.configure(cursor="xterm")

        self.TCombobox4 = ttk.Combobox(self.Labelframe2)
        self.TCombobox4.place(relx=0.321, rely=0.326, relheight=0.041
                , relwidth=0.435, bordermode='ignore')
        self.TCombobox4.configure(textvariable=Input_cpu_support.combobox)
        self.TCombobox4.configure(takefocus="")

        self.TCombobox5 = ttk.Combobox(self.Labelframe2)
        self.TCombobox5.place(relx=0.321, rely=0.446, relheight=0.044
                , relwidth=0.435, bordermode='ignore')
        self.TCombobox5.configure(textvariable=Input_cpu_support.combobox)
        self.TCombobox5.configure(takefocus="")

        self.TCombobox6 = ttk.Combobox(self.Labelframe2)
        self.TCombobox6.place(relx=0.321, rely=0.55, relheight=0.041
                , relwidth=0.435, bordermode='ignore')
        self.TCombobox6.configure(textvariable=Input_cpu_support.combobox)
        self.TCombobox6.configure(takefocus="")



        self.Labelframe3 = tk.LabelFrame(top)
        self.Labelframe3.place(relx=0.066, rely=0.383, relheight=0.522
                , relwidth=0.433)
        self.Labelframe3.configure(relief='groove')
        self.Labelframe3.configure(text='''DSE''')

        self.Label3 = tk.Label(self.Labelframe3)
        self.Label3.place(relx=0.065, rely=0.167, height=21, width=99
                , bordermode='ignore')
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(text='''ORIG CORES''')

        self.Label4 = tk.Label(self.Labelframe3)
        self.Label4.place(relx=0.065, rely=0.367, height=21, width=89
                , bordermode='ignore')
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(text='''IP CORES''')

        self.Label5 = tk.Label(self.Labelframe3)
        self.Label5.place(relx=0.065, rely=0.5, height=41, width=149
                , bordermode='ignore')
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(text='''Max. Power Density''')

        self.Entry1 = tk.Entry(self.Labelframe3)
        self.Entry1.place(relx=0.438, rely=0.167, height=23, relwidth=0.122
                , bordermode='ignore')
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(selectbackground="blue")
        self.Entry1.configure(selectforeground="white")
        self.tooltip_font = "TkDefaultFont"
        self.Entry1_tooltip = \
        ToolTip(self.Entry1, self.tooltip_font, '''de''')

        self.Label6 = tk.Label(self.Labelframe3)
        self.Label6.place(relx=0.065, rely=0.7, height=41, width=119
                , bordermode='ignore')
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(text='''Maximum Area''')

        self.Entry2 = tk.Entry(self.Labelframe3)
        self.Entry2.place(relx=0.436, rely=0.533, height=23, relwidth=0.318
                , bordermode='ignore')
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(selectbackground="blue")
        self.Entry2.configure(selectforeground="white")

        self.Entry3 = tk.Entry(self.Labelframe3)
        self.Entry3.place(relx=0.438, rely=0.733, height=23, relwidth=0.318
                , bordermode='ignore')
        self.Entry3.configure(background="white")
        self.Entry3.configure(font="TkFixedFont")
        self.Entry3.configure(selectbackground="blue")
        self.Entry3.configure(selectforeground="white")

        self.Entry4 = tk.Entry(self.Labelframe3)
        self.Entry4.place(relx=0.438, rely=0.367, height=23, relwidth=0.122
                , bordermode='ignore')
        self.Entry4.configure(background="white")
        self.Entry4.configure(font="TkFixedFont")
        self.Entry4.configure(selectbackground="blue")
        self.Entry4.configure(selectforeground="white")

        self.Label7 = tk.Label(self.Labelframe3)
        self.Label7.place(relx=0.786, rely=0.533, height=21, width=59
                , bordermode='ignore')
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(text='''(W/mm²)''')

        self.Label8 = tk.Label(self.Labelframe3)
        self.Label8.place(relx=0.808, rely=0.733, height=21, width=39
                , bordermode='ignore')
        self.Label8.configure(activebackground="#f9f9f9")
        self.Label8.configure(text='''(mm²)''')

        self.Label10 = tk.Label(self.Labelframe3)
        self.Label10.place(relx=0.59, rely=0.167, height=21, width=39
                , bordermode='ignore')
        self.Label10.configure(activebackground="#f9f9f9")
        self.Label10.configure(text='''To''')

        self.Label11 = tk.Label(self.Labelframe3)
        self.Label11.place(relx=0.59, rely=0.367, height=21, width=39
                , bordermode='ignore')
        self.Label11.configure(activebackground="#f9f9f9")
        self.Label11.configure(text='''To''')

        self.Entry5 = tk.Entry(self.Labelframe3)
        self.Entry5.place(relx=0.721, rely=0.167, height=23, relwidth=0.144
                , bordermode='ignore')
        self.Entry5.configure(background="white")
        self.Entry5.configure(font="TkFixedFont")
        self.Entry5.configure(selectbackground="blue")
        self.Entry5.configure(selectforeground="white")

        self.Entry6 = tk.Entry(self.Labelframe3)
        self.Entry6.place(relx=0.721, rely=0.367, height=23, relwidth=0.144
                , bordermode='ignore')
        self.Entry6.configure(background="white")
        self.Entry6.configure(font="TkFixedFont")
        self.Entry6.configure(selectbackground="blue")
        self.Entry6.configure(selectforeground="white")

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.05, rely=0.911, height=33, width=73)
        self.Button1.configure(activebackground="#f9f9f9")
        self.Button1.configure(borderwidth="2")
        self.Button1.configure(text='''Back''')

        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.783, rely=0.911, height=33, width=73)
        self.Button2.configure(activebackground="#f9f9f9")
        self.Button2.configure(borderwidth="2")
        self.Button2.configure(text='''Run''')

# ======================================================
# Support code for Balloon Help (also called tooltips).
# Found the original code at:
# http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# Modified by Rozen to remove Tkinter import statements and to receive
# the font as an argument.
# ======================================================

from time import time, localtime, strftime

class ToolTip(tk.Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """
    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None,
                 delay=0.5, follow=True):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          tooltip_font: Font to be used
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master
        # Initalise the Toplevel
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)

        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        # The text of the ToolTip is displayed in a Message widget
        tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                font=tooltip_font,
                aspect=1000).grid()

        # Add bindings to the widget.  This will NOT override
        # bindings that the widget already has
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in milliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        # If the follow flag is not set, motion within the
        # widget will make the ToolTip disappear
        #
        if self.follow is False:
            self.withdraw()
            self.visible = 1

        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
        try:
            # Try to call the message function.  Will not change
            # the message if the message function is None or
            # the message function fails
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()

    def update(self, msg):
        """
        Updates the Tooltip with a new message. Added by Rozen
        """
        self.msgVar.set(msg)

# ===========================================================
#                   End of Class ToolTip
# ===========================================================

if __name__ == '__main__':
    vp_start_gui()





