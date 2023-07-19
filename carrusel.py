from tkinter import *
from PIL import Image, ImageTk
import os
from math import e

pictureFolderWin = r"C:\Users\Alexis Aragon\OneDrive\Imágenes/"

ASUS = r"C:\Users\Alexis Aragon\OneDrive\Imágenes\ASUS/"

root = Tk()
root.title('Carrusel')


# len = len(os.listdir(pictureFolderWin))
# print(len)

# Buscar archivos en directorio

cont = 1

for filename in os.listdir(pictureFolderWin): 
    name, extension = os.path.splitext(pictureFolderWin + filename)
    
    if extension in [".jpg", ".jpeg"]:
        os.rename(pictureFolderWin + filename, ASUS + 'name' + str(cont) + '.jpg')
        cont+=1
      
Lista = []
for i in range(1, len(os.listdir(ASUS))):
    img = Image.open(ASUS + 'name' + str(i) + '.jpg')
    w, h = img.size
    if h > 800:
        z = 1.2651*e**(-6*10**(-4)*h) # porcentaje en que se modificará el ancho de la imagen para mantener la relación de aspecto
        img = img.resize((int(w*z), int(742))) 
    img = ImageTk.PhotoImage(img)
    Lista.append(img)


# Lista = []
# for i in range(1,6):
#     img = ImageTk.PhotoImage(Image.open('images/' + str(i) + '.png'))
#     Lista.append(img)
    
l = Label(root, image=Lista[0], height=742, width=1020)
l.grid(row=0, column=0, columnspan=3)

def pasar(img_num):
    global l
    global btn_next
    global btn_back

    l.grid_forget() # olvidar lo que esta dentro de la grilla
    btn_back.grid_forget()
    btn_next.grid_forget()
    l = Label(root, image=Lista[img_num], height=742, width=1020)
    btn_back = Button(root, text='<-', command=lambda: pasar(img_num - 1))
    btn_next = Button(root, text='->', command=lambda: pasar(img_num + 1))

    if img_num == len(Lista)-1:
        btn_next = Button(root, text='N/A', state=DISABLED)
    
    if img_num == 0:
        btn_back = Button(root, text='N/A', state=DISABLED)
    
    l.grid(row=0, column=0, columnspan=3)
    btn_back.grid(row=1, column=0)
    btn_next.grid(row=1, column=2)

btn_back = Button(root, text='N/A', state=DISABLED)
btn_next = Button(root, text='->', command=lambda: pasar(1))

btn_back.grid(row=1, column=0)
btn_next.grid(row=1, column=2)

root.mainloop()