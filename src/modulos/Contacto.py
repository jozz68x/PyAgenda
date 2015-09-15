
__author__="admin"
__date__ ="$23/02/2015 08:52:56 AM$"

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import *
import sqlite3

from modulos.textView import TextView

class Contacto(object):
    
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
    FONT = ("Microsoft Sans Serif", 10)
    FONT_SMALL = ("Microsoft Sans Serif", 9)
    
    MENUBUTTON_BOTTOM = dict(width=65, relief=FLAT, bd=1, font=FONT, fg=FOREGROUND_2,
                    activebackground=ACTIVE_BACKGROUND_2,activeforeground=FOREGROUND_2)
                    
    def __init__(self, master):
        self.LISTA_CONTACTOS = []
        self.contador_contactos_agregados_recientemente = 0
        self.master = master
        self.cargar_imagenes()
        self.frames_principales()
        self.barra_lateral()
        self.interfaz()
        self.listar_listbox()
        
    def cargar_imagenes(self):
        self.imagenIconContacto = ImageTk.PhotoImage(Image.open(r"image\Icon_contacto.png"))
        
        self.imagenBuscar = ImageTk.PhotoImage(Image.open(r"image\buscar.png"))
        self.imagenOpcionOrdenar = ImageTk.PhotoImage(Image.open(r"image\opcion_ordenar.png"))
        self.imagenOpcionOrdenar2 = ImageTk.PhotoImage(Image.open(r"image\opcion_ordenar_2.png"))
        
        self.imagenNuevo = ImageTk.PhotoImage(Image.open(r"image\nuevo.png"))
        self.imagenGuardar = ImageTk.PhotoImage(Image.open(r"image\guardar.png"))
        self.imagenEditar = ImageTk.PhotoImage(Image.open(r"image\editar.png"))
        self.imagenCancelar = ImageTk.PhotoImage(Image.open(r"image\cancelar.png"))
        self.imagenEliminar = ImageTk.PhotoImage(Image.open(r"image\eliminar.png"))
        self.imagenCerrar = ImageTk.PhotoImage(Image.open(r"image\cerrar.png"))
        
    
    def frames_principales(self):
        self.panel = PanedWindow(self.master, bg="#262A2E", orient=HORIZONTAL, relief=FLAT, bd=0, opaqueresize=False)
        self.panel.pack(fill=BOTH, expand=True)
        
        self.fr_left = Frame(self.panel, bg=self.BACKGROUND_MENU_2)
        self.fr_left.pack(side=LEFT, fill=Y, expand=True)
        
        self.fr_right = Frame(self.panel)
        self.fr_right.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.right_bottom = Frame(self.fr_right, bg=self.BACKGROUND)
        self.right_bottom.pack(side=BOTTOM, fill=X)
        
        self.panel.add(self.fr_left)
        self.panel.add(self.fr_right)
    
    def barra_lateral(self):
        """Frame Left"""
        fr_left_top = Frame(self.fr_left, bg="#262A2E")
        fr_left_top.pack(side=TOP, fill=X)
        fr_left_both = Frame(self.fr_left, bg=self.BACKGROUND_MENU_2)
        fr_left_both.pack(fill=BOTH, expand=True, padx=1)
        
        self.var_contactos_recientemente = StringVar()
        lb_records = Label(fr_left_both, textvariable=self.var_contactos_recientemente, font=("Microsoft Sans Serif", 9), bg=fr_left_both['bg'], fg=self.BACKGROUND_MENU_INTO)
        lb_records.pack(side=BOTTOM, fill=X, anchor="center")
        
        self.lb_records = Button(fr_left_both, image=self.imagenIconContacto, compound=TOP, relief=FLAT, bd=0, font=("Microsoft Sans Serif", 10), 
                bg=fr_left_both['bg'], fg=self.BACKGROUND_MENU_INTO, activebackground=fr_left_both['bg'], activeforeground=self.BACKGROUND_MENU_INTO)
        self.lb_records.pack(side=BOTTOM, fill=X, anchor="center")
        
        self.var_ent_buscar = StringVar()
        self.var_ent_buscar.set('Buscar contacto')
        
        ent_buscar = Entry(fr_left_top, width=30, textvariable=self.var_ent_buscar, bg="#99A2AE", font=self.FONT, relief=FLAT, bd=1)
        btn_buscar_contacto = Menubutton(fr_left_top, image=self.imagenBuscar, relief=FLAT, bg=ent_buscar['bg'], activebackground="#009846")
        btn_buscar_contacto.place(in_=ent_buscar, relx=1.0, rely=0, x=21, y=-1, anchor=NE)
        #btn_buscar_contacto.place(in_=ent_buscar, relx=1.1, x=0, y=-1, anchor=NE)
        btn_buscar_contacto.bind('<Button-1>', lambda e: self.buscar_contacto())
        ent_buscar.pack(anchor="w", padx=5, pady=10)
        ent_buscar.bind('<Button-1>', lambda evt: self.listar_listbox())
        ent_buscar.bind('<Key>', lambda evt: self.buscar_contacto())
        ent_buscar.bind('<Return>', lambda evt: self.buscar_contacto())
        ent_buscar.bind('<Enter>', lambda evt: self.var_ent_buscar.set(''))
        ent_buscar.bind('<Leave>', lambda evt: self.var_ent_buscar.set('Buscar contacto'), ent_buscar.config(fg="#546E7A"))
        ent_buscar.bind('<FocusIn>', lambda evt: ent_buscar.config(fg="#000000"))
        ent_buscar.bind('<FocusOut>', lambda evt: ent_buscar.config(fg="#546E7A"))
        
        btn_opc_ordenar = Menubutton(fr_left_top, image=self.imagenOpcionOrdenar, bg=fr_left_top['bg'], activebackground=fr_left_top['bg'], relief=FLAT, bd=0, direction='flush')
        btn_opc_ordenar.place(in_=fr_left_top, relx=1, rely=0, x=2, y=4, anchor=NE, bordermode="outside")
        menu_ord_contactos = Menu(btn_opc_ordenar, tearoff=0, activebackground=self.ACTIVE_BACKGROUND, activeforeground = "#FFFFFF")
        menu_ord_contactos.add_radiobutton(label = " Ordenar en orden A-Z", command=self.ordenar_contacto_asc)
        menu_ord_contactos.add_radiobutton(label = " Ordenar en orden Z-A", command=self.ordenar_contacto_desc)
        menu_ord_contactos.add_separator()
        menu_ord_contactos.add_command(label = " Vaciar Lista", command=self.vaciar_lista_contactos)
        
        btn_opc_ordenar["menu"] = menu_ord_contactos
        
        btn_opc_ordenar.bind('<Enter>', lambda evt: btn_opc_ordenar.config(image=self.imagenOpcionOrdenar2))
        btn_opc_ordenar.bind('<Leave>', lambda evt: btn_opc_ordenar.config(image=self.imagenOpcionOrdenar))
        
        
        separador = Frame(fr_left_both, bg=self.BACKGROUND_MENU_2, height=1, width=200)
        separador.pack(fill=X)
        
        self.listbox = Listbox(fr_left_both, width=40, bg=fr_left_both['bg'], fg="#B0BEC5", relief=FLAT, bd=0, font=self.FONT, activestyle='dotbox',
                                selectbackground=self.ACTIVE_BACKGROUND, highlightbackground=fr_left_both['bg'], highlightcolor=fr_left_both['bg'], highlightthickness=0)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        scroll = ttk.Scrollbar(fr_left_both, orient=VERTICAL, command=self.listbox.yview)
        scroll.pack(side=LEFT, fill=Y)
        self.listbox['yscrollcommand'] = scroll.set
        
        #Menu de Opciones Anticlick en ListBox
        self.menu_opc_lista = Menu(self.listbox, tearoff=0, activebackground=self.ACTIVE_BACKGROUND, activeforeground = "#FFFFFF")
        self.menu_opc_lista.add_command(label = "Ver")
        self.menu_opc_lista.add_separator()
        self.menu_opc_lista.add_command(label = "Editar", command=self.editar_contacto)
        self.menu_opc_lista.add_command(label = "Eliminar", command=self.eliminar_contacto)
        
        self.listbox.bind("<ButtonRelease-3>", self.opciones_anticlick_listbox)
        self.listbox.bind("<Double-1>", lambda e: self.editar_contacto())
        
    def interfaz(self):
        """Frame Right"""
        self.notebook_contacto = ttk.Notebook(self.fr_right, style="ButtonNotebook")
        self.fr_info_personal = Frame(self.notebook_contacto)
        self.fr_info_trabajo = Frame(self.notebook_contacto)
        self.fr_info_nota = Frame(self.notebook_contacto)
        self.fr_info_foto = Frame(self.notebook_contacto)
        # se aniade los encabezados a las pestanias creadas
        self.notebook_contacto.add(self.fr_info_personal, text='Informacion Personal', padding=-3)
        self.notebook_contacto.add(self.fr_info_trabajo, text='Trabajo', padding=-3)
        self.notebook_contacto.add(self.fr_info_nota, text='Nota', padding=-3)
        self.notebook_contacto.add(self.fr_info_foto, text='Fotografia', padding=-3)
        
        self.notebook_contacto.pack(expand=True)
        
        """ Pestania Informacion Personal """
        fr_info_personal_apoyo = Frame(self.fr_info_personal)
        fr_info_personal_apoyo.pack(fill=BOTH, expand=True, padx=15, pady=5)
        
        lb_id = Label(fr_info_personal_apoyo, text="ID", font=self.FONT_SMALL)
        lb_id.grid(row=0, column=0, pady=2, sticky="w")
        lb_nombre = Label(fr_info_personal_apoyo, text="Nombre", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_nombre.grid(row=1, column=0, pady=2, sticky="w")
        lb_nombre.grid_propagate()
        lb_apellido = Label(fr_info_personal_apoyo, text="Apellido", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_apellido.grid(row=2, column=0, pady=2, sticky="w")
        lb_movil = Label(fr_info_personal_apoyo, text="Movil", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_movil.grid(row=3, column=0, pady=2, sticky="w")
        lb_telefono = Label(fr_info_personal_apoyo, text="Telefono", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_telefono.grid(row=4, column=0, pady=2, sticky="w")
        lb_email = Label(fr_info_personal_apoyo, text="Email", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_email.grid(row=5, column=0, pady=2, sticky="w")
        lb_casa = Label(fr_info_personal_apoyo, text="Casa", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_casa.grid(row=6, column=0, pady=2, sticky="w")
        lb_nickFacebook = Label(fr_info_personal_apoyo, text="Nick facebook", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_nickFacebook.grid(row=11, column=0, pady=2, sticky="w")
        lb_paginaWeb = Label(fr_info_personal_apoyo, text="Pagina Web", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_paginaWeb.grid(row=12, column=0, pady=2, sticky="w")
        lb_cumpleanios = Label(fr_info_personal_apoyo, text="Cumpleanios", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_cumpleanios.grid(row=13, column=0, pady=2, sticky="w")
        
        
        self.var_id = StringVar()
        self.var_nombre = StringVar()
        self.var_apellido = StringVar()
        self.var_movil = StringVar()
        self.var_telefono = StringVar()
        self.var_email = StringVar()
        self.var_direccion = StringVar()
        self.var_ciudad = StringVar()
        self.var_provincia = StringVar()
        self.var_codigoPostal = StringVar()
        self.var_pais = StringVar()
        self.var_nickFacebook = StringVar()
        self.var_paginaWeb = StringVar()
        self.var_cumpleanio_dia = StringVar()
        self.var_cumpleanio_mes = StringVar()
        self.var_cumpleanio_anio = StringVar()
        
        
        ent_id = ttk.Entry(fr_info_personal_apoyo, textvariable=self.var_id, state='disabled', font=self.FONT)
        self.var_id.set("")
        ent_id.grid(row=0, column=1, pady=2, sticky=W+E, ipadx=320)
        self.ent_nombre = Entry(fr_info_personal_apoyo, textvariable=self.var_nombre, relief=FLAT, font=self.FONT)
        self.ent_nombre.grid(row=1, column=1, pady=2, sticky=W+E)
        self.ent_nombre.bind('<FocusIn>', lambda evt: lb_nombre.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        self.ent_nombre.bind('<FocusOut>', lambda evt: lb_nombre.config(bg="#F0F0F0", fg="#000000"))
        
        ent_apellido = Entry(fr_info_personal_apoyo, textvariable=self.var_apellido, relief=FLAT, font=self.FONT)
        ent_apellido.grid(row=2, column=1, pady=2, sticky=W+E)
        ent_apellido.bind('<FocusIn>', lambda evt: lb_apellido.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_apellido.bind('<FocusOut>', lambda evt: lb_apellido.config(bg="#F0F0F0", fg="#000000"))
        
        ent_movil = Entry(fr_info_personal_apoyo, textvariable=self.var_movil, relief=FLAT, font=self.FONT)
        self.var_movil.set("")
        ent_movil.grid(row=3, column=1, pady=2, sticky=W+E)
        ent_movil.bind('<FocusIn>', lambda evt: lb_movil.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_movil.bind('<FocusOut>', lambda evt: lb_movil.config(bg="#F0F0F0", fg="#000000"))
        
        ent_telefono = Entry(fr_info_personal_apoyo, textvariable=self.var_telefono, relief=FLAT, font=self.FONT)
        self.var_telefono.set("")
        ent_telefono.grid(row=4, column=1, pady=2, sticky=W+E)
        ent_telefono.bind('<FocusIn>', lambda evt: lb_telefono.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_telefono.bind('<FocusOut>', lambda evt: lb_telefono.config(bg="#F0F0F0", fg="#000000"))
        
        ent_email = Entry(fr_info_personal_apoyo, textvariable=self.var_email, relief=FLAT, font=self.FONT)
        ent_email.grid(row=5, column=1, pady=2, sticky=W+E)
        ent_email.bind('<FocusIn>', lambda evt: lb_email.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_email.bind('<FocusOut>', lambda evt: lb_email.config(bg="#F0F0F0", fg="#000000"))
        
        ent_direccion = Entry(fr_info_personal_apoyo, textvariable=self.var_direccion, relief=FLAT, font=self.FONT)
        self.var_direccion.set("Direccion")
        ent_direccion.grid(row=6, column=1, pady=2, sticky=W+E)
        ent_direccion.bind('<FocusIn>', lambda evt: self.var_direccion.set(''), ent_direccion.config(fg="#000000"))
        ent_direccion.bind('<FocusOut>', lambda evt: self.var_direccion.set('Direccion'), ent_direccion.config(fg="#546E7A"))
        ent_direccion.bind('<Button-1>', lambda evt: self.evt_entry_Button_1(ent_direccion,self.var_direccion, text="Direccion"))
        ent_ciudad = Entry(fr_info_personal_apoyo, textvariable=self.var_ciudad, relief=FLAT, font=self.FONT)
        self.var_ciudad.set("Ciudad")
        ent_ciudad.grid(row=7, column=1, pady=2, sticky=W+E)
        ent_ciudad.bind('<FocusIn>', lambda evt: self.var_ciudad.set(''), ent_ciudad.config(fg="#000000"))
        ent_ciudad.bind('<FocusOut>', lambda evt: self.var_ciudad.set('Ciudad'), ent_ciudad.config(fg="#546E7A"))
        ent_ciudad.bind('<Button-1>', lambda evt: self.evt_entry_Button_1(ent_ciudad,self.var_ciudad, text="Ciudad"))
        ent_provincia = Entry(fr_info_personal_apoyo, textvariable=self.var_provincia, relief=FLAT, font=self.FONT)
        self.var_provincia.set("Provincia")
        ent_provincia.grid(row=8, column=1, pady=2, sticky=W+E)
        ent_provincia.bind('<FocusIn>', lambda evt: self.var_provincia.set(''), ent_provincia.config(fg="#000000"))
        ent_provincia.bind('<FocusOut>', lambda evt: self.var_provincia.set('Provincia'), ent_provincia.config(fg="#546E7A"))
        ent_provincia.bind('<Button-1>', lambda evt: self.evt_entry_Button_1(ent_provincia,self.var_provincia, text="Provincia"))
        ent_codigoPostal = Entry(fr_info_personal_apoyo, textvariable=self.var_codigoPostal, relief=FLAT, font=self.FONT)
        self.var_codigoPostal.set("Codigo Postal")
        ent_codigoPostal.grid(row=9, column=1, pady=2, sticky=W+E)
        ent_codigoPostal.bind('<FocusIn>', lambda evt: self.var_codigoPostal.set(''), ent_codigoPostal.config(fg="#000000"))
        ent_codigoPostal.bind('<FocusOut>', lambda evt: self.var_codigoPostal.set('Ciudad'), ent_codigoPostal.config(fg="#546E7A"))
        ent_codigoPostal.bind('<Button-1>', lambda evt: self.evt_entry_Button_1(ent_codigoPostal,self.var_codigoPostal, text="Codigo Postal"))
        ent_pais = Entry(fr_info_personal_apoyo, textvariable=self.var_pais, relief=FLAT, font=self.FONT)
        self.var_pais.set("Pais")
        ent_pais.grid(row=10, column=1, pady=2, sticky=W+E)
        ent_pais.bind('<FocusIn>', lambda evt: self.var_pais.set(''), ent_pais.config(fg="#000000"))
        ent_pais.bind('<FocusOut>', lambda evt: self.var_pais.set('Ciudad'), ent_pais.config(fg="#546E7A"))
        ent_pais.bind('<Button-1>', lambda evt: self.evt_entry_Button_1(ent_pais,self.var_pais, text="Pais"))
        
        ent_nickFacebook = Entry(fr_info_personal_apoyo, textvariable=self.var_nickFacebook, relief=FLAT, font=self.FONT)
        ent_nickFacebook.grid(row=11, column=1, pady=2, sticky=W+E)
        ent_nickFacebook.bind('<FocusIn>', lambda evt: lb_nickFacebook.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_nickFacebook.bind('<FocusOut>', lambda evt: lb_nickFacebook.config(bg="#F0F0F0", fg="#000000"))
        
        ent_paginaWeb = Entry(fr_info_personal_apoyo, textvariable=self.var_paginaWeb, relief=FLAT, font=self.FONT)
        ent_paginaWeb.grid(row=12, column=1, pady=2, sticky=W+E)
        ent_paginaWeb.bind('<FocusIn>', lambda evt: lb_paginaWeb.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_paginaWeb.bind('<FocusOut>', lambda evt: lb_paginaWeb.config(bg="#F0F0F0", fg="#000000"))

        fr_ayuda = ttk.Frame(fr_info_personal_apoyo)
        fr_ayuda.grid(row=13, column=1, pady=2, sticky="w")
        DIAS = ['01','02','03','04','05','06','07','08','09',10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        MESES = ['01','02','03','04','05','06','07','08','09',10,11,12]
        ANIOS = []
        fecha = date.today()
        for i in range(1940, fecha.year+1):
                ANIOS.append(i)
        ANIOS.sort(reverse=True)
        ent_cumpleanios_dia = ttk.Combobox(fr_ayuda, textvariable=self.var_cumpleanio_dia, width=3, state='readonly', font=self.FONT, values=DIAS)
        ent_cumpleanios_dia.pack(side=LEFT, pady=10)
        ent_cumpleanios_dia.bind('<FocusIn>', lambda evt: lb_cumpleanios.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_cumpleanios_dia.bind('<FocusOut>', lambda evt: lb_cumpleanios.config(bg="#F0F0F0", fg="#000000"))
        
        Label(fr_ayuda, text="/").pack(side=LEFT, padx=2, pady=10)
        ent_cumpleanios_mes = ttk.Combobox(fr_ayuda, textvariable=self.var_cumpleanio_mes, width=3, state='readonly', font=self.FONT, values=MESES)
        ent_cumpleanios_mes.pack(side=LEFT, pady=10)
        ent_cumpleanios_mes.bind('<FocusIn>', lambda evt: lb_cumpleanios.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_cumpleanios_mes.bind('<FocusOut>', lambda evt: lb_cumpleanios.config(bg="#F0F0F0", fg="#000000"))
        
        Label(fr_ayuda, text="/").pack(side=LEFT, padx=2, pady=10)
        ent_cumpleanios_anio = ttk.Combobox(fr_ayuda, textvariable=self.var_cumpleanio_anio, width=4, state='readonly', font=self.FONT, values=ANIOS)
        ent_cumpleanios_anio.pack(side=LEFT, pady=10)
        ent_cumpleanios_anio.bind('<FocusIn>', lambda evt: lb_cumpleanios.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_cumpleanios_anio.bind('<FocusOut>', lambda evt: lb_cumpleanios.config(bg="#F0F0F0", fg="#000000"))
        
        
        """ Pestania Informacion de Trabajo """
        fr_info_trabajo_apoyo = Frame(self.fr_info_trabajo)
        fr_info_trabajo_apoyo.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        lb_compania = Label(fr_info_trabajo_apoyo, text="Compania", font=self.FONT_SMALL, justify="left", anchor="w", width=21)
        lb_compania.grid(row=0, column=0, pady=2, sticky="w")
        lb_cargo = Label(fr_info_trabajo_apoyo, text="Cargo", font=self.FONT_SMALL, justify="left", anchor="w", width=21)
        lb_cargo.grid(row=1, column=0, pady=2, sticky="w")
        lb_datos_trabajo_telefono = Label(fr_info_trabajo_apoyo, text="Datos Trabajo: Telefono", font=self.FONT_SMALL, justify="left", anchor="w", width=21)
        lb_datos_trabajo_telefono.grid(row=2, column=0, pady=2, sticky="w")
        lb_datos_trabajo_email = Label(fr_info_trabajo_apoyo, text="Datos Trabajo: Email", font=self.FONT_SMALL, justify="left", anchor="w", width=21)
        lb_datos_trabajo_email.grid(row=3, column=0, pady=2, sticky="w")
        lb_datos_trabajo_paginaWeb = Label(fr_info_trabajo_apoyo, text="Datos Trabajo: Pagina Web", font=self.FONT_SMALL, justify="left", anchor="w", width=21)
        lb_datos_trabajo_paginaWeb.grid(row=4, column=0, pady=2, sticky="w")
        lb_trabajo = Label(fr_info_trabajo_apoyo, text="Trabajo", font=self.FONT_SMALL, justify="left", anchor="w", width=21)
        lb_trabajo.grid(row=5, column=0, pady=2, sticky="w")
        lb_datos_trabajo_movil = Label(fr_info_trabajo_apoyo, text="Datos Trabajo: Movil", font=self.FONT_SMALL, justify="left", anchor="w", width=21)
        lb_datos_trabajo_movil.grid(row=10, column=0, pady=2, sticky="w")
        
        self.var_compania = StringVar()
        self.var_cargo = StringVar()
        self.var_telefono_trabajo = StringVar()
        self.var_email_trabajo = StringVar()
        self.var_paginaWeb_trabajo = StringVar()
        self.var_direccion_trabajo = StringVar()
        self.var_ciudad_trabajo = StringVar()
        self.var_provincia_trabajo = StringVar()
        self.var_codigoPostal_trabajo = StringVar()
        self.var_pais_trabajo = StringVar()
        self.var_movil_trabajo = StringVar()
        
        ent_compania = Entry(fr_info_trabajo_apoyo, textvariable=self.var_compania, relief=FLAT, width=200, font=self.FONT)
        ent_compania.grid(row=0, column=1, pady=2, sticky="w")
        ent_compania.bind('<FocusIn>', lambda evt: lb_compania.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_compania.bind('<FocusOut>', lambda evt: lb_compania.config(bg="#F0F0F0", fg="#000000"))
        
        ent_cargo = Entry(fr_info_trabajo_apoyo, textvariable=self.var_cargo, relief=FLAT, width=200, font=self.FONT)
        ent_cargo.grid(row=1, column=1, pady=2, sticky="w")
        ent_cargo.bind('<FocusIn>', lambda evt: lb_cargo.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_cargo.bind('<FocusOut>', lambda evt: lb_cargo.config(bg="#F0F0F0", fg="#000000"))
        
        ent_trabajo_telefono = Entry(fr_info_trabajo_apoyo, textvariable=self.var_telefono_trabajo, relief=FLAT, width=200, font=self.FONT)
        ent_trabajo_telefono.grid(row=2, column=1, pady=2, sticky="w")
        ent_trabajo_telefono.bind('<FocusIn>', lambda evt: lb_datos_trabajo_telefono.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_trabajo_telefono.bind('<FocusOut>', lambda evt: lb_datos_trabajo_telefono.config(bg="#F0F0F0", fg="#000000"))
        
        ent_trabajo_email = Entry(fr_info_trabajo_apoyo, textvariable=self.var_email_trabajo, relief=FLAT, width=200, font=self.FONT)
        ent_trabajo_email.grid(row=3, column=1, pady=2, sticky="w")
        ent_trabajo_email.bind('<FocusIn>', lambda evt: lb_datos_trabajo_email.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_trabajo_email.bind('<FocusOut>', lambda evt: lb_datos_trabajo_email.config(bg="#F0F0F0", fg="#000000"))
        
        ent_trabajo_paginaWeb = Entry(fr_info_trabajo_apoyo, textvariable=self.var_paginaWeb_trabajo, relief=FLAT, width=200, font=self.FONT)
        ent_trabajo_paginaWeb.grid(row=4, column=1, pady=2, sticky="w")
        ent_trabajo_paginaWeb.bind('<FocusIn>', lambda evt: lb_datos_trabajo_paginaWeb.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_trabajo_paginaWeb.bind('<FocusOut>', lambda evt: lb_datos_trabajo_paginaWeb.config(bg="#F0F0F0", fg="#000000"))
        
        ent_datos_direccion = Entry(fr_info_trabajo_apoyo, textvariable=self.var_direccion_trabajo, relief=FLAT, width=200, font=self.FONT)
        self.var_direccion_trabajo.set("Direccion")
        ent_datos_direccion.grid(row=5, column=1, pady=2, sticky="w")
        ent_datos_direccion.bind('<FocusIn>', lambda evt: self.var_direccion_trabajo.set(''), ent_datos_direccion.config(fg="#000000"))
        ent_datos_direccion.bind('<FocusOut>', lambda evt: self.var_direccion_trabajo.set('Direccion'), ent_datos_direccion.config(fg="#546E7A"))
        ent_datos_direccion.bind('<Button-1>', lambda evt: self.evt_entry_Button_1(ent_datos_direccion,self.var_direccion_trabajo, text="Direccion"))
        ent_datos_ciudad = Entry(fr_info_trabajo_apoyo, textvariable=self.var_ciudad_trabajo, relief=FLAT, width=200, font=self.FONT)
        self.var_ciudad_trabajo.set("Ciudad")
        ent_datos_ciudad.grid(row=6, column=1, pady=2, sticky="w")
        ent_datos_ciudad.bind('<FocusIn>', lambda evt: self.var_ciudad_trabajo.set(''), ent_datos_ciudad.config(fg="#000000"))
        ent_datos_ciudad.bind('<FocusOut>', lambda evt: self.var_ciudad_trabajo.set('Ciudad'), ent_datos_ciudad.config(fg="#546E7A"))
        ent_datos_ciudad.bind('<Button-1>', lambda evt: self.evt_entry_Button_1(ent_datos_ciudad,self.var_ciudad_trabajo, text="Ciudad"))
        ent_datos_provincia = Entry(fr_info_trabajo_apoyo, textvariable=self.var_provincia_trabajo, relief=FLAT, width=200, font=self.FONT)
        self.var_provincia_trabajo.set("Provincia")
        ent_datos_provincia.grid(row=7, column=1, pady=2, sticky="w")
        ent_datos_provincia.bind('<FocusIn>', lambda evt: self.var_provincia_trabajo.set(''), ent_datos_provincia.config(fg="#000000"))
        ent_datos_provincia.bind('<FocusOut>', lambda evt: self.var_provincia_trabajo.set('Provincia'), ent_datos_provincia.config(fg="#546E7A"))
        ent_datos_provincia.bind('<Button-1>', lambda evt: self.evt_entry_Button_1(ent_datos_provincia,self.var_provincia_trabajo, text="Provincia"))
        ent_datos_codigoPostal = Entry(fr_info_trabajo_apoyo, textvariable=self.var_codigoPostal_trabajo, relief=FLAT, width=200, font=self.FONT)
        self.var_codigoPostal_trabajo.set("Codigo Postal")
        ent_datos_codigoPostal.grid(row=8, column=1, pady=2, sticky="w")
        ent_datos_codigoPostal.bind('<FocusIn>', lambda evt: self.var_codigoPostal_trabajo.set(''), ent_datos_codigoPostal.config(fg="#000000"))
        ent_datos_codigoPostal.bind('<FocusOut>', lambda evt: self.var_codigoPostal_trabajo.set('Codigo Postal'), ent_datos_codigoPostal.config(fg="#546E7A"))
        ent_datos_codigoPostal.bind('<Button-1>', lambda evt: self.evt_entry_Button_1(ent_datos_codigoPostal,self.var_codigoPostal_trabajo, text="Codigo Postal"))
        ent_datos_pais = Entry(fr_info_trabajo_apoyo, textvariable=self.var_pais_trabajo, relief=FLAT, width=200, font=self.FONT)
        self.var_pais_trabajo.set("Pais")
        ent_datos_pais.grid(row=9, column=1, pady=2, sticky="w")
        ent_datos_pais.bind('<FocusIn>', lambda evt: self.var_pais_trabajo.set(''), ent_datos_pais.config(fg="#000000"))
        ent_datos_pais.bind('<FocusOut>', lambda evt: self.var_pais_trabajo.set('Pais'), ent_datos_pais.config(fg="#546E7A"))
        ent_datos_pais.bind('<Button-1>', lambda evt: self.evt_entry_Button_1(ent_datos_pais,self.var_pais_trabajo, text="Pais"))
        ent_trabajo_movil = Entry(fr_info_trabajo_apoyo, textvariable=self.var_movil_trabajo, relief=FLAT, width=200, font=self.FONT)
        ent_trabajo_movil.grid(row=10, column=1, pady=2, sticky="w")
        ent_trabajo_movil.bind('<FocusIn>', lambda evt: lb_datos_trabajo_movil.config(bg=self.ACTIVE_BACKGROUND, fg="#FFFFFF"))
        ent_trabajo_movil.bind('<FocusOut>', lambda evt: lb_datos_trabajo_movil.config(bg="#F0F0F0", fg="#000000"))
        
        
        """ Pestania Nota """
        fr_nota = Frame(self.fr_info_nota)
        TextView(fr_nota)
        fr_nota.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        
        """ Pestania Fotografia """
        self.fr_info_foto.bind('<Configure>', self._resize_image)
        
        fr_foto_bottom = Frame(self.fr_info_foto)
        fr_foto_bottom.pack(side=BOTTOM, fill=X)
        
        btn_cargar_foto = ttk.Button(fr_foto_bottom, command=self.cargar_foto_contacto, text="Cargar")
        btn_cargar_foto.pack(side=LEFT, fill=X, padx=10, pady=10, anchor="center")
        btn_limpiar_foto = ttk.Button(fr_foto_bottom, command=self.limpiar_foto_contacto, text="Limpiar")
        btn_limpiar_foto.pack(side=LEFT, fill=X, padx=10, pady=10, anchor="center")
        
        self.file_foto = "" #Variable para la ruta de la foto
        
        self.lb_foto = Label(self.fr_info_foto)
        self.lb_foto.pack(fill=BOTH, expand=True, padx=100, pady=30, anchor="center")
        
        self.lb_foto.bind("<Double-1>", lambda evt: self.cargar_foto_contacto())
        
        """ Frame lateral derecha - bottom """
        self.btn_nuevo = Menubutton(self.right_bottom, text="Nuevo", image=self.imagenNuevo, compound=TOP,  
                                    bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_nuevo.pack(side=LEFT, padx=8, pady=2)
        self.btn_nuevo.bind("<Button-1>", lambda e: self.btn_nuevo_contacto())
        
        self.btn_guardar = Menubutton(self.right_bottom, text="Guardar", image=self.imagenGuardar, compound=TOP, 
                                      bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_guardar.pack(side=LEFT, padx=0, pady=2)
        self.btn_guardar.bind("<Button-1>", lambda e: self.btn_guardar_contacto())
        
        self.btn_eliminar = Menubutton(self.right_bottom, text="Eliminar", image=self.imagenEliminar, compound=TOP, state=DISABLED,
                                       disabledforeground="dark gray", bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_eliminar.pack(side=LEFT, padx=8, pady=2)
        self.btn_eliminar.bind("<Button-1>", lambda e: self.eliminar_contacto())
        
        self.btn_cancelar = Menubutton(self.right_bottom, text="Cancelar", image=self.imagenCancelar, compound=TOP,
                                       bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_cancelar.pack(side=LEFT, padx=0, pady=2)
        self.btn_cancelar.bind("<Button-1>", lambda e: self.btn_cancelar_contacto())
        
        self.btn_cerrar =Menubutton(self.right_bottom, text="Cerrar", image=self.imagenCerrar, compound=TOP,
                                    bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_cerrar.pack(side=RIGHT, padx=10, pady=2)
        self.btn_cerrar.bind("<Button-1>", lambda e: self.btn_salir_contacto())
       
        
    def btn_salir_contacto(self):
        self.panel.destroy()
    
    def btn_nuevo_contacto(self):
        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
        self.btn_guardar.bind("<Button-1>", lambda e: self.btn_guardar_contacto())
        self.btn_eliminar.config(state=DISABLED)
        self.notebook_contacto.select(self.fr_info_personal)
        self.ent_nombre.focus_set()
        self.limpiar_entradas()
        
    def btn_guardar_contacto(self):
        try:
            if self.var_nombre.get()=="" and self.var_apellido.get()=="":
                pass
            else:
                nombre = self.var_nombre.get()
                apellido = self.var_apellido.get()
                movil = self.var_movil.get()
                telefono = self.var_telefono.get()
                email = self.var_email.get()
                direccion = self.var_direccion.get()
                ciudad = self.var_ciudad.get()
                provincia = self.var_provincia.get()
                codigoPostal = self.var_codigoPostal.get()
                pais = self.var_pais.get()
                nickFacebook = self.var_nickFacebook.get()
                paginaWeb = self.var_paginaWeb.get()
                cumpleanios = self.var_cumpleanio_dia.get() + "/" + self.var_cumpleanio_mes.get() + "/" + self.var_cumpleanio_anio.get()
                compania = self.var_compania.get()
                cargo = self.var_cargo.get()
                telefono_trabajo = self.var_telefono_trabajo.get()
                email_trabajo = self.var_email_trabajo.get()
                paginaWeb_trabajo = self.var_paginaWeb_trabajo.get()
                direccion_trabajo = self.var_direccion_trabajo.get()
                ciudad_trabajo = self.var_ciudad_trabajo.get()
                provincia_trabajo = self.var_provincia_trabajo.get()
                codigoPostal_trabajo = self.var_codigoPostal_trabajo.get()
                pais_trabajo = self.var_pais_trabajo.get()
                movil_trabajo = self.var_movil_trabajo.get()
                nota = TextView.text.get(0.0,END)
                foto = self.file_foto
                
                if cumpleanios=="//":
                        cumpleanios = ""
                if direccion=="Direccion":
                        direccion = ""
                if ciudad=="Ciudad":
                        ciudad = ""
                if provincia=="Provincia":
                        provincia = ""
                if codigoPostal=="Codigo Postal":
                        codigoPostal = ""
                if pais=="Pais":
                        pais = ""
                if direccion_trabajo=="Direccion":
                        direccion_trabajo = ""
                if ciudad_trabajo=="Ciudad":
                        ciudad_trabajo = ""
                if provincia_trabajo=="Provincia":
                        provincia_trabajo = ""
                if codigoPostal_trabajo=="Codigo Postal":
                        codigoPostal_trabajo = ""
                if pais_trabajo=="Pais":
                        pais_trabajo = ""
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    cursor.execute('''INSERT INTO CONTACTO(NOMBRE,APELLIDO,MOVIL,TELEFONO,EMAIL,DIRECCION,CIUDAD,PROVINCIA,
                                                    CODIGO_POSTAL,PAIS,NICK_FACEBOOK,PAGINA_WEB,CUMPLEANIOS,COMPANIA,CARGO,
                                                    TELEFONO_TRABAJO,EMAIL_TRABAJO,PAGINA_WEB_TRABAJO,DIRECCION_TRABAJO,
                                                    CIUDAD_TRABAJO,PROVINCIA_TRABAJO,CODIGO_POSTAL_TRABAJO, PAIS_TRABAJO,
                                                    MOVIL_TRABAJO,NOTA,FOTO)
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(nombre,apellido, movil,telefono,
                                                    email,direccion,ciudad,provincia,codigoPostal,pais,nickFacebook,paginaWeb,
                                                    cumpleanios,compania,cargo,telefono_trabajo,email_trabajo,paginaWeb_trabajo,
                                                    direccion_trabajo,ciudad_trabajo,provincia_trabajo,codigoPostal_trabajo,
                                                    pais_trabajo,movil_trabajo,nota,foto))
                    con.commit()
                    
                    mensaje = Message(self.master, text="Contacto registrado", width=200, bg='#ffffe1', font=("Arial",10))
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(2000,lambda: mensaje.destroy())
                    
                    self.file_foto = "" #Limpia la ruta para la foto
                    self.contador_contactos_agregados_recientemente = self.contador_contactos_agregados_recientemente + 1
                    self.notebook_contacto.select(self.fr_info_personal)
                    self.listbox.delete(0,END)
                    self.listar_listbox()
                    self.limpiar_entradas()
                    
                    """Compara el dato agregado con lo de la lista existente para luego seleccionarlo en el listbox"""
                    dato_a_seleccionar = nombre+" "+apellido
                    for i in range(0,len(self.LISTA_CONTACTOS)):
                        if(self.LISTA_CONTACTOS[i] == dato_a_seleccionar):
                            self.listbox.selection_set(first=i)
                                        
                except sqlite3.IntegrityError:
                    con.rollback()
                except sqlite3.OperationalError:
                    con.rollback()
                finally:
                    con.close()
        except Exception:
            pass
        
    def btn_cancelar_contacto(self):
        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
        self.btn_guardar.bind("<Button-1>", lambda e: self.btn_guardar_contacto())
        self.btn_eliminar.config(state=DISABLED)
        self.notebook_contacto.select(self.fr_info_personal)
        self.limpiar_entradas()
    
    def editar_contacto(self):
        if len(self.LISTA_CONTACTOS)==0:
            pass
        else:
                index = self.listbox.curselection() #devuelve el indice de la seleccion
                seltext = self.listbox.get(index) #optine los dotos del indice seleccionado
                self.id_contacto = seltext #optenemos solo el codigo
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    SQL = """SELECT ID,NOMBRE,APELLIDO,MOVIL,TELEFONO,EMAIL,DIRECCION,CIUDAD,PROVINCIA,CODIGO_POSTAL,PAIS,
                                    NICK_FACEBOOK,PAGINA_WEB,CUMPLEANIOS,COMPANIA,CARGO,TELEFONO_TRABAJO,EMAIL_TRABAJO,
                                    PAGINA_WEB_TRABAJO,DIRECCION_TRABAJO,CIUDAD_TRABAJO,PROVINCIA_TRABAJO,CODIGO_POSTAL_TRABAJO,
                                    PAIS_TRABAJO,MOVIL_TRABAJO,NOTA,FOTO FROM CONTACTO WHERE NOMBRE ||' '|| APELLIDO='%s'""" % (self.id_contacto)
                    cursor.execute(SQL)
                    for i in cursor:
                        self.var_id.set(i[0])
                        self.var_nombre.set(i[1])
                        self.var_apellido.set(i[2])
                        self.var_movil.set(i[3])
                        self.var_telefono.set(i[4])
                        self.var_email.set(i[5])
                        self.var_direccion.set(i[6])
                        self.var_ciudad.set(i[7])
                        self.var_provincia.set(i[8])
                        self.var_codigoPostal.set(i[9])
                        self.var_pais.set(i[10])
                        self.var_nickFacebook.set(i[11])
                        self.var_paginaWeb.set(i[12])
                        CUMPLE_DIA = i[13]
                        self.var_cumpleanio_dia.set(CUMPLE_DIA[:2])
                        self.var_cumpleanio_mes.set(CUMPLE_DIA[3:5])
                        self.var_cumpleanio_anio.set(CUMPLE_DIA[6:])
                        self.var_compania.set(i[14])
                        self.var_cargo.set(i[15])
                        self.var_telefono_trabajo.set(i[16])
                        self.var_email_trabajo.set(i[17])
                        self.var_paginaWeb_trabajo.set(i[18])
                        self.var_direccion_trabajo.set(i[19])
                        self.var_ciudad_trabajo.set(i[20])
                        self.var_provincia_trabajo.set(i[21])
                        self.var_codigoPostal_trabajo.set(i[22])
                        self.var_pais_trabajo.set(i[23])
                        self.var_movil_trabajo.set(i[24])
                        TextView.text.delete(0.0, END)
                        TextView.text.insert(END, i[25])
                        self.file_foto = i[26]

                    if self.var_direccion.get() == "":
                        self.var_direccion.set("Direccion")
                    if self.var_ciudad.get() == "":
                        self.var_ciudad.set("Ciudad")
                    if self.var_provincia.get() == "":
                        self.var_provincia.set("Provincia")
                    if self.var_codigoPostal.get() == "":
                        self.var_codigoPostal.set("Codigo Postal")
                    if self.var_pais.get() == "":
                        self.var_pais.set("Pais")
                    if self.var_direccion_trabajo.get() == "":
                        self.var_direccion_trabajo.set("Direccion")
                    if self.var_ciudad_trabajo.get() == "":
                        self.var_ciudad_trabajo.set("Ciudad")
                    if self.var_provincia_trabajo.get() == "":
                        self.var_provincia_trabajo.set("Provincia")
                    if self.var_codigoPostal_trabajo.get() == "":
                        self.var_codigoPostal_trabajo.set("Codigo Postal")
                    if self.var_pais_trabajo.get() == "":
                        self.var_pais_trabajo.set("Pais")
                    if self.file_foto == "":
                        self.limpiar_foto_contacto()
                    else:
                        file_img = Image.open(self.file_foto)
                        self.foto_contacto_cargado = ImageTk.PhotoImage(file_img)
                        self.lb_foto.config(image=self.foto_contacto_cargado)
                        
                    self.btn_guardar.config(text="Editar", image=self.imagenEditar)
                    self.btn_guardar.bind("<Button-1>", lambda e: self.btn_editar_contacto())
                    self.btn_eliminar.config(state=NORMAL)
                    self.notebook_contacto.select(self.fr_info_personal)
                except sqlite3.IntegrityError:
                    pass
                except sqlite3.OperationalError:
                    pass
                finally:
                    con.close()
        
    def btn_editar_contacto(self):
        try:
                id = self.var_id.get()
                nombre = self.var_nombre.get()
                apellido = self.var_apellido.get()
                movil = self.var_movil.get()
                telefono = self.var_telefono.get()
                email = self.var_email.get()
                direccion = self.var_direccion.get()
                ciudad = self.var_ciudad.get()
                provincia = self.var_provincia.get()
                codigoPostal = self.var_codigoPostal.get()
                pais = self.var_pais.get()
                nickFacebook = self.var_nickFacebook.get()
                paginaWeb = self.var_paginaWeb.get()
                cumpleanios = self.var_cumpleanio_dia.get() + "/" + self.var_cumpleanio_mes.get() + "/" + self.var_cumpleanio_anio.get()
                compania = self.var_compania.get()
                cargo = self.var_cargo.get()
                telefono_trabajo = self.var_telefono_trabajo.get()
                email_trabajo = self.var_email_trabajo.get()
                paginaWeb_trabajo = self.var_paginaWeb_trabajo.get()
                direccion_trabajo = self.var_direccion_trabajo.get()
                ciudad_trabajo = self.var_ciudad_trabajo.get()
                provincia_trabajo = self.var_provincia_trabajo.get()
                codigoPostal_trabajo = self.var_codigoPostal_trabajo.get()
                pais_trabajo = self.var_pais_trabajo.get()
                movil_trabajo = self.var_movil_trabajo.get()
                nota = TextView.text.get(0.0,END)
                foto = self.file_foto
                
                if cumpleanios=="//":
                        cumpleanios = ""
                if direccion=="Direccion":
                        direccion = ""
                if ciudad=="Ciudad":
                        ciudad = ""
                if provincia=="Provincia":
                        provincia = ""
                if codigoPostal=="Codigo Postal":
                        codigoPostal = ""
                if pais=="Pais":
                        pais = ""
                if direccion_trabajo=="Direccion":
                        direccion_trabajo = ""
                if ciudad_trabajo=="Ciudad":
                        ciudad_trabajo = ""
                if provincia_trabajo=="Provincia":
                        provincia_trabajo = ""
                if codigoPostal_trabajo=="Codigo Postal":
                        codigoPostal_trabajo = ""
                if pais_trabajo=="Pais":
                        pais_trabajo = ""
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    SQL = """   UPDATE CONTACTO SET NOMBRE='%s',APELLIDO='%s',MOVIL='%s', TELEFONO='%s',EMAIL='%s',DIRECCION='%s',
                                        CIUDAD='%s',PROVINCIA='%s',CODIGO_POSTAL='%s',PAIS='%s',NICK_FACEBOOK='%s',PAGINA_WEB='%s',
                                        CUMPLEANIOS='%s',COMPANIA='%s',CARGO='%s',TELEFONO_TRABAJO='%s',EMAIL_TRABAJO='%s',
                                        PAGINA_WEB_TRABAJO='%s',DIRECCION_TRABAJO='%s',CIUDAD_TRABAJO='%s',PROVINCIA_TRABAJO='%s',
                                        CODIGO_POSTAL_TRABAJO='%s',PAIS_TRABAJO='%s',MOVIL_TRABAJO='%s',NOTA='%s',FOTO='%s'
                                WHERE ID=%s""" % (nombre,apellido, movil,telefono,email,direccion,ciudad,provincia,codigoPostal,
                                        pais,nickFacebook,paginaWeb,cumpleanios,compania,cargo,telefono_trabajo,email_trabajo,
                                        paginaWeb_trabajo,direccion_trabajo,ciudad_trabajo,provincia_trabajo,codigoPostal_trabajo,
                                        pais_trabajo,movil_trabajo,nota,foto,id)
                    cursor.execute(SQL)
                    con.commit()
                    
                    mensaje = Message(self.master, text="Contacto actualizado", width=200, bg='#ffffe1', font=("Arial",10))
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(2000,lambda: mensaje.destroy())
                    
                    self.file_foto = "" #Limpia la ruta para la foto
                    self.notebook_contacto.select(self.fr_info_personal)
                    self.listbox.delete(0,END)
                    self.listar_listbox()
                    self.limpiar_entradas()
                    
                    self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
                    self.btn_guardar.bind("<Button-1>", lambda e: self.btn_guardar_contacto())
                    self.btn_eliminar.config(state=DISABLED)
                    
                except sqlite3.IntegrityError:
                    con.rollback()
                except sqlite3.OperationalError:
                    con.rollback()
                finally:
                    con.close()
        except Exception:
            pass
        
    def eliminar_contacto(self):
        if len(self.LISTA_CONTACTOS)==0:
            pass
        else:
            try:
                index = self.listbox.curselection() #devuelve el indice de la seleccion
                seltext = self.listbox.get(index) #optine los dotos del indice seleccionado
                self.id_contacto = seltext #optenemos solo el codigo
                
                borrar = messagebox.askquestion(parent=self.master, icon='question', title="Confirmacion:", message="Realmente desea Eliminar?")
                if borrar=='yes':
                    try:
                        con = sqlite3.connect(r'DB\db.s3db')
                        cursor = con.cursor()
                        sql = "DELETE  FROM CONTACTO WHERE NOMBRE ||' '|| APELLIDO LIKE '"+self.id_contacto+"'"
                        cursor.execute(sql)
                        con.commit()

                        mensaje = Message(self.master, text="Contacto eliminado", width=200, bg='#ffffe1', font=("Arial",10))
                        mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                        mensaje.after(2000,lambda: mensaje.destroy())

                        self.contador_contactos_agregados_recientemente = self.contador_contactos_agregados_recientemente - 1

                        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
                        self.btn_guardar.bind("<Button-1>", lambda e: self.btn_guardar_contacto())
                        self.btn_eliminar.config(state=DISABLED)

                        self.notebook_contacto.select(self.fr_info_personal)
                        self.listbox.delete(0,END)
                        self.listar_listbox()
                        self.limpiar_entradas()

                    except sqlite3.IntegrityError:
                        con.rollback()
                    except sqlite3.OperationalError:
                        con.rollback()
                    finally:
                        con.close()
                else:
                    pass
            except Exception:
                pass
            
    def buscar_contacto(self):
        try:
            if self.var_ent_buscar.get() == "":
                self.listar_listbox()
            elif self.var_ent_buscar.get() == "Buscar contacto":
                pass
            else:
                self.id_contacto = self.var_ent_buscar.get()
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    sql = "SELECT NOMBRE ||' '|| APELLIDO FROM CONTACTO WHERE NOMBRE ||' '|| APELLIDO LIKE'"+"%"+self.id_contacto+"%"+"'" 
                    valor = cursor.execute(sql)
                    encontrado = False
                    if valor.fetchone() and encontrado==False:
                            sql = "SELECT NOMBRE ||' '|| APELLIDO FROM CONTACTO WHERE NOMBRE ||' '|| APELLIDO LIKE'"+"%"+self.id_contacto+"%"+"'" 
                            cursor.execute(sql)
                            encontrado = True
                            resultados = cursor.fetchall()
                            
                            self.listbox.delete(0,END)
                            for i in resultados:
                                self.listbox.insert(END, str(i[0]))
                            self.colorear_listbox(self.listbox, resultados)
                    else:
                            self.listbox.delete(0, END)
                            self.listbox.insert(END, "Ningun resultado coincide con su busqueda.")
                    
                    if self.listbox.get(0)=="Ningun resultado coincide con su busqueda.":
                        self.lb_records.config(text="Sin resultados")
                    else:
                        self.lb_records.config(text=str(self.listbox.size())+" Busqueda Contactos")
                                
                except sqlite3.IntegrityError:
                        pass
                except sqlite3.OperationalError:
                        pass
                finally:
                    con.close()
        except Exception:
            pass
            
    def ordenar_contacto_asc(self):
        self.LISTA_CONTACTOS = [] #Vacia la lista
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            sql = "SELECT NOMBRE ||' '|| APELLIDO FROM CONTACTO ORDER BY UPPER(NOMBRE), UPPER(APELLIDO)"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            self.listbox.delete(0,END)
            for i in resultados:
                self.LISTA_CONTACTOS.append(i[0])
            for registro in self.LISTA_CONTACTOS:
                    self.listbox.insert(END, registro)
            self.colorear_listbox(self.listbox, self.LISTA_CONTACTOS) #Colorea el listbox en paralelo
            
        except sqlite3.IntegrityError:
            pass
        finally:
            con.close()
           
    def ordenar_contacto_desc(self):
        self.LISTA_CONTACTOS = [] #Vacia la lista
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            sql = "SELECT NOMBRE ||' '|| APELLIDO FROM CONTACTO ORDER BY UPPER(NOMBRE) DESC, UPPER(APELLIDO) DESC"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            self.listbox.delete(0, END)
            for i in resultados:
                self.LISTA_CONTACTOS.append(i[0])
            for registro in self.LISTA_CONTACTOS:
                self.listbox.insert(END, registro)
            self.colorear_listbox(self.listbox, self.LISTA_CONTACTOS)
            
            
        except sqlite3.IntegrityError:
            pass
        finally:
            con.close()
            
 
    def listar_listbox(self):
        self.ordenar_contacto_asc() # Ordena y lista la lista
        
        if len(self.LISTA_CONTACTOS)==0:
            self.listbox.delete(0, END)
            self.listbox.insert(END, "Sin contactos.")
            
        self.lb_records.config(text=str(self.cantidad_contactos())+" Todos Contactos")
        
        if self.contador_contactos_agregados_recientemente == 0:
            self.var_contactos_recientemente.set("")
        else:
            self.var_contactos_recientemente.set(str(self.contador_contactos_agregados_recientemente)+" Agregado recientemente.")
        
      
    def vaciar_lista_contactos(self):
        if len(self.LISTA_CONTACTOS)==0:
                mensaje = Message(self.master, text="Lista de Contactos vacio.", width=200, bg='#ffffe1', font=("Arial",10))
                mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                mensaje.after(3000,lambda: mensaje.destroy())
        else:
            borrar = messagebox.askquestion(parent=self.master, title="Confirmacion:", message="Realmente desea vaciar la lista de Contactos?")
            if borrar=='yes':
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    SQL = "DELETE  FROM CONTACTO"
                    cursor.execute(SQL)
                    con.commit()

                    mensaje = Message(self.master, text="Se ha vaciado la lista de Contactos.", width=200, bg='#ffffe1', font=("Arial",10))
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(3000,lambda: mensaje.destroy())
                    
                    self.contador_contactos_agregados_recientemente = 0
                    
                    self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
                    self.btn_guardar.bind("<Button-1>", lambda e: self.btn_guardar_contacto())
                    self.btn_eliminar.config(state=DISABLED)
                    
                    self.notebook_contacto.select(self.fr_info_personal)
                    self.listbox.delete(0,END)
                    self.listar_listbox()
                    self.limpiar_entradas()

                except sqlite3.IntegrityError:
                    con.rollback()
                except sqlite3.OperationalError:
                    con.rollback()
                finally:
                    con.close()
            else:
                pass
        
        
    def limpiar_entradas(self):        
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_movil.set("")
        self.var_telefono.set("")
        self.var_email.set("")
        self.var_direccion.set("Direccion")
        self.var_ciudad.set("Ciudad")
        self.var_provincia.set("Provincia")
        self.var_codigoPostal.set("Codigo Postal")
        self.var_pais.set("Pais")
        self.var_nickFacebook.set("")
        self.var_paginaWeb.set("")
        self.var_cumpleanio_dia.set("")
        self.var_cumpleanio_mes.set("")
        self.var_cumpleanio_anio.set("")
        self.var_compania.set("")
        self.var_cargo.set("")
        self.var_telefono_trabajo.set("")
        self.var_email_trabajo.set("")
        self.var_paginaWeb_trabajo.set("")
        self.var_direccion_trabajo.set("Direccion")
        self.var_ciudad_trabajo.set("Ciudad")
        self.var_provincia_trabajo.set("Provincia")
        self.var_codigoPostal_trabajo.set("Codigo Postal")
        self.var_pais_trabajo.set("Pais")
        self.var_movil_trabajo.set("")
        TextView.text.delete(0.0, END)
        self.limpiar_foto_contacto()
        
    
        
    """---------------------------------------------------------------"""
    def cargar_foto_contacto(self):
        self.file_foto = filedialog.askopenfilename(title='Seleccionar Fotografia',filetypes=[("All", "*.jpg; *.png; *.gif; *.jpe; *.jpeg; *.jfif"),("JPEG", "*.jpg; *.jpe; *.jpeg; *.jfif"),("PNG", "*.png"),("GIF", "*.gif")])
        if self.file_foto:
            self.file_img = Image.open(self.file_foto)
            self.img_copy = self.file_img.copy()
            self.foto = ImageTk.PhotoImage(self.file_img)
            self.lb_foto.config(image=self.foto)
        else:
            pass
            
        return self.file_foto
        
    def limpiar_foto_contacto(self):
        self.lb_foto.destroy()
        self.file_foto = ""
        self.lb_foto = Label(self.fr_info_foto)
        self.lb_foto.pack(fill=BOTH, expand=True, padx=100, pady=30, anchor="center")
        self.lb_foto.bind("<Double-1>", lambda evt: self.cargar_foto_contacto())
        
    def _resize_image(self, event):
        try:
            new_width = event.width
            new_height = event.height
            
            if self.file_foto:
                self.file_img = self.img_copy.resize((new_width, new_height))
                #self.file_img.rotate(45, expand=0).show()
                self.background_image = ImageTk.PhotoImage(self.file_img)
                self.lb_foto.configure(image=self.background_image)
            else:
                pass
        except Exception as e:
            print(e)
        
        
        
    """---------------------------------------------------------------"""
    
    def opciones_anticlick_listbox(self, *evento):
        evento = evento[0]
        self.listbox_x, self.listbox_y = evento.x_root, evento.y_root
        self.menu_opc_lista.post(self.listbox_x, self.listbox_y)
        
        
    
    """---------------------------------------------------------------"""
    """                     Metodos de apoyo                          """
    """---------------------------------------------------------------"""
    def colorear_listbox(self, listbox, lista):
        for i in range(0,len(lista),2):
            listbox.itemconfigure(i, background='#3A3F46')
            
    def evt_entry_Button_1(self, widget, textvariable, text=""):
        if textvariable.get()=="":
            widget.bind('<FocusOut>', lambda evt: textvariable.set(text), widget.config(fg="#546E7A"))
        elif len(textvariable.get()) >= 0:
            widget.bind('<FocusOut>', lambda evt: textvariable.set(textvariable.get()), widget.config(fg="#000000"))
            
    
    """---------------------------------------------------------------"""
    """                     Metodos con retono                        """
    """---------------------------------------------------------------"""
    def cantidad_contactos(self):
        cant_contactos = 0
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            cursor.execute("SELECT COUNT(ID) FROM CONTACTO")
            for i in cursor:
                cant_contactos = i[0]
            con.close()
        except:
            pass
        return cant_contactos
        print(cant_contactos)
    
    
        
    
'''
if __name__ == "__main__":
    Contacto()
'''