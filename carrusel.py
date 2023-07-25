"""Carrusel es un visor de imágenes"""

from tkinter import *
from PIL import Image, ImageTk
import os
from math import e
from tkinter import filedialog # para que el usuario elija el archivo o directorio


root = Tk()
root.title('Carrusel')
root.geometry('1020x750')
root.minsize(1020,750)

# Ajustar al tamaño de la ventana
n_rows = 2
n_columns = 3
for i in range(n_rows):
    root.grid_rowconfigure(i,  weight =1)
for i in range(n_columns):
    root.grid_columnconfigure(i,  weight =1)


fname = [] # donde se guardaran los nombre de los archivos
img = ImageTk.PhotoImage(Image.open(r"C:\Users\Alexis Aragon\OneDrive\Imágenes/muslos.jpg")) # imagen de la ventana inicial
img_num = 0
dir = '' # donde se guardará el directorio

#------------------------------#------------------------------------#
# Función para que el usuario seleccione un directorio donde buscar
def open():

    global l
    global lname
    global btn_next
    global btn_back
    global dir    

    dir = filedialog.askdirectory(initialdir=r"C:\Users\Alexis Aragon\OneDrive\Imágenes/")
    dir = str(dir) + '/'  

    fname.clear()
   
    for i in os.listdir(dir):
        fname.append(i)

    getImage(dir, img_num)

    lname = Label(root, text=fname[img_num])
    lname.grid(row=0, column=1)
    l = Label(root, image=img, height=750, width=1020, )
    l.grid(row=1, column=0, columnspan=3)

    btn_back = Button(root, text='N/A', state=DISABLED, borderwidth=1)
    btn_next = Button(root, text='->', command=lambda: pasar(1), borderwidth=1)

    # btn_back = customtkinter.CTkButton(master=root, text='N/A', state=DISABLED, width=0, height=0, fg_color="#262626", hover_color="#262626")

    btn_back.grid(row=1, column=0, sticky=W, ipady=340, ipadx=50)
    btn_next.grid(row=1, column=2, sticky=E, ipady=340, ipadx=50) 
    
#------------------------------#------------------------------------#
# Función para obtener imágenes y modificar las dimensiones de la misma
def getImage(dir, img_num):  
    global img
    
    l.grid_forget()
    lname.grid_forget() 

    img = Image.open(dir + fname[img_num])
    w, h = img.size
    if h >= 800:
        z = 1.2651*e**(-6*10**(-4)*h) # porcentaje en que se modificará el ancho de la imagen para mantener la relación de aspecto
        img = img.resize((int(w*z), int(720)))

    img = ImageTk.PhotoImage(img)
    return img
      
#------------------------------#------------------------------------#
# Función para cambiar a la imagen siguiente o anterior
def pasar(num):
    global l
    global lname
    global btn_next
    global btn_back
    
    img_num = num
    btn_back.grid_forget()
    btn_next.grid_forget()

    getImage(dir, img_num)
    
    lname = Label(root, text=fname[img_num])
    l = Label(root, image=img, height=750, width=1020, )

    btn_back = Button(root, text='<-', command=lambda: pasar(img_num - 1), borderwidth=1)
    btn_next = Button(root, text='->', command=lambda: pasar(img_num + 1), borderwidth=1)
    # btn_back = customtkinter.CTkButton(master=root, text='<-', command=lambda: pasar(img_num - 1), width=0, height=0, fg_color="#262626", hover_color="#262626")

    if img_num == len(fname)-1:
        btn_next = Button(root, text='N/A', state=DISABLED, borderwidth=1)
    
    if img_num == 0:
        btn_back = Button(root, text='N/A', state=DISABLED, borderwidth=1)
        # btn_back = customtkinter.CTkButton(master=root, text='N/A', state=DISABLED, width=0, height=0, fg_color="#262626", hover_color="#262626")
    
    lname.grid(row=0, column=1)
    l.grid(row=1, column=0, columnspan=3)
    btn_back.grid(row=1, column=0, sticky=W, ipady=340,ipadx=50)
    btn_next.grid(row=1, column=2, sticky=E, ipady=340,ipadx=50)

#------------------------------#------------------------------------#
# Se imprime la primera ventana
btn = Button(root, text='Abrir Directorio', command=open)  
btn.grid(row=0, column=0, sticky=W, ipady=10, ipadx=10)

lname = Label(root, text='muslos.jpg')
lname.grid(row=0, column=1)
l = Label(root, image=img, height=750, width=1020, )
l.grid(row=1, column=0, columnspan=3)
    
root.mainloop()