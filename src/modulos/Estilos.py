
__author__ = "admin"
__date__ = "$10/01/2015 12:29:49 AM$"

from tkinter import ttk

def estilos():
    #Style font general
    s = ttk.Style()
    s.configure('.', font=('Franklin Gothic Book', 10))
        
    curr_theme = s.theme_use()
    s.theme_settings(curr_theme, {"TEntry": {"configure": {"padding":
                     2}, "map": {"foreground": [("focus", "red")]}}})
        
        
    #Style Notebook
    style_book = ttk.Style()
    style_book.configure("ButtonNotebook", 
                         background='#555D69', 
                         padding=-5, 
                         relief="flat", 
                         borderwidth=0)
    style_book.map("ButtonNotebook",
                   highlightcolor=[('focus', 'green'), ('!focus', 'red')],
                   fieldbackground=[("!disabled", "green3")])
    style_book.configure("ButtonNotebook.Tab",
                         background='#29373e',
                         foreground='black',
                         font=('Franklin Gothic Book', 10),
                         padding=3,
                         borderwidth=0)
    style_book.layout("ButtonNotebook", [("ButtonNotebook.client", {"sticky": "nswe"})])
    style_book.layout("ButtonNotebook.Tab", [
                      ("ButtonNotebook.tab", {"sticky": "nswe", "children":
                      [("ButtonNotebook.padding", {"side": "top", "sticky": "nswe",
                      "children":
                      [("ButtonNotebook.focus", {"side": "top", "sticky": "nswe",
                      "children":
                      [("ButtonNotebook.label", {"side": "left", "sticky": ''}),
                      ("ButtonNotebook.close", {"side": "left", "sticky": ''})]
                      })]
                      })]
                      })]
                      )
    style_book.map("ButtonNotebook.Tab", 
                   foreground=[('disabled', 'dark gray'), ('pressed', 'white'), ('active', '#4A148C'), ('selected', '#4A148C')],
                   background=[('disabled', 'red'), ('active', '#263238'), ('pressed', '!focus', '#263238'), ('selected', '#263238')],
                   font=[('selected', ('Franklin Gothic Book', 10, 'bold'))],
                   relief=[('selected', 'flat')]
                   )
        
        
        
        