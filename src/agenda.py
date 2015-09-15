
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Jose Diaz"
__credits__ = ["person_1", "person_2", "person_3", "person_n"]
__copyright__ = "Copyright (C) 2015, Jose Diaz"
__license__ = "GPL"
__version__ = "1.1"
__revision__ = "8"
__date__ = "$23/02/2015 08:52:56 AM$"
__status__ = "Desarrollo"
__maintainer__ = "Jose Diaz"
__contact__ = "966403361"
__email__ = "jozz.18x@gmail.com"


from tkinter import *
from tkinter import ttk
from modulos.Estilos import estilos
from modulos.Notas import Notas
from modulos.Recordatorio import Recordatorio
from modulos.Contacto import Contacto
from modulos.Cuenta import Cuenta
from PIL import Image, ImageTk

from modulos.centerWindow import center_window #Modulo para centrar una ventana


class GUI(Frame):
    
    MENUBUTTON_TOOLBAR_MENU = dict(relief=FLAT, bd=0, fg="#37474F", justify=CENTER, wraplength=0,
                                   width=60, activebackground="#4CAF50", activeforeground="#FFFFFF")
        
    MENUBUTTON_TOOLBAR_IZQ = dict(font=("Microsoft Sans Serif", 10), width=137, anchor=W, 
                                  relief=FLAT, activebackground="#343940", activeforeground="#FFFFFF")
    
    BACKGROUND_GENERAL = "#99A2AE"
    BACKGROUND_MENU = "#555D69"
    BACKGROUND_MENU_INTO = "#99A2AE"
    FOREGROUND_1 = "#CFD8DC"
    FOREGROUND_2 = "#FFFFFF"
    FOREGROUND_3 = "#000000"
    FOREGROUND_4 = "#37474F"
    SELECT_BACKGROUND = "#4CAF50"
    SELECT_BACKGROUND_2 = "#000000"
    FONT = ("Microsoft Sans Serif", 10)
    
    @classmethod
    def main(cls):
        root = Tk()
        root.title("Agenda Personal")
        root['bg'] = "#99A2AE"
        
        center_window(root, width=1050, height=660, windowsbar=True) #Centra la ventana principal.
        
        vista = cls(root)
        vista.pack(fill=BOTH, expand=True)
        
        root.wm_iconbitmap(r"image\Icon.ico")
        
        root.minsize(1010,580)
        root.mainloop()
        
    def __init__(self, master):
        super().__init__(master)
        self.estado = False
        self.estado_btn_flotante = False
        self.contador_contactos_agregados_recientemente = 0
        self.cargar_estilos_ttk()
        self.cargar_imagenes()
        
        self.toolbar_menu_top = self.crear_toolbar_menu_top()
        self.toolbar_menu_top.pack(side=TOP, fill=X)
        
        self.toolbar_lateral = self.crear_toolbar_lateral_izquierda()
        self.toolbar_lateral.pack(side=LEFT, fill=Y)
        
        separador = Frame(self, bg="#262A2E")
        separador.pack(side=LEFT, fill=Y)
        
        self.frame_principal = Frame(self)
        self.frame_principal.pack(side=LEFT, fill=BOTH, expand=True)
                
        self.crear_btn_flotante()
        
        self.interfaz()
        
    def cargar_estilos_ttk(self):
        estilos()
    
    def cargar_imagenes(self):
        # Icons barra de titulo
        self.imagenSlideTop = ImageTk.PhotoImage(Image.open(r"image\slide_top.png"))
        self.imagenSlideBottom = ImageTk.PhotoImage(Image.open(r"image\slide_bottom.png"))
        self.imagenMenuOpciones = ImageTk.PhotoImage(Image.open(r"image\menu_opciones.png"))
        self.imagenAyuda = ImageTk.PhotoImage(Image.open(r"image\ayuda.png"))
        self.imagenAbout = ImageTk.PhotoImage(Image.open(r"image\about.png"))
        self.imagenOpciones = ImageTk.PhotoImage(Image.open(r"image\opciones.png"))
        self.imagenLike = ImageTk.PhotoImage(Image.open(r"image\like.png"))
        
        # Iconos Barra Menu - 32*32
        self.imagenInicioMenu = ImageTk.PhotoImage(Image.open(r"image\barra_menu\inicio.png"))
        self.imagenCalendarioMenu = ImageTk.PhotoImage(Image.open(r"image\barra_menu\calendario.png"))
        self.imagenTareasMenu = ImageTk.PhotoImage(Image.open(r"image\barra_menu\tareas.png"))
        self.imagenRecordatorioMenu = ImageTk.PhotoImage(Image.open(r"image\barra_menu\recordatorio.png"))
        self.imagenNotasMenu = ImageTk.PhotoImage(Image.open(r"image\barra_menu\notas.png"))
        self.imagenContactosMenu = ImageTk.PhotoImage(Image.open(r"image\barra_menu\contactos.png"))
        self.imagenCuentasMenu = ImageTk.PhotoImage(Image.open(r"image\barra_menu\cuentas.png"))
        # Iconos barra lateral - 48*32
        self.imagenInicio = ImageTk.PhotoImage(Image.open(r"image\barra_lateral\inicio.png"))
        self.imagenCalendario = ImageTk.PhotoImage(Image.open(r"image\barra_lateral\calendario.png"))
        self.imagenTareas = ImageTk.PhotoImage(Image.open(r"image\barra_lateral\tareas.png"))
        self.imagenRecordatorio = ImageTk.PhotoImage(Image.open(r"image\barra_lateral\recordatorio.png"))
        self.imagenNotas = ImageTk.PhotoImage(Image.open(r"image\barra_lateral\notas.png"))
        self.imagenContactos = ImageTk.PhotoImage(Image.open(r"image\barra_lateral\contactos.png"))
        self.imagenCuentas = ImageTk.PhotoImage(Image.open(r"image\barra_lateral\cuentas.png"))
        # Iconos pestania Menu - 20x20
        self.imagenInicioPestania = ImageTk.PhotoImage(Image.open(r"image\petanias_menu\inicio.png"))
        self.imagenCalendarioPestania = ImageTk.PhotoImage(Image.open(r"image\petanias_menu\calendario.png"))
        self.imagenTareasPestania = ImageTk.PhotoImage(Image.open(r"image\petanias_menu\tareas.png"))
        self.imagenRecordatorioPestania = ImageTk.PhotoImage(Image.open(r"image\petanias_menu\recordatorio.png"))
        self.imagenNotasPestania = ImageTk.PhotoImage(Image.open(r"image\petanias_menu\notas.png"))
        self.imagenContactosPestania = ImageTk.PhotoImage(Image.open(r"image\petanias_menu\contactos.png"))
        self.imagenCuentasPestania = ImageTk.PhotoImage(Image.open(r"image\petanias_menu\cuentas.png"))
        
        self.imagenFlotanteOpen = ImageTk.PhotoImage(Image.open(r"image\nuevo_lollipop.png"))
        self.imagenFlotanteClose = ImageTk.PhotoImage(Image.open(r"image\nuevo_lollipop_2.png"))
        
        self.imagenFlotanteNotas = ImageTk.PhotoImage(Image.open(r"image\nuevo_lollipop_notas.png"))
        self.imagenFlotanteContactos = ImageTk.PhotoImage(Image.open(r"image\nuevo_lollipop_contactos.png"))
        self.imagenFlotanteTareas = ImageTk.PhotoImage(Image.open(r"image\nuevo_lollipop_tareas.png"))
        self.imagenFlotanteRecordatorio = ImageTk.PhotoImage(Image.open(r"image\nuevo_lollipop_recordatorio.png"))
    
    def crear_toolbar_lateral_izquierda(self):
        toolbar_lateral_izquierda = Frame(self, bg=self.BACKGROUND_MENU)
        
        btn = Menubutton(toolbar_lateral_izquierda, text="Inicio", bg=toolbar_lateral_izquierda['bg'],
                         fg=self.FOREGROUND_1, image=self.imagenInicio, compound=LEFT, ** self.MENUBUTTON_TOOLBAR_IZQ)
        btn.pack(fill=X, pady=1)
        separador = Frame(toolbar_lateral_izquierda, bg="#4c545e", height=1)
        separador.pack(fill=X, padx=5)
        btn = Menubutton(toolbar_lateral_izquierda, text="Calendario", bg=toolbar_lateral_izquierda['bg'], 
                         fg=self.FOREGROUND_1, image=self.imagenCalendario, compound=LEFT, ** self.MENUBUTTON_TOOLBAR_IZQ)
        btn.pack(fill=X)
        separador = Frame(toolbar_lateral_izquierda, bg="#4c545e", height=1)
        separador.pack(fill=X, padx=5)
        btn = Menubutton(toolbar_lateral_izquierda, text="Tareas", bg=toolbar_lateral_izquierda['bg'], 
                         fg=self.FOREGROUND_1, image=self.imagenTareas, compound=LEFT, ** self.MENUBUTTON_TOOLBAR_IZQ)
        btn.pack(fill=X)
        separador = Frame(toolbar_lateral_izquierda, bg="#4c545e", height=1)
        separador.pack(fill=X, padx=5)
        btn_notas = Menubutton(toolbar_lateral_izquierda, text="Notas", bg=toolbar_lateral_izquierda['bg'], 
                         fg=self.FOREGROUND_1, image=self.imagenNotas, compound=LEFT, ** self.MENUBUTTON_TOOLBAR_IZQ)
        btn_notas.pack(fill=X)
        btn_notas.bind("<Button-1>", lambda evt: self.notas())
        separador = Frame(toolbar_lateral_izquierda, bg="#4c545e", height=1)
        separador.pack(fill=X, padx=5)
        btn_recordatorio = Menubutton(toolbar_lateral_izquierda, text="Recordatorio", bg=toolbar_lateral_izquierda['bg'], 
                         fg=self.FOREGROUND_1, image=self.imagenRecordatorio, compound=LEFT, ** self.MENUBUTTON_TOOLBAR_IZQ)
        btn_recordatorio.pack(fill=X)
        btn_recordatorio.bind("<Button-1>", lambda evt: self.recordatorio())
        separador = Frame(toolbar_lateral_izquierda, bg="#4c545e", height=1)
        separador.pack(fill=X, padx=5)
        btn_contactos = Menubutton(toolbar_lateral_izquierda, text="Contactos", bg=toolbar_lateral_izquierda['bg'], 
                         fg=self.FOREGROUND_1, image=self.imagenContactos, compound=LEFT, ** self.MENUBUTTON_TOOLBAR_IZQ)
        btn_contactos.pack(fill=X)
        btn_contactos.bind("<Button-1>", lambda evt: self.contactos())
        separador = Frame(toolbar_lateral_izquierda, bg="#4c545e", height=1)
        separador.pack(fill=X, padx=5)
        btn_cuentas = Menubutton(toolbar_lateral_izquierda, text="Cuentas", bg=toolbar_lateral_izquierda['bg'], 
                         fg=self.FOREGROUND_1, image=self.imagenCuentas, compound=LEFT, ** self.MENUBUTTON_TOOLBAR_IZQ)
        btn_cuentas.pack(fill=X)
        btn_cuentas.bind("<Button-1>", lambda evt: self.cuentas())
        separador = Frame(toolbar_lateral_izquierda, bg="#4c545e", height=1)
        separador.pack(fill=X, padx=5)
        
        return toolbar_lateral_izquierda
        
    def crear_toolbar_menu_top(self):
        toolbar_menu_top = Frame(self, relief=FLAT, bg=self.BACKGROUND_MENU)
        # Se crea las pestanias a la ventana
        self.notebook_principal = ttk.Notebook(toolbar_menu_top, style="ButtonNotebook")
        pestania_invalida = Frame(self.notebook_principal, bg=self.BACKGROUND_MENU_INTO)
        self.pestania_inicio = Frame(self.notebook_principal, bg=self.BACKGROUND_MENU_INTO)
        self.pestania_cita = Frame(self.notebook_principal, bg=self.BACKGROUND_MENU_INTO)
        self.pestania_tareas = Frame(self.notebook_principal, bg=self.BACKGROUND_MENU_INTO)
        self.pestania_notas = Frame(self.notebook_principal, bg=self.BACKGROUND_MENU_INTO)
        self.pestania_recordatorio = Frame(self.notebook_principal, bg=self.BACKGROUND_MENU_INTO)
        self.pestania_cuentas = Frame(self.notebook_principal, bg=self.BACKGROUND_MENU_INTO)
        # Se aniade los Frames y los encabezados a las pestanias creadas
        self.notebook_principal.add(pestania_invalida, text='\t                         ')
        self.notebook_principal.add(self.pestania_inicio, text='  INICIO  ', image=self.imagenInicioPestania, compound=RIGHT)
        self.notebook_principal.add(self.pestania_cita, text='  CITAS  ', image=self.imagenCalendarioPestania, compound=RIGHT)
        self.notebook_principal.add(self.pestania_tareas, text='  TAREAS  ', image=self.imagenTareasPestania, compound=RIGHT)
        self.notebook_principal.add(self.pestania_notas, text='  NOTAS  ', image=self.imagenNotasPestania, compound=RIGHT)
        self.notebook_principal.add(self.pestania_recordatorio, text='  RECORDATORIO  ', image=self.imagenRecordatorioPestania, compound=RIGHT)
        self.notebook_principal.add(self.pestania_cuentas, text='  CUENTAS  ', image=self.imagenCuentasPestania, compound=RIGHT)
        self.notebook_principal.configure(height=80)
        
        ''' Botton SISTEMA '''
        btn_archivo = Menubutton(toolbar_menu_top, relief=FLAT, text='AGENDA', bg="#262A2E", font=self.FONT,
                                    fg="#FFFFFF", activebackground=self.SELECT_BACKGROUND, activeforeground="#FFFFFF")
        btn_archivo.place(in_=self.notebook_principal, relx=0, y=10, anchor="w", width=150, height=31)
        menu_archivo = Menu(btn_archivo, tearoff=0, font=self.FONT, activebackground=self.SELECT_BACKGROUND, activeforeground = "#FFFFFF", disabledforeground='dark gray')
        menu_archivo.add_command(label = "Acerca del Software", compound=LEFT)
        menu_archivo.add_separator()
        menu_archivo.add_command(label = "Acerca del Desarrollador", compound=LEFT)
        menu_archivo.add_separator()
        menu_archivo.add_command(label = "Opciones", compound=LEFT)
        menu_archivo.add_separator()
        menu_archivo.add_command(label = "Ayuda", compound=LEFT)
        menu_archivo.add_separator()
        menu_archivo.add_command(label = "Salir", command=self.salir, compound=LEFT)
        btn_archivo["menu"] = menu_archivo
        
        ''' Slide barra Notebook '''
        self.btn_slide = Menubutton(toolbar_menu_top, image=self.imagenSlideBottom, cursor="hand2", relief=FLAT, 
                    bg=self.BACKGROUND_MENU, activebackground=self.pestania_inicio['bg'])
        self.btn_slide.place(in_=self.notebook_principal, relx=1, y=4, x=-24, bordermode="outside")
        self.btn_slide.bind("<Button-1>", self.slide)
        ''' Menu Opciones - barra Notebook '''
        btn_menu_opciones = Menubutton(toolbar_menu_top, image=self.imagenMenuOpciones, cursor="hand2", relief=FLAT, 
                    bg=self.BACKGROUND_MENU, activebackground="#484f59")
        btn_menu_opciones.place(in_=self.notebook_principal, relx=1, y=2, x=-50, bordermode="outside")
        #btn_ayuda.bind("<Button-1>", self.slide)
        ''' Ayuda barra Notebook '''
        btn_ayuda = Menubutton(toolbar_menu_top, image=self.imagenAyuda, cursor="hand2", relief=FLAT, 
                    bg=self.BACKGROUND_MENU, activebackground="#484f59")
        btn_ayuda.place(in_=self.notebook_principal, relx=1, y=2, x=-78, bordermode="outside")
        #btn_ayuda.bind("<Button-1>", self.slide)
        ''' Opciones barra Notebook '''
        btn_opciones = Menubutton(toolbar_menu_top, image=self.imagenOpciones, cursor="hand2", relief=FLAT, 
                    bg=self.BACKGROUND_MENU, activebackground="#484f59")
        btn_opciones.place(in_=self.notebook_principal, relx=1, y=2, x=-106, bordermode="outside")
        #btn_opciones.bind("<Button-1>", self.slide)
        ''' About barra Notebook '''
        btn_about = Menubutton(toolbar_menu_top, image=self.imagenAbout, cursor="hand2", relief=FLAT, 
                    bg=self.BACKGROUND_MENU, activebackground="#484f59")
        btn_about.place(in_=self.notebook_principal, relx=1, y=2, x=-134, bordermode="outside")
        #btn_about.bind("<Button-1>", self.slide)
        ''' Like barra Notebook '''
        btn_like = Menubutton(toolbar_menu_top, image=self.imagenLike, cursor="hand2", relief=FLAT, 
                    bg=self.BACKGROUND_MENU, activebackground="#484f59")
        btn_like.place(in_=self.notebook_principal, relx=1, y=2, x=-162, bordermode="outside")
        #btn_about.bind("<Button-1>", self.slide)
        
        
        fr_inicio_1 = Frame(self.pestania_inicio, bg=self.pestania_inicio['bg'])
        fr_inicio_1.pack(side=LEFT, fill=X, padx=5)
        separador = Frame(self.pestania_inicio, bg=self.BACKGROUND_MENU, height=1)
        separador.pack(side=LEFT, fill=Y, padx=5)
        fr_inicio_2 = Frame(self.pestania_inicio, bg=self.pestania_inicio['bg'])
        fr_inicio_2.pack(side=LEFT, fill=X)
        
        self.btn_pestania_calendario = Menubutton(fr_inicio_1, text='Nueva\nCita', image=self.imagenCalendarioMenu, compound=TOP,
                                                  bg=self.pestania_inicio['bg'], **self.MENUBUTTON_TOOLBAR_MENU)
        self.btn_pestania_calendario.pack(side=LEFT)
        self.btn_pestania_tareas = Menubutton(fr_inicio_1, text='Nueva\nTarea', image=self.imagenTareasMenu, compound=TOP,
                                              bg=self.pestania_inicio['bg'], **self.MENUBUTTON_TOOLBAR_MENU)
        self.btn_pestania_tareas.pack(side=LEFT)
        self.btn_pestania_notas = Menubutton(fr_inicio_1, text='Nueva\nNota', image=self.imagenNotasMenu, compound=TOP,
                                             bg=self.pestania_inicio['bg'], **self.MENUBUTTON_TOOLBAR_MENU)
        self.btn_pestania_notas.pack(side=LEFT)
        self.btn_pestania_recordatorio = Menubutton(fr_inicio_1, text='Nuevo\nRecordatorio', image=self.imagenRecordatorioMenu, compound=TOP,
                                                    bg=self.pestania_inicio['bg'], **self.MENUBUTTON_TOOLBAR_MENU)
        self.btn_pestania_recordatorio.pack(side=LEFT)
        self.btn_pestania_contactos = Menubutton(fr_inicio_1, text='Nuevo\nContacto', image=self.imagenContactosMenu, compound=TOP,
                                                 bg=self.pestania_inicio['bg'], **self.MENUBUTTON_TOOLBAR_MENU)
        self.btn_pestania_contactos.pack(side=LEFT)
        self.btn_pestania_cuentas = Menubutton(fr_inicio_1, text='Nueva\nCuenta', image=self.imagenCuentasMenu, compound=TOP,
                                                bg=self.pestania_inicio['bg'], **self.MENUBUTTON_TOOLBAR_MENU)
        self.btn_pestania_cuentas.pack(side=LEFT)
        
        self.notebook_principal.tab(pestania_invalida, state='disabled') # Desabilita la pestania
        self.notebook_principal.select(self.pestania_inicio) # Abre la pestania Inicio al iniciar
        self.notebook_principal.pack(fill=BOTH, expand=True)
        
        return toolbar_menu_top
    
    """---------------------------------------------------------------------"""
    """                                NOTAS                                """
    """---------------------------------------------------------------------"""
    def notas(self):
        """ Instancia de la clase Recordatorio """
        self.obj_notas = Notas(self.frame_principal)
        
        
    """---------------------------------------------------------------------"""
    """                             RECORDATORIO                            """
    """---------------------------------------------------------------------"""
    def recordatorio(self):
        """ Instancia de la clase Recordatorio """
        self.obj_recordatorio = Recordatorio(self.frame_principal)
        
        
    """---------------------------------------------------------------------"""
    """                             CONTACTOS                               """
    """---------------------------------------------------------------------"""
    def contactos(self):
        """ Instancia  de la clase contactos """
        self.obj_contacto = Contacto(self.frame_principal)
        
        """ Se agrega una nueva pestania  -  Pestania Contacto """
        self.pestania_contactos = Frame(self.notebook_principal, bg=self.BACKGROUND_MENU_INTO)
        self.notebook_principal.insert('end', self.pestania_contactos, text=' CONTACTO ', image=self.imagenContactosPestania, compound=RIGHT)
        
        fr_contacto_1 = Frame(self.pestania_contactos, bg=self.pestania_contactos['bg'])
        fr_contacto_1.pack(side=LEFT, fill=Y, padx=5, pady=2)
        separador = Frame(self.pestania_contactos, bg=self.BACKGROUND_MENU, height=90, width=1)
        separador.pack(side=LEFT, padx=5, pady=1)
        fr_contacto_2 = Frame(self.pestania_contactos, bg=self.pestania_contactos['bg'])
        fr_contacto_2.pack(side=LEFT, fill=Y, pady=2)
        separador = Frame(self.pestania_contactos, bg=self.BACKGROUND_MENU, height=90, width=1)
        separador.pack(side=LEFT, padx=5, pady=1)
        
        self.btn_pestania_nuevo = Menubutton(fr_contacto_1, text='Nuevo\nContacto', image=self.imagenNotasMenu, compound=TOP,
                                             bg=self.pestania_contactos['bg'], **self.MENUBUTTON_TOOLBAR_MENU)
        self.btn_pestania_nuevo.pack(side=LEFT)
        
        self.btn_pestania_editar = Menubutton(fr_contacto_1, text='Editar\nContacto', image=self.imagenNotasMenu, compound=TOP,
                                              bg=self.pestania_contactos['bg'], **self.MENUBUTTON_TOOLBAR_MENU)
        self.btn_pestania_editar.pack(side=LEFT)
        
        self.btn_pestania_eliminar = Menubutton(fr_contacto_1, text='Eliminar\nContacto', image=self.imagenNotasMenu, compound=TOP,
                                                bg=self.pestania_contactos['bg'], **self.MENUBUTTON_TOOLBAR_MENU)
        self.btn_pestania_eliminar.pack(side=LEFT)
        
        self.btn_pestania_salir = Menubutton(fr_contacto_2, text='Cerrar\nContacto', image=self.imagenNotasMenu, compound=TOP,
                                             bg=self.pestania_contactos['bg'], **self.MENUBUTTON_TOOLBAR_MENU)
        self.btn_pestania_salir.pack(side=LEFT)
        self.btn_pestania_salir.bind('<Button-1>', lambda e: self.salir_pestania_contacto())
        
        self.notebook_principal.select(self.pestania_contactos)
        
        
    def ver_cantidad_contactos(self):
        return self.obj_contacto.cantidad_contactos()
        
    def salir_pestania_contacto(self):
        self.obj_contacto.btn_salir_contacto()
        self.notebook_principal.forget(self.pestania_contactos)
        self.notebook_principal.select(self.pestania_inicio)
    
    """---------------------------------------------------------------------"""
    """                             self.pestania_cuentas                                 """
    """---------------------------------------------------------------------"""
    def cuentas(self):
        """ Instancia de la clase Cuenta """
        self.obj_cuenta = Cuenta(self.frame_principal)
        
    
    
    def interfaz(self):
        #self.master.overrideredirect(True)
        #self.master.wm_attributes("-topmost", True) #Posiciona delante la ventana de las otras ventanas
        #self.master.wm_attributes("-disabled", True) #Hace que sea imposible para interactuar con la ventana y vuelve a dibujar el foco.
        #self.master.wm_attributes("-transparentcolor", "white")
        #self.master.wm_attributes("-fullscreen", True) #Pantalla completa, incluye la barra de tareas y oculta borde de la ventana.
        #self.master.wm_attributes("-toolwindow", True) #hace una ventana con un solo primer boton (cerrar)
        #self.master.wm_attributes("-transparent", "black")
        self.master.wait_visibility(self.master)
        #self.master.call('wm', 'attributes', '.', '-topmost', True) #Posiciona delante la ventana de las otras ventanas
        
    def crear_btn_flotante(self):
        """Crea el boton flotante en la ventana principal"""
        self.btn_flotante = Button(self, image=self.imagenFlotanteOpen, relief=FLAT, bd=0,
                                    command=self.abrir_boton_flotante)
        self.btn_flotante.place(in_=self, relx=1, rely=1, x=-30, y=-20, anchor=SE, bordermode="outside")
    
    def abrir_boton_flotante(self):
        """Abre los detalles cuando se presiona el boton flotante."""
        if not self.estado_btn_flotante:
            self.btn_flotante.config(image=self.imagenFlotanteClose)
            self.crear_botones_flotante()
            self.estado_btn_flotante = True
        else:
            self.btn_flotante.config(image=self.imagenFlotanteOpen)
            self.lb_flotante_tareas.destroy()
            self.btn_flotante_tareas.destroy()
            self.lb_flotante_notas.destroy()
            self.btn_flotante_notas.destroy()
            self.lb_flotante_contactos.destroy()
            self.btn_flotante_contactos.destroy()
            self.lb_flotante_recordatorio.destroy()
            self.btn_flotante_recordatorio.destroy()
            self.estado_btn_flotante = False
    
    def crear_botones_flotante(self):
        """Crea los widgets al presionar el boton flotante."""
        self.lb_flotante_recordatorio = Label(self.frame_principal, text="Recordatorio", bg="gray", fg="white")
        self.lb_flotante_recordatorio.place(in_=self.frame_principal, relx=0.9, rely=0.8, x=-20, y=-40, anchor=SE, bordermode="outside")
        self.btn_flotante_recordatorio = Button(self.frame_principal, command=self.recordatorio, image=self.imagenFlotanteRecordatorio, relief=FLAT, bd=0)
        self.btn_flotante_recordatorio.place(in_=self.frame_principal, relx=1, rely=0.8, x=-30, y=-20, anchor=SE, bordermode="outside")
        
        self.lb_flotante_contactos = Label(self.frame_principal, text="Contactos", bg="gray", fg="white")
        self.lb_flotante_contactos.place(in_=self.frame_principal, relx=0.9, rely=0.6, x=-20, y=-40, anchor=SE, bordermode="outside")
        self.btn_flotante_contactos = Button(self.frame_principal, command=self.contactos, image=self.imagenFlotanteContactos, relief=FLAT, bd=0)
        self.btn_flotante_contactos.place(in_=self.frame_principal, relx=1, rely=0.6, x=-30, y=-20, anchor=SE, bordermode="outside")
        
        self.lb_flotante_notas = Label(self.frame_principal, text="Notas", bg="gray", fg="white")
        self.lb_flotante_notas.place(in_=self.frame_principal, relx=0.9, rely=0.4, x=-20, y=-40, anchor=SE, bordermode="outside")
        self.btn_flotante_notas = Button(self.frame_principal, image=self.imagenFlotanteNotas, relief=FLAT, bd=0)
        self.btn_flotante_notas.place(in_=self.frame_principal, relx=1, rely=0.4, x=-30, y=-20, anchor=SE, bordermode="outside")
        
        self.lb_flotante_tareas = Label(self.frame_principal, text="Tareas", bg="gray", fg="white")
        self.lb_flotante_tareas.place(in_=self.frame_principal, relx=0.9, rely=0.2, x=-20, y=-40, anchor=SE, bordermode="outside")
        self.btn_flotante_tareas = Button(self.frame_principal, image=self.imagenFlotanteTareas, relief=FLAT, bd=0)
        self.btn_flotante_tareas.place(in_=self.frame_principal, relx=1, rely=0.2, x=-30, y=-20, anchor=SE, bordermode="outside")
        
        
    def slide(self, event=None):
        if self.estado==False:
            self.notebook_principal.configure(height=1)
            self.btn_slide['image'] = self.imagenSlideBottom
            self.estado = True
        else:
            self.notebook_principal.configure(height=80)
            self.btn_slide['image'] = self.imagenSlideTop
            self.estado = False
    
    def salir(self):
        self.master.destroy()
            
        
if __name__ == "__main__":
    GUI.main()
