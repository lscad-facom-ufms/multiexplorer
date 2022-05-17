import Tkinter as Tk

def set_Tk_var():
    global combobox
    combobox = Tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import MultiExplorer
    MultiExplorer.Tela_inicial_gui()
