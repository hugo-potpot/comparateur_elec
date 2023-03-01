import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("produits.db",check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS SITE (id INTEGER PRIMARY KEY, nom_site text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS PRODUIT ("
                         "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                         "id_site REFERENCES SITE(id),"
                         "reference text, "
                         "nom_produit text, "
                         "prix DECIMAL(10,2),"
                         "url text)")
        self.conn.commit()

    def insert_data(self, info_produit):
        self.cur.execute("INSERT INTO PRODUIT(id_site, reference, nom_produit, prix, url) VALUES (?,?,?,?,?)", (info_produit))
        self.conn.commit()
        print("Data inserted successfully")

    def insert_site(self, site):
        self.cur.execute("INSERT INTO SITE(nom_site) VALUES (?)", (site,))
        self.conn.commit()
        print("Site inserted successfully")

    def search(self, reference):
        self.cur.execute("SELECT * FROM PRODUIT WHERE reference=?", (reference,))
        rows = self.cur.fetchall()
        return rows

    def search_item(self, id_site, reference):
        self.cur.execute("SELECT * FROM PRODUIT WHERE reference=? AND id_site=?", (reference,id_site))
        rows = self.cur.fetchall()
        if len(rows) == 0:
            return False
        return True

    def search_site(self, site):
        self.cur.execute("SELECT * FROM SITE WHERE nom_site=?", (site,))
        rows = self.cur.fetchall()
        if len(rows) == 0:
            return False
        return True

    def update(self, info_produit):
        info_produit = list(info_produit)
        self.cur.execute("UPDATE PRODUIT SET nom_produit=?, prix=?, url=? WHERE reference=? AND id_site=?",
                         (info_produit[2], info_produit[3], info_produit[4], info_produit[1], info_produit[0]))
        self.conn.commit()

    def best_price(self,ref):
        self.cur.execute("SELECT SITE.nom_site, PRODUIT.nom_produit, PRODUIT.reference, MIN(PRODUIT.prix), PRODUIT.url FROM PRODUIT JOIN SITE ON PRODUIT.id_site = SITE.id WHERE reference=?", (ref,))
        rows = self.cur.fetchall()
        if rows is not None:
            return rows[0]
        return None

    def get_info_produit(self, reference):
        self.cur.execute("SELECT SITE.nom_site, PRODUIT.nom_produit, PRODUIT.prix, PRODUIT.url FROM PRODUIT JOIN SITE ON PRODUIT.id_site = SITE.id WHERE reference=? ", (reference,))
        rows = self.cur.fetchall()
        return rows

    def get_info_by_search(self, search):
        search_terms = search.split()
        search_conditions = []
        for term in search_terms:
            search_conditions.append("(nom_produit LIKE '%{}%' OR reference LIKE '%{}%')".format(term, term))
        search_query = " AND ".join(search_conditions)
        sql_query = """
            SELECT SITE.nom_site, PRODUIT.nom_produit, PRODUIT.reference, PRODUIT.prix, PRODUIT.url
            FROM PRODUIT JOIN SITE ON PRODUIT.id_site = SITE.id
            WHERE {}
            ORDER BY SITE.nom_site, PRODUIT.nom_produit;
        """.format(search_query, search[0])
        self.cur.execute(sql_query)
        rows = self.cur.fetchall()
        if len(rows) == 0:
            return "Aucun résultat"
        print(len(list(rows)))
        return rows

    def __del__(self):
        self.conn.close()

