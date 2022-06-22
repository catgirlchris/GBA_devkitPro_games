import tkinter as tk
import tkinter.ttk as ttk
import ttkthemes
from turtle import bgcolor, left

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.themed_style = ttkthemes.ThemedStyle(self)
        self.selected_theme = tk.StringVar()

        themed_styles_list = self.themed_style.theme_names()

        min_width  = "600"
        min_height = "540"
        max_width = "1920"
        max_height = "1080"

        self.title("gba_img_manager")
        self.geometry('1800x900+30+10')
        self.resizable(True, True)
        self.minsize(min_width, min_height)
        self.maxsize(max_width, max_height)

        self.themed_style.set_theme("black")
        self.attributes('-alpha', 1)
        self.attributes('-topmost', 1)

        # TODO remove height and width later when widgets added
        self.toolbar = tk.Frame(self, background="#d5e8d4", height=80)
        self.statusbar = tk.Frame(self, background="#e3e3e3", height=40)
        self.main = tk.PanedWindow(self, background="#99fb99")
        self.left_pane = tk.Frame(self.main, background="#99ceff", width=400)
        self.right_pane = tk.PanedWindow(self.main, background="#99fb99", width=800)

        self.toolbar.pack(side="top", fill="x")
        self.statusbar.pack(side="bottom", fill="x")
        self.main.pack(side="top", fill="both", expand=True)
        self.main.add(self.left_pane)
        self.main.add(self.right_pane)

    def create_frame(self, grid_pos) -> ttk.Frame:
        frame = ttk.Frame(self, name="presentacion", padding=10)
        frame.grid(column=grid_pos[0], row=grid_pos[1], columnspan=3, padx=5, pady=5)
        label_1 = ttk.Label(frame, text="Hello world!").grid(column=0, row=0)
        label_2 = ttk.Label(frame, text="My name is Chris").grid(column=0, row=1)
        #button_click_me = ttk.Button(frame, text="Click me", command=my_click(frame)).grid(column=2, row=2)
        button_quit = ttk.Button(frame, text="Quit", command=self.destroy).grid(column=3, row=3)
        return frame
    
    def create_theme_radiobutton_frame(self, grid_pos, theme_list=None) -> ttk.Frame:
        if theme_list is None:
            theme_list = ['black', 'adapta', 'clam']

        theme_frame = ttk.LabelFrame(self, text='Themes')
        theme_frame.grid(column=grid_pos[0], row=grid_pos[1], rowspan=1, padx=5, pady=5, ipadx=5, ipady=0, sticky='nw')
        for theme_name in theme_list:
            rb = ttk.Radiobutton(
                theme_frame,
                text=theme_name,
                value=theme_name,
                padding=1,
                variable=self.selected_theme,
                command=self.change_theme)
            rb.pack(expand=True, fill='both')
        return theme_frame

    def create_calculator_frame(self, grid_pos) -> ttk.Frame:
        calc_frame = ttk.Frame(self, name='simple Calculator')
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
        
        '''button_list = list()
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
                row += 1'''

    def change_theme(self):
        self.themed_style.set_theme(self.selected_theme.get())

def button_add():
    return

def create_note_frame(father, grid_pos : tuple):
    note_frame = ttk.LabelFrame(father, text='notes')
    note_frame.grid(column=grid_pos[0], row=grid_pos[1], columnspan=5, padx=5, pady=5, ipadx=5, ipady=0, sticky='nw')
    entry = ttk.Entry(note_frame)
    entry.grid(column=0, row=0)

    result_frame = ttk.LabelFrame(note_frame, text="notes", borderwidth=10)
    result_frame.grid(column=0, row=3, sticky='sw')

    button_click_me = ttk.Button(note_frame, text="Enter your click", 
                command= (lambda : ttk.Label(result_frame, text=entry.get()).pack(side='top'))).grid(column=0, row=1)



def my_click(father):
    label = ttk.Label(father, text="has introducido texto").grid(column=0, row=2)


if __name__ == "__main__":
    root = Window()
    root.mainloop()