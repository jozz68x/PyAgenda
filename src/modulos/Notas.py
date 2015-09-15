
__author__="Jose Diaz"
__date__ ="$23/02/2015 08:52:56 AM$"

from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3

from modulos.centerWindow import center_toplevel
from modulos.textView import TextView


class Notas(object):
    
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
        
        self.customFont = tkFont.Font(family="Helvetica", size=10, weight='normal', slant='roman', underline=0, overstrike=0)
        
        self.cargar_imagenes()
        self.frames_principales()
        self.barra_lateral()
        self.interfaz()
        self.listar_listbox()
        
        
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
        self.iconCommit = ImageTk.PhotoImage(Image.open(r"image\icons_show\commit.png"))
        self.iconLimpiar = ImageTk.PhotoImage(Image.open(r"image\icons_show\limpiar.png"))
        self.iconAtras = ImageTk.PhotoImage(Image.open(r"image\icons_show\atras.png"))
        self.iconAdelante = ImageTk.PhotoImage(Image.open(r"image\icons_show\adelante.png"))
        self.iconTextFg = ImageTk.PhotoImage(Image.open(r"image\icons_show\fg.png"))
        self.iconTextBg = ImageTk.PhotoImage(Image.open(r"image\icons_show\bg.png"))
        self.iconTextBgSelect = ImageTk.PhotoImage(Image.open(r"image\icons_show\bg_select.png"))
        
        self.imagenBuscar = ImageTk.PhotoImage(Image.open(r"image\buscar.png"))
        self.imagenOpcionOrdenar = ImageTk.PhotoImage(Image.open(r"image\opcion_ordenar.png"))
        self.imagenOpcionOrdenar2 = ImageTk.PhotoImage(Image.open(r"image\opcion_ordenar_2.png"))
        
        self.imagenNuevo = ImageTk.PhotoImage(Image.open(r"image\add.png"))
        self.imagenGuardar = ImageTk.PhotoImage(Image.open(r"image\guardar.png"))
        self.imagenEditar = ImageTk.PhotoImage(Image.open(r"image\editar.png"))
        self.imagenCancelar = ImageTk.PhotoImage(Image.open(r"image\cancelar.png"))
        self.imagenEliminar = ImageTk.PhotoImage(Image.open(r"image\eliminar.png"))
        self.imagenCerrar = ImageTk.PhotoImage(Image.open(r"image\cerrar.png"))
        
    
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
        
        """ Frame lateral derecha - bottom """
        self.right_bottom = Frame(self.fr_right, bg=self.BACKGROUND)
        self.right_bottom.pack(side=BOTTOM, fill=X)
        
        """ Frame lateral derecha - top """
        self.fr_right_top = Frame(self.fr_right, bg=self.BACKGROUND)
        self.fr_right_top.pack(fill=X, side=TOP)
        
        """ Frame lateral derecha - both """
        self.fr_right_both = Frame(self.fr_right)
        self.fr_right_both.pack(fill=BOTH, expand=True, padx=8, pady=1)
        
        self.panel.add(self.fr_left)
        self.panel.add(self.fr_right)
    
    def barra_lateral(self):
        """Frame izquierda"""
        fr_left_top = Frame(self.fr_left, bg="#262A2E")
        fr_left_top.pack(side=TOP, fill=X)
        fr_left_both = Frame(self.fr_left, bg=self.BACKGROUND_MENU_2)
        fr_left_both.pack(fill=BOTH, expand=True, padx=1)
        
        self.var_notas_recientemente = StringVar()
        lb_records = Label(fr_left_both, textvariable=self.var_notas_recientemente, font=(self.FONT[0], 9), bg=fr_left_both['bg'], fg=self.BACKGROUND_MENU_INTO)
        lb_records.pack(side=BOTTOM, fill=X, anchor="center")
        
        self.lb_records = Button(fr_left_both, image=self.imagenIconContacto, compound=TOP, relief=FLAT, bd=0, font=self.FONT, 
                bg=fr_left_both['bg'], fg=self.BACKGROUND_MENU_INTO, activebackground=fr_left_both['bg'], activeforeground=self.BACKGROUND_MENU_INTO)
        self.lb_records.pack(side=BOTTOM, fill=X, anchor="center")
        
        self.var_ent_buscar = StringVar()
        self.var_ent_buscar.set('Buscar notas')
        
        ent_buscar = Entry(fr_left_top, width=30, textvariable=self.var_ent_buscar, bg="#99A2AE", font=self.FONT, relief=FLAT, bd=1)
        btn_buscar_notas = Menubutton(fr_left_top, image=self.imagenBuscar, relief=FLAT, bg=ent_buscar['bg'], activebackground="#009846")
        btn_buscar_notas.place(in_=ent_buscar, relx=1.0, rely=0, x=21, y=-1, anchor=NE)
        btn_buscar_notas.bind('<Button-1>', lambda e: self.buscar_nota())
        ent_buscar.pack(anchor="w", padx=5, pady=10)
        ent_buscar.bind('<Button-1>', lambda evt: self.listar_listbox())
        ent_buscar.bind('<Key>', lambda evt: self.buscar_nota())
        ent_buscar.bind('<Return>', lambda evt: self.buscar_nota())
        ent_buscar.bind('<Enter>', lambda evt: self.var_ent_buscar.set(''))
        ent_buscar.bind('<Leave>', lambda evt: self.var_ent_buscar.set('Buscar notas'), ent_buscar.config(fg="#546E7A"))
        ent_buscar.bind('<FocusIn>', lambda evt: ent_buscar.config(fg="#000000"))
        ent_buscar.bind('<FocusOut>', lambda evt: ent_buscar.config(fg="#546E7A"))
        
        btn_opc_ordenar = Menubutton(fr_left_top, image=self.imagenOpcionOrdenar, bg=fr_left_top['bg'], activebackground=fr_left_top['bg'], relief=FLAT, bd=0, direction='flush')
        btn_opc_ordenar.place(in_=fr_left_top, relx=1, rely=0, x=2, y=4, anchor=NE, bordermode="outside")
        menu_ord_notas = Menu(btn_opc_ordenar, tearoff=0, font=self.FONT, activebackground=self.ACTIVE_BACKGROUND, activeforeground = "#FFFFFF")
        menu_ord_notas.add_radiobutton(label = " Ordenar en orden A-Z", command=self.ordenar_notas_asc)
        menu_ord_notas.add_radiobutton(label = " Ordenar en orden Z-A", command=self.ordenar_notas_desc)
        menu_ord_notas.add_separator()
        menu_ord_notas.add_command(label = " Vaciar Lista", command=self.vaciar_lista_notas)
        
        btn_opc_ordenar["menu"] = menu_ord_notas
        
        btn_opc_ordenar.bind('<Enter>', lambda evt: btn_opc_ordenar.config(image=self.imagenOpcionOrdenar2))
        btn_opc_ordenar.bind('<Leave>', lambda evt: btn_opc_ordenar.config(image=self.imagenOpcionOrdenar))
        
        
        separador = Frame(fr_left_both, bg=self.BACKGROUND_MENU_2, height=1, width=200)
        separador.pack(fill=X)
        self.crear_opciones_anticlick_listbox(fr_left_both) #Crea las opciones y eventos para el anticlick
        self.listbox = Listbox(fr_left_both, width=40, bg=fr_left_both['bg'], fg="#B0BEC5", relief=FLAT, bd=0, font=self.FONT, activestyle='dotbox',
                                selectbackground=self.ACTIVE_BACKGROUND, highlightbackground=fr_left_both['bg'], highlightcolor=fr_left_both['bg'], highlightthickness=0)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        scroll = ttk.Scrollbar(fr_left_both, orient=VERTICAL, command=self.listbox.yview)
        scroll.pack(side=LEFT, fill=Y)
        self.listbox['yscrollcommand'] = scroll.set
        
        self.listbox.bind("<ButtonRelease-3>", self.ver_opciones_anticlick_listbox)
        self.listbox.bind("<Double-1>", lambda e: self.mostrar_todos_datos())
    
            
    
    def interfaz(self):
        """ Frame lateral derecha - both """
        self.lb_titulo_detalle = Label(self.fr_right_top, text="Nueva Nota", font=(self.FONT[0], 14), anchor=W, justify=LEFT, width=80,
                bg=self.fr_right_top['bg'], fg="#000000")
        self.lb_titulo_detalle.pack(side=TOP, fill=X, padx=8, pady=2)
        
        
        TextView(self.fr_right_both)
        
        """ Frame lateral derecha - bottom """
        self.btn_nuevo = Menubutton(self.right_bottom, text="Nuevo", image=self.imagenNuevo, compound=TOP,  
                                    bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_nuevo.pack(side=LEFT, padx=8, pady=2)
        self.btn_nuevo.bind("<Button-1>", lambda evt: self.btn_nueva_nota())
        
        self.btn_guardar = Menubutton(self.right_bottom, text="Guardar", image=self.imagenGuardar, compound=TOP, 
                                      bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_guardar.pack(side=LEFT, padx=0, pady=2)
        self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_texto_nota())
        
        self.btn_eliminar = Menubutton(self.right_bottom, text="Eliminar", image=self.imagenEliminar, compound=TOP, state=DISABLED,
                                       disabledforeground="dark gray", bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_eliminar.pack(side=LEFT, padx=8, pady=2)
        self.btn_eliminar.bind("<Button-1>", lambda evt: self.eliminar_nota())
        
        self.btn_cancelar = Menubutton(self.right_bottom, text="Cancelar", image=self.imagenCancelar, compound=TOP,
                                       bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_cancelar.pack(side=LEFT, padx=0, pady=2)
        self.btn_cancelar.bind("<Button-1>", lambda evt: self.btn_cancelar_nota())
        
        self.btn_cerrar = Menubutton(self.right_bottom, text="Cerrar", image=self.imagenCerrar, compound=TOP,
                                    bg=self.right_bottom['bg'], **self.MENUBUTTON_BOTTOM)
        self.btn_cerrar.pack(side=RIGHT, padx=10, pady=2)
        self.btn_cerrar.bind("<Button-1>", lambda evt: self.btn_salir_notas())
    
    
    def btn_salir_notas(self):
        self.panel.destroy()
    
    def ventana_titulo(self):
        """Ventana nueva Nota - titulo"""
        self.top_titulo = Toplevel(self.master)
        self.top_titulo.title("Nueva Nota")
        self.top_titulo.focus_set()
        self.top_titulo.grab_set()
        self.top_titulo.transient(self.master)
        
        center_toplevel(self.top_titulo, self.master, width=320, height=100)
        
        self.var_titulo_nota = StringVar()
        
        frame_top = Frame(self.top_titulo)
        btn = ttk.Button(frame_top, text="Aceptar", command=lambda: self.btn_guardar_titulo_nota())
        btn.pack(side=BOTTOM, anchor=E)
        ttk.Label(frame_top, text="Nombre").pack(side=LEFT)
        entry = ttk.Entry(frame_top, textvariable=self.var_titulo_nota, width=40)
        entry.focus_set()
        entry.pack(side=LEFT)
        frame_top.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        
    def btn_nueva_nota(self):
        self.ventana_titulo()
        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
        self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_texto_nota())
        self.btn_eliminar.config(state=DISABLED)
        TextView.text .focus_set()
        
    def btn_guardar_titulo_nota(self):
        if self.var_titulo_nota.get()=="":
            pass
        else:
            self.top_titulo.destroy()
            self.titulo = self.var_titulo_nota.get()
            try:
                con = sqlite3.connect(r'DB\db.s3db')
                cursor = con.cursor()
                cursor.execute("INSERT INTO NOTA(TITULO) VALUES(?)", (self.titulo,))#Es necesario poner la coma al final para determinar que es una tupla
                con.commit()
                    
                mensaje = Message(self.master, text="Nota creada", width=200, bg='#ffffe1', font=self.FONT)
                mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                mensaje.after(2000, lambda: mensaje.destroy())
                    
                self.contador_notas_agregados_recientemente = self.contador_notas_agregados_recientemente + 1
                self.listbox.delete(0,END)
                self.listar_listbox()
                self.limpiar_entradas()
                
                """Compara el dato agregado con lo de la lista existente para luego seleccionarlo en el listbox"""
                dato_a_seleccionar = self.titulo
                for i in range(0,len(self.LISTA_NOTAS)):
                    if(self.LISTA_NOTAS[i] == dato_a_seleccionar):
                        self.listbox.selection_set(first=i)
                                        
            except sqlite3.IntegrityError:
                con.rollback()
            except sqlite3.OperationalError:
                con.rollback()
            finally:
                con.close()
        
    def btn_guardar_texto_nota(self):
            if TextView.text .get(0.0, END) == "":
                pass
            else:
                texto = TextView.text .get(0.0, END)
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    cursor.execute("UPDATE NOTA SET TEXTO='%s' WHERE TITULO='%s'" %(texto, self.titulo))
                    con.commit()
                    
                    mensaje = Message(self.master, text="Nota Guardada", width=200, bg='#ffffe1', font=self.FONT)
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(2000,lambda: mensaje.destroy())
                           
                except sqlite3.IntegrityError:
                    con.rollback()
                except sqlite3.OperationalError:
                    con.rollback()
                finally:
                    con.close()
        
    def btn_cancelar_nota(self):
        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
        self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_texto_nota())
        self.btn_eliminar.config(state=DISABLED)
        self.limpiar_entradas()
       
       
    def mostrar_todos_datos(self):
        if len(self.LISTA_NOTAS)==0:
            pass
        else:
                index = self.listbox.curselection() #devuelve el indice de la seleccion
                seltext = self.listbox.get(index) #optine los dotos del indice seleccionado
                self.id_nota = seltext #optenemos solo el id
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    SQL = """SELECT ID, TITULO, TEXTO FROM NOTA WHERE TITULO='%s'""" % (self.id_nota)
                    cursor.execute(SQL)
                    TextView.text .delete(0.0, END)
                    for i in cursor:
                        self.id_nota = i[0]
                        self.titulo_nota = i[1]
                        TextView.text .insert(INSERT, i[2])
                    self.lb_titulo_detalle.config(text=self.titulo_nota)
                    
                    self.btn_guardar.config(text="Editar", image=self.imagenEditar)
                    self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_editar_nota())
                    self.btn_eliminar.config(state=NORMAL)
                except sqlite3.IntegrityError:
                    pass
                except sqlite3.OperationalError:
                    pass
                finally:
                    con.close()
        
    def btn_editar_nota(self):
        try:
                id = self.id_nota
                titulo = self.titulo_nota
                texto = TextView.text .get(0.0, END)
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    SQL = """UPDATE NOTA SET TITULO='%s', TEXTO='%s'
                             WHERE ID=%s""" % (titulo, texto, estado,id)
                    cursor.execute(SQL)
                    con.commit()
                    
                    mensaje = Message(self.master, text="Nota actualizada", width=200, bg='#ffffe1', font=self.FONT)
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(2000,lambda: mensaje.destroy())
                    
                    self.listbox.delete(0,END)
                    self.listar_listbox()
                    self.limpiar_entradas()
                    
                    self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
                    self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_texto_nota())
                    self.btn_eliminar.config(state=DISABLED)
                    
                except sqlite3.IntegrityError:
                    con.rollback()
                except sqlite3.OperationalError:
                    con.rollback()
                finally:
                    con.close()
        except Exception:
            pass
        
    def eliminar_nota(self):
        if len(self.LISTA_NOTAS)==0:
            pass
        else:
            try:
                index = self.listbox.curselection() #devuelve el indice de la seleccion
                seltext = self.listbox.get(index) #optine los dotos del indice seleccionado
                self.id_nota = seltext #optenemos solo el codigo
                
                borrar = messagebox.askquestion(parent=self.master, icon='question', title="Confirmacion:", message="Realmente desea Eliminar?")
                if borrar=='yes':
                    try:
                        con = sqlite3.connect(r'DB\db.s3db')
                        cursor = con.cursor()
                        sql = "DELETE  FROM NOTA WHERE TITULO LIKE '"+self.id_nota+"'"
                        cursor.execute(sql)
                        con.commit()

                        mensaje = Message(self.master, text="Nota eliminado", width=200, bg='#ffffe1', font=self.FONT)
                        mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                        mensaje.after(2000,lambda: mensaje.destroy())
 
                        self.contador_notas_agregados_recientemente = self.contador_notas_agregados_recientemente - 1

                        self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
                        self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_texto_nota())
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
            
    def buscar_nota(self):
        try:
            if self.var_ent_buscar.get() == "":
                self.listar_listbox()
            elif self.var_ent_buscar.get() == "Buscar nota":
                pass
            else:
                self.id_nota = self.var_ent_buscar.get()
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    sql = "SELECT TITULO FROM NOTA WHERE TITULO LIKE'"+"%"+self.id_nota+"%"+"'" 
                    valor = cursor.execute(sql)
                    encontrado = False
                    if valor.fetchone() and encontrado==False:
                            sql = "SELECT TITULO FROM NOTA WHERE TITULO LIKE'"+"%"+self.id_nota+"%"+"'" 
                            cursor.execute(sql)
                            encontrado = True
                            resultados = cursor.fetchall()
                            
                            self.listbox.delete(0, END)
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
            
    def ordenar_notas_asc(self):
        self.LISTA_NOTAS = [] # Vacia la lista
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            sql = "SELECT TITULO FROM NOTA ORDER BY UPPER(TITULO)"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            self.listbox.delete(0,END)
            for i in resultados:
                self.LISTA_NOTAS.append(i[0])
            for registro in self.LISTA_NOTAS:
                    self.listbox.insert(END, registro)
            self.colorear_listbox(self.listbox, self.LISTA_NOTAS) #Colorea el listbox en paralelo
            
        except sqlite3.IntegrityError:
            pass
        finally:
            con.close()
           
    def ordenar_notas_desc(self):
        self.LISTA_NOTAS = [] # Vacia la lista
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            sql = "SELECT TITULO FROM NOTA ORDER BY UPPER(TITULO) DESC"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            self.listbox.delete(0, END)
            for i in resultados:
                self.LISTA_NOTAS.append(i[0])
            for registro in self.LISTA_NOTAS:
                self.listbox.insert(END, registro)
            self.colorear_listbox(self.listbox, self.LISTA_NOTAS)
            
        except sqlite3.IntegrityError:
            pass
        finally:
            con.close()
            
 
    def listar_listbox(self):
        self.ordenar_notas_asc() # Ordena y lista la lista
        
        if len(self.LISTA_NOTAS)==0:
            self.listbox.delete(0, END)
            self.listbox.insert(END, "Sin notas.")
            
        self.lb_records.config(text=str(self.cantidad_recordatorios())+" Todas Notas")
        
        if self.contador_notas_agregados_recientemente == 0:
            self.var_notas_recientemente.set("")
        else:
            self.var_notas_recientemente.set(str(self.contador_notas_agregados_recientemente)+" Agregado recientemente.")
        
      
    def vaciar_lista_notas(self):
        if len(self.LISTA_NOTAS)==0:
                mensaje = Message(self.master, text="Lista de Notas vacio.", width=200, bg='#ffffe1', font=self.FONT)
                mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                mensaje.after(3000,lambda: mensaje.destroy())
        else:
            borrar = messagebox.askquestion(parent=self.master, title="Confirmacion:", message="Realmente desea vaciar la lista de Notas?")
            if borrar=='yes':
                try:
                    con = sqlite3.connect(r'DB\db.s3db')
                    cursor = con.cursor()
                    SQL = "DELETE  FROM NOTA"
                    cursor.execute(SQL)
                    con.commit()

                    mensaje = Message(self.master, text="Se ha vaciado la lista de Notas.", width=200, bg='#ffffe1', font=self.FONT)
                    mensaje.place(in_=self.master, relx=1, anchor="e", y=15, x=-5, bordermode="outside")
                    mensaje.after(3000,lambda: mensaje.destroy())
                    
                    self.contador_notas_agregados_recientemente = 0
                    
                    self.btn_guardar.config(text="Guardar", image=self.imagenGuardar)
                    self.btn_guardar.bind("<Button-1>", lambda evt: self.btn_guardar_texto_nota())
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
        TextView.text .delete(0.0, END)
        self.lb_titulo_detalle.config(text="Nueva Nota")
        
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
    def cantidad_recordatorios(self):
        cant_recordatorios = 0
        try:
            con = sqlite3.connect(r'DB\db.s3db')
            cursor = con.cursor()
            cursor.execute("SELECT COUNT(ID) FROM NOTA")
            for i in cursor:
                cant_recordatorios = i[0]
            con.close()
        except:
            pass
        return cant_recordatorios
    
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
        TextView.text .tag_add("bold", SEL_FIRST, SEL_LAST)
        TextView.text .tag_config("bold", font="-weight bold")
        
    def italic(self):
        """Italics texto seleccionado."""
        TextView.text .tag_add("italic", SEL_FIRST, SEL_LAST)
        TextView.text .tag_config("italic", font="-slant italic")
        
    def underline(self):
        """Negrita al texto seleccionado."""
        TextView.text .tag_add("underline", SEL_FIRST, SEL_LAST)
        TextView.text .tag_config("underline", font="-underline 1")
        
    def overstrike(self):
        """Italics texto seleccionado."""
        TextView.text .tag_add("overstrike", SEL_FIRST, SEL_LAST)
        TextView.text .tag_config("overstrike", font="-overstrike 1")
        
    def left(self):
        """A la izquierda texto."""
        TextView.text .tag_remove('center', '1.0', END)
        TextView.text .tag_remove('right', '1.0', END)
        
        TextView.text .tag_add("left", 1.0, END)
        TextView.text .tag_config("left", justify='left')
        
    def center(self):
        """Centrado texto."""
        TextView.text .tag_remove('left', '1.0', END)
        TextView.text .tag_remove('right', '1.0', END)
        
        TextView.text .tag_add("center", 1.0, END)
        TextView.text .tag_config("center", justify='center')
    
    def right(self):
        """A la derecha texto."""
        TextView.text .tag_remove('left', '1.0', END)
        TextView.text .tag_remove('center', '1.0', END)
        
        TextView.text .tag_add("right", 1.0, END)
        TextView.text .tag_config("right", justify='right')
    
    def limpiar(self):
        """Limpia widget Text."""
        TextView.text .delete(0.0,  END)
    
    def commit(self):
        """Guarda los datos del Text."""
        self.btn_guardar_texto_nota()
        
    def color_foreground(self):
        color = colorchooser.askcolor(parent=self.master)
        
        if color!=None:
            TextView.text .tag_add("foreground", SEL_FIRST, SEL_LAST)
            TextView.text .tag_config("foreground", foreground=color[1])
        else:
            pass
        
    def color_resaltado(self):
        color = colorchooser.askcolor(parent=self.master)
        
        if color!=None:
            TextView.text .tag_add("background", SEL_FIRST, SEL_LAST)
            TextView.text .tag_config("background", background=color[1])
        else:
            pass
    
    def color_background(self):
        color = colorchooser.askcolor(parent=self.master)
        
        if color!=None:
            TextView.text .config(background=color[1])
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
            TextView.text .image_create(END, image=self.imagen, padx=10, pady=10)
        else:
            pass
            
    def insertar_separador(self):
        """Inserta separador."""
        separador = Frame(TextView.text , bg="#4c545e", height=2, width=900).pack(padx=10, pady=10)
        TextView.text .window_create(END, window=separador)
        
        