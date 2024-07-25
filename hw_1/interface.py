import tkinter as tk                # является стандартной библиотекой
from tkinter.ttk import Combobox
from tkinter.messagebox import showerror, showwarning, showinfo
from graph import Graph

class Interface:

    def __init__(self):

        self.rows = 0
        self.cols = 0
        self.count_click = 0
        self.buttons = []
        self.way = []
        self.vertices = 0
        self.selection = ''
        self.map_matrix = []
        self.adj_matrix = []

        self.window = tk.Tk()
        self.window.title('Кратчайший путь')
        self.window.geometry('750x500')


        frame = tk.Frame(self.window, padx = 10, pady = 10)
        # frame.pack(expand = True)       # виджет заполняет весь контейнер, выделенный для него
        frame.pack(fill = tk.Y)       # виджет заполняет все доступное пространство
        # frame = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=5)

        algorithm_lbl = tk.Label(frame, text = "Выберите алгоритм поиска пути")
        algorithm_lbl.grid(row = 0, column = 0, pady = (20, 0))
        # algorithm_lbl.configure(text = "хзхзхз")    # изменяет виджет уже после добавления

        methods = ["Dijkstra", "A*"]

        cb = Combobox(frame, values = methods, width = 15, 
                    state = "readonly", justify = 'center')
        cb.grid(row = 1, column = 0, pady = (5, 0))
        cb.set("")                                                  # пустое значение по умолчанию
        cb.bind("<<ComboboxSelected>>", self.selected(cb))          # узнаем выбранное пользователем значение

        height_lbl = tk.Label(frame, text = "Высота поля:")
        height_lbl.grid(row = 2, column = 0, pady = (15, 5))
        height_ent = tk.Entry(frame)
        height_ent.grid(row = 3, column = 0)

        width_lbl = tk.Label(frame, text = "Ширина поля:")
        width_lbl.grid(row = 4, column = 0, pady = (10, 5))
        width_ent = tk.Entry(frame)
        width_ent.grid(row = 5, column = 0)

        build_btn = tk.Button(frame, text = "Построить", height = 1, width = 10,
                            command = lambda: self.alg_build(self.window, height_ent.get(), 
                                                             width_ent.get(), frame))
        build_btn.grid(row = 6, column = 0, pady = (5, 0))

        calc_btn = tk.Button(frame, text = "Запустить расчет", height = 1, width = 15,
                            command = lambda: self.alg_calc())
        calc_btn.grid(row = 7, column = 0, pady = (5, 0))

        reset_btn = tk.Button(frame, text = "Сбросить",
                            command = lambda: self.reset(height_ent, width_ent))
        reset_btn.grid(row = 8, column = 0, pady = (5, 0))

        self.window.mainloop()

    def selected(self, cb):
        # global selection
        self.selection = ''
        self.selection = cb.get()

    def alg_calc(self):
        self.vertices = self.rows * self.cols
        start, finish = 0, 0                        # ошибка - игнорирует серые клетки
        for i in range(self.rows):                  # баг в рассчетах появляется в циклах
            for j in range(self.cols):              # на выходе изменения в матрице пропадают
                num = ((i * self.cols) + j)
                if self.map_matrix[i][j] == 2:
                    start = num
                    # print(f'start {start}')
                elif self.map_matrix[i][j] == 3:
                    finish = num
                    # print(f'finish {finish}')
                # elif self.map_matrix[i][j] == 1:
                    # g.remove(num)
                elif self.map_matrix[i][j] == 1:
                    for k in range(self.vertices):
                        self.adj_matrix[num][k] = 0
                        # print(self.adj_matrix[num][k], num, k)
                        self.adj_matrix[k][num] = 0
                    # print(f'if выколотой точки сработал, num {num}')
                    # print(f'adj_matrxi: {self.adj_matrix}')
                    # print(self.adj_matrix)
                else:
                    for k in range(self.vertices):
                        if (k % self.cols != (self.cols - 1)):    # сосед справа
                            self.adj_matrix[k][k + 1] = 1
                            self.adj_matrix[k + 1][k] = 1
                        if self.vertices - k > self.cols:         # сосед снизу
                            self.adj_matrix[k + self.cols][k] = 1
                            self.adj_matrix[k][k + self.cols] = 1
        # print(f'map_matrix: {self.map_matrix}')
        
        g = Graph(self.vertices)
        g.graph = self.adj_matrix
        # print(f'graph: {g.graph}')
        src, fnsh, pred = g.Dijkstra(start, finish)
        self.way = g.printSolution(src, fnsh, pred)
        self.way = self.way[::-1]
        count = 0
        i = 0
        for btn in self.buttons:
            if count in self.way:
                btn.config(bg = "#ccffcc")
                i += 1
            count += 1
        print('\nway', self.way)
        # print(adj_matrix)

    def alg_build(self, window, rows_str,  cols_str, frame):
        showinfo("Руководство", "Порядок:\nПрепятствия -> Start -> Finish\nИначе - Сбросить!" +
                 "\n\nПожалуйста, оставьте старт и финиш в единичных экземплярах")
        self.reset_buttons()
        # global buttons
        # global rows, cols, vertices
        self.rows, self.cols = int(rows_str), int(cols_str)
        vertices = self.rows * self.cols
        # global map_matrix, adj_matrix
        self.map_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.adj_matrix = [[0 for _ in range(vertices)] for _ in range(vertices)]

        for k in range(vertices):
            if (k % self.cols != (self.cols - 1)):    # сосед справа
                self.adj_matrix[k][k + 1] = 1
                self.adj_matrix[k + 1][k] = 1
            if vertices - k > self.cols:         # сосед снизу
                self.adj_matrix[k + self.cols][k] = 1
                self.adj_matrix[k][k + self.cols] = 1

        for i in range(self.rows):
            for j in range(self.cols):
                btn = tk.Button(frame, text=f"", bg="white", height = 2, width = 2)
                self.buttons.append(btn)
                btn.grid(row = i + 1, column = j + 1)
                btn.count = 0
                btn.i, btn.j = i, j
                btn.config(command = lambda button = btn: self.update_count(button, self.rows, self.cols))

    def update_count(self, button, rows, cols):
        # global start_point, finish_point
        i, j = button.i, button.j
        num = ((i * cols) + j)
        button.count += 1
        x = 0
        match button.count:
            case 1:
                button.config(bg="gray")
                # x = 1
            case 2:
                button.config(bg="#4cd473")
                button.config(text=f"Start")
                # x = 0
            case 3:
                button.config(bg="#61c9cf")
                button.config(text=f"Finish")
                # x = 0
            case 4:
                button.config(bg="white", text=f"")
                button.count = 0
                # x = 0
        # button.config(text=f"{button.count}")
        self.map_matrix[i][j] = button.count

    def reset(self, height_ent, width_ent):
        # global buttons
        # height = width = 0
        height_ent.delete(0, len(height_ent.get()))
        width_ent.delete(0, len(width_ent.get()))
        self.reset_buttons()

    def reset_buttons(self):
        # global buttons
        for button in self.buttons:
            button.destroy()
        self.buttons = []

    # def wait(self):
    #     self.window.mainloop()

# if __name__ == "__main__":
#     # interface = Interface()
#     Interface().window.mainloop()