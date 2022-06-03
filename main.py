from tkinter import *
from tkinter import ttk
import sqlite3


root = Tk()

class Functions():

    def clear_entries(self):
        self.entry_id.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_category.delete(0, END)
        self.entry_release_date.delete(0, END)
        self.entry_country.delete(0, END)
        self.entry_director.delete(0, END)
        self.entry_synopsis.delete('1.0', END)
        self.entry_name.focus()

    def db_conect(self):
        self.connection = sqlite3.connect('movies.db')
        self.cursor = self.connection.cursor()
        # print("connecting to database");

    def db_desconect(self):
        self.connection.close()
        # print("Desconnecting to database sqlite3");

    def create_table(self):
        self.db_conect();
        #Creating a table if it doesn't exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(35) NOT NULL,
            category VARCHAR(35) NOT NULL,
            release_date DATE NOT NULL,
            country VARCHAR(35) NOT NULL,
            director VARCHAR(35) NOT NULL,
            synopsis VARCHAR(150));""");
        self.connection.commit(); print("created database");
        self.db_desconect()

    def capture_entries(self):
        self.id = self.entry_id.get()
        self.name = self.entry_name.get()
        self.category = self.entry_category.get()
        self.release_date = self.entry_release_date.get()
        self.country = self.entry_country.get()
        self.director = self.entry_director.get()
        self.synopsis = self.entry_synopsis.get(1.0,'end')

    def add_movies(self):
        # get data from fields
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""INSERT INTO movies (name,category,release_date,country,director,synopsis) 
        VALUES(?,?,?,?,?,?)""",(self.name,self.category,self.release_date,self.country,self.director,self.synopsis))
        self.connection.commit()
        self.db_desconect()
        self.select_list()
        self.clear_entries()

    def tab_actors(self):
        exec(open("actors.py").read(), {'x': 10})

    def tab_categories(self):
        exec(open("categories.py").read(), {'x': 10})

    def tab_countries(self):
        exec(open("countries.py").read(), {'x': 10})

    def tab_directors(self):
        exec(open("directors.py").read(), {'x': 10})

    def list_category(self):
        self.db_conect()
        options = []
        sql = 'SELECT * FROM categories ORDER BY name ASC;'
        self.cursor.execute(sql)
        ids = self.cursor.fetchall()
        for i in ids:
            options.append(i[1])
        self.db_desconect()
        return options

    def list_director(self):
        self.db_conect()
        options = []
        sql = 'SELECT * FROM directors ORDER BY name ASC;'
        self.cursor.execute(sql)
        ids = self.cursor.fetchall()
        for i in ids:
            options.append(i[1])
        self.db_desconect()
        return options


    def list_country(self):
        self.db_conect()
        options = []
        sql = 'SELECT * FROM countries ORDER BY name ASC;'
        self.cursor.execute(sql)
        ids = self.cursor.fetchall()
        for i in ids:
            options.append(i[1])
        self.db_desconect()
        return options

    def select_list(self):
        self.list_grid.tag_configure('oddrow', background="white")
        self.list_grid.tag_configure('evenrow', background="lightblue")
        self.list_grid.delete(*self.list_grid.get_children())
        self.db_conect()
        list = self.cursor.execute("""SELECT * FROM movies ORDER BY name ASC;""")
        count = 0
        for l in list:
            if count % 2 == 0:
                self.list_grid.insert("",END,values=l, tags=('evenrow',))
            else:
                self.list_grid.insert("", END, values=l, tags=('oddrow',))
            # increment counter
            count += 1
        self.db_desconect()

    def OnDoubleClick(self,event):
        self.clear_entries()
        self.list_grid.selection()

        for x in self.list_grid.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.list_grid.item(x, 'values')
            self.entry_id.insert(END, col1)
            self.entry_name.insert(END, col2)
            self.entry_category.insert(END, col3)
            self.entry_release_date.insert(END, col4)
            self.entry_country.insert(END, col5)
            self.entry_director.insert(END, col6)
            self.entry_synopsis.insert(END, col7)

    def delete_movies(self):
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""DELETE FROM movies WHERE id = ?""",(self.id,))
        self.connection.commit()
        self.db_desconect()
        self.clear_entries()
        self.select_list()

    def update_movies(self):
        self.capture_entries()
        self.db_conect()
        self.cursor.execute("""UPDATE movies SET name = ?, category = ?, release_date = ?, country = ? , 
        director = ? , synopsis = ? WHERE id = ?;
        """,(self.name,self.category,self.release_date,self.country,self.director,self.synopsis, self.id))
        self.connection.commit()
        self.db_desconect()
        self.clear_entries()
        self.select_list()

    def Search_movies(self):
        self.db_conect()
        self.list_grid.delete(*self.list_grid.get_children())
        self.entry_category.insert(END,'%')
        category = '%'+self.entry_category.get()
        self.cursor.execute("""SELECT * FROM movies WHERE name LIKE '%s' COLLATE NOCASE ORDER BY category ASC""" % category)
        result_search = self.cursor.fetchall()
        for movies in result_search:
            self.list_grid.insert("",END,values=movies)
        self.db_desconect()
        self.clear_entries()
        self.db_desconect()


class Aplication(Functions):

    def __init__(self):
        self.root = root
        self.screen()
        self.frames_screen()
        self.grid_movies()
        self.widgets_frame1()
        self.Menus()
        self.create_table()
        self.select_list()
        self.list_category()
        self.list_director()
        self.list_country()
        root.mainloop()

    def screen(self):
        self.root.title("Registration Movies")
        self.root.geometry("1024x768")
        self.root.resizable(True, True)
        self.root.maxsize(width=1024, height=768)
        self.root.minsize(width=512, height=384)
        self.root.iconbitmap('Palm-tree.ico')

    def frames_screen(self):
        self.frame1 = LabelFrame(self.root, bd=2, text='Movies Table Maintenance')
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame2 = LabelFrame(self.root, bd=2, text='Movies Table List')
        self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        # botão Clear
        self.bt_Clear = Button(self.frame1, text="Clear", command=self.clear_entries)
        self.bt_Clear.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        # botão Search
        self.bt_Search = Button(self.frame1, text="Search", command=self.Search_movies)
        self.bt_Search.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        # botão Add
        self.bt_Add = Button(self.frame1, text="Add", command=self.add_movies)
        self.bt_Add.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Update
        self.bt_update = Button(self.frame1, text="update", command=self.update_movies)
        self.bt_update.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Delete
        self.bt_Delete = Button(self.frame1, text="Delete", command=self.delete_movies)
        self.bt_Delete.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # label / entry - id -----------------------------
        self.lb_id = Label(self.frame1, text="id", )
        self.lb_id.place(relx=0.05, rely=0.05)

        self.entry_id = Entry(self.frame1, )
        self.entry_id.place(relx=0.05, rely=0.15, relwidth=0.08)

        # label / entry - name ----------------------------------
        self.lb_name = Label(self.frame1, text="name",)
        self.lb_name.place(relx=0.05, rely=0.35)

        self.entry_name = Entry(self.frame1, )
        self.entry_name.place(relx=0.15, rely=0.35, relwidth=0.7)

        # label / entry - category ----------------------------------
        self.lb_category = Label(self.frame1, text="category",)
        self.lb_category.place(relx=0.32, rely=0.45)

        self.entry_category = ttk.Combobox(self.frame1,values=self.list_category(), )
        self.entry_category.place(relx=0.40, rely=0.45, relwidth=0.45)

        # label / entry - Release Date --------------------------
        self.lb_release_date = Label(self.frame1, text="Release", )
        self.lb_release_date.place(relx=0.05, rely=0.55)

        self.entry_release_date = Entry(self.frame1, )
        self.entry_release_date.place(relx=0.15, rely=0.55, relwidth=0.15)

        # label / entry - director -----------------------
        self.lb_director = Label(self.frame1, text="director", )
        self.lb_director.place(relx=0.32, rely=0.55)

        self.entry_director = ttk.Combobox(self.frame1,values=self.list_director(), )
        self.entry_director.place(relx=0.40, rely=0.55, relwidth=0.45)

        # label / entry - country --------------------------
        self.lb_country = Label(self.frame1, text="country", )
        self.lb_country.place(relx=0.32, rely=0.65)

        self.entry_country = ttk.Combobox(self.frame1,values=self.list_country(), )
        self.entry_country.place(relx=0.40, rely=0.65, relwidth=0.45)

        # label / entry - synopsis -----------------------
        self.lb_synopsis = Label(self.frame1, text="synopsis", )
        self.lb_synopsis.place(relx=0.05, rely=0.75)

        self.entry_synopsis = Text(self.frame1, )
        self.entry_synopsis.place(relx=0.15, rely=0.75, relwidth=0.70, relheight=0.20)


    def grid_movies(self):
        self.list_grid = ttk.Treeview(self.frame2, height=3,
           column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'),show='headings')
        # self.list_grid.heading("#0", text='')
        self.list_grid.heading("#1", text='id')
        self.list_grid.heading("#2", text='name')
        self.list_grid.heading("#3", text='category')
        self.list_grid.heading("#4", text='Dt Lcto')
        self.list_grid.heading("#5", text='country')
        self.list_grid.heading("#6", text='director')
        self.list_grid.heading("#7", text='synopsis')

        # self.list_grid.column("#0", width=1, minwidth=0)
        self.list_grid.column("#1", width=10, minwidth=0, anchor='center')
        self.list_grid.column("#2", width=70, minwidth=0)
        self.list_grid.column("#3", width=120, minwidth=0)
        self.list_grid.column("#4", width=30, minwidth=0, anchor='center')
        self.list_grid.column("#5", width=100, minwidth=0)
        self.list_grid.column("#6", width=70, minwidth=0)
        self.list_grid.column("#7", width=200, minwidth=0)
        self.list_grid.place(relx=0.005, rely=0.1, relwidth=0.95, relheight=0.86)

        self.scrol_list = Scrollbar(self.frame2, orient='vertical')
        self.list_grid.configure(yscroll=self.scrol_list.set)
        self.scrol_list.config(command=self.list_grid.yview)
        self.scrol_list.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.88)
        self.list_grid.bind("<Double-1>",self.OnDoubleClick)


    def Menus(self):
        Menubar = Menu(self.root)
        self.root.config(menu=Menubar)
        filemenu = Menu(Menubar,tearoff=0)
        filemenu2 = Menu(Menubar,tearoff=0)

        def Quit(): self.root.destroy()

        Menubar.add_cascade(label="Options",menu=filemenu)
        Menubar.add_cascade(label="Functions", menu=filemenu2)

        filemenu.add_command(label="actors",command=self.tab_actors)
        filemenu.add_command(label="categories", command=self.tab_categories)
        filemenu.add_command(label="countries", command=self.tab_countries)
        filemenu.add_command(label="directors", command=self.tab_directors)
        filemenu.add_separator()
        filemenu.add_command(label="Sair", command=Quit)
        filemenu2.add_command(label="Clear campos", command=self.clear_entries)


Aplication()
