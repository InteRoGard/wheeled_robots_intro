import tkinter as tk            # является стандартной библиотекой
from tkinter.ttk import Combobox
from tkinter.messagebox import showerror, showwarning, showinfo

def selected(event):
    selection = Combobox.get()
    if selection == "Dijkstra":
        algorithm_Dijkstra()
    elif selection == "A*":
        algorithm_Astar()

def alg_calc():
    print(map_matrix)

def algorithm_Dijkstra():
    return 0

def algorithm_Astar():
    return 0

def alg_build(window, rows_str,  cols_str):
    showinfo("Руководство", "Пожалуйста, оставь старт и финиш в единичных экземплярах")
    reset_buttons()
    global buttons
    rows, cols = int(rows_str), int(cols_str)
    global map_matrix
    map_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            btn = tk.Button(frame, text=f"", bg="white", height = 2, width = 2)
            buttons.append(btn)
            btn.grid(row = i + 1, column = j + 1)
            btn.count = 0
            btn.i, btn.j = i, j
            btn.config(command = lambda button=btn: update_count(button, rows, cols))

def update_count(button, rows, cols):
    button.count += 1
    i, j = button.i, button.j
    match button.count:
        case 1:
            button.config(bg="gray")
        case 2:
            button.config(bg="#4cd473")
            button.config(text=f"Start")
        case 3:
            button.config(bg="#61c9cf")
            button.config(text=f"Finish")
        case 4:
            button.config(bg="white", text=f"")
            button.count = 0
    # button.config(text=f"{button.count}")
    map_matrix[i][j] = button.count

def reset():
    global buttons
    height = width = 0
    height_ent.delete(0, len(height_ent.get()))
    width_ent.delete(0, len(width_ent.get()))
    reset_buttons()
    
def reset_buttons():
    global buttons
    for button in buttons:
        button.destroy()
    buttons = []



h = w = 0
count_click = 0
buttons = []

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
height_lbl.grid(row = 2, column = 0, pady = (15, 5))
height_ent = tk.Entry(frame)
height_ent.grid(row = 3, column = 0)

width_lbl = tk.Label(frame, text = "Ширина поля:")
width_lbl.grid(row = 4, column = 0, pady = (10, 5))
width_ent = tk.Entry(frame)
width_ent.grid(row = 5, column = 0)

build_btn = tk.Button(frame, text = "Построить", height = 1, width = 10,
                     command = lambda: alg_build(window, height_ent.get(), width_ent.get()))
build_btn.grid(row = 6, column = 0, pady = (5, 0))

calc_btn = tk.Button(frame, text = "Запустить расчет", height = 1, width = 15,
                     command = lambda: alg_calc())
calc_btn.grid(row = 7, column = 0, pady = (5, 0))

reset_btn = tk.Button(frame, text = "Сбросить",
                     command = lambda: reset())
reset_btn.grid(row = 8, column = 0, pady = (5, 0))



###     ###     ###
window.mainloop()