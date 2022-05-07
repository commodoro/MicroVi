from random import randint
import tkinter as tk
import tkinter.font as tkfont
from PIL import ImageTk, Image
import cv2
import os
from time import strftime
import model


class Fonts:
    def __init__(self, master) -> None:
        self.master = master
        self.title_font = tkfont.Font(
            self.master, size=18, weight='bold', family='Liberation Sans')
        self.count_font = tkfont.Font(
            self.master, size=28, family='Liberation Sans', weight='bold')
        self.txt1_font = tkfont.Font(
            self.master, size=18, family='Liberation Sans')
        self.txt2_font = tkfont.Font(
            self.master, size=11, family='Liberation Sans', weight='bold')
        self.txt3_font = tkfont.Font(
            self.master, size=16, family='Liberation Sans', weight='bold')
        self.txt4_font = tkfont.Font(
            self.master, size=14, family='Liberation Sans', weight='bold')
        self.txt5_font = tkfont.Font(
            self.master, size=14, family='Liberation Sans')
        self.info_font = tkfont.Font(
            self.master, size=12, family='Liberation Sans')
        self.emph_color = '#355269'


class App(tk.Frame, Fonts):
    def __init__(self, master: tk.Tk, modelh: model.ModelHandler):
        super().__init__(master)
        Fonts.__init__(self, master)
        self.master = master
        self.master.title('Taylor Swift fan app')

        self.master.bind("<F11>", lambda event: root.attributes("-fullscreen",
                                                                not root.attributes("-fullscreen")))
        master.attributes("-fullscreen", True)
        self.master.geometry("800x480+0+0")

        self.main_frame = tk.Frame(self.master, bd=4)
        self.main_frame.pack()
        self.main_frame.config(width=800, height=480)

        # Etiquetas y gráficos

        # Graficos
        self.canva = tk.Canvas(self.main_frame, width=800,
                               height=480, bd=0, highlightthickness=0)
        self.canva.pack(padx=0, pady=0)
        self.canva.create_line(470, 150, 785, 150, fill=self.emph_color)
        self.canva.create_line(470, 405, 785, 405, fill=self.emph_color)

        # Hora y fecha
        self.time = tk.StringVar(self.main_frame, '')
        self.time_lab = tk.Label(
            self.main_frame, textvariable=self.time, justify='right', anchor='e')
        self.time_lab.place(x=10, y=450)
        self.clock()

        # Modelo
        self.model_handler = modelh
        self.model_lab = tk.Label(
            self.main_frame, text='Modelo:', font=self.title_font, fg=self.emph_color)
        self.model_lab.place(x=470, y=10)

        self.modeltext = tk.StringVar(
            self.main_frame, self.model_handler['name'])
        self.selected_model_lab = tk.Label(self.main_frame, textvariable=self.modeltext, font=self.txt1_font,
                                           fg='#000000', highlightthickness=1, highlightbackground=self.emph_color,
                                           width=21, anchor='w', padx=5)
        self.selected_model_lab.place(x=470, y=52)

        # Conteo
        self.conteo_lab = tk.Label(
            self.main_frame, text='Cuenta:', font=self.title_font, fg=self.emph_color)
        self.conteo_lab.place(x=470, y=160)

        self.ntext = tk.StringVar(self.main_frame, '0')
        self.n_lab = tk.Label(self.main_frame, textvariable=self.ntext, font=self.txt5_font,
                              fg='#000000', highlightthickness=1, highlightbackground=self.emph_color,
                              width=9, pady=10, padx=8, anchor='e')
        self.n_lab.place(x=665, y=268)

        self.recuentotext = tk.StringVar(self.main_frame, '0')
        self.recuento_lab = tk.Label(self.main_frame, textvariable=self.recuentotext, font=self.count_font,
                                     fg='#000000', highlightthickness=1, highlightbackground=self.emph_color,
                                     width=14, anchor='e', padx=8, height=1, pady=12)
        self.recuento_lab.place(x=470, y=325)

        # Botones
        self.infomodel_b = tk.Button(self.main_frame, text="🛈", height=1,
                                     highlightbackground=self.emph_color, font=self.info_font, width=1, highlightthickness=2, command=self.info_model)
        self.infomodel_b.place(x=745, y=52)

        self.selmodel_b = tk.Button(self.main_frame, text="Cambiar", height=1, width=8,
                                    highlightbackground=self.emph_color, font=self.txt2_font, highlightthickness=2, fg=self.emph_color, command=self.modelb1)
        self.selmodel_b.place(x=470, y=105)

        self.lockmodel_b_txt = tk.StringVar(self.main_frame, 'Marcar')
        self.lockmodel_b = tk.Button(self.main_frame, textvariable=self.lockmodel_b_txt, height=1, width=8,
                                     highlightbackground=self.emph_color, font=self.txt2_font, highlightthickness=2, fg=self.emph_color, command=self.modelb2)
        self.lockmodel_b.place(x=580, y=105)
        self.lockmodel = False

        self.train_b = tk.Button(self.main_frame, text="Entrenar", height=1, width=8,
                                 highlightbackground=self.emph_color, font=self.txt2_font, highlightthickness=2, fg=self.emph_color, command=self.modelb3)
        self.train_b.place(x=690, y=105)
        self.train_b.configure(state='disable')
        #self.train_b.bind('<Button-1>', self.modelb3)

        self.count_b = tk.Button(self.main_frame, text="Contar", height=2, highlightbackground=self.emph_color,
                                 font=self.count_font, width=7, highlightthickness=2, fg=self.emph_color,
                                 padx=15, pady=10, command=self.countb1)
        self.count_b.place(x=470, y=200)

        self.autocount_b = tk.Button(self.main_frame, text="Auto", height=2, highlightbackground=self.emph_color,
                                     font=self.txt4_font, width=8, highlightthickness=2, fg=self.emph_color, command=self.countb2)
        self.autocount_b.place(x=665, y=200)

        self.bri_b = tk.Button(self.main_frame, text="Brillo", height=1, width=8,
                               highlightbackground=self.emph_color, font=self.txt2_font, highlightthickness=2, fg=self.emph_color, command=self.optb1)
        self.bri_b.place(x=470, y=415)

        self.opt_b = tk.Button(self.main_frame, text="Opciones", height=1, width=8,
                               highlightbackground=self.emph_color, font=self.txt2_font, highlightthickness=2, fg=self.emph_color, command=self.optb2)
        self.opt_b.place(x=580, y=415)

        self.reset_b = tk.Button(self.main_frame, text="Reset", height=1, width=8,
                                 highlightbackground=self.emph_color, font=self.txt2_font, highlightthickness=2, fg=self.emph_color, command=self.optb3)
        self.reset_b.place(x=690, y=415)

        # Captura continua
        self.vs = cv2.VideoCapture(0)
        self.panel = tk.Label(self.main_frame)
        self.panel.place(x=10, y=10)
        self.capture()

    def capture(self):
        ok, frame = self.vs.read()
        if ok:
            self.cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            self.current_image = Image.fromarray(self.cv2image)
            self.current_image = self.current_image.crop((0, 0, 440, 440))
            self.imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.config(image=self.imgtk)
        # call the same function after 30 milliseconds
        self.main_frame.after(30, self.capture)

    def clock(self):
        self.time.set(strftime("%H:%M:%S, %d/%m/%Y"))
        self.main_frame.after(1000, self.clock)

    def info_model(self, event=None):
        print('Info about model')
        self.disable_frame()
        self.options_windows = tk.Toplevel(self.master)
        self.options_windows.geometry("800x480+0+0")
        self.options_windows.attributes("-fullscreen", True)
        self.options_windows.bind('<Destroy>', self.enable_frame)
        self.secondary_frame = InfoPanel(
            self.options_windows, self.model_handler)

    def modelb1(self, event=None):
        print('Select model')
        self.model_handler.next_model()
        self.modeltext.set(self.model_handler['name'])
        if not self.lockmodel:
            self.lockmodel = True
            self.lockmodel_b_txt.set('Desmarcar')
            self.train_b.configure(state='normal')
            self.selected_model_lab.config(fg=self.emph_color)

    def modelb2(self, event=None):
        print('Lock model')
        if self.lockmodel:
            self.lockmodel = False
            self.lockmodel_b_txt.set('Marcar')
            self.train_b.configure(state='disable')
            self.selected_model_lab.config(fg='#000000')
        else:
            self.lockmodel = True
            self.lockmodel_b_txt.set('Desmarcar')
            self.train_b.configure(state='normal')
            self.selected_model_lab.config(fg=self.emph_color)

    def modelb3(self):
        print('Train model')
        # model.train_model()

    def countb1(self, event=None):
        print('Count', self.ntext.get())
        self.ntext.set(int(self.ntext.get())+1)
        self.recuentotext.set(randint(50, 10000))

    def countb2(self, event=None):
        print('Auto mode')

    def optb1(self, event=None):
        print('Brightness control')

    def optb2(self, event=None):
        print('Options')
        self.menu_options()

    def optb3(self, event=None):
        print('Reset')
        self.ntext.set(0)
        self.recuentotext.set(0)

    def disable_frame(self):
        for child in self.main_frame.winfo_children():
            child.configure(state='disable')

    def enable_frame(self, event=None):
        for child in self.main_frame.winfo_children():
            child.configure(state='normal')

    def menu_options(self):
        self.disable_frame()
        self.options_windows = tk.Toplevel(self.master)
        self.options_windows.geometry("800x480+0+0")
        self.options_windows.attributes("-fullscreen", True)
        self.options_windows.bind('<Destroy>', self.enable_frame)
        self.secondary_frame = MenuOptions(self.options_windows)


class InfoPanel(tk.Frame, Fonts):
    def __init__(self, master, model_h):
        super().__init__(master)
        Fonts.__init__(self, master)
        self.master = master
        self.master.bind("<F11>", lambda event: self.master.attributes("-fullscreen",
                                                                       not self.master.attributes("-fullscreen")))
        self.pack()
        self.config(width=800, height=480)

        self.exit_options_b = tk.Button(self, text="X", height=1, width=1,
                                        highlightbackground=self.emph_color, font=self.txt2_font,
                                        highlightthickness=2, fg=self.emph_color, command=self.master.destroy)
        self.exit_options_b.place(x=10, y=10)

        self.model_handler = model_h

        self.txtModel = tk.StringVar(self, self.model_handler['name'])
        self.model_name = tk.Label(self, textvariable=self.txtModel, font=self.txt1_font,
                                fg='#000000', highlightthickness=1, highlightbackground=self.emph_color,
                                width=50, anchor='w', padx=5)
        self.model_name.place(x=60, y=10)

        self.txtinfo = tk.StringVar(self, self.model_handler['info'] + f'\n\nVer: {self.model_handler["version"]}\nAlgorithm: {self.model_handler["alg_path"]}')
        if model_h['img'] == '':
            self.info = tk.Message(self, textvariable=self.txtinfo, font=self.txt5_font,
                                fg=self.emph_color, anchor='w', width=770)
            self.info.place(x=0, y=50)
        else:
            with Image.open(model_h['img']) as im:
                self.img = ImageTk.PhotoImage(image=im.crop((0, 0, 400, 400)))
            self.panel = tk.Label(self, image=self.img)
            self.panel.place(x=10, y=50)
            self.info = tk.Message(self, textvariable=self.txtinfo, font=self.txt5_font,
                                fg=self.emph_color, anchor='w', width=325)
            self.info.place(x=415, y=50)

        self.master.bind("<F12>", lambda event: self.info.place(x=50, y=50))


class MenuOptions(tk.Frame, Fonts):
    def __init__(self, master):
        super().__init__(master)
        Fonts.__init__(self, master)
        self.master = master

        self.pack()
        self.config(width=800, height=480)

        self.exit_options_b = tk.Button(self, text="X", height=1, width=1,
                                        highlightbackground=self.emph_color, font=self.txt2_font,
                                        highlightthickness=2, fg=self.emph_color, command=self.master.destroy)
        self.exit_options_b.place(x=10, y=10)

        # etc.


app_path = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(
    file=app_path+'/petri_icon.png'))

mh = model.ModelHandler('models.yaml')

app = App(root, mh)
app.mainloop()
