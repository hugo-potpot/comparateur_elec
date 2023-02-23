import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("produits.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS SITE (id INTEGER PRIMARY KEY, nom_site text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS PRODUIT ("
                         "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                         "id_site REFERENCES SITE(id),"
                         "reference text, "
                         "nom_produit text, "
                         "prix DECIMAL(10.2),"
                         "url text)")
        self.conn.commit()
        print("Database created successfully")

    def insert(self, reference, site, id_site, nom_produit, prix, lien):
        self.cur.execute("INSERT INTO SITE(nom_site) VALUES (?)", (site,))
        self.cur.execute("INSERT INTO PRODUIT(id_site, reference, nom_produit, prix, url) VALUES (?,?,?,?,?)", (id_site, reference, nom_produit, prix, lien))
        self.conn.commit()
        print("Data inserted successfully")

    def view(self):
        self.cur.execute("SELECT * FROM PRODUIT")
        rows = self.cur.fetchall()
        return rows

    def search(self, title="", author="", year="", isbn=""):
        self.cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?",
                         (title, author, year, isbn))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM book WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, title, author, year, isbn):
        self.cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",
                         (title, author, year, isbn, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


database = Database()
database.insert("123", "123", 1, "123", 123.00, "123")
print(database.view())
