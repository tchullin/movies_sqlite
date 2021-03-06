from tkinter import *
from tkinter import ttk
import sqlite3


root = Tk()

class Functions():

    def Clear_data(self):
        self.entry_id.delete(0, END)
        self.entry_artistic_name.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_birth_date.delete(0, END)
        self.entry_death_date.delete(0, END)
        self.entry_birth_place.delete(0, END)
        self.entry_death_place.delete(0, END)
        self.entry_artistic_name.focus()

    def db_conect(self):
        self.connection = sqlite3.connect('movies.db')
        self.cursor = self.connection.cursor()
        print("connecting to database");

    def db_desconect(self):
        self.connection.close()
        print("Desconnecting from database sqlite3");

    def criar_tabela(self):
        self.db_conect();
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS actors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artistic_name VARCHAR(25) NOT NULL,
            name VARCHAR(35) NOT NULL,
            birth_date DATE NOT NULL,
            death_date DATE,
            birth_place VARCHAR(15) NOT NULL,
            death_place VARCHAR(15));""");
        self.connection.commit(); print("created database");
        self.db_desconect()

    def capture_entries(self):
        self.id = self.entry_id.get()
        self.artistic_name = self.entry_artistic_name.get()
        self.name = self.entry_name.get()
        self.birth_date = self.entry_birth_date.get()
        self.death_date = self.entry_death_date.get()
        self.birth_place = self.entry_birth_place.get()
        self.death_place = self.entry_death_place.get()

    def add_actor(self):
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""INSERT INTO actors (artistic_name,name,birth_date,death_date,birth_place,death_place) 
        VALUES(?,?,?,?,?,?)""",(self.artistic_name,self.name,self.birth_date,self.death_date,self.birth_place,self.death_place))
        self.connection.commit()
        self.db_desconect()
        self.select_list()
        self.Clear_data()

    def select_list(self):
        self.list_grid.tag_configure('oddrow', background="white")
        self.list_grid.tag_configure('evenrow', background="lightblue")
        self.list_grid.delete(*self.list_grid.get_children())
        self.db_conect()
        list = self.cursor.execute("""SELECT * FROM actors ORDER BY artistic_name ASC;""")
        count = 0
        for l in list:
            if count % 2 == 0:
                self.list_grid.insert("",END,values=l, tags=('evenrow',))
            else:
                self.list_grid.insert("", END, values=l, tags=('oddrow',))
            count += 1
        self.db_desconect()

    def OnDoubleClick(self,event):
        self.Clear_data()
        self.list_grid.selection()

        for x in self.list_grid.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.list_grid.item(x, 'values')
            self.entry_id.insert(END, col1)
            self.entry_artistic_name.insert(END, col2)
            self.entry_name.insert(END, col3)
            self.entry_birth_date.insert(END, col4)
            self.entry_death_date.insert(END, col5)
            self.entry_birth_place.insert(END, col6)
            self.entry_death_place.insert(END, col7)

    def delete_actor(self):
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""DELETE FROM actors WHERE id = ?""",(self.id,))
        self.connection.commit()
        self.db_desconect()
        self.Clear_data()
        self.select_list()

    def update_actor(self):
        self.capture_entries()
        self.db_conect()


        self.cursor.execute("""UPDATE actors SET artistic_name = ?, name = ?, birth_date = ?, death_date = ? , 
        birth_place = ? , death_place = ? WHERE id = ?;
        """,(self.artistic_name,self.name,self.birth_date,self.death_date,self.birth_place,self.death_place, self.id))
        self.connection.commit()
        self.db_desconect()
        self.Clear_data()
        self.select_list()

    def Search_actor(self):
        self.db_conect()
        self.list_grid.delete(*self.list_grid.get_children())
        self.entry_name.insert(END,'%')
        name = '%'+self.entry_name.get()
        self.cursor.execute("""SELECT * FROM actors WHERE artistic_name LIKE '%s' COLLATE NOCASE ORDER BY name ASC""" % name)
        result_search = self.cursor.fetchall()
        for actors in result_search:
            self.list_grid.insert("",END,values=actors)
        self.db_desconect()
        self.Clear_data()
        self.db_desconect()


class Aplication(Functions):

    def __init__(self):
        self.root = root
        self.screen()
        self.frames_screen()
        self.grid_actor()
        self.widgets_frame1()
        self.criar_tabela()
        self.select_list()
        root.mainloop()

    def screen(self):
        self.root.title("Actors Registration")
        self.root.geometry("1024x768")
        self.root.resizable(True, True)
        self.root.maxsize(width=1024, height=768)
        self.root.minsize(width=512, height=384)
        self.root.iconbitmap('Palm-tree.ico')

    def frames_screen(self):
        self.frame1 = LabelFrame(self.root, bd=2, text='Actors Table Maintenance')
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame2 = LabelFrame(self.root, bd=2, text='Actors Tabel List')
        self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        # bot??o Clear
        self.bt_Clear = Button(self.frame1, text="Clear",  command=self.Clear_data)
        self.bt_Clear.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        # bot??o Search
        self.bt_Search = Button(self.frame1, text="Search", command=self.Search_actor)
        self.bt_Search.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        # bot??o Add
        self.bt_Add = Button(self.frame1, text="Add", command=self.add_actor)
        self.bt_Add.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        # Bot??o Update
        self.bt_update = Button(self.frame1, text="update", command=self.update_actor)
        self.bt_update.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        # Bot??o Delete
        self.bt_Delete = Button(self.frame1, text="Delete", command=self.delete_actor)
        self.bt_Delete.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # label / entry - id -----------------------------
        self.lb_id = Label(self.frame1, text="id", )
        self.lb_id.place(relx=0.05, rely=0.05)

        self.entry_id = Entry(self.frame1, text="id", )
        self.entry_id.place(relx=0.05, rely=0.15, relwidth=0.08)

        # label / entry - artistic_name ----------------------------------
        self.lb_artistic_name = Label(self.frame1, text="Art Name", )
        self.lb_artistic_name.place(relx=0.05, rely=0.35)

        self.entry_artistic_name = Entry(self.frame1, )
        self.entry_artistic_name.place(relx=0.15, rely=0.35, relwidth=0.7)

        # label / entry - name ----------------------------------
        self.lb_name = Label(self.frame1, text="Name", )
        self.lb_name.place(relx=0.05, rely=0.45)

        self.entry_name = Entry(self.frame1, )
        self.entry_name.place(relx=0.15, rely=0.45, relwidth=0.7)

        # label / entry - Data Nascimento --------------------------
        self.lb_birth_date = Label(self.frame1, text="Birth", )
        self.lb_birth_date.place(relx=0.05, rely=0.55)

        self.entry_birth_date = Entry(self.frame1, )
        self.entry_birth_date.place(relx=0.15, rely=0.55, relwidth=0.15)

        # label / entry - Local Nascimento -----------------------
        self.lb_lc_nasc = Label(self.frame1, text="Local", )
        self.lb_lc_nasc.place(relx=0.33, rely=0.55)

        self.entry_birth_place = Entry(self.frame1, )
        self.entry_birth_place.place(relx=0.40, rely=0.55, relwidth=0.45)

        # label / entry - Data Morte --------------------------
        self.lb_death_date = Label(self.frame1, text="Death", )
        self.lb_death_date.place(relx=0.05, rely=0.65)

        self.entry_death_date = Entry(self.frame1, )
        self.entry_death_date.place(relx=0.15, rely=0.65, relwidth=0.15)

        # label / entry - Local Morte -----------------------
        self.lb_lc_morte = Label(self.frame1, text="Local", )
        self.lb_lc_morte.place(relx=0.33, rely=0.65)

        self.entry_death_place = Entry(self.frame1, )
        self.entry_death_place.place(relx=0.40, rely=0.65, relwidth=0.45)


    def grid_actor(self):
        self.list_grid = ttk.Treeview(self.frame2, height=3,
           column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'),show='headings')

        self.list_grid.heading("#1", text='id')
        self.list_grid.heading("#2", text='Artistic Name', anchor=W)
        self.list_grid.heading("#3", text='Name', anchor=W)
        self.list_grid.heading("#4", text='Birth Date')
        self.list_grid.heading("#5", text='Death date')
        self.list_grid.heading("#6", text='Birth Local', anchor=W)
        self.list_grid.heading("#7", text='Death Local', anchor=W)

        self.list_grid.column("#1", width=10, minwidth=0, anchor='center')
        self.list_grid.column("#2", width=70, minwidth=0)
        self.list_grid.column("#3", width=120, minwidth=0)
        self.list_grid.column("#4", width=30, minwidth=0, anchor='center')
        self.list_grid.column("#5", width=30, minwidth=0, anchor='center')
        self.list_grid.column("#6", width=120, minwidth=0)
        self.list_grid.column("#7", width=120, minwidth=0)
        self.list_grid.place(relx=0.005, rely=0.1, relwidth=0.95, relheight=0.86)

        self.scrol_list = Scrollbar(self.frame2, orient='vertical')
        self.list_grid.configure(yscroll=self.scrol_list.set)
        self.scrol_list.config(command=self.list_grid.yview)
        self.scrol_list.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.88)
        self.list_grid.bind("<Double-1>",self.OnDoubleClick)


Aplication()
