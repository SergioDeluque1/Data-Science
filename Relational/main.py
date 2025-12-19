
from tkinter import *
from ventana import Ventana


def main():
    root = Tk()
    root.wm_title("Base de Datos")
    app = Ventana(root) 
    app.mainloop()



if __name__ == "__main__":
    main()