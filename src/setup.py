__author__ = "Jose Diaz"

# Let's start with some default (for me) imports...
import sys
from cx_Freeze import setup, Executable


build_exe_options = {
"include_msvcr": True   #skip error msvcr100.dll missing
}
# Process the includes, excludes and packages first

carpeta = 'Siconu'  #nombre de la carpeta donde se instalara el programa

if 'bdist_msi' in sys.argv:
    sys.argv += ['--initial-target-dir', 'C:\Program File\\ ' + carpeta]

includes = ["tkinter","PIL","os","sys","platform","sqlite3","datetime","winsound","modulos"] #librerias que lleva tu proyecto o tus propios modulos
excludes = []
packages = []
path = []
include_files = ['image','audio','DB'] #carpeta de las imagenes o otras carpetas que deseas que los copea Nota:NO es recomendado poner scripts o codigo fuente ya que esto se vera por el usuario.
include_msvcr = ['networkChanger.exe.manifest']

if sys.platform == 'win32':
    base = 'Win32GUI'
if sys.platform == 'linux' or sys.platform == 'linux2':
    base = None

angy = Executable(
    # what to build
    script = "agenda.py", #archivo q ejecuta todo el programa
    initScript = None,
    base = base,
    compress = True,
    copyDependentFiles = True,
    appendScriptToExe = True,
    appendScriptToLibrary = True,
    icon = "image\Icon.ico", #icono del programa
    #shortcutName="DHCP",
    #shortcutDir="ProgramMenuFolder"
    )

setup(

    version = "1.0",
    description = "Control de alarmas, notas, agenda, entro otas funcionalidades mas.", #pequeña descripcion
    author = "Jose Diaz", #autor
    name = "Agenda Personal", #nombre del programa
    #long_description=open('README.md').read(), #Descripcion larga
    author_email='jozz.18x@gmail.com', #Email del autor
    url='https://www.facebook.com/jozz.diaz.m', #Sitio web
    download_url='https://www.facebook.com/jozz.diaz.m', #Sitio web de descarga
    platforms = ['OS Independent'], #Nombre de la plataforma (En este caso multiplataforma)
    #license = 'LGPL v3', #Nombre de la Licencia del software.

    options = {"build_exe": {"includes": includes,
                 "excludes": excludes,
                 "packages": packages,
                 "path": path,
                 "include_files": include_files,
                 "include_msvcr": include_msvcr,
                 }
           },

    executables=[angy]
    )
