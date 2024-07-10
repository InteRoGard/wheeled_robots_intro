'''
import turtle as t

n = int(input())
k = 100
screen_size = n * k

t.turtlesize(5, 5)
t.screensize(screen_size * 2, screen_size * 2)  # размер холста
#t.setup(screen_size * 4, screen_size * 4)      # размер окна в целом
t.speed(3)

# #square = t.Turtle()
# t.pencolor("black")
# t.fillcolor("black")
# t.begin_fill()
# t.circle(50)
# t.end_fill()

for i in range(n - 1):
    t.penup()
    t.goto(0, k + k*i)
    t.pendown()
    t.goto(n*k, k + k*i)

    t.penup()
    t.goto(k + k*i, 0)
    t.pendown()
    t.goto(k + k*i, n*k)

t.mainloop()
#t.exitonclick()

'''


import tkinter as tk    # является стандартной библиотекой
from tkinter.ttk import Combobox
from tkinter.messagebox import showerror, showwarning, showinfo



def selected(event):
    selection = Combobox.get()
    if selection == "Dijkstra":
        algorithm_Dijkstra()
    elif selection == "A*":
        algorithm_A()

def algorithm_Dijkstra():
    return 0

def algorithm_A():
    return 0

def alg_build(h_str,  w_str):
    # if ((type(h) is not int) or (type(w) is not int)):
        # showwarning(title = "Предупреждение", message = "Введите целочисленные значения")
    for widget in frame.winfo_children():
        widget.destroy()
    h = int(h_str)
    w = int(w_str)
    for i in range(h):
        for j in range(w):
            tk.Button(frame, height = 2, width = 4).grid(row = i + 1, column = j + 1, padx = 0, pady = 0)

def alg_calc():
    return 0

def alg_reset():
    height = width = 0
    height_ent.delete(0, len(height_ent.get()))
    width_ent.delete(0, len(width_ent.get()))


height = width = 0
h = w = 0

window = tk.Tk()
window.title('Кратчайший путь')
window.geometry('750x500')


frame = tk.Frame(window, padx = 10, pady = 10)
# frame.pack(expand = True)       # виджет заполняет весь контейнер, выделенный для него
frame.pack(fill = tk.Y)       # виджет заполняет все доступное пространство
# frame = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=5)

algorithm_lbl = tk.Label(frame, text = "Выберите алгоритм поиска пути")
algorithm_lbl.grid(row = 0, column = 0, pady = (20, 0))         # координаты считаются относительно наличия других элементов
# algorithm_lbl.configure(text = "хзхзхз")    # изменяет виджет уже после добавления

methods = ["Dijkstra", "A*"]

cb = Combobox(frame, values = methods, width = 15, 
              state = "readonly", justify = 'center')
cb.grid(row = 1, column = 0, pady = (5, 0))
cb.set("Dijkstra")                              # значение по умолчанию
cb.bind("<<ComboboxSelected>>", selected)       # узнаем выбранное пользователем значение

height_lbl = tk.Label(frame, text = "Высота поля:")
height_lbl.grid(row = 2, column = 0, pady = (25, 5))
height_ent = tk.Entry(frame)
height_ent.grid(row = 3, column = 0)

width_lbl = tk.Label(frame, text = "Ширина поля:")
width_lbl.grid(row = 4, column = 0, pady = (10, 5))
width_ent = tk.Entry(frame)
width_ent.grid(row = 5, column = 0)

build_btn = tk.Button(frame, text = "Построить", height = 2, width = 10,
                     command = lambda: alg_build(height_ent.get(), width_ent.get()))
build_btn.grid(row = 6, column = 0, pady = (25, 0))

calc_btn = tk.Button(frame, text = "Запустить расчет", height = 2, width = 15,
                     command = lambda: alg_calc())
calc_btn.grid(row = 7, column = 0, pady = (5, 0))

reset_btn = tk.Button(frame, text = "Сбросить",
                     command = lambda: alg_reset())
reset_btn.grid(row = 8, column = 0, pady = (15, 0))



###     ###     ###
window.mainloop()