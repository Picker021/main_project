import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_main()

    # метод инициализации виджетов
    def init_main(self):

        #Тулбар
        toolbar = tk.Frame(bg = '#d7d7d7', bd = 2)
        toolbar.pack(side = tk.TOP, fill = tk.X)

        # кнопка добавления
        self.add_image = tk.PhotoImage(file = './img/add.png')
        btn_add = tk.Button(toolbar, text = 'Добавить',
                            image = self.add_image,
                            bg = '#d7d7d7', bd = 0,
                            command=self.open_child)                        
        btn_add.pack(side = tk.LEFT)

        # кнопка изменения
        self.upd_image = tk.PhotoImage(file = './img/update.png')
        btn_upd = tk.Button(toolbar,
                            image = self.upd_image,
                            bg = '#d7d7d7', bd = 0,
                            command=self.open_upd)                        
        btn_upd.pack(side = tk.LEFT)

        # кнопка удаления
        self.del_image = tk.PhotoImage(file = './img/delete.png')
        btn_dlt = tk.Button(toolbar,
                            image = self.del_image,
                            bg = '#d7d7d7', bd = 0,
                            command=self.del_records)                        
        btn_dlt.pack(side = tk.LEFT)

        # кнопка поиска
        self.srch_image = tk.PhotoImage(file = './img/search.png')
        btn_srch = tk.Button(toolbar,
                            image = self.srch_image,
                            bg = '#d7d7d7', bd = 0,
                            command=self.open_search)                        
        btn_srch.pack(side = tk.LEFT)

        # кнопка сброса
        self.ref_image = tk.PhotoImage(file = './img/refresh.png')
        btn_ref = tk.Button(toolbar,
                            image = self.ref_image,
                            bg = '#d7d7d7', bd = 0,
                            command=self.view_records)                        
        btn_ref.pack(side = tk.LEFT)

        #Таблица вывода инфы для контактов
        self.tree = ttk.Treeview(self, columns = ('ID', 'name', 'phone', 'email', 'salary'),
                                show='headings', height = 17) 

        #настройки для столбцов
        self.tree.column('ID', width= 45, anchor = tk.CENTER)
        self.tree.column('name', width= 300, anchor = tk.CENTER)
        self.tree.column('phone', width= 150, anchor = tk.CENTER)
        self.tree.column('email', width= 150, anchor = tk.CENTER)
        self.tree.column('salary', width= 150, anchor = tk.CENTER)

        #задание подписи столбцов
        self.tree.heading('ID', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Номер')
        self.tree.heading('email', text='Эл. почта')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack()

        #Создание скроллбара
        scroll = tk.Scrollbar(root, command= self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill= tk.Y)
        self.tree.configure(yscrollcommand = scroll.set)
        
    #метод добавления в бд(посредник)
    def record(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    #Метод редактирования
    def upd_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE users SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
            ''', (name, phone, email, salary, id))
        self.db.conn.commit()
        self.view_records()

    #Метод удаления
    def del_records(self):
        for i in self.tree.selection():
            self.db.cur.execute('DELETE FROM users WHERE id = ?',
                                (self.tree.set(i, '#1'), ))
        self.db.conn.commit()
        self.view_records()

    #Метод поиска
    def search_records(self, name):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM users WHERE name LIKE ? ', ('%' + name + '%',))
        r = self.db.cur.fetchall()
        for i in r:
            self.tree.insert('', 'end', values = i)

    #перезаполнение виджета таблицы
    def view_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM users')
        r = self.db.cur.fetchall()
        for i in r:
            self.tree.insert('', 'end', values = i)


    #Метод открытия окна добавления
    def open_child(self):
        Child()

    #Метод открытия окна редактирования
    def open_upd(self):
        Update()

    #Метод открытия окна поиска
    def open_search(self):
        Search()


#Класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    #Создание виджетов дочернего окна
    def init_child(self):
        self.title('Добавить контакт')
        self.geometry('400x220')
        self.resizable(False, False)
        #перехват событий в приложении
        self.grab_set()
        #Перехват фокуса
        self.focus_set()

        label_name = tk.Label(self, text = 'ФИО')
        label_phone = tk.Label(self, text = 'Номер')
        label_email = tk.Label(self, text = 'Эл. почта')
        label_salary = tk.Label(self, text = 'Зарплата')
        label_name.place(x=60, y=50)
        label_phone.place(x=60, y=80)
        label_email.place(x=60, y=110)
        label_salary.place(x=60, y=140)

        self.entry_name = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_salary = tk.Entry(self)
        self.entry_name.place(x=220, y=50)
        self.entry_phone.place(x=220, y=80)
        self.entry_email.place(x=220, y=110)
        self.entry_salary.place(x=220, y=140)

        btn_close = tk.Button(self, text = 'Закрыть', command=self.destroy)
        btn_close.place(x=220, y=180)

        self.btn_ok = tk.Button(self, text = 'Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.record(self.entry_name.get(),
                                                                   self.entry_phone.get(),
                                                                   self.entry_email.get(),
                                                                   self.entry_salary.get()))
        self.btn_ok.place(x=290, y=180)

#Клас редактирвоания
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Изменить контакт')
        self.btn_ok.destroy()
        self.btn_upd = tk.Button(self, text = 'Сохранить')
        self.btn_upd.bind('<Button-1>',
                           lambda ev: self.view.upd_record(self.entry_name.get(),
                                                           self.entry_phone.get(),
                                                           self.entry_email.get(),
                                                           self.entry_salary.get()))
        self.btn_upd.bind('<Button-1>',
                          lambda ev: self.destroy(), 
                          add = '+')
        self.btn_upd.place(x=290, y=160)

    #метод автозаполнения формы
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * FROM users WHERE id = ?', (id, ))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

#Класс окна поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_search()

    #Создание виджетов дочернего окна
    def init_search(self):
        self.title('Найти контакт')
        self.geometry('300x100')
        self.resizable(False, False)
        #перехват событий в приложении
        self.grab_set()
        #Перехват фокуса
        self.focus_set()

        label_name = tk.Label(self, text = 'ФИО')
        label_name.place(x=40, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=140, y=20)

        btn_close = tk.Button(self, text = 'Закрыть', command=self.destroy)
        btn_close.place(x=130, y=70)

        self.btn_ok = tk.Button(self, text = 'Найти')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add = '+')
        self.btn_ok.place(x=220, y=70)

#Класс бд
class Db:

    #создание соединения, курсора и таблицы если её нет
    def __init__(self):
        self.conn = sqlite3.connect('contacts,db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT,
                         salary TEXT
        )''')
        

    #добавление в бд
    def insert_data(self, name, phone, email, salary):
        self.cur.execute('''
            INSERT INTO users (name, phone, email, salary)
            VALUES (?, ?, ?, ?)
    ''', (name, phone, email, salary))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Список сотрудников компании')
    root.geometry('945x450')
    root.resizable(False, False)
    db = Db()
    app = Main(root)
    app.pack()
    root.mainloop()