
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

def center_window(window, width=290, height=150, windowsbar=False):
        """
        CENTRA UNA VENTANA PRINCIPAL.
        ------------------------------------------------
        Los parametros:
            window: ventana principal. (Tk)
            width: ancho de la ventana. (int)
            height: largo de la ventana. (int)
            windowsbar: consideracion de la barra de tareas de Windows. (boolean)
                    -True: si se desea considerar la barra
                    -False: si no se quiere considerar la barra.
        """
        window.withdraw()
        window.update_idletasks()

        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw - width)/2
        y = (sh - height)/2 - (35 if windowsbar else 0)
        
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
        window.deiconify()
        
        
        
def center_toplevel(window, parent, width=290, height=150, center_all=True):
        """
        CENTRA UNA VENTANA HIJA (TOPLEVEL).
        ------------------------------------------------
        Los parametros:
            window: ventana hija. (Toplevel)
            width: ancho de la ventana. (int)
            height: largo de la ventana. (int)
        """
        if center_all:
            window.update_idletasks()
            width = window.winfo_width()
            frm_width = window.winfo_rootx() - window.winfo_x()
            win_width = width + 2 * frm_width
            height = window.winfo_height()
            titlebar_height = window.winfo_rooty() - window.winfo_y()
            win_height = height + titlebar_height + frm_width
            x = window.winfo_screenwidth() // 2 - win_width // 2
            y = window.winfo_screenheight() // 2 - win_height // 2
            window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        else:
            sw = parent.winfo_rootx()
            sh = parent.winfo_rooty()
            x = (sw + 20)
            y = (sh + 30)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.update_idletasks()
            
            
if __name__ == "__main__":
    """Prueba del metodo centrar ventana."""
    def toplevel(tk):
        top = Toplevel(tk)
        top.title('Toplevel')
        center_toplevel(top, tk)
        
    root = Tk()
    root.title('Tk')
    center_window(root)
    ttk.Button(root, text="Abrir Toplevel", command=lambda: toplevel(root)).pack(anchor=CENTER, padx=10, pady=20)
    root.mainloop()
    