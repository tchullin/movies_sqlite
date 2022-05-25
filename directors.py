from tkinter import *
from tkinter import ttk
import sqlite3


root = Tk()

class Functions():

    def Clear_data(self):
        self.entry_id.delete(0, END)
        self.entry_name.delete(0, END)

    def db_conect(self):
        self.connection = sqlite3.connect('movies.db')
        self.cursor = self.connection.cursor()
        print("connecting to database");

    def db_desconect(self):
        self.connection.close()
        print("Desconnecting from database sqlite3");

    def create_table(self):
        self.db_conect();
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS directors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL)""");
        self.connection.commit(); print("created database");
        self.db_desconect()

    def capture_entries(self):
        self.id = self.entry_id.get()
        self.name = self.entry_name.get()

    def add_directors(self):
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""INSERT INTO directors (name) VALUES(?)""",(self.name,))
        self.connection.commit()
        self.db_desconect()
        self.select_list()
        self.Clear_data()

    def select_list(self):
        self.list_grid.tag_configure('oddrow', background="white")
        self.list_grid.tag_configure('evenrow', background="lightblue")
        self.list_grid.delete(*self.list_grid.get_children())
        self.db_conect()
        list = self.cursor.execute("""SELECT id , name FROM directors ORDER BY name ASC;""")
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
            col1, col2 = self.list_grid.item(x, 'values')
            self.entry_id.insert(END, col1)
            self.entry_name.insert(END, col2)

    def delete_directors(self):
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""DELETE FROM directors WHERE id = ?""",(self.id,))
        self.connection.commit()
        self.db_desconect()
        self.Clear_data()
        self.select_list()

    def update_directors(self):
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""UPDATE directors SET name = ? WHERE id = ?;""",(self.name, self.id))
        self.connection.commit()
        self.db_desconect()
        self.Clear_data()
        self.select_list()

    def Search_directors(self):
        self.db_conect()
        self.list_grid.delete(*self.list_grid.get_children())
        self.entry_name.insert(END,'%')
        name = '%'+self.entry_name.get()
        self.cursor.execute("""SELECT * FROM directors WHERE name LIKE '%s' COLLATE NOCASE ORDER BY name ASC""" % name)
        result_search = self.cursor.fetchall()
        for directors in result_search:
            self.list_grid.insert("",END,values=directors)
        self.db_desconect()
        self.Clear_data()
        self.db_desconect()


class Aplication(Functions):

    def __init__(self):
        self.root = root
        self.screen()
        self.frames_screen()
        self.grid_directors()
        self.widgets_frame1()
        self.create_table()
        self.select_list()
        root.mainloop()

    def screen(self):
        self.root.title("directors")
        self.root.geometry("1024x768")
        self.root.resizable(True, True)
        self.root.maxsize(width=1024, height=768)
        self.root.minsize(width=512, height=384)
        self.root.iconbitmap('Palm-tree.ico')

    def frames_screen(self):
        self.frame1 = LabelFrame(self.root, bd=2, text="Directors Table Maintenance")
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        self.frame2 = LabelFrame(self.root, bd=2, text="Directors Table List")
        self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):

        # botão Clear
        self.bt_Clear = Button(self.frame1, text="Clear",  command=self.Clear_data)
        self.bt_Clear.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        # botão Search
        self.bt_Search = Button(self.frame1, text="Search", command=self.Search_directors)
        self.bt_Search.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        # botão Add
        self.bt_Add = Button(self.frame1, text="Add", command=self.add_directors)
        self.bt_Add.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Update
        self.bt_update = Button(self.frame1, text="update", command=self.update_directors)
        self.bt_update.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Delete
        self.bt_Delete = Button(self.frame1, text="Delete", command=self.delete_directors)
        self.bt_Delete.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # label / entry - id -----------------------------
        self.lb_id = Label(self.frame1, text="id", )
        self.lb_id.place(relx=0.05, rely=0.05)

        self.entry_id = Entry(self.frame1, )
        self.entry_id.place(relx=0.05, rely=0.15, relwidth=0.08)

        # label / entry - name ----------------------------------
        self.lb_name = Label(self.frame1, text="Name", )
        self.lb_name.place(relx=0.05, rely=0.35)

        self.entry_name = Entry(self.frame1, )
        self.entry_name.place(relx=0.05, rely=0.45, relwidth=0.7)

    def grid_directors(self):
        self.list_grid = ttk.Treeview(self.frame2, height=3, column=('col1', 'col2'),show='headings')
        self.list_grid.heading("#1", text='Id')
        self.list_grid.heading("#2", text='Name', anchor=W)

        self.list_grid.column("#1", width=25, anchor='center')
        self.list_grid.column("#2", width=200)
        self.list_grid.place(relx=0.005, rely=0.1, relwidth=0.95, relheight=0.86)

        self.scrol_list = Scrollbar(self.frame2, orient='vertical')
        self.list_grid.configure(yscroll=self.scrol_list.set)
        self.scrol_list.config(command=self.list_grid.yview)
        self.scrol_list.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.88)
        self.list_grid.bind("<Double-1>",self.OnDoubleClick)


Aplication()
