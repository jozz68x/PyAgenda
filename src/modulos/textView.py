# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Jose Diaz"
__date__ = "$11/04/2015 12:28:54 PM$"


from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk


class TextView(object):
    
    text = None
    
    FUENTES = list()
    LETRA_TAM = (8,9,10,11,12, 14,16,18,20,22,24,26,28,36,48,72)
    
    BACKGROUND = "#C8C8C8"
    BACKGROUND_MENU = "#555D69"
    BACKGROUND_MENU_2 = "#343940"
    BACKGROUND_MENU_INTO = "#99A2AE"
    ACTIVE_BACKGROUND = "#4CAF50"
    ACTIVE_BACKGROUND_2 = "#B0B6B6"
    SELECT_BACKGROUND = '#00878b'
    BACKGROUND_BUTTON = "#f0f0f0"
    FOREGROUND = "#B0BEC5"
    FOREGROUND_2 = "#37474F"
    FONT = ("Arial", 10)
    
    MENUBUTTON_BOTTOM = dict(width=65, relief=FLAT, bd=1, font=FONT, fg=FOREGROUND_2,
                    activebackground=ACTIVE_BACKGROUND_2,activeforeground=FOREGROUND_2)
    
    def __init__(self, master):
        self.LISTA_NOTAS = []
        self.contador_notas_agregados_recientemente = 0
        
        self.master = master
        self.frame = Frame(self.master, highlightbackground='DARK GRAY', highlightcolor='DARK GRAY', highlightthickness=1)
        self.frame.pack(fill=BOTH, expand=True)
        TextView.text = None
        
        self.customFont = tkFont.Font(family="Helvetica", size=10, weight='normal', slant='roman', underline=0, overstrike=0)
        
        self.cargar_imagenes()

        self.crear_toolbar()
        self.crear_text_area()
        
        
    def cargar_imagenes(self):
        self.imagenIconContacto = ImageTk.PhotoImage(Image.open(r"image\Icon_nota.png"))
        
        self.iconEditar = ImageTk.PhotoImage(Image.open(r"image\icons_show\editar.png"))
        self.iconRefrescar = ImageTk.PhotoImage(Image.open(r"image\icons_show\refrescar.png"))
        self.iconAgregar = ImageTk.PhotoImage(Image.open(r"image\icons_show\agregar.png"))
        self.iconRenombrar = ImageTk.PhotoImage(Image.open(r"image\icons_show\renombrar.png"))
        self.iconEliminar = ImageTk.PhotoImage(Image.open(r"image\icons_show\eliminar.png"))
        self.iconDeshacer = ImageTk.PhotoImage(Image.open(r"image\icons_show\deshacer.png"))
        self.iconRehacer = ImageTk.PhotoImage(Image.open(r"image\icons_show\rehacer.png"))
        self.iconCopiar = ImageTk.PhotoImage(Image.open(r"image\icons_show\copiar.png"))
        self.iconCortar = ImageTk.PhotoImage(Image.open(r"image\icons_show\cortar.png"))
        self.iconPegar = ImageTk.PhotoImage(Image.open(r"image\icons_show\pegar.png"))
        
        self.iconBold = ImageTk.PhotoImage(Image.open(r"image\icons_show\bold.png"))
        self.iconItalic = ImageTk.PhotoImage(Image.open(r"image\icons_show\italic.png"))
        self.iconUnderline = ImageTk.PhotoImage(Image.open(r"image\icons_show\underline.png"))
        self.iconOverstrike = ImageTk.PhotoImage(Image.open(r"image\icons_show\overstrike.png"))
        self.iconTextLeft = ImageTk.PhotoImage(Image.open(r"image\icons_show\left.png"))
        self.iconTextRight = ImageTk.PhotoImage(Image.open(r"image\icons_show\right.png"))
        self.iconTextCenter = ImageTk.PhotoImage(Image.open(r"image\icons_show\center.png"))
        self.iconLimpiar = ImageTk.PhotoImage(Image.open(r"image\icons_show\limpiar.png"))
        self.iconAtras = ImageTk.PhotoImage(Image.open(r"image\icons_show\atras.png"))
        self.iconAdelante = ImageTk.PhotoImage(Image.open(r"image\icons_show\adelante.png"))
        self.iconTextFg = ImageTk.PhotoImage(Image.open(r"image\icons_show\fg.png"))
        self.iconTextBg = ImageTk.PhotoImage(Image.open(r"image\icons_show\bg.png"))
        self.iconTextBgSelect = ImageTk.PhotoImage(Image.open(r"image\icons_show\bg_select.png"))
        
    
    def crear_toolbar(self):
        """Crea la barra de herramientas."""
        frame_toolbar = Frame(self.frame)
        
        self.cargar_fonts()
        
        toolbar_tarea = Frame(frame_toolbar)
        toolbar_tarea.pack(fill=BOTH, expand=True, padx=8)
        
        ttk.Combobox(toolbar_tarea, values=self.FUENTES, width=20).pack(side=LEFT, padx=2)
        
        ttk.Combobox(toolbar_tarea, values=self.LETRA_TAM, width=5).pack(side=LEFT)
        
        Frame(toolbar_tarea, bg="DARK GRAY", height=1).pack(side=LEFT, fill=Y, padx=5, pady=2)
        Button(toolbar_tarea, font=("Microsoft YaHei UI", 10, "bold"), relief=FLAT, bd=0, image=self.iconBold, command=self.bold,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        Button(toolbar_tarea, font=("Microsoft YaHei UI", 10, "italic"), relief=FLAT, bd=0, image=self.iconItalic, command=self.italic,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        Button(toolbar_tarea, font=("Microsoft YaHei UI", 10, "underline"), relief=FLAT, bd=0, image=self.iconUnderline, command=self.underline,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        Button(toolbar_tarea, font=("Microsoft YaHei UI", 10, "overstrike"), relief=FLAT, bd=0, image=self.iconOverstrike, command=self.overstrike,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        
        Frame(toolbar_tarea, bg="DARK GRAY", height=1).pack(side=LEFT, fill=Y, padx=5, pady=2)
        Button(toolbar_tarea, relief=FLAT, bd=0, image=self.iconTextLeft, command=self.left,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        Button(toolbar_tarea, relief=FLAT, bd=0, image=self.iconTextCenter, command=self.center,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        Button(toolbar_tarea, relief=FLAT, bd=0, image=self.iconTextRight, command=self.right,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        
        Frame(toolbar_tarea, bg="DARK GRAY", height=1).pack(side=LEFT, fill=Y, padx=5, pady=2)
        Button(toolbar_tarea, relief=FLAT, bd=0, image=self.iconLimpiar, command=self.limpiar,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
                  
        Frame(toolbar_tarea, bg="DARK GRAY", height=1).pack(side=LEFT, fill=Y, padx=5, pady=2)
        Button(toolbar_tarea, relief=FLAT, bd=0, image=self.iconAtras, command=lambda: TextView.text.event_generate("<<Undo>>"),
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        Button(toolbar_tarea, relief=FLAT, bd=0, image=self.iconAdelante, command=lambda: TextView.text.event_generate("<<Redo>>"),
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
                  
        Frame(toolbar_tarea, bg="DARK GRAY", height=1).pack(side=LEFT, fill=Y, padx=5, pady=2)
        Button(toolbar_tarea, relief=FLAT, bd=0, image=self.iconTextFg, command=self.color_foreground,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        Button(toolbar_tarea, relief=FLAT, bd=0, image=self.iconTextBgSelect, command=self.color_resaltado,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        Button(toolbar_tarea, relief=FLAT, bd=0, image=self.iconTextBg, command=self.color_background,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
                  
        Frame(toolbar_tarea, bg="DARK GRAY", height=1).pack(side=LEFT, fill=Y, padx=5, pady=2)
        Button(toolbar_tarea, relief=FLAT, bd=0, text="Image", command=self.insertar_image,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        Button(toolbar_tarea, relief=FLAT, bd=0, text="Separator", command=self.insertar_separador,
                  activebackground="#4CAF50", activeforeground="#FFFFFF").pack(side=LEFT)
        
        
        frame_toolbar.pack(side=TOP, fill=X)
    
        
    
    def crear_text_area(self):
        """ Crea el area de texto para el widget. """
        frame_text_area = Frame(self.frame)
        
        self.crear_menu_anticlick(frame_text_area)
        TextView.text = Text(frame_text_area, relief=FLAT, bd=0, cursor='arrow', state='normal', font=('Verdana', 10), selectbackground=self.SELECT_BACKGROUND, autoseparators=5, spacing1=5, wrap=WORD, undo=True) #Nota el parametro wrap=WORD separara una en palabras al ampliar el widget
        scroller = ttk.Scrollbar(frame_text_area, command=TextView.text.yview)
        TextView.text.config(yscrollcommand=scroller.set)
        scroller.pack(side=RIGHT, fill=Y)
        TextView.text.pack(fill=BOTH, expand=True)
        
        TextView.text.bind("<ButtonRelease-3>", self.ver_menu_anticlick)
        
        frame_text_area.pack(fill=BOTH, expand=True)
    

        
    """---------------------------------------------------------------"""
    def crear_opciones_anticlick_listbox(self, widget):
        """"Menu de Opciones Anticlick en ListBox"""
        global menu_anticlik_listbox
        menu_anticlik_listbox = Menu(widget, tearoff=0, font=self.FONT, activebackground=self.ACTIVE_BACKGROUND, activeforeground = "#FFFFFF")
        menu_anticlik_listbox.add_command(label = "Editar", command=self.mostrar_todos_datos, image=self.iconEditar, compound=LEFT)
        menu_anticlik_listbox.add_separator()
        menu_anticlik_listbox.add_command(label = "Agregar nueva nota", command=self.btn_nueva_nota, image=self.iconAgregar, compound=LEFT)
        menu_anticlik_listbox.add_separator()
        menu_anticlik_listbox.add_command(label = "Renombrar", image=self.iconRenombrar, compound=LEFT)
        menu_anticlik_listbox.add_command(label = "Eliminar", command=self.eliminar_nota, image=self.iconEliminar, compound=LEFT)
        menu_anticlik_listbox.add_separator()
        menu_anticlik_listbox.add_command(label = "Refrescar", command=self.listar_listbox, image=self.iconRefrescar, compound=LEFT)
        
    def ver_opciones_anticlick_listbox(self, evento):
        menu_anticlik_listbox.tk.call("tk_popup", menu_anticlik_listbox, evento.x_root, evento.y_root)
    
    
    def crear_menu_anticlick(self, widget):
        """Crea un menu para anticlick en los campos de entrada de texto."""
        global menu_anticlick_text
        menu_anticlick_text = Menu(widget, tearoff=0)
        menu_anticlick_text.add_command(label="Deshacer", accelerator='Ctr+Z', image=self.iconDeshacer, compound=LEFT)
        menu_anticlick_text.add_command(label="Rehacer", accelerator='Ctr+Y', image=self.iconRehacer, compound=LEFT)
        menu_anticlick_text.add_separator()
        menu_anticlick_text.add_command(label="Copiar", accelerator='Ctrl+C', image=self.iconCopiar, compound=LEFT)
        menu_anticlick_text.add_command(label="Cortar", accelerator='Ctrl+X', image=self.iconCortar, compound=LEFT)
        menu_anticlick_text.add_command(label="Pegar", accelerator='Ctrl+V', image=self.iconPegar, compound=LEFT)
        menu_anticlick_text.add_separator()
        menu_anticlick_text.add_command(label="Suprimir")
        menu_anticlick_text.add_separator()
        menu_anticlick_text.add_command(label="Inicio de linea")
        menu_anticlick_text.add_command(label="Final de linea")
        menu_anticlick_text.add_separator()
        menu_anticlick_text.add_command(label="Seleccionar todo", accelerator='Ctrl+A')
        
    def ver_menu_anticlick(self, e):
        """Genera los eventos basicos para las opciones del menu anticlick."""
        w = e.widget
        menu_anticlick_text.entryconfigure("Deshacer", command=lambda: w.event_generate("<<Undo>>"))
        menu_anticlick_text.entryconfigure("Rehacer", command=lambda: w.event_generate("<<Redo>>"))
        menu_anticlick_text.entryconfigure("Copiar", command=lambda: w.event_generate("<<Copy>>"))
        menu_anticlick_text.entryconfigure("Cortar", command=lambda: w.event_generate("<<Cut>>"))
        menu_anticlick_text.entryconfigure("Pegar", command=lambda: w.event_generate("<<Paste>>"))
        menu_anticlick_text.entryconfigure("Suprimir", command=lambda: w.event_generate("<<Clear>>"))
        menu_anticlick_text.entryconfigure("Inicio de linea", command=lambda: w.event_generate("<<LineStart>>"))
        menu_anticlick_text.entryconfigure("Final de linea", command=lambda: w.event_generate("<<LineEnd>>"))
        menu_anticlick_text.entryconfigure("Seleccionar todo", command=lambda: w.event_generate("<<SelectAll>>"))
        menu_anticlick_text.tk.call("tk_popup", menu_anticlick_text, e.x_root, e.y_root)
            
    
    """-------------------------------------------------"""
    """                     Toolbar Text                """
    """-------------------------------------------------"""
    def cargar_fonts(self):
        """Carga los formatos de letras."""
        fonts = list(tkFont.families(self.master))
        fonts.sort()
        for font in fonts:
            self.FUENTES.append(font)
            
    def bold(self):
        """Negrita al texto seleccionado."""
        TextView.text.tag_add("bold", SEL_FIRST, SEL_LAST)
        TextView.text.tag_config("bold", font="-weight bold")
        
    def italic(self):
        """Italics texto seleccionado."""
        TextView.text.tag_add("italic", SEL_FIRST, SEL_LAST)
        TextView.text.tag_config("italic", font="-slant italic")
        
    def underline(self):
        """Negrita al texto seleccionado."""
        TextView.text.tag_add("underline", SEL_FIRST, SEL_LAST)
        TextView.text.tag_config("underline", font="-underline 1")
        
    def overstrike(self):
        """Italics texto seleccionado."""
        TextView.text.tag_add("overstrike", SEL_FIRST, SEL_LAST)
        TextView.text.tag_config("overstrike", font="-overstrike 1")
        
    def left(self):
        """A la izquierda texto."""
        TextView.text.tag_remove('center', '1.0', END)
        TextView.text.tag_remove('right', '1.0', END)
        
        TextView.text.tag_add("left", 1.0, END)
        TextView.text.tag_config("left", justify='left')
        
    def center(self):
        """Centrado texto."""
        TextView.text.tag_remove('left', '1.0', END)
        TextView.text.tag_remove('right', '1.0', END)
        
        TextView.text.tag_add("center", 1.0, END)
        TextView.text.tag_config("center", justify='center')
    
    def right(self):
        """A la derecha texto."""
        TextView.text.tag_remove('left', '1.0', END)
        TextView.text.tag_remove('center', '1.0', END)
        
        TextView.text.tag_add("right", 1.0, END)
        TextView.text.tag_config("right", justify='right')
    
    def limpiar(self):
        """Limpia widget Text."""
        TextView.text.delete(0.0,  END)
        
    def color_foreground(self):
        color = colorchooser.askcolor(parent=self.master)
        
        if color!=None:
            TextView.text.tag_add("foreground", SEL_FIRST, SEL_LAST)
            TextView.text.tag_config("foreground", foreground=color[1])
        else:
            pass
        
    def color_resaltado(self):
        color = colorchooser.askcolor(parent=self.master)
        
        if color!=None:
            TextView.text.tag_add("background", SEL_FIRST, SEL_LAST)
            TextView.text.tag_config("background", background=color[1])
        else:
            pass
    
    def color_background(self):
        color = colorchooser.askcolor(parent=self.master)
        
        if color!=None:
            TextView.text.config(background=color[1])
        else:
            pass
    
    def insertar_image(self):
        """Inserta imagenes."""
        file_img = filedialog.askopenfile(parent=self.master, mode='rb', title='Abrir',
                                        filetypes=[("all files","*"),("Bitmap Files","*.bmp; *.dib"), 
                                        ("JPEG", "*.jpg; *.jpe; *.jpeg; *.jfif"),
                                        ("PNG", "*.png"), ("TIFF", "*.tiff; *.tif")])
        
        if file_img:
            image = Image.open(file_img)
            self.imagen = ImageTk.PhotoImage(image)
            TextView.text.image_create(END, image=self.imagen, padx=10, pady=10)
        else:
            pass
            
    def insertar_separador(self):
        """Inserta separador."""
        separador = Frame(TextView.text, bg="#4c545e", height=2, width=900).pack(padx=10, pady=10)
        TextView.text.window_create(INSERT, window=separador)
        
        
    
    def btn_salir_notas(self):
        self.panel.destroy()
        

'''
def main():
    root = Tk()
    TextView(root)
    root.mainloop()

main()
'''