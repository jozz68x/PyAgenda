
__author__="admin"
__date__ ="$27/02/2015 12:29:25 PM$"

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3


class Cuenta(object):
    
    BACKGROUND_MENU_2 = "#343940"
    BACKGROUND_MENU_INTO = "#99A2AE"
    SELECT_BACKGROUND = "#4CAF50"
    BACKGROUND_BUTTON = "#f0f0f0"
    FOREGROUND = "#B0BEC5"
    FOREGROUND_2 = "#37474F"
    FONT = ("Microsoft Sans Serif", 10)
    FONT_SMALL = ("Microsoft Sans Serif", 9)
    
    def __init__(self, master):
        self.estado_ocultar_clave = False
        self.master = master
        self.cargar_imagenes()
        self.frames_principales()
        self.barra_lateral()
        self.interfaz()
        self.listar_listbox()
        
    def cargar_imagenes(self):
        self.imagenBuscar = ImageTk.PhotoImage(Image.open(r"image\buscar.png"))
        self.imagenOpcionOrdenar = ImageTk.PhotoImage(Image.open(r"image\opcion_ordenar.png"))
        self.imagenOpcionOrdenar2 = ImageTk.PhotoImage(Image.open(r"image\opcion_ordenar_2.png"))
        
        self.imagenNuevo = ImageTk.PhotoImage(Image.open(r"image\add.png"))
        self.imagenGuardar = ImageTk.PhotoImage(Image.open(r"image\guardar.png"))
        self.imagenEditar = ImageTk.PhotoImage(Image.open(r"image\editar.png"))
        self.imagenCancelar = ImageTk.PhotoImage(Image.open(r"image\cancelar.png"))
        self.imagenEliminar = ImageTk.PhotoImage(Image.open(r"image\eliminar.png"))
        self.imagenCerrar = ImageTk.PhotoImage(Image.open(r"image\cerrar.png"))
        
        self.imagenVerClave = ImageTk.PhotoImage(Image.open(r"image\ver_clave.png"))
        self.imagenNoVerClave = ImageTk.PhotoImage(Image.open(r"image\no_ver_clave.png"))

    def frames_principales(self):
        self.frame = Frame(self.master, bg=self.BACKGROUND_MENU_2)
        self.frame.pack(fill=BOTH, expand=True)
        
        self.fr_left = Frame(self.frame, bg=self.BACKGROUND_MENU_2)
        self.fr_left.pack(side=LEFT, fill=Y)
        
        self.right_bottom = Frame(self.frame, bg=self.BACKGROUND_MENU_INTO)
        self.right_bottom.pack(side=BOTTOM, fill=X)
        
        self.fr_right = Frame(self.frame)
        self.fr_right.pack(side=LEFT, fill=BOTH, expand=True)
        
    def barra_lateral(self):
        """Frame Left"""
        fr_left_top = Frame(self.fr_left, bg="#262A2E")
        fr_left_top.pack(side=TOP, fill=X)
        fr_left_both = Frame(self.fr_left, bg=self.BACKGROUND_MENU_2)
        fr_left_both.pack(fill=BOTH, expand=True, padx=1)
        
        self.var_cuentas_recientemente = StringVar()
        lb_records = Label(fr_left_both, textvariable=self.var_cuentas_recientemente, font=("Microsoft Sans Serif", 9), 
                                bg=fr_left_both['bg'], fg="#78909C")
        self.var_cuentas_recientemente.set("")
        lb_records.pack(side=BOTTOM,anchor="w")
        
        self.var_cantidad_cuentas = StringVar()
        lb_records = Label(fr_left_both, textvariable=self.var_cantidad_cuentas, font=("Microsoft Sans Serif", 9),
                                bg=fr_left_both['bg'], fg="#78909C")
        lb_records.pack(side=BOTTOM,anchor="w")
        
        self.var_ent_buscar = StringVar()
        self.var_ent_buscar.set('Buscar cuenta')
        
        ent_buscar = Entry(fr_left_top, width=25, textvariable=self.var_ent_buscar, bg="#99A2AE", font=self.FONT, relief=FLAT, bd=1)
        btn_buscar_contacto = Menubutton(ent_buscar, image=self.imagenBuscar, cursor='arrow', relief=FLAT, bg=ent_buscar['bg'], activebackground = "#c7ebe6", activeforeground = "#FFFFFF")
        btn_buscar_contacto.place(in_=ent_buscar, relx=1, x=0, y=0, anchor=NE)
        btn_buscar_contacto.bind('<Button-1>', lambda e: self.buscar_cuenta())
        ent_buscar.pack(anchor="w", padx=5, pady=10)
        ent_buscar.bind('<Button-1>', lambda evt: self.var_ent_buscar.set(''))
        ent_buscar.bind('<Key>', lambda evt: self.buscar_cuenta())
        ent_buscar.bind('<Return>', lambda evt: self.buscar_cuenta())
        ent_buscar.bind('<Enter>', lambda evt: self.var_ent_buscar.set(''))
        ent_buscar.bind('<Leave>', lambda evt: self.var_ent_buscar.set('Buscar cuenta'), ent_buscar.config(fg="#546E7A"))
        ent_buscar.bind('<FocusIn>', lambda evt: ent_buscar.config(fg="black"))
        ent_buscar.bind('<FocusOut>', lambda evt: ent_buscar.config(fg="#546E7A"))
        
        btn_opc_ordenar = Menubutton(fr_left_top, image=self.imagenOpcionOrdenar, bg=fr_left_top['bg'], activebackground=fr_left_top['bg'], relief=FLAT, bd=0, direction='flush')
        btn_opc_ordenar.place(in_=fr_left_top, relx=1, rely=0, x=2, y=4, anchor=NE, bordermode="outside")
        menu_ord_contactos = Menu(btn_opc_ordenar, tearoff=0, activebackground=self.SELECT_BACKGROUND, activeforeground = "#FFFFFF")
        menu_ord_contactos.add_command(label = " Ordenar por Nombre de A-Z", command=self.ordenar_cuenta_asc)
        menu_ord_contactos.add_command(label = " Ordenar por Nombre de Z-A", command=self.ordenar_cuenta_desc)
        menu_ord_contactos.add_separator()
        menu_ord_contactos.add_command(label = " Ordenar orden Normal", command=self.listar_listbox)
        btn_opc_ordenar["menu"] = menu_ord_contactos
        
        btn_opc_ordenar.bind('<Enter>', lambda evt: btn_opc_ordenar.config(image=self.imagenOpcionOrdenar2))
        btn_opc_ordenar.bind('<Leave>', lambda evt: btn_opc_ordenar.config(image=self.imagenOpcionOrdenar))
        
        
        separador = Frame(fr_left_both, bg=self.BACKGROUND_MENU_2, height=1, width=200)
        separador.pack(fill=X)
        
        self.lista = Listbox(fr_left_both, width=25, bg=fr_left_both['bg'], fg="#B0BEC5", relief=FLAT, bd=0, font=self.FONT, activestyle='dotbox',
                                selectbackground=self.SELECT_BACKGROUND, highlightbackground=fr_left_both['bg'], highlightcolor=fr_left_both['bg'], highlightthickness=0)
        self.lista.pack(side=LEFT, fill=BOTH, expand=1)
        scroll = ttk.Scrollbar(fr_left_both, orient=VERTICAL, command=self.lista.yview)
        scroll.pack(side=LEFT, fill=Y)
        self.lista['yscrollcommand'] = scroll.set
        
        #Menu de Opciones Anticlick en ListBox
        self.menu_opc_lista = Menu(self.lista, tearoff=0, activebackground=self.SELECT_BACKGROUND, activeforeground = "#FFFFFF")
        self.menu_opc_lista.add_command(label = "Ver ")
        self.menu_opc_lista.add_separator()
        self.menu_opc_lista.add_command(label = "Editar ", command=self.editar_cuenta)
        self.menu_opc_lista.add_command(label = "Eliminar ", command=self.eliminar_cuenta)
        
        ent_buscar.bind('<FocusOut>', lambda evt: self.listar_listbox()) #Lista el ListBox cuando el entry no tiene el focus(muy neecesario despues de una busqueda)
        self.lista.bind("<ButtonRelease-3>", self.opciones_anticlick_listbox)
        self.lista.bind("<Double-1>", lambda e: self.editar_cuenta())
        
    def interfaz(self):
        """Frame principal"""
        self.notebook_cuenta = ttk.Notebook(self.fr_right, style="ButtonNotebook")
        self.fr_info_entrada = Frame(self.notebook_cuenta)
        self.fr_info_nota = Frame(self.notebook_cuenta)
        self.notebook_cuenta.add(self.fr_info_entrada, text='Entrada', padding=-3)
        self.notebook_cuenta.add(self.fr_info_nota, text='Nota', padding=-3)
        
        self.notebook_cuenta.pack(expand=True, fill=BOTH)
        
        """ Pestania Entrada """
        lb_titulo = Label(self.fr_info_entrada, text="Titulo", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_titulo.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        lb_usuario = Label(self.fr_info_entrada, text="Nombre usuario", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_usuario.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.lb_clave = Label(self.fr_info_entrada, text="Clave", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        self.lb_clave.grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.lb_clave_repetido = Label(self.fr_info_entrada, text="Repetir Clave", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        self.lb_clave_repetido.grid(row=3, column=0, padx=5, pady=2, sticky="w")
        lb_url = Label(self.fr_info_entrada, text="URL", font=self.FONT_SMALL, justify="left", anchor="w", width=13)
        lb_url.grid(row=4, column=0, padx=5, pady=2, sticky="w")
        
        self.var_titulo = StringVar()
        self.var_usuario = StringVar()
        self.var_clave = StringVar()
        self.var_clave_repetido = StringVar()
        self.var_url = StringVar()
        
        self.ent_titulo = Entry(self.fr_info_entrada, textvariable=self.var_titulo, relief=FLAT, width=74, font=self.FONT)
        self.ent_titulo.grid(row=0, column=1, pady=2, sticky="w")
        self.ent_titulo.bind('<FocusIn>', lambda evt: lb_titulo.config(bg=self.SELECT_BACKGROUND, fg="#FFFFFF"))
        self.ent_titulo.bind('<FocusOut>', lambda evt: lb_titulo.config(bg="#F0F0F0", fg="#000000"))
        
        ent_usuario = Entry(self.fr_info_entrada, textvariable=self.var_usuario, relief=FLAT, width=74, font=self.FONT)
        ent_usuario.grid(row=1, column=1, pady=2, sticky="w")
        ent_usuario.bind('<FocusIn>', lambda evt: lb_usuario.config(bg=self.SELECT_BACKGROUND, fg="#FFFFFF"))
        ent_usuario.bind('<FocusOut>', lambda evt: lb_usuario.config(bg="#F0F0F0", fg="#000000"))
        
        self.ent_clave = Entry(self.fr_info_entrada, textvariable=self.var_clave, relief=FLAT, width=70, font=self.FONT)
        self.ent_clave.grid(row=2, column=1, pady=2, sticky="w")
        self.ent_clave.bind('<FocusIn>', lambda evt: self.lb_clave.config(bg=self.SELECT_BACKGROUND, fg="#FFFFFF"))
        self.ent_clave.bind('<FocusOut>', lambda evt: self.lb_clave.config(bg="#F0F0F0", fg="#000000"))
        
        self.ent_clave_repetido = Entry(self.fr_info_entrada, textvariable=self.var_clave_repetido, relief=FLAT, width=74, font=self.FONT)
        self.ent_clave_repetido.grid(row=3, column=1, pady=2, sticky="w")
        self.ent_clave_repetido.bind('<FocusIn>', lambda evt: self.lb_clave_repetido.config(bg=self.SELECT_BACKGROUND, fg="#FFFFFF"))
        self.ent_clave_repetido.bind('<FocusOut>', lambda evt: self.lb_clave_repetido.config(bg="#F0F0F0", fg="#000000"))

        ent_url = Entry(self.fr_info_entrada, textvariable=self.var_url, relief=FLAT, width=74, font=self.FONT)
        ent_url.grid(row=4, column=1, pady=2, sticky="w")
        ent_url.bind('<FocusIn>', lambda evt: lb_url.config(bg=self.SELECT_BACKGROUND, fg="#FFFFFF"))
        ent_url.bind('<FocusOut>', lambda evt: lb_url.config(bg="#F0F0F0", fg="#000000"))
        
        self.btn_ver_ocultar_clave = ttk.Button(self.fr_info_entrada, image=self.imagenVerClave, command=self.ver_ocultar_clave)
        self.btn_ver_ocultar_clave.place(in_=self.ent_clave, relx=1.0, rely=0, x=30, y=-4, anchor=NE)
        
        
        """ Pestania Nota """
        self.text_nota = Text(self.fr_info_nota, cursor='arrow', state='normal', font=('Verdana', 10), selectbackground='#00878b', autoseparators=5, spacing1=5, wrap=WORD) #Nota el parametro wrap=WORD separara una en palabras al ampliar el widget
        scroller = ttk.Scrollbar(self.fr_info_nota, command=self.text_nota.yview)
        self.text_nota.config(yscrollcommand=scroller.set)
        scroller.pack(side=RIGHT, fill=Y)
        self.text_nota.pack(fill=BOTH, expand=True, padx=2)
        
        """ Barra inferior """
        self.btn_nuevo = Button(self.right_bottom, text="Nuevo", image=self.imagenNuevo, compound=LEFT, command=self.btn_nueva_cuenta, width=100,
                relief=FLAT, bd=1, bg=self.BACKGROUND_BUTTON,font=self.FONT, fg=self.FOREGROUND_2,activebackground=self.BACKGROUND_MENU_2,activeforeground="#ffffff")
        self.btn_nuevo.pack(side=LEFT, padx=10, pady=10)
        
        self.btn_guardar = Button(self.right_bottom, text="Guardar", image=self.imagenGuardar, compound=LEFT, command=self.btn_guardar_cuenta, width=100,
                relief=FLAT, bd=1, bg=self.BACKGROUND_BUTTON,font=self.FONT,fg=self.FOREGROUND_2,activebackground=self.BACKGROUND_MENU_2,activeforeground="#ffffff")
        self.btn_guardar.pack(side=LEFT, padx=5, pady=5)
        
        self.btn_eliminar = Button(self.right_bottom, text="Eliminar", image=self.imagenEliminar, compound=LEFT, command=self.eliminar_cuenta, width=100, state=DISABLED, disabledforeground="dark gray",
                relief=FLAT, bd=1, bg=self.BACKGROUND_BUTTON,font=self.FONT,fg=self.FOREGROUND_2,activebackground=self.BACKGROUND_MENU_2,activeforeground="#ffffff")
        self.btn_eliminar.pack(side=LEFT, padx=10, pady=5)
        
        self.btn_cancelar = Button(self.right_bottom, text="Cancelar", image=self.imagenCancelar, compound=LEFT, command=self.btn_cancelar_cuenta, width=100,
                relief=FLAT, bd=1, bg=self.BACKGROUND_BUTTON,font=self.FONT,fg=self.FOREGROUND_2,activebackground=self.BACKGROUND_MENU_2,activeforeground="#ffffff")
        self.btn_cancelar.pack(side=LEFT, padx=5, pady=5)
        
        self.btn_cerrar = Button(self.right_bottom, text="Cerrar", image=self.imagenCerrar, compound=LEFT, command=self.btn_salir_cuenta, width=100,
                relief=FLAT, bd=1, bg=self.BACKGROUND_BUTTON,font=self.FONT,fg=self.FOREGROUND_2,activebackground=self.BACKGROUND_MENU_2,activeforeground="#ffffff")
        self.btn_cerrar.pack(side=RIGHT, padx=10, pady=5)
        self.btn_help = Button(self.right_bottom, text="?", command=self.btn_help, relief=FLAT, bd=1, width=3, 
                bg=self.BACKGROUND_BUTTON,font=self.FONT,fg=self.FOREGROUND_2,activebackground=self.BACKGROUND_MENU_2,activeforeground="#ffffff")
        self.btn_help.pack(side=RIGHT, padx=5, pady=5)
        
    def btn_salir_cuenta(self):
        self.frame.destroy()
    def btn_help(self):
        pass
    def btn_cancelar_cuenta(self):
        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar, command=self.btn_guardar_cuenta)
        self.btn_eliminar.config(state=DISABLED)
        self.notebook_cuenta.select(self.fr_info_entrada)
        self.limpiar_entradas()
    
    def btn_nueva_cuenta(self):
        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar, command=self.btn_guardar_cuenta)
        self.btn_eliminar.config(state=DISABLED)
        self.notebook_cuenta.select(self.fr_info_entrada)
        self.ent_titulo.focus_set()
        self.limpiar_entradas()
        
    def btn_guardar_cuenta(self):
        try:
            if self.var_titulo.get()=="":
                pass
            else:
                titulo = self.var_titulo.get()
                usuario = self.var_usuario.get()
                clave = self.var_clave.get().strip()
                clave_repetido = self.var_clave_repetido.get().strip()
                url = self.var_url.get()
                nota = self.text_nota.get(0.0, END)
                
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    cursor.execute('''INSERT INTO CUENTA(TITULO,USUARIO,CLAVE,CLAVE_REPETIDO,URL,NOTA)
                                    VALUES(?,?,?,?,?,?)''',(titulo,usuario,clave,clave_repetido,url,nota))
                    con.commit()
                    
                    mensaje = Message(self.master, text="Cuenta registrada", width=200, bg='#ffffe1', font=("Arial",10))
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(2000,lambda: mensaje.destroy())
                    
                    self.lista.delete(0, END)
                    self.listar_listbox()
                    self.limpiar_entradas()
                    
                except sqlite3.IntegrityError:
                    con.rollback()
                finally:
                    con.close()
        except Exception:
            pass
        
    
    def editar_cuenta(self):
        #if self.lista.curselection:
        index = self.lista.curselection() #devuelve el indice de la seleccion
        seltext = self.lista.get(index) #optine los dotos del indice seleccionado
        self.id_cuenta = seltext #optenemos solo el codigo
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            SQL = """SELECT * FROM CUENTA WHERE TITULO='%s'""" % (self.id_cuenta)
            cursor.execute(SQL)
            for i in cursor:
                self.var_id = i[0]
                self.var_titulo.set(i[1])
                self.var_usuario.set(i[2])
                self.var_clave.set(i[3])
                self.var_clave_repetido.set(i[4])
                self.var_url.set(i[5])
                self.text_nota.delete(0.0, END)
                self.text_nota.insert(END, i[6])
            
            self.btn_guardar.config(text="Editar", image=self.imagenEditar, command=self.btn_editar_cuenta)
            self.btn_eliminar.config(state=NORMAL)
            self.notebook_cuenta.select(self.fr_info_entrada)
        except sqlite3.IntegrityError:
            pass
        finally:
            con.close()
            
    def btn_editar_cuenta(self):
                id = self.var_id
                titulo = self.var_titulo.get()
                usuario = self.var_usuario.get()
                clave = self.var_clave.get()
                clave_repetido = self.var_clave_repetido.get()
                url = self.var_url.get()
                nota = self.text_nota.get(0.0,END)
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    SQL = """   UPDATE CUENTA SET TITULO='%s',USUARIO='%s',CLAVE='%s', CLAVE_REPETIDO='%s',URL='%s',NOTA='%s'
                                WHERE ID=%s""" % (titulo,usuario,clave,clave_repetido,url,nota,id)
                    cursor.execute(SQL)
                    con.commit()
                    
                    mensaje = Message(self.master, text="Cuenta actualizada", width=200, bg='#ffffe1', font=("Arial",10))
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(2000,lambda: mensaje.destroy())
                    
                    self.lista.delete(0,END)
                    self.listar_listbox()
                    self.limpiar_entradas()
                    
                    self.btn_guardar.config(text="Guardar", image=self.imagenGuardar, command=self.btn_guardar_cuenta)
                    self.btn_eliminar.config(state=DISABLED)
                    
                except sqlite3.IntegrityError:
                    con.rollback()
                finally:
                    con.close()
        
    
    def eliminar_cuenta(self):
            index = self.lista.curselection() #devuelve el indice de la seleccion
            seltext = self.lista.get(index) #optine los datos del indice seleccionado
            self.id_cuenta = seltext #optenemos solo el codigo
            
            borrar = messagebox.askquestion(parent=self.master, icon='question', title="Confirmacion:", message="Realmente desea Eliminar?")
            if borrar=='yes':
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    sql = "DELETE  FROM CUENTA WHERE TITULO LIKE '"+self.id_cuenta+"'"
                    cursor.execute(sql)
                    con.commit()
                    
                    mensaje = Message(self.master, text="Cuenta eliminada", width=200, bg='#ffffe1', font=("Arial",10))
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(2000,lambda: mensaje.destroy())
                    
                    self.lista.delete(0,END)
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
    
    def buscar_cuenta(self):
        try:
            if self.var_ent_buscar.get() == "":
                pass
            else:
                self.id_titulo_cuenta = self.var_ent_buscar.get()
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    sql = "SELECT TITULO FROM CUENTA WHERE TITULO LIKE'"+self.id_titulo_cuenta+"%"+"'" 
                    valor = cursor.execute(sql)
                    encontrado = False
                    if valor.fetchone() and encontrado==False:
                            SQL = "SELECT TITULO FROM CUENTA WHERE TITULO LIKE'"+self.id_titulo_cuenta+"%"+"'" 
                            cursor.execute(SQL)
                            encontrado = True
                            resultados = cursor.fetchall()
                            self.lista.delete(0,END)
                            for i in resultados:
                                self.lista.insert(END, str(i[0]))
                    else:
                            self.lista.delete(0,END)
                            self.lista.insert(END, "No se encontro cuenta.")
                except sqlite3.IntegrityError:
                        pass
                except sqlite3.OperationalError:
                        pass
                finally:
                    con.close()
        except Exception:
            pass
        
    def ordenar_cuenta_asc(self):
        CUENTAS = []
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            sql = "SELECT TITULO FROM CUENTA ORDER BY TITULO"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            self.lista.delete(0,END)
            for i in resultados:
                CUENTAS.append(i[0])
            for registro in CUENTAS:
                self.lista.insert(END, registro)
            for color in range(0,len(CUENTAS),2):
                self.lista.itemconfigure(color, background='#3A3F46')
        except sqlite3.IntegrityError:
            pass
        finally:
            con.close()
            
    def ordenar_cuenta_desc(self):
        CUENTAS = []
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            sql = "SELECT TITULO FROM CUENTA ORDER BY TITULO DESC"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            self.lista.delete(0,END)
            for i in resultados:
                CUENTAS.append(i[0])
            for registro in CUENTAS:
                self.lista.insert(END, registro)
            for color in range(0,len(CUENTAS),2):
                self.lista.itemconfigure(color, background='#3A3F46')
        except sqlite3.IntegrityError:
            pass
        finally:
            con.close()

    def listar_listbox(self):
        CUENTAS = []
        
        con = sqlite3.connect(r'DB\db.s3db')
        cursor = con.cursor()
        cursor.execute("SELECT TITULO FROM CUENTA")
        
        self.lista.delete(0,END)
        
        for i in cursor:
            CUENTAS.append(str(i[0]))
        for registros in CUENTAS:
            self.lista.insert(END, registros)            
        
        cursor.execute("SELECT COUNT(ID) FROM CUENTA")
        for i in cursor:
            self.var_cantidad_cuentas.set(str(i[0])+" Cuentas en la lista.")
        
        ## Colorea las lineas alternas del listbox.
        for i in range(0,len(CUENTAS),2):
            self.lista.itemconfigure(i, background='#3A3F46')
            
    def limpiar_entradas(self):        
        self.var_titulo.set("")
        self.var_usuario.set("")
        self.var_clave.set("")
        self.var_clave_repetido.set("")
        self.var_url.set("")
        self.text_nota.delete(0.0, END)
        
    
    """---------------------------------------------------------------"""
    def opciones_anticlick_listbox(self, *evento):
        evento = evento[0]
        self.lista_x, self.lista_y = evento.x_root, evento.y_root
        self.menu_opc_lista.post(self.lista_x, self.lista_y)
        
    def ver_ocultar_clave(self):
        if self.estado_ocultar_clave == False:
            self.ent_clave.config(show="*")
            self.ent_clave_repetido.config(show="*")
            self.btn_ver_ocultar_clave.config(image=self.imagenNoVerClave)
            self.estado_ocultar_clave = True
        else:
            self.ent_clave.destroy()
            self.btn_ver_ocultar_clave.destroy()
            self.ent_clave_repetido.destroy()
            
            self.ent_clave = Entry(self.fr_info_entrada, textvariable=self.var_clave, relief=FLAT, width=70, font=self.FONT)
            self.ent_clave.grid(row=2, column=1, pady=2, sticky="w")
            self.ent_clave.bind('<FocusIn>', lambda evt: self.lb_clave.config(bg=self.SELECT_BACKGROUND, fg="#FFFFFF"))
            self.ent_clave.bind('<FocusOut>', lambda evt: self.lb_clave.config(bg="#F0F0F0", fg="#000000"))

            self.ent_clave_repetido = Entry(self.fr_info_entrada, textvariable=self.var_clave_repetido, relief=FLAT, width=74, font=self.FONT)
            self.ent_clave_repetido.grid(row=3, column=1, pady=2, sticky="w")
            self.ent_clave_repetido.bind('<FocusIn>', lambda evt: self.lb_clave_repetido.config(bg=self.SELECT_BACKGROUND, fg="#FFFFFF"))
            self.ent_clave_repetido.bind('<FocusOut>', lambda evt: self.lb_clave_repetido.config(bg="#F0F0F0", fg="#000000"))
            
            self.btn_ver_ocultar_clave = ttk.Button(self.fr_info_entrada, image=self.imagenVerClave, command=self.ver_ocultar_clave)
            self.btn_ver_ocultar_clave.place(in_=self.ent_clave, relx=1.0, rely=0, x=30, y=-4, anchor=NE)
            
            self.estado_ocultar_clave = False


        