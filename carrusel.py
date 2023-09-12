"""Carrusel es un visor de imágenes"""

from tkinter import (DISABLED, Label, filedialog, messagebox, StringVar)
import os
from math import e
from PIL import Image, ImageTk

from customtkinter import (CTk, set_appearance_mode,
                           CTkButton, CTkLabel, CTkOptionMenu)


def get_images_dir():
    """
    Función para encontrar la ruta del directorio de imagenes por defecto de windows
    """

    # Obtener la ubicación de la carpeta de imágenes en Windows
    ruta_imagenes = os.path.join(os.environ['USERPROFILE'], 'Pictures')

    # Verificar si la carpeta de imágenes existe en la ubicación predeterminada
    if os.path.exists(ruta_imagenes):
        return ruta_imagenes

    # Intenta obtener la ubicación de la carpeta de imágenes dentro de OneDrive
    ruta_onedrive_base = os.path.join(os.environ['USERPROFILE'], 'OneDrive')
    ruta_imagenes_onedrive = os.path.join(ruta_onedrive_base, 'Imágenes')

    # Comprueba si la carpeta de imágenes en OneDrive existe
    if os.path.exists(ruta_imagenes_onedrive):
        return ruta_imagenes_onedrive

    # Si ninguna ubicación es válida, devuelve None
    return None

# ------------------------------#------------------------------------#


def open_dir(img_num=0):
    """
    Función para que el usuario seleccione un directorio donde buscar imágenes
    """
    ruta_default = get_images_dir()

    # seleccionar directorio
    selected_directory = str(
        filedialog.askdirectory(initialdir=ruta_default)) + '/'

    fname.clear()  # almacena los nombres de los archivos

    for name in os.listdir(selected_directory):
        _, extension = os.path.splitext(selected_directory + name)
        if extension == '.jpg' or extension == '.png':
            fname.append(name)

    if len(fname) == 0:
        messagebox.showwarning('titulo', 'No hay imágenes en el directorio')
    else:
        pasar_imagen(selected_directory, img_num)

    return selected_directory

# ------------------------------#------------------------------------#
# Función para obtener imágenes y modificar las dimensiones de la misma


def get_image(selected_directory: str, img_num: int):
    """
    Función para obtener la imágen. 
    Se implementa un algoritmo para redimencionar la imágen
    y conservar su relación de aspecto
    """
    global img

    l.grid_forget()
    lname.grid_forget()

    img = Image.open(selected_directory + fname[img_num])
    w, h = img.size
    resize_w = w
    resize_h = h

    # porcentaje en que se modificará el ancho de la imagen para mantener la relación de aspecto
    if h >= 750:
        z = 1.2651*e**(-6*10**(-4)*h)
        resize_w = int(w*z)
        img = img.resize((resize_w, int(722)))

    if resize_w >= 820:
        x = 1.2651*e**(-6*10**(-4)*w)
        resize_h = int(h*x)
        img = img.resize((820, resize_h))

    img = ImageTk.PhotoImage(img)
    return img


# ------------------------------#------------------------------------#
def pasar_imagen(selected_directory: str, num: int):
    """ 
    Función para mostrar las imágenes y botones en la interfaz 

    recibe como argumento un número entero que se usara como indice para buscar la imagen
    en la lista de nombres imagenes (fname) 
    """
    global l
    global lname
    global btn_back
    global btn_next

    img_num = num

    get_image(selected_directory, img_num)
    lname = CTkLabel(root, text=fname[img_num])
    lname.grid(row=0, column=1)
    l = Label(root, image=img, bg=color_theme)
    l.grid(row=1, column=0, columnspan=3, rowspan=2)

    btn_back = CTkButton(root, text='<-',
                         command=lambda: pasar_imagen(
                             selected_directory, img_num - 1), text_color=text_color,
                         hover_color=color_theme, fg_color=color_theme, width=100)
    btn_next = CTkButton(root, text='->',
                         command=lambda: pasar_imagen(
                             selected_directory, img_num + 1), text_color=text_color,
                         hover_color=color_theme, fg_color=color_theme, width=100)
    btn_back.grid_forget()
    btn_next.grid_forget()
    if img_num == 0:
        btn_back = CTkButton(root, text='N/A', state=DISABLED, text_color=text_color,
                             hover_color=color_theme, fg_color=color_theme, width=100)

    if img_num == len(fname)-1:
        btn_next = CTkButton(root, text='N/A', state=DISABLED, text_color=text_color,
                             hover_color=color_theme, fg_color=color_theme, width=100)
    btn_back.grid(row=1, column=0, sticky='w', ipady=340)
    btn_next.grid(row=1, column=2, sticky='e', ipady=340)


def change_theme(theme: str):
    """ Función para cambiar el tema de la app
        'Dark' o 'Light'
    """
    global color_theme
    global text_color

    if theme == 'Dark':
        set_appearance_mode("dark")
        color_theme = '#242424'
        text_color = '#f2f2f2'
    else:
        set_appearance_mode("light")
        color_theme = '#ebebeb'
        text_color = '#000'
    # Configura el color de fondo
    if btn_back is not None and btn_next is not None:
        btn_back.configure(fg_color=color_theme,
                           hover_color=color_theme, text_color=text_color)
        btn_next.configure(fg_color=color_theme,
                           hover_color=color_theme, text_color=text_color)
    l.configure(bg=color_theme)


# ------------------------------#------------------------------------#
root = CTk()
root.title('Carrusel')
root.geometry('1020x750')
root.minsize(1020, 750)

# Ajustar al tamaño de la ventana
for j in range(2):
    root.grid_rowconfigure(j,  weight=1)
for k in range(3):
    root.grid_columnconfigure(k,  weight=1)

btn_next = None
btn_back = None
# Se imprime la primera ventana
btn = CTkButton(root, text='Abrir Directorio', command=open_dir)
btn.grid(row=0, column=0, sticky='w', ipadx=10)

# imagen de la ventana inicial
basedir = os.path.dirname(__file__)
ruta_img_portada = os.path.join(basedir, 'muslos.jpg')
img = ImageTk.PhotoImage(Image.open(ruta_img_portada))

lname = CTkLabel(root, text='muslos.jpg')
lname.grid(row=0, column=1)
l = Label(root, image=img, height=722, width=1020)
l.grid(row=1, column=0, columnspan=3)

fname = []


color_theme = '#ebebeb'
text_color = '#000'
themes = ['Dark', 'Light']
value = StringVar()
value.set('Light')

drop = CTkOptionMenu(root, values=themes, variable=value,
                     command=lambda x: change_theme(value.get()))
drop.grid(row=0, column=2, sticky='E', ipadx=10)


root.mainloop()
