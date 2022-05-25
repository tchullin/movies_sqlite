from tkinter import *
from tkinter import ttk
import sqlite3


root = Tk()

class Functions():

    def clear_entries(self):
        self.entry_id.delete(0, END)
        self.entry_name.delete(0, END)

    def db_conect(self):
        self.connection = sqlite3.connect('movies.db')
        self.cursor = self.connection.cursor()
        print("connecting to database");

    def db_disconect(self):
        self.connection.close()
        print("Desconnecting from database sqlite3");

    def create_table(self):
        self.db_conect();
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL)""");
        self.connection.commit()
        self.db_disconect()

    def capture_entries(self):
        self.id = self.entry_id.get()
        self.name = self.entry_name.get()

    def add_countries(self):
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""INSERT INTO countries (name) VALUES(?)""",(self.name,))
        self.connection.commit()
        self.db_disconect()
        self.list_selection()
        self.clear_entries()

    def list_selection(self):
        self.list_grid.tag_configure('oddrow', background="white")
        self.list_grid.tag_configure('evenrow', background="lightblue")
        self.list_grid.delete(*self.list_grid.get_children())
        self.db_conect()
        lista = self.cursor.execute("""SELECT id , name FROM countries ORDER BY name ASC;""")
        count = 0
        for l in lista:
            if count % 2 == 0:
                self.list_grid.insert("",END,values=l, tags=('evenrow',))
            else:
                self.list_grid.insert("", END, values=l, tags=('oddrow',))
            # increment counter
            count += 1
        self.db_disconect()

    def OnDoubleClick(self,event):
        self.clear_entries()
        self.list_grid.selection()
        for x in self.list_grid.selection():
            col1, col2 = self.list_grid.item(x, 'values')
            self.entry_id.insert(END, col1)
            self.entry_name.insert(END, col2)

    def delete_countries(self):
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""DELETE FROM countries WHERE id = ?""",(self.id,))
        self.connection.commit()
        self.db_disconect()
        self.clear_entries()
        self.list_selection()

    def update_countries(self):
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""UPDATE countries SET name = ? WHERE id = ?;""",(self.name, self.id))
        self.connection.commit()
        self.db_disconect()
        self.clear_entries()
        self.list_selection()

    def search_countries(self):
        self.db_conect()
        self.list_grid.delete(*self.list_grid.get_children())
        self.entry_name.insert(END,'%')
        name = '%'+self.entry_name.get()
        self.cursor.execute("""SELECT * FROM countries WHERE name LIKE '%s' COLLATE NOCASE ORDER BY name ASC""" % name)
        Resultado_busca = self.cursor.fetchall()

        for countries in Resultado_busca:
            self.list_grid.insert("",END,values=countries)
        self.db_disconect()
        self.clear_entries()
        self.db_disconect()


class Aplication(Functions):
    def __init__(self):
        self.root = root
        self.tela()
        self.screen_frames()
        self.grid_countries()
        self.widgets_frame1()
        self.create_table()
        self.list_selection()
        root.mainloop()

    def tela(self):
        self.root.title("Country Registration")
        self.root.geometry("1024x768")
        self.root.resizable(True, True)
        self.root.maxsize(width=1024, height=768)
        self.root.minsize(width=512, height=384)
        self.root.iconbitmap('Palm-tree.ico')

    def screen_frames(self):
        self.frame1 = LabelFrame(self.root, bd=2, text='Manutenção countries')
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        self.frame2 = LabelFrame(self.root, bd=2, text='Listagem countries')
        self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        # botão clear
        self.bt_clear = Button(self.frame1, text="Clear",  command=self.clear_entries)
        self.bt_clear.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        # botão search
        self.bt_search = Button(self.frame1, text="Search", command=self.search_countries)
        self.bt_search.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        # botão add
        self.bt_add = Button(self.frame1, text="Add", command=self.add_countries)
        self.bt_add.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão update
        self.bt_update = Button(self.frame1, text="Update", command=self.update_countries)
        self.bt_update.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão delete
        self.bt_delete = Button(self.frame1, text="Delete", command=self.delete_countries)
        self.bt_delete.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # label / entry - id -----------------------------
        self.lb_id = Label(self.frame1, text="Id", )
        self.lb_id.place(relx=0.05, rely=0.05)

        self.entry_id = Entry(self.frame1, )
        self.entry_id.place(relx=0.05, rely=0.15, relwidth=0.08)

        # label / entry - name ----------------------------------
        self.lb_name = Label(self.frame1, text="Name", )
        self.lb_name.place(relx=0.05, rely=0.35)

        self.entry_name = Entry(self.frame1, )
        self.entry_name.place(relx=0.05, rely=0.45, relwidth=0.7)

    def grid_countries(self):
        self.list_grid = ttk.Treeview(self.frame2, height=3, column=('col1', 'col2'),show='headings')

        self.list_grid.heading("#1", text='Id')
        self.list_grid.heading("#2", text='Name', anchor=W)

        self.list_grid.column("#1", width=25, anchor='center')
        self.list_grid.column("#2", width=200)
        self.list_grid.place(relx=0.005, rely=0.1, relwidth=0.95, relheight=0.86)

        self.scrol_lista = Scrollbar(self.frame2, orient='vertical')
        self.list_grid.configure(yscroll=self.scrol_lista.set)
        self.scrol_lista.config(command=self.list_grid.yview)
        self.scrol_lista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.88)
        self.list_grid.bind("<Double-1>",self.OnDoubleClick)


Aplication()
