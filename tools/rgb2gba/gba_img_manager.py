from genericpath import isfile
import tkinter as tk
from tkinter import HORIZONTAL, VERTICAL, font, filedialog
import tkinter.ttk as ttk
import ttkthemes
from turtle import bgcolor, left
import os


def print_font_families(file_path : str):
    fonts = list()
    for f in font.families():
        fonts.append(str(f)+'\n')
    fonts_str = ''.join(fonts)
    with open(file_path, "w") as file:
        file.write(fonts_str)

def get_img_files_from_dir(path : str) -> list:
    # Recoge ficheros png (no directorios por ahora) con profundidad 0
    # TODO profundidad, solo imagenes, etc
    files = [f for f in os.listdir(path) if (os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1] == ".png")]
    return files


class MyListbox(tk.Listbox):
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master=master, **kw)


class FolderlistPane(tk.PanedWindow):
    def __init__(self, master, **kw):
        tk.PanedWindow.__init__(self, master, **kw)
        self.folders = list()
        self.folders_var = tk.StringVar(value=self.folders)
        self.folders_listbox = MyListbox(self, listvariable=self.folders_var,
                                    background="#252526", width=300, height=10, foreground="#ffffff")
        self.top_bar = tk.PanedWindow(self, background="#252526", width=20, height=20, orient=HORIZONTAL)
        self.add_folder_button = tk.Button(self, text="add folder", width=10, command=self.add_folder_to_list)
        self.top_bar.add(self.add_folder_button)
        
        self.add(self.top_bar)
        self.add(self.folders_listbox)
    
    def add_folder_to_list(self):
        folder = filedialog.askdirectory()
        self.folders.append(folder)
        self.folders_var.set(self.folders)


class ImagelistPane(tk.PanedWindow):
    def __init__(self, master, **kw):
        tk.PanedWindow.__init__(self, master, **kw)
        self.top_bar = tk.PanedWindow(self, background="#252526", width=20, height=20, orient=HORIZONTAL)
        self.add_folder_button = tk.Button(self, text="add folder")
        self.top_bar.add(self.add_folder_button)
        
        self.images = get_img_files_from_dir(os.curdir+"/input")
        self.images_var = tk.StringVar(value=self.images)
        self.image_listbox = MyListbox(self, listvariable=self.images_var,
                                    background="#252526", width=300, height=10, foreground="#ffffff")
        
        self.add(self.top_bar)
        self.add(self.image_listbox)

    def change_imagelist_folder(self, folder_path : str):
        self.images = get_img_files_from_dir(folder_path)
        self.images_var.set(self.images)
        
def folderlist_select_event(event, *args, **kwargs):
    print(event)
    print(args)
    print(kwargs['opt1'])
    img_pane : ImagelistPane = args[0]
    dir_pane : FolderlistPane = kwargs['opt1']
    selected_folder_idx = dir_pane.folders_listbox.curselection()[0]
    print(selected_folder_idx)
    print(dir_pane.folders_listbox.get(selected_folder_idx))
    selected_folder = dir_pane.folders_listbox.get(selected_folder_idx)
    print(selected_folder)
    img_pane.change_imagelist_folder(selected_folder)
    

class SidebarPane(tk.PanedWindow):
    def __init__(self, master, **kw):
        tk.PanedWindow.__init__(self, master, **kw)
        self.imagelist_pane = ImagelistPane(master, background='#252526', width=200, orient=VERTICAL)
        self.folderlist_pane = FolderlistPane(master, background='#252526', width=250, orient=VERTICAL)
        self.folderlist_pane.folders_listbox.bind('<<ListboxSelect>>', 
            lambda event, arg=self.imagelist_pane, kw=self.folderlist_pane : folderlist_select_event(event, arg, opt1=kw))
        #listbox.bind("<<ListboxSelect>>", callback)

        self.add(self.folderlist_pane)
        self.add(self.imagelist_pane)

class MainPane(tk.PanedWindow):
    def __init__(self, master, **kw):
        tk.PanedWindow.__init__(self, master, **kw)
        

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        min_width  = "600"
        min_height = "540"
        max_width = "1920"
        max_height = "1080"

        self.title("gba_img_manager")
        self.geometry('1800x900+60+10')
        self.resizable(True, True)
        self.minsize(min_width, min_height)
        self.maxsize(max_width, max_height)

        self.font_default = font.Font(family='Console mono', name='appHighlightFont', size=14, weight='normal')
        self.attributes('-alpha', 1)
        #self.attributes('-topmost', 1)

        # TODO remove height and width later when widgets added
        self.toolbar    = tk.Frame(self, background="#3c3c3c", height=35)
        self.statusbar  = tk.Frame(self, background="#007acc", height=30)
        self.main       = MainPane(self, background="#141415")
        self.sidebar    = SidebarPane(self.main, background="#252526", width=300, orient=VERTICAL)
        self.image_edit = tk.PanedWindow(self.main, background="#1e1e1e", width=800)

        self.toolbar.pack(side="top", fill="x", padx=0, pady=0)
        self.statusbar.pack(side="bottom", fill="x", padx=0, pady=0)
        self.main.pack(side="top", fill="both", expand=True)
        self.main.add(self.sidebar)
        self.main.add(self.image_edit)


'''    def create_frame(self, grid_pos) -> ttk.Frame:
        frame = ttk.Frame(self, name="presentacion", padding=10)
        frame.grid(column=grid_pos[0], row=grid_pos[1], columnspan=3, padx=5, pady=5)
        label_1 = ttk.Label(frame, text="Hello world!").grid(column=0, row=0)
        label_2 = ttk.Label(frame, text="My name is Chris").grid(column=0, row=1)
        #button_click_me = ttk.Button(frame, text="Click me", command=my_click(frame)).grid(column=2, row=2)
        button_quit = ttk.Button(frame, text="Quit", command=self.destroy).grid(column=3, row=3)
        return frame
    
    def create_theme_radiobutton_frame(self, grid_pos, theme_list=None) -> ttk.Frame:
        if theme_list is None:
            theme_list = ["black", "adapta", "clam"]

        theme_frame = ttk.LabelFrame(self, text="Themes")
        theme_frame.grid(column=grid_pos[0], row=grid_pos[1], rowspan=1, padx=5, pady=5, ipadx=5, ipady=0, sticky='nw')
        for theme_name in theme_list:
            rb = ttk.Radiobutton(
                theme_frame,
                text=theme_name,
                value=theme_name,
                padding=1,
                variable=self.selected_theme,
                command=self.change_theme)
            rb.pack(expand=True, fill="both")
        return theme_frame

    def create_calculator_frame(self, grid_pos) -> ttk.Frame:
        calc_frame = ttk.Frame(self, name="simple Calculator")
        calc_frame.grid(column=grid_pos[0], row=grid_pos[1], columnspan=5, rowspan=5, padx=10, pady=10)
        entry = ttk.Entry(calc_frame, width=35)
        #entry.grid(column=0, row=0, rowspan=5, columnspan=1, padx=10, pady=10, sticky="n")
        entry.pack(side=tk.LEFT)

        button_frame = ttk.LabelFrame(calc_frame, text="botones")
        #button_frame.grid(column=0, row=1, columnspan=5, rowspan=4, padx=10, pady=10)
        button_frame.pack(side=tk.BOTTOM)
        button_1 = ttk.Button(button_frame, text='1', padding=(10, 10), command=button_add)
        #button_1.grid(column=0, row=4, sticky="s")
        #button_1.pack(side=tk.LEFT, before=entry)
        
        """button_list = list()
        for i in range(10):
            button = ttk.Button(button_frame, text=str(i), padding=(10, 10), command=button_add)
            button_list.append(button)
        row = 0
        column = 0
        for button in button_frame.grid_slaves():
            button.grid(column=column, row=row)
            column += 1
            if column == 2:
                column = 0
                row += 1"""

    def change_theme(self):
        self.themed_style.set_theme(self.selected_theme.get())

def button_add():
    return

def create_note_frame(father, grid_pos : tuple):
    note_frame = ttk.LabelFrame(father, text="notes")
    note_frame.grid(column=grid_pos[0], row=grid_pos[1], columnspan=5, padx=5, pady=5, ipadx=5, ipady=0, sticky='nw')
    entry = ttk.Entry(note_frame)
    entry.grid(column=0, row=0)

    result_frame = ttk.LabelFrame(note_frame, text="notes", borderwidth=10)
    result_frame.grid(column=0, row=3, sticky="sw")

    button_click_me = ttk.Button(note_frame, text="Enter your click", 
                command= (lambda : ttk.Label(result_frame, text=entry.get()).pack(side="top"))).grid(column=0, row=1)



def my_click(father):
    label = ttk.Label(father, text="has introducido texto").grid(column=0, row=2)
'''

if __name__ == "__main__":
    root = Window()
    root.mainloop()