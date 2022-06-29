from genericpath import isfile
import tkinter as tk
from tkinter import HORIZONTAL, LEFT, VERTICAL, Y, font, filedialog, messagebox

import tkinter.ttk as ttk
from pygments import highlight
import ttkthemes
from PIL import ImageTk, Image
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

class ImageEditPane(tk.PanedWindow):
    class ImageView(tk.PanedWindow):
        def __init__(self, master, **kw):
            tk.PanedWindow.__init__(self, master, kw)
            #self.pack(expand=False)
            self.image = ImageTk.PhotoImage(Image.open('input/pueblecito_1.png'))
            self.label = tk.Label(self, width=100, height=100)
            self.label['image'] = self.image
            self.add(self.label)
            self.label.pack(side='top')

            self.label2 = tk.Label(self, borderwidth=50, width=50, height=50)
            self.label2['image'] = self.image
            self.add(self.label2)
            self.label2.pack(side='top')
        def change_image(self, image : str):
            self.image = self.image = ImageTk.PhotoImage(Image.open(image))
            self.label['image'] = self.image
            self.add(self.label)

    def __init__(self, master, **kw):
        tk.PanedWindow.__init__(self, master, kw)
        self.image_pane = self.ImageView(self, background="#112211", width=300, height=300, orient=VERTICAL)
        self.add(self.image_pane)
        self.image_pane.pack(expand=False, side=LEFT, fill=Y)
        #self.pack_propagate(False)

        self.image_pane_2 = self.ImageView(self, background="#330000", width=300, height=300, orient=VERTICAL)
        self.add(self.image_pane_2)
        self.image_pane_2.pack(expand=False, side=LEFT, fill=Y)

    def change_image(self, image : str):
        self.image_pane.change_image(image)

class FolderlistPane(tk.PanedWindow):
    def __init__(self, master, **kw):
        tk.PanedWindow.__init__(self, master, **kw)
        self.folders = list()
        self.folders_var = tk.StringVar(value=self.folders)
        self.folders_listbox = MyListbox(self, listvariable=self.folders_var,
                                    background="#252526", width=300, height=10,
                                    foreground="#ffffff", exportselection=False)
        self.top_bar = tk.PanedWindow(self, background="#252526", width=20, height=20, orient=HORIZONTAL)
        self.add_folder_button_img = ImageTk.PhotoImage(Image.open('images/add_folder_button.png'))
        self.add_folder_button = tk.Button(
                    self.top_bar,
                    command=self.add_folder_ask,
                    image = self.add_folder_button_img,
                    background="#252526",
                    border=0,
                    cursor='hand2')
        self.top_bar.add(self.add_folder_button)
        self.add_folder_button.pack(side='right')
        
        self.add(self.top_bar)
        self.add(self.folders_listbox)
    
    def add_folder(self, folder):
        self.folders.append(folder)
        self.folders_var.set(self.folders)

    def add_folder_ask(self):
        folder = filedialog.askdirectory()
        self.add_folder(folder)

    def bind_select_event(self, sequence : str, func):
        self.folders_listbox.bind(sequence, func)

def folderlist_select_event(event, *args, **kwargs):
    '''Callback function used when <<ListboxSelect>> event is triggered on folderlistPane.'''
    img_pane : ImagelistPane = args[0]
    dir_pane : FolderlistPane = kwargs['opt1']
    print('args', args)
    print('kwargs', kwargs)
    # TODO posible error aqui
    selected_folder_idx = dir_pane.folders_listbox.curselection()[0]
    print('selected_folder_idx', selected_folder_idx)
    selected_folder = dir_pane.folders_listbox.get(str(selected_folder_idx))

    img_pane.change_imagelist_folder(selected_folder)

def imagelist_select_event(event, *args, **kwargs):
    '''Callback function used when <<ListboxSelect>> event is triggered on imagelist.'''
    imagelist_pane : ImagelistPane = args[0]
    image_edit_pane : ImageEditPane = kwargs['opt1']
    selected_image_idx = imagelist_pane.image_listbox.curselection()[0]
    selected_image = imagelist_pane.image_listbox.get(str(selected_image_idx))
    folder_path = imagelist_pane.folder_path
    print(folder_path+'/'+selected_image)
    image_edit_pane.change_image(folder_path+'/'+selected_image)

class ImagelistPane(tk.PanedWindow):
    def __init__(self, master, **kw):
        tk.PanedWindow.__init__(self, master, **kw)
        self.folder_path = None
        self.images = list()
        self.images_var = tk.StringVar(value=self.images)
        self.image_listbox = MyListbox(self, listvariable=self.images_var,
                                    background="#252526", width=300, height=10, foreground="#ffffff",
                                    highlightbackground="#252526", exportselection=False)
        self.add(self.image_listbox)

    def change_imagelist_folder(self, folder_path : str):
        self.folder_path = folder_path
        self.images = get_img_files_from_dir(self.folder_path)
        self.images_var.set(self.images)
    def bind_select_image_event(self, image_edit_pane:ImageEditPane):
        self.image_listbox.bind(
            '<<ListboxSelect>>',
            lambda event, arg=self, kw=image_edit_pane : imagelist_select_event(event, arg, opt1=kw)
        )

class SidebarPane(tk.PanedWindow):
    def __init__(self, master, **kw):
        tk.PanedWindow.__init__(self, master, **kw)
        self.imagelist_pane = ImagelistPane(master, background='#252526', width=200, orient=VERTICAL)
        self.folderlist_pane = FolderlistPane(master, background='#252526', width=250, orient=VERTICAL)
        self.folderlist_pane.bind_select_event('<<ListboxSelect>>', 
            lambda event, arg=self.imagelist_pane, kw=self.folderlist_pane : folderlist_select_event(event, arg, opt1=kw))

        self.add(self.folderlist_pane)
        self.add(self.imagelist_pane)

    def add_folder(self, folder):
        self.folderlist_pane.add_folder(folder)

    def bind_select_image_event(self, image_edit_pane:ImageEditPane):
        self.imagelist_pane.bind_select_image_event(image_edit_pane)

class MainPane(tk.PanedWindow):
    def __init__(self, master, **kw):
        tk.PanedWindow.__init__(self, master, **kw)
        self.sidebar    = SidebarPane(master, background="#252526", width=300, orient=VERTICAL)
        self.image_edit = ImageEditPane(master, background="#252526", width=800, orient=HORIZONTAL)
        self.sidebar.bind_select_image_event(self.image_edit)
        self.add(self.sidebar)
        self.add(self.image_edit)

    def bind_select_image_event(self, image_edit_pane:ImageEditPane):
        self.sidebar.bind_select_image_event(image_edit_pane)
        

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("gba_img_manager")
        self.geometry('1800x900+60+10')
        self.resizable(True, True)
        self.set_window_min_max_size('600', '540', '1920', '1080')

        self.font_default = font.Font(family='Console mono', name='appHighlightFont', size=14, weight='normal')
        self.attributes('-alpha', 1)

        # TODO remove height and width later when widgets added
        self.toolbar    = tk.Frame(self, background="#3c3c3c", height=35)
        self.statusbar  = tk.Frame(self, background="#007acc", height=30)
        self.main       = MainPane(self, background="#141415")

        self.toolbar.pack(side="top", fill="x", padx=0, pady=0)
        self.statusbar.pack(side="bottom", fill="x", padx=0, pady=0)
        self.main.pack(side="top", fill="both", expand=True)
    
        self.ask_initial_folder()

    def set_window_min_max_size(self, min_width, min_height, max_width, max_height):
        self.min_width  = min_width
        self.min_height = min_height
        self.max_width  = max_width
        self.max_height = max_height
        self.minsize(min_width, min_height)
        self.maxsize(max_width, max_height)

    def ask_folder(self, title) -> str:
        #messagebox.showinfo(message='Please select an initial folder')
        folder = filedialog.askdirectory(title=title)
        return folder

    def ask_initial_folder(self):
        initial_folder = self.ask_folder('Choose a folder')
        if initial_folder:
            self.main.sidebar.add_folder(initial_folder)

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