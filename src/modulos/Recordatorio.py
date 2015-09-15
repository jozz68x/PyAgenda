
__author__="Jose Diaz"
__date__ ="$23/02/2015 08:52:56 AM$"

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime
import sqlite3
import winsound

from modulos.centerWindow import center_toplevel

class Recordatorio(object):
    
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
        self.LISTA_RECORDATORIOS = []
        self.contador_recordatorios_agregados_recientemente = 0
        self.master = master
        self.ahora = datetime.now()
        
        self.curtime_hh = ""
        self.curtime_mm = ""
        self.curtime_ss = ""
        
        self.FORMATO = ("AM", "PM")
        
        self.HORA_ACTUAL = IntVar()
        self.MINUTO_ACTUAL = IntVar()
        self.SEGUNDO_ACTUAL = IntVar()
        self.FORMATO_ACTUAL = StringVar()
        
        self.cargar_imagenes()
        self.frames_principales()
        self.barra_lateral()
        self.interfaz()
        self.listar_listbox()
        self.hora()
        self.minuto()
        self.segundo()
        self.procesar_recordatorio()
        
        
    def cargar_imagenes(self):
        self.imagenIconContacto = ImageTk.PhotoImage(Image.open(r"image\Icon_despertador.png"))
        
        self.imagenActivado = ImageTk.PhotoImage(Image.open(r"image\activado.png"))
        self.imagenDesactivado = ImageTk.PhotoImage(Image.open(r"image\desactivado.png"))
        
        self.imagenBuscar = ImageTk.PhotoImage(Image.open(r"image\buscar.png"))
        self.imagenOpcionOrdenar = ImageTk.PhotoImage(Image.open(r"image\opcion_ordenar.png"))
        self.imagenOpcionOrdenar2 = ImageTk.PhotoImage(Image.open(r"image\opcion_ordenar_2.png"))
        
        self.imagenNuevo = ImageTk.PhotoImage(Image.open(r"image\add.png"))
        self.imagenGuardar = ImageTk.PhotoImage(Image.open(r"image\guardar.png"))
        self.imagenEditar = ImageTk.PhotoImage(Image.open(r"image\editar.png"))
        self.imagenCancelar = ImageTk.PhotoImage(Image.open(r"image\cancelar.png"))
        self.imagenEliminar = ImageTk.PhotoImage(Image.open(r"image\eliminar.png"))
        self.imagenCerrar = ImageTk.PhotoImage(Image.open(r"image\cerrar.png"))
        
        self.imagenPlay = ImageTk.PhotoImage(Image.open(r"image\play.png"))
        self.imagenStop = ImageTk.PhotoImage(Image.open(r"image\stop.png"))
    
    def frames_principales(self):
        """ Panel general para la ventana Recordatorio"""
        self.panel = PanedWindow(self.master, bg="#262A2E", orient=HORIZONTAL, relief=FLAT, bd=0, opaqueresize=False)
        self.panel.pack(fill=BOTH, expand=True)
        
        """ Frame lateral izquierda """
        self.fr_left = Frame(self.panel, bg=self.BACKGROUND_MENU_2)
        self.fr_left.pack(side=LEFT, fill=Y, expand=True)
        
        """ Frame lateral derecha """
        self.fr_right = Frame(self.panel, bg=self.BACKGROUND)
        self.fr_right.pack(side=LEFT, fill=BOTH, expand=True)
        
        """ Frame lateral derecha - top """
        self.fr_right_top = Frame(self.fr_right, bg=self.BACKGROUND)
        self.fr_right_top.pack(fill=X, side=TOP)
        
        """ Frame lateral derecha - both """
        self.fr_right_both = Frame(self.fr_right)
        self.fr_right_both.pack(fill=BOTH, expand=True, padx=8, pady=1)
        
        """ Frame lateral derecha - bottom """
        self.right_bottom = Frame(self.fr_right, bg=self.BACKGROUND)
        self.right_bottom.pack(side=BOTTOM, fill=X)
        
        self.panel.add(self.fr_left)
        self.panel.add(self.fr_right)
    
    def barra_lateral(self):
        """Frame izquierda"""
        fr_left_top = Frame(self.fr_left, bg="#262A2E")
        fr_left_top.pack(side=TOP, fill=X)
        fr_left_both = Frame(self.fr_left, bg=self.BACKGROUND_MENU_2)
        fr_left_both.pack(fill=BOTH, expand=True, padx=1)
        
        self.var_recordatorios_recientemente = StringVar()
        lb_records = Label(fr_left_both, textvariable=self.var_recordatorios_recientemente, font=(self.FONT[0], 9), bg=fr_left_both['bg'], fg=self.BACKGROUND_MENU_INTO)
        lb_records.pack(side=BOTTOM, fill=X, anchor="center")
        
        self.lb_records = Button(fr_left_both, image=self.imagenIconContacto, compound=TOP, relief=FLAT, bd=0, font=self.FONT, 
                bg=fr_left_both['bg'], fg=self.BACKGROUND_MENU_INTO, activebackground=fr_left_both['bg'], activeforeground=self.BACKGROUND_MENU_INTO)
        self.lb_records.pack(side=BOTTOM, fill=X, anchor="center")
        
        self.var_ent_buscar = StringVar()
        self.var_ent_buscar.set('Buscar recordatorio')
        
        ent_buscar = Entry(fr_left_top, width=30, textvariable=self.var_ent_buscar, bg="#99A2AE", font=self.FONT, relief=FLAT, bd=1)
        btn_buscar_recordatorio = Menubutton(fr_left_top, image=self.imagenBuscar, relief=FLAT, bg=ent_buscar['bg'], activebackground="#009846")
        btn_buscar_recordatorio.place(in_=ent_buscar, relx=1.0, rely=0, x=21, y=-1, anchor=NE)
        btn_buscar_recordatorio.bind('<Button-1>', lambda e: self.buscar_contacto())
        ent_buscar.pack(anchor="w", padx=5, pady=10)
        ent_buscar.bind('<Button-1>', lambda evt: self.listar_listbox())
        ent_buscar.bind('<Key>', lambda evt: self.buscar_contacto())
        ent_buscar.bind('<Return>', lambda evt: self.buscar_contacto())
        ent_buscar.bind('<Enter>', lambda evt: self.var_ent_buscar.set(''))
        ent_buscar.bind('<Leave>', lambda evt: self.var_ent_buscar.set('Buscar recordatorio'), ent_buscar.config(fg="#546E7A"))
        ent_buscar.bind('<FocusIn>', lambda evt: ent_buscar.config(fg="#000000"))
        ent_buscar.bind('<FocusOut>', lambda evt: ent_buscar.config(fg="#546E7A"))
        
        btn_opc_ordenar = Menubutton(fr_left_top, image=self.imagenOpcionOrdenar, bg=fr_left_top['bg'], activebackground=fr_left_top['bg'], relief=FLAT, bd=0, direction='flush')
        btn_opc_ordenar.place(in_=fr_left_top, relx=1, rely=0, x=2, y=4, anchor=NE, bordermode="outside")
        menu_ord_contactos = Menu(btn_opc_ordenar, tearoff=0, font=self.FONT, activebackground=self.ACTIVE_BACKGROUND, activeforeground = "#FFFFFF")
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
        
        '''
        style = ttk.Style()
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])
        style.configure('.',              # every class of object
                        relief = 'flat',  # flat ridge for separator
                        borderwidth = 0,  # zero width for the border
                )
        tree = ttk.Treeview(fr_left_both, show="headings")
        tree.pack(side=LEFT, fill=BOTH, expand=1)
        
        tree["columns"]=("Hora","Titulo")
        tree.column("Hora", width=100)
        tree.column("Titulo", width=100)
        tree.heading("Hora", text="Hora")
        tree.heading("Titulo", text="Titulo")
        '''
        
        #Menu de Opciones Anticlick en ListBox
        self.menu_opc_lista = Menu(self.listbox, tearoff=0, font=self.FONT, activebackground=self.ACTIVE_BACKGROUND, activeforeground = "#FFFFFF")
        self.menu_opc_lista.add_command(label = "Ver evento", command=self.reloj)
        self.menu_opc_lista.add_command(label = "Ver detalles", command=self.mostrar_todos_datos)
        self.menu_opc_lista.add_separator()
        self.menu_opc_lista.add_command(label = "Activar", command=self.activar_recordatorio)
        self.menu_opc_lista.add_command(label = "Desactivar", command=self.desactivar_recordatorio)
        self.menu_opc_lista.add_separator()
        self.menu_opc_lista.add_command(label = "Editar", command=self.mostrar_todos_datos)
        self.menu_opc_lista.add_command(label = "Eliminar", command=self.eliminar_recordatorio)
        
        self.listbox.bind("<ButtonRelease-3>", self.opciones_anticlick_listbox)
        self.listbox.bind("<Double-1>", lambda e: self.mostrar_todos_datos())
        
        
    def validar_valores_estado_recordatorio(self, event):
        if self.estado_recordatorio==True:
            self.var_estado_recordatorio = "Desactivado"
            self.chek_estado_recordatorio.config(image=self.imagenDesactivado, text="Desactivado")
            self.estado_recordatorio = False
        else:
            self.var_estado_recordatorio = "Activado"
            self.chek_estado_recordatorio.config(image=self.imagenActivado, text="Activado")
            self.estado_recordatorio = True
            
    
    def interfaz(self):
        """ Frame lateral derecha - both """
        self.estado_recordatorio = True
        self.var_estado_recordatorio = "Activado"
        
        self.chek_estado_recordatorio = Label(self.fr_right_top, text="Activado", image=self.imagenActivado, compound=RIGHT, justify=LEFT, anchor=E,
                bg=self.fr_right_top['bg'])
        self.chek_estado_recordatorio.pack(side=RIGHT, padx=8, pady=2)
        self.chek_estado_recordatorio.bind("<Button-1>", self.validar_valores_estado_recordatorio)
        
        
        self.lb_titulo_detalle = Label(self.fr_right_top, text="Nuevo Recordatorio", font=(self.FONT[0], 14), anchor=W, justify=LEFT, width=80,
                bg=self.fr_right_top['bg'], fg="#000000")
        self.lb_titulo_detalle.pack(side=LEFT, fill=X, padx=8, pady=2)
        
        
        """ Frame lateral derecha - both """
        fr_contorno = Frame(self.fr_right_both)
        fr_contorno.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        lb_titulo = Label(fr_contorno, text="Titulo", font=(self.FONT[0], 9), justify="left", anchor="w", width=25)
        lb_titulo.grid(row=0, column=0, pady=2, sticky="w")
        lb_hora = Label(fr_contorno, text="Hora", font=(self.FONT[0], 9), justify="left", anchor="w", width=25)
        lb_hora.grid(row=1, column=0, pady=2, sticky="w")
        lb_sonido = Label(fr_contorno, text="Opciones", font=(self.FONT[0], 9), justify="left", anchor="w", width=25)
        lb_sonido.grid(row=2, column=0, pady=2, sticky="w")
        lb_duracion = Label(fr_contorno, text="Duracion de postergacion", font=(self.FONT[0], 9), justify="left", anchor="w", width=25)
        lb_duracion.grid(row=3, column=0, pady=2, sticky="w")
        
        
        self.var_id = IntVar()
        
        self.var_titulo = StringVar()
        self.var_hora = StringVar()
        self.var_minuto = StringVar()
        self.var_segundo = StringVar()
        self.var_formato = StringVar()
        self.var_repetir = StringVar()
        self.var_sonido = StringVar()
        self.var_duracion = IntVar()
        
        self.ent_titulo = ttk.Entry(fr_contorno, textvariable=self.var_titulo, font=self.FONT)
        self.ent_titulo.grid(row=0, column=1, pady=2, sticky=W+E)
        self.ent_titulo.bind("<KeyPress>", lambda evt: self.lb_titulo_detalle.config(text=self.var_titulo.get()))
        
        fr_hora_ayuda = ttk.Frame(fr_contorno)
        fr_hora_ayuda.grid(row=1, column=1, pady=2, sticky="w")
        
        self.spb_hora = Spinbox(fr_hora_ayuda, textvariable=self.var_hora, width=4, font=(self.FONT[0],11),
                relief=FLAT, bd=0, buttondownrelief=FLAT, buttonup=FLAT, format='%2.0f',
                buttonbackground="#EBEBEB", insertwidth=1.0,
                highlightbackground="#ACACAC", highlightcolor="#64B5F6", highlightthickness=1,
                from_=0.0, to=24.0, increment=1,
                repeatdelay=200, repeatinterval=50)
        self.var_hora.set(self.ahora.hour)
        self.spb_hora.pack(side=LEFT, padx=0, pady=0)
        
        self.spb_minuto = Spinbox(fr_hora_ayuda, textvariable=self.var_minuto, width=4, font=(self.FONT[0],11),
                relief=FLAT, bd=0, buttondownrelief=FLAT, buttonup=FLAT, format='%2.0f',
                buttonbackground="#EBEBEB", insertwidth=1,
                highlightbackground="#ACACAC", highlightcolor="#64B5F6", highlightthickness=1,
                from_=0.0, to=59.0, increment=1,
                repeatdelay=200, repeatinterval=50)
        self.var_minuto.set(self.ahora.minute)
        self.spb_minuto.pack(side=LEFT, padx=5, pady=0)
        
        self.spb_segundo = Spinbox(fr_hora_ayuda, textvariable=self.var_segundo, width=4, font=(self.FONT[0],11),
                relief=FLAT, bd=0, buttondownrelief=FLAT, buttonup=FLAT, justify=LEFT, format='%2.0f',
                buttonbackground="#EBEBEB", insertwidth=1,
                highlightbackground="#ACACAC", highlightcolor="#64B5F6", highlightthickness=1,
                from_=0.0, to=59.0, increment=1, insertofftime=400, insertontime=600,
                repeatdelay=200, repeatinterval=50)
        self.var_segundo.set(self.ahora.second)
        self.spb_segundo.pack(side=LEFT, padx=0, pady=0)
        
        self.spb_formato = Spinbox(fr_hora_ayuda, textvariable=self.var_formato, width=4, font=(self.FONT[0],11), state="readonly",
                relief=FLAT, bd=0, buttondownrelief=FLAT, buttonup=FLAT, insertwidth=1,
                readonlybackground="#FFFFFF", buttonbackground="#EBEBEB",
                highlightbackground="#ACACAC", highlightcolor="#64B5F6", highlightthickness=1,
                values=self.FORMATO)
        self.spb_formato.pack(side=LEFT, padx=5, pady=0)
        
        btn_sonido = ttk.Button(fr_contorno, text="Avanzado...", command=self.ventana_recordatorio_avanzado)
        btn_sonido.grid(row=2, column=1, pady=2, sticky=W)
        
        cbx_duracion = ttk.Combobox(fr_contorno, textvariable=self.var_duracion, width=10, state='readonly', font=self.FONT, values=(5,10,15,20,25,30))
        self.var_duracion.set(5)
        cbx_duracion.grid(row=3, column=1, pady=2, sticky=W)
        
        lb_duracion_minutos = Label(fr_contorno, text="Minutos", font=(self.FONT[0], 9), justify="left", anchor="w")
        lb_duracion_minutos.grid(row=3, column=1, pady=2, sticky=E, rowspan=4)
        
        self.var_scale = IntVar()
        self.scale_duracion = ttk.Scale(fr_contorno, command=self.update_duracion_postergacion, variable=self.var_scale, orient=HORIZONTAL, value=5, length=300, from_=5, to=30)
        self.scale_duracion.grid(pady=10, padx=10, sticky=W+E)
        
        """ Frame lateral derecha - bottom """
        self.btn_nuevo = Menubutton(self.right_bottom, text="Nuevo", image=self.imagenNuevo, compound=TOP,  
                                    bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_nuevo.pack(side=LEFT, padx=8, pady=2)
        self.btn_nuevo.bind("<Button-1>", lambda evt: self.btn_nuevo_recordatorio())
        
        self.btn_guardar = Menubutton(self.right_bottom, text="Guardar", image=self.imagenGuardar, compound=TOP, 
                                      bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_guardar.pack(side=LEFT, padx=0, pady=2)
        self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_recordatorio())
        
        self.btn_eliminar = Menubutton(self.right_bottom, text="Eliminar", image=self.imagenEliminar, compound=TOP, state=DISABLED,
                                       disabledforeground="dark gray", bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_eliminar.pack(side=LEFT, padx=8, pady=2)
        self.btn_eliminar.bind("<Button-1>", lambda evt: self.eliminar_recordatorio())
        
        self.btn_cancelar = Menubutton(self.right_bottom, text="Cancelar", image=self.imagenCancelar, compound=TOP,
                                       bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_cancelar.pack(side=LEFT, padx=0, pady=2)
        self.btn_cancelar.bind("<Button-1>", lambda evt: self.btn_cancelar_recordatorio())
        
        self.btn_cerrar = Menubutton(self.right_bottom, text="Cerrar", image=self.imagenCerrar, compound=TOP,
                                    bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_cerrar.pack(side=RIGHT, padx=10, pady=2)
        self.btn_cerrar.bind("<Button-1>", lambda evt: self.btn_salir_recordatorio())
        
    def update_duracion_postergacion(self, value):
        valor = self.var_scale.get()
        if int(valor) != value:
            self.var_duracion.set(round(valor))
            
        self.scale_duracion.after(1000, lambda: self.update_duracion_postergacion(value))
            
        
    def btn_salir_recordatorio(self):
        self.panel.destroy()
        
    def btn_nuevo_recordatorio(self):
        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
        self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_recordatorio())
        self.btn_eliminar.config(state=DISABLED)
        self.ent_titulo.focus_set()
        self.limpiar_entradas()
        
    def btn_guardar_recordatorio(self):
            if self.var_titulo.get()=="":
                pass
            else:
                titulo = self.var_titulo.get()
                hora_recordar = self.var_hora.get()+":"+self.var_minuto.get()+":"+self.var_segundo.get()
                estado = self.var_estado_recordatorio
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    cursor.execute("INSERT INTO RECORDATORIO(TITULO, HORA_RECORDAR, ESTADO) VALUES(?,?,?)", (titulo,hora_recordar, estado))
                    con.commit()
                    
                    mensaje = Message(self.master, text="Recordatorio registrado", width=200, bg='#ffffe1', font=self.FONT)
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(2000,lambda: mensaje.destroy())
                    
                    self.contador_recordatorios_agregados_recientemente = self.contador_recordatorios_agregados_recientemente + 1
                    self.listbox.delete(0,END)
                    self.listar_listbox()
                    self.limpiar_entradas()
                    
                    """Compara el dato agregado con lo de la lista existente para luego seleccionarlo en el listbox"""
                    dato_a_seleccionar = hora_recordar+"    "+titulo
                    for i in range(0,len(self.LISTA_RECORDATORIOS)):
                        if(self.LISTA_RECORDATORIOS[i] == dato_a_seleccionar):
                            self.listbox.selection_set(first=i)
                                        
                except sqlite3.IntegrityError:
                    con.rollback()
                except sqlite3.OperationalError:
                    con.rollback()
                finally:
                    con.close()
        
    def btn_cancelar_recordatorio(self):
        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
        self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_recordatorio())
        self.btn_eliminar.config(state=DISABLED)
        self.limpiar_entradas()
        
    def activar_recordatorio(self):
        try:
            index = self.listbox.curselection()
            seltext = self.listbox.get(index)
            self.id_recordatorio = seltext
            try:
                con = sqlite3.connect(r'DB\db.s3db')
                cursor = con.cursor()
                SQL = """UPDATE RECORDATORIO SET ESTADO='Activado'
                                 WHERE HORA_RECORDAR ||'    '|| TITULO='%s'""" % (self.id_recordatorio)
                cursor.execute(SQL)
                con.commit()

                mensaje = Message(self.master, text="Recordatorio activado", width=200, bg='#ffffe1', font=self.FONT)
                mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                mensaje.after(2000,lambda: mensaje.destroy())

                self.mostrar_todos_datos()

            except sqlite3.IntegrityError:
                con.rollback()
            except sqlite3.OperationalError:
                con.rollback()
            finally:
                con.close()
        except Exception:
                pass
            
    def desactivar_recordatorio(self):
        try:
            index = self.listbox.curselection()
            seltext = self.listbox.get(index)
            self.id_recordatorio = seltext
            try:
                con = sqlite3.connect(r'DB\db.s3db')
                cursor = con.cursor()
                SQL = """UPDATE RECORDATORIO SET ESTADO='Desactivado'
                                 WHERE HORA_RECORDAR ||'    '|| TITULO='%s'""" % (self.id_recordatorio)
                cursor.execute(SQL)
                con.commit()

                mensaje = Message(self.master, text="Recordatorio desactivado", width=200, bg='#ffffe1', font=self.FONT)
                mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                mensaje.after(2000,lambda: mensaje.destroy())

                self.mostrar_todos_datos()

            except sqlite3.IntegrityError:
                con.rollback()
            except sqlite3.OperationalError:
                con.rollback()
            finally:
                con.close()
        except Exception:
                pass
    
    def mostrar_todos_datos(self):
        if len(self.LISTA_RECORDATORIOS)==0:
            pass
        else:
                index = self.listbox.curselection() #devuelve el indice de la seleccion
                seltext = self.listbox.get(index) #optine los dotos del indice seleccionado
                self.id_recordatorio = seltext #optenemos solo el codigo
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    SQL = """SELECT ID, TITULO, HORA_RECORDAR, ESTADO FROM RECORDATORIO WHERE HORA_RECORDAR ||'    '|| TITULO='%s'""" % (self.id_recordatorio)
                    cursor.execute(SQL)
                    for i in cursor:
                        self.var_id.set(i[0])
                        self.var_titulo.set(i[1])
                        dato_hora = i[2]
                        find = dato_hora.find(":")
                        find2 = dato_hora.rfind(":")
                        hora = dato_hora[:find]
                        minuto = dato_hora[find+1:find2]
                        segundo = dato_hora[find2+1:]
                        self.var_hora.set(hora)
                        self.var_minuto.set(minuto)
                        self.var_segundo.set(segundo)
                        estado = i[3]
                        if estado == "Activado":
                            self.var_estado_recordatorio = "Activado"
                            self.chek_estado_recordatorio.config(image=self.imagenActivado, text="Activado")
                        else:
                            self.var_estado_recordatorio = "Desactivado"
                            self.chek_estado_recordatorio.config(image=self.imagenDesactivado, text="Desactivado")
                        
                    self.lb_titulo_detalle.config(text=self.var_titulo.get())
                    
                    self.btn_guardar.config(text="Editar", image=self.imagenEditar)
                    self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_editar_recordatorio())
                    self.btn_eliminar.config(state=NORMAL)
                except sqlite3.IntegrityError:
                    pass
                except sqlite3.OperationalError:
                    pass
                finally:
                    con.close()
        
    def btn_editar_recordatorio(self):
        try:
                id = self.var_id.get()
                titulo = self.var_titulo.get()
                hora_recordar = self.var_hora.get()+":"+self.var_minuto.get()+":"+self.var_segundo.get()
                estado = self.var_estado_recordatorio
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    SQL = """UPDATE RECORDATORIO SET TITULO='%s', HORA_RECORDAR='%s', ESTADO='%s'
                             WHERE ID=%s""" % (titulo,hora_recordar, estado,id)
                    cursor.execute(SQL)
                    con.commit()
                    
                    mensaje = Message(self.master, text="Recordatorio actualizado", width=200, bg='#ffffe1', font=self.FONT)
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(2000,lambda: mensaje.destroy())
                    
                    self.listbox.delete(0,END)
                    self.listar_listbox()
                    self.limpiar_entradas()
                    
                    self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
                    self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_recordatorio())
                    self.btn_eliminar.config(state=DISABLED)
                    
                except sqlite3.IntegrityError:
                    con.rollback()
                except sqlite3.OperationalError:
                    con.rollback()
                finally:
                    con.close()
        except Exception:
            pass
        
    def eliminar_recordatorio(self):
        if len(self.LISTA_RECORDATORIOS)==0:
            pass
        else:
            try:
                index = self.listbox.curselection() #devuelve el indice de la seleccion
                seltext = self.listbox.get(index) #optine los dotos del indice seleccionado
                self.id_recordatorio = seltext #optenemos solo el codigo
                
                borrar = messagebox.askquestion(parent=self.master, icon='question', title="Confirmacion:", message="Realmente desea Eliminar?")
                if borrar=='yes':
                    try:
                        con = sqlite3.connect(r'DB\db.s3db')
                        cursor = con.cursor()
                        sql = "DELETE  FROM RECORDATORIO WHERE HORA_RECORDAR ||'    '|| TITULO LIKE '"+self.id_recordatorio+"'"
                        cursor.execute(sql)
                        con.commit()

                        mensaje = Message(self.master, text="Recordatorio eliminado", width=200, bg='#ffffe1', font=self.FONT)
                        mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                        mensaje.after(2000,lambda: mensaje.destroy())
 
                        self.contador_recordatorios_agregados_recientemente = self.contador_recordatorios_agregados_recientemente - 1

                        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
                        self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_recordatorio())
                        self.btn_eliminar.config(state=DISABLED)

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
            elif self.var_ent_buscar.get() == "Buscar recordatorio":
                pass
            else:
                self.id_recordatorio = self.var_ent_buscar.get()
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    sql = "SELECT HORA_RECORDAR ||'    '|| TITULO FROM RECORDATORIO WHERE HORA_RECORDAR ||'    '|| TITULO LIKE'"+"%"+self.id_recordatorio+"%"+"'" 
                    valor = cursor.execute(sql)
                    encontrado = False
                    if valor.fetchone() and encontrado==False:
                            sql = "SELECT HORA_RECORDAR ||'    '|| TITULO FROM RECORDATORIO WHERE HORA_RECORDAR ||'    '|| TITULO LIKE'"+"%"+self.id_recordatorio+"%"+"'" 
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
                        self.lb_records.config(text=str(self.listbox.size())+" Busqueda Recordatorio")
                                
                except sqlite3.IntegrityError:
                        pass
                except sqlite3.OperationalError:
                        pass
                finally:
                    con.close()
        except Exception:
            pass
            
    def ordenar_contacto_asc(self):
        self.LISTA_RECORDATORIOS = [] #Vacia la lista
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            sql = "SELECT HORA_RECORDAR ||'    '|| TITULO FROM RECORDATORIO ORDER BY UPPER(TITULO), UPPER(HORA_RECORDAR)"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            self.listbox.delete(0,END)
            for i in resultados:
                self.LISTA_RECORDATORIOS.append(i[0])
            for registro in self.LISTA_RECORDATORIOS:
                    self.listbox.insert(END, registro)
            self.colorear_listbox(self.listbox, self.LISTA_RECORDATORIOS) #Colorea el listbox en paralelo
            
        except sqlite3.IntegrityError:
            pass
        finally:
            con.close()
           
    def ordenar_contacto_desc(self):
        self.LISTA_RECORDATORIOS = [] #Vacia la lista
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            sql = "SELECT HORA_RECORDAR ||'    '|| TITULO FROM RECORDATORIO ORDER BY UPPER(TITULO) DESC, UPPER(HORA_RECORDAR) DESC"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            self.listbox.delete(0, END)
            for i in resultados:
                self.LISTA_RECORDATORIOS.append(i[0])
            for registro in self.LISTA_RECORDATORIOS:
                self.listbox.insert(END, registro)
            self.colorear_listbox(self.listbox, self.LISTA_RECORDATORIOS)
            
        except sqlite3.IntegrityError:
            pass
        finally:
            con.close()
            
 
    def listar_listbox(self):
        self.ordenar_contacto_asc() # Ordena y lista la lista
        
        if len(self.LISTA_RECORDATORIOS)==0:
            self.listbox.delete(0, END)
            self.listbox.insert(END, "Sin recordatorios.")
            
        self.lb_records.config(text=str(self.cantidad_recordatorios())+" Todos Recordatorios")
        
        if self.contador_recordatorios_agregados_recientemente == 0:
            self.var_recordatorios_recientemente.set("")
        else:
            self.var_recordatorios_recientemente.set(str(self.contador_recordatorios_agregados_recientemente)+" Agregado recientemente.")
        
      
    def vaciar_lista_contactos(self):
        if len(self.LISTA_RECORDATORIOS)==0:
                mensaje = Message(self.master, text="Lista de Recordatorio vacio.", width=200, bg='#ffffe1', font=self.FONT)
                mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                mensaje.after(3000,lambda: mensaje.destroy())
        else:
            borrar = messagebox.askquestion(parent=self.master, title="Confirmacion:", message="Realmente desea vaciar la lista de Recordatorios?")
            if borrar=='yes':
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    SQL = "DELETE  FROM RECORDATORIO"
                    cursor.execute(SQL)
                    con.commit()

                    mensaje = Message(self.master, text="Se ha vaciado la lista de Recordatorios.", width=200, bg='#ffffe1', font=self.FONT)
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(3000,lambda: mensaje.destroy())
                    
                    self.contador_recordatorios_agregados_recientemente = 0
                    
                    self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
                    self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_recordatorio())
                    self.btn_eliminar.config(state=DISABLED)
                    
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
        self.var_titulo.set("")
        self.var_hora.set(self.HORA_ACTUAL.get())
        self.var_minuto.set(self.MINUTO_ACTUAL.get())
        self.var_segundo.set(self.SEGUNDO_ACTUAL.get())
        
        self.lb_titulo_detalle.config(text="Nuevo Recordatorio")
        self.var_estado_recordatorio = "Activado"
        self.chek_estado_recordatorio.config(image=self.imagenActivado, text="Activado")
        
     
        
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
    
    
    @staticmethod
    def despertar(hora_dormir, minuto_dormir, hora_acordar, minuto_acordar):
        '''Check period of time between hours return minutes total '''
        validar_hora_dormir  = Recordatorio.validar_hora(hora_dormir)
        validar_hora_acordar = Recordatorio.validar_hora(hora_acordar)
  
        if validar_hora_dormir == False or validar_hora_acordar == False:
            pass
        
        return Recordatorio.conversao_minutos(hora_acordar, minuto_acordar) - Despertador.conversao_minutos(hora_dormir, minuto_dormir)
      
    @staticmethod
    def validar_hora(hora):
        if hora <= 23 and hora >= 0:
            return True
        else:
            return False
        
    #@staticmethod
    def procesar_recordatorio(self):
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            sql = "SELECT HORA_RECORDAR FROM RECORDATORIO"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            for i in resultados:
                dato_hora = i[0]
                find = dato_hora.find(":")
                find2 = dato_hora.rfind(":")
                hora = dato_hora[:find]
                minuto = dato_hora[find+1:find2]
                segundo = dato_hora[find2+1:]
            if self.HORA_ACTUAL.get()==hora and self.MINUTO_ACTUAL.get()==minuto and self.SEGUNDO_ACTUAL.get()==segundo:
                self.lb_titulo_detalle.config(text="Alarma Encendiada")
            else:
                pass
            #print("Si" , hora,minuto,segundo, "== ", self.HORA_ACTUAL.get(),self.MINUTO_ACTUAL.get(),self.SEGUNDO_ACTUAL.get())
        except sqlite3.IntegrityError:
            pass
        finally:
            con.close()
            
        self.master.after(200, self.procesar_recordatorio)
            
        
            
    
        
    """---------------------------------------------------------------"""
    """                     Metodos con retono                        """
    """---------------------------------------------------------------"""
    def cantidad_recordatorios(self):
        cant_recordatorios = 0
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            cursor.execute("SELECT COUNT(ID) FROM RECORDATORIO")
            for i in cursor:
                cant_recordatorios = i[0]
            con.close()
        except:
            pass
        return cant_recordatorios
    
    def reloj(self):
        reloj_digital = Toplevel(self.master)
        reloj_digital.title("Digital")
        
        #center_window(reloj_digital, width=320, height=30)
        center_toplevel(reloj_digital, self.master, width=320, height=30, center_all=True)
        
        self.spb_hora_reloj = Spinbox(reloj_digital, textvariable=self.HORA_ACTUAL, width=6, font=("DS-Digital",16),
                relief=FLAT, bd=0, buttondownrelief=FLAT, justify=CENTER, format='%2.0f',
                bg="#262A2E", fg="red", buttonbackground="#262A2E",activebackground="red", insertbackground="red",selectbackground="#555D69",
                highlightcolor="red", highlightthickness=1,
                from_=0.0, to=24.0, increment=1,
                repeatdelay=200, repeatinterval=50)
        self.spb_hora_reloj.pack(side=LEFT, padx=0, pady=0)
        
        self.spb_minuto_reloj = Spinbox(reloj_digital, textvariable=self.MINUTO_ACTUAL, width=6, font=("DS-Digital",16),
                relief=FLAT, bd=0, buttondownrelief=FLAT, buttonup=FLAT, justify=CENTER, format='%2.0f',
                bg="#262A2E", fg="red", buttonbackground="#262A2E", activebackground="red", insertbackground="red",selectbackground="#555D69",
                highlightcolor="red", highlightthickness=1,
                from_=0.0, to=59.0, increment=1,
                repeatdelay=200, repeatinterval=50)
        self.spb_minuto_reloj.pack(side=LEFT, padx=5, pady=0)
        
        self.spb_segundo_reloj = Spinbox(reloj_digital, textvariable=self.SEGUNDO_ACTUAL, width=6, font=("DS-Digital",16),
                relief=FLAT, bd=0, buttondownrelief=FLAT, buttonup=FLAT, justify=CENTER, format='%2.0f',
                bg="#262A2E", fg="red", buttonbackground="#262A2E", activebackground="red", insertbackground="red",selectbackground="#555D69",
                highlightcolor="red", highlightthickness=1,
                from_=0.0, to=59.0, increment=1, insertofftime=400, insertontime=600,
                repeatdelay=200, repeatinterval=50)
        self.spb_segundo_reloj.pack(side=LEFT, padx=0, pady=0)
        
        self.spb_formato_reloj = Spinbox(reloj_digital, textvariable=self.FORMATO_ACTUAL, width=6, font=("DS-Digital",16), state="readonly",
                relief=FLAT, bd=0, buttondownrelief=FLAT, buttonup=FLAT, justify=CENTER,
                readonlybackground="#262A2E", fg="red", buttonbackground="#262A2E", activebackground="red",insertbackground="red",selectbackground="#555D69",
                highlightcolor="red", highlightthickness=1,
                values=self.FORMATO)
        self.spb_formato_reloj.pack(side=LEFT, padx=0, pady=0)
        
        self.hora()
        self.minuto()
        self.segundo()
    
    def hora(self):
        self.ahora = datetime.now()
        hora_actual_continua = self.ahora.hour
        if hora_actual_continua != self.curtime_hh:
            self.curtime_hh = hora_actual_continua
            self.HORA_ACTUAL.set(self.curtime_hh)
        if hora_actual_continua < 12:
            self.FORMATO_ACTUAL.set(self.FORMATO[0])
        else:
            self.FORMATO_ACTUAL.set(self.FORMATO[1])
        self.master.after(200, self.hora)
        
    
    def minuto(self):
        self.ahora = datetime.now()
        minuto_actual_continuo= self.ahora.minute
        if minuto_actual_continuo != self.curtime_mm:
            self.curtime_mm = minuto_actual_continuo
            self.MINUTO_ACTUAL.set(self.curtime_mm)
        self.master.after(200, self.minuto)
    
    def segundo(self):
        self.ahora = datetime.now()
        segundo_actual_continuo = self.ahora.second
        if segundo_actual_continuo != self.curtime_ss:
            self.curtime_ss = segundo_actual_continuo
            self.SEGUNDO_ACTUAL.set(self.curtime_ss)
        self.master.after(200, self.segundo)
        
    
    def ventana_recordatorio_avanzado(self):
        """ Ventana de opciones avanzadas."""
        top_recordatorio_avanzado = Toplevel(self.master)
        top_recordatorio_avanzado.title("Avanzado")
        top_recordatorio_avanzado.focus_set()
        top_recordatorio_avanzado.grab_set()
        top_recordatorio_avanzado.transient(self.master)
        
        center_toplevel(top_recordatorio_avanzado, self.master, width=522, height=360, center_all=True)
        
        self.estado_play_audio = False
        
        top_recordatorio_avanzado.protocol("WM_DELETE_WINDOW", lambda: self.btn_salir_top_recordatorio_avanzado(top_recordatorio_avanzado))
        top_recordatorio_avanzado.bind("<Key>", self.evt_key_press_audio)
        
        """Frame inferior"""
        fr_bottom = Frame(top_recordatorio_avanzado)
        fr_bottom.pack(side=BOTTOM, fill=X, padx=10, pady=10)
        separador = Frame(fr_bottom, bg="#D6D3D3", height=1)
        separador.pack(side=TOP, fill=X, pady=5, expand=True)
        
        """Frame izquierdo"""
        fr_left = Frame(top_recordatorio_avanzado)
        fr_left.pack(side=LEFT, fill=BOTH, expand=True)
        
        lb_fr_sonido = ttk.LabelFrame(fr_left, text="Sonido", underline=0)
        lb_fr_sonido.pack(fill=BOTH, expand=True, anchor="center", padx=10, pady=10)
        
        lb_fr_mensaje = ttk.LabelFrame(fr_left, text="Mensaje", underline=0)
        lb_fr_mensaje.pack(fill=BOTH, expand=True, anchor="center", padx=10)
                
        
        """Frame derecho"""
        fr_right = Frame(top_recordatorio_avanzado)
        fr_right.pack(fill=BOTH, expand=True)
        
        lb_fr_repetir = ttk.LabelFrame(fr_right, text="Repetir Patron", underline=0)
        lb_fr_repetir.pack(fill=BOTH, expand=True, anchor="center", padx=10, pady=10)
        
        
        """Sonido"""
        self.var_sonido = StringVar()
        self.var_sonido_ruta = ""
        rd_btn_sin_sonido = ttk.Radiobutton(lb_fr_sonido, command=self.determinar_sonido, text="Sin sonido", variable=self.var_sonido, value="Sin sonido", width=30)
        rd_btn_sin_sonido.pack(anchor=W, padx=5, pady=2)
        rd_btn_sonido_predeterminado = ttk.Radiobutton(lb_fr_sonido, command=self.determinar_sonido, text="Sonido predeterminado", variable=self.var_sonido, value="Sonido predeterminado", width=30)
        rd_btn_sonido_predeterminado.invoke()
        rd_btn_sonido_predeterminado.pack(anchor=W, padx=5, pady=2)
        rd_btn_archivo_sonido = ttk.Radiobutton(lb_fr_sonido, command=self.determinar_sonido, text="Archivo de sonido", variable=self.var_sonido, value="Archivo de sonido", width=30)
        rd_btn_archivo_sonido.pack(anchor=W, padx=5, pady=0)
        
        fr_explorar_audio = Frame(lb_fr_sonido)
        fr_explorar_audio.pack(anchor=E, padx=5, pady=0)
        
        self.btn_explorar_audio = ttk.Button(fr_explorar_audio, text="Explorar...", width=8, command=self.btn_explorar_sonido_top_recordatorio_avanzado, state=DISABLED)
        self.btn_explorar_audio.pack(side=RIGHT, anchor=E, pady=2)
        
        self.var_ruta_audio = StringVar()
        self.en_explorar_audio = ttk.Entry(fr_explorar_audio, font=("Arial", 10), textvariable=self.var_ruta_audio, state=DISABLED)
        self.en_explorar_audio.pack(side=RIGHT, anchor=E, padx=5, pady=2, ipadx=13)
        
        self.fr_audio = Frame(lb_fr_sonido, highlightbackground="#ACACAC", highlightthickness=1)
        
        self.lb_nombre_audio = Label(self.fr_audio, width=20, fg="#474a56", font=("Arial", 10, "bold"), justify=CENTER, anchor=W)
        self.lb_nombre_audio.pack(side=LEFT, fill=X, expand=True)
        
        separador = Frame(self.fr_audio, bg="#ACACAC", height=1)
        separador.pack(side=LEFT, fill=Y, padx=2)
        
        self.btn_reproducir_audio = Menubutton(self.fr_audio, image=self.imagenPlay, width=25, 
                relief=FLAT, bd=1, bg=self.fr_audio['bg'], activebackground="#d5dadc")
        self.btn_reproducir_audio.pack(side=LEFT, anchor=E)
        self.btn_reproducir_audio.bind("<Button-1>", lambda evt: self.btn_reproducir_audio_top_recordatorio_avanzado(self.var_ruta_audio.get()))
        
        """Mensaje"""
        self.var_mensaje = StringVar()
        self.mensaje_recordatorio = ""
        rd_btn_predeterminado = ttk.Radiobutton(lb_fr_mensaje, command=self.determinar_mensaje, text="Mensaje predeterminado", variable=self.var_mensaje, value="Mensaje predeterminado", width=30)
        rd_btn_predeterminado.invoke()
        rd_btn_predeterminado.pack(anchor=W, padx=5, pady=2)
        rd_btn_personalizado = ttk.Radiobutton(lb_fr_mensaje, command=self.determinar_mensaje, text="Mensaje personalizado", variable=self.var_mensaje, value="Mensaje personalizado", width=30)
        rd_btn_personalizado.pack(anchor=W, padx=5, pady=2)
        
        self.en_mensaje = ttk.Entry(lb_fr_mensaje, font=("Arial", 10), state=DISABLED)
        self.en_mensaje.pack(anchor=E, padx=5, pady=5, ipadx=52)
        
        """Repetir"""
        self.var_repetir_dia_lunes = BooleanVar()
        self.var_repetir_dia_martes = BooleanVar()
        self.var_repetir_dia_miercoles = BooleanVar()
        self.var_repetir_dia_jueves = BooleanVar()
        self.var_repetir_dia_viernes =BooleanVar()
        self.var_repetir_dia_sabado = BooleanVar()
        self.var_repetir_dia_domingo = BooleanVar()
        
        self.chek_btn_lunes = ttk.Checkbutton(lb_fr_repetir, text="Lunes", variable=self.var_repetir_dia_lunes, onvalue=1, offvalue=0, width=20)
        self.chek_btn_lunes.pack(anchor=W, padx=5, pady=2)
        self.chek_btn_martes = ttk.Checkbutton(lb_fr_repetir, text="Martes", variable=self.var_repetir_dia_martes, onvalue=1, offvalue=0, width=20)
        self.chek_btn_martes.pack(anchor=W, padx=5, pady=2)
        self.chek_btn_miercoles = ttk.Checkbutton(lb_fr_repetir, text="Miercoles", variable=self.var_repetir_dia_miercoles, onvalue=1, offvalue=0, width=20)
        self.chek_btn_miercoles.pack(anchor=W, padx=5, pady=0)
        self.chek_btn_jueves = ttk.Checkbutton(lb_fr_repetir, text="Jueves", variable=self.var_repetir_dia_jueves, onvalue=1, offvalue=0, width=20)
        self.chek_btn_jueves.pack(anchor=W, padx=5, pady=0)
        self.chek_btn_viernes = ttk.Checkbutton(lb_fr_repetir, text="Viernes", variable=self.var_repetir_dia_viernes, onvalue=1, offvalue=0, width=20)
        self.chek_btn_viernes.pack(anchor=W, padx=5, pady=2)
        self.chek_btn_sabado = ttk.Checkbutton(lb_fr_repetir, text="Sabado", variable=self.var_repetir_dia_sabado, onvalue=1, offvalue=0, width=20)
        self.chek_btn_sabado.pack(anchor=W, padx=5, pady=2)
        self.chek_btn_domingo = ttk.Checkbutton(lb_fr_repetir, text="Domingo", variable=self.var_repetir_dia_domingo, onvalue=1, offvalue=0, width=20)
        self.chek_btn_domingo.pack(anchor=W, padx=5, pady=0)
        
        
        separador = Frame(lb_fr_repetir, bg="#D6D3D3", height=1)
        separador.pack(side=TOP, fill=X, pady=5, padx=10)
        
        lb_seleccionar_todo = Label(lb_fr_repetir, text="Seleccionar todo", fg="#009846", cursor="hand2", underline=1, font=("Arial", 10, "bold"))
        lb_seleccionar_todo.pack(side=TOP, anchor="ne", padx=10)
        lb_seleccionar_todo.bind("<Button-1>", lambda e: self.select_todos_dias())
        lb_seleccionar_todo.bind("<Enter>", lambda evt: lb_seleccionar_todo.config(fg="#22bF6B", font=("Arial", 10, "bold", "underline")))
        lb_seleccionar_todo.bind("<Leave>", lambda evt: lb_seleccionar_todo.config(fg="#009846", font=("Arial", 10, "bold")))
        
        lb_seleccionar_dias_laborales = Label(lb_fr_repetir, text="Seleccionar dias laborales", fg="#009846", cursor="hand2", underline=1, font=("Arial", 10, "bold"))
        lb_seleccionar_dias_laborales.pack(side=TOP, anchor="ne", padx=10)
        lb_seleccionar_dias_laborales.bind("<Button-1>", lambda e: self.select_dias_no_particulares())
        lb_seleccionar_dias_laborales.bind("<Enter>", lambda evt: lb_seleccionar_dias_laborales.config(fg="#22bF6B", font=("Arial", 10, "bold", "underline")))
        lb_seleccionar_dias_laborales.bind("<Leave>", lambda evt: lb_seleccionar_dias_laborales.config(fg="#009846", font=("Arial", 10, "bold")))
        
        lb_seleccionar_dias_particulares = Label(lb_fr_repetir, text="Seleccionar dias particulares", fg="#009846", cursor="hand2", underline=1, font=("Arial", 10, "bold"))
        lb_seleccionar_dias_particulares.pack(side=TOP, anchor="ne", padx=10)
        lb_seleccionar_dias_particulares.bind("<Button-1>", lambda e: self.select_dias_particulares())
        lb_seleccionar_dias_particulares.bind("<Enter>", lambda evt: lb_seleccionar_dias_particulares.config(fg="#22bF6B", font=("Arial", 10, "bold", "underline")))
        lb_seleccionar_dias_particulares.bind("<Leave>", lambda evt: lb_seleccionar_dias_particulares.config(fg="#009846", font=("Arial", 10, "bold")))
        
        
        """Botones inferiores ventana"""
        btn_cancelar = ttk.Button(fr_bottom, text="Cancelar", command=lambda: self.btn_salir_top_recordatorio_avanzado(top_recordatorio_avanzado))
        btn_cancelar.pack(side=RIGHT, anchor=E)
        btn_aceptar = ttk.Button(fr_bottom, text="Aceptar", command=self.btn_aceptar_top_recordatorio_avanzado)
        btn_aceptar.pack(side=RIGHT, anchor=E, padx=10)
    
        
    def btn_salir_top_recordatorio_avanzado(self, ventana):
        self.btn_detener_audio_top_recordatorio_avanzado()
        ventana.destroy()
        
    def btn_aceptar_top_recordatorio_avanzado(self):
        pass
    
    
    def btn_explorar_sonido_top_recordatorio_avanzado(self):
        self.file_audio = filedialog.askopenfilename(parent=self.master, title='Abrir',filetypes=[("Audio", "*.wav")])
        if self.file_audio:
            self.var_ruta_audio.set(self.file_audio)
            find = self.file_audio.rfind("/") + 1 #Busca desde el final el primer "/" para luego procesarlo y mostrarlo
            #find_2 = self.file_audio.find(".") #esto podria ayudar a que solo mostremos el nombre del audio y no la extencion
            nombre_musica = str(self.file_audio[find:])
            self.lb_nombre_audio.pack(side=LEFT, fill=X, expand=True, pady=2) #Posiciona el Label
            self.lb_nombre_audio.config(text=nombre_musica)
            self.btn_reproducir_audio.pack(side=LEFT, anchor=CENTER, padx=5, pady=2)
            self.btn_reproducir_audio.focus_set()
            self.fr_audio.pack(fill=X, anchor=W, expand=True, padx=5, pady=0)
        else:
            pass
        return self.file_audio
    
    # funciones para reproducir y detener el audio
    def btn_reproducir_audio_top_recordatorio_avanzado(self, file_audio):
        if file_audio:
            self.btn_reproducir_audio.config(image=self.imagenStop)
            self.btn_reproducir_audio.bind("<Button-1>", lambda evt: self.btn_detener_audio_top_recordatorio_avanzado())
            flags = winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
            winsound.PlaySound(file_audio, flags)
        else:
            pass
        
    def btn_detener_audio_top_recordatorio_avanzado(self):
        self.btn_reproducir_audio.config(image=self.imagenPlay)
        self.btn_reproducir_audio.bind("<Button-1>", lambda evt: self.btn_reproducir_audio_top_recordatorio_avanzado(self.var_ruta_audio.get()))
        flags = winsound.SND_FILENAME
        winsound.PlaySound(None, flags)
        
    def evt_key_press_audio(self, event):
        if event.keysym == 'space' and self.estado_play_audio==False:
            self.btn_reproducir_audio_top_recordatorio_avanzado(self.var_ruta_audio.get())
            self.estado_play_audio = True
        else:
            self.btn_detener_audio_top_recordatorio_avanzado()
            self.estado_play_audio = False
            
            
    def select_todos_dias(self):
        self.chek_btn_lunes.invoke()
        self.chek_btn_martes.invoke()
        self.chek_btn_miercoles.invoke()
        self.chek_btn_jueves.invoke()
        self.chek_btn_viernes.invoke()
        self.chek_btn_sabado.invoke()
        self.chek_btn_domingo.invoke()
        
    def select_dias_no_particulares(self):
        self.chek_btn_lunes.invoke()
        self.chek_btn_martes.invoke()
        self.chek_btn_miercoles.invoke()
        self.chek_btn_jueves.invoke()
        self.chek_btn_viernes.invoke()
    
    def select_dias_particulares(self):
        self.chek_btn_sabado.invoke()
        self.chek_btn_domingo.invoke()
            
    def determinar_sonido(self):
        if self.var_sonido.get()=="Sin sonido":
            self.var_sonido_ruta = " "
        elif self.var_sonido.get()=="Sonido predeterminado":
            ruta = "r\audio\DefaultSound.wav"
            self.var_sonido_ruta = ruta
        elif self.var_sonido.get()=="Archivo de sonido":
            self.var_sonido_ruta = self.var_ruta_audio.get()
            self.btn_explorar_audio.config(state=NORMAL)
            self.en_explorar_audio.config(state=NORMAL)
            
    def determinar_mensaje(self):
        if self.var_mensaje.get()=="Mensaje predeterminado":
            self.mensaje_recordatorio = "Recordatorio"
        elif self.var_mensaje.get()=="Mensaje personalizado":
            self.mensaje_recordatorio = self.en_mensaje.get()
            self.en_mensaje.config(state=NORMAL)
        
            
