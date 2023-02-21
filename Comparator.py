import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Comparator:
    def __init__(self, ref):
        self.ref = ref
        self.data = []

    def add(self, info):
        self.data.append(info)

    def getData(self):
        return self.data

    def getBestPrice(self):
        best_price = self.data[0]["price"]
        for i in range(1, len(self.data)):
            if self.data[i]["price"] != "Not Found":
                if self.data[i]["price"] < best_price or best_price == 0:
                    best_price = self.data[i]["price"]
        return best_price

    def writeCSV(self):
        with open("result.csv", "w") as f:
            f.write("Référence,Item,Prix,Lien,Meilleur Prix\n")
            for i in range(len(self.data)):
                f.write("{0},{1},{2},{3},{4}\n".format(self.data[i]["ref"], self.data[i]["item"], self.data[i]["price"],
                                                       self.data[i]["link"], self.getBestPrice()))

    def get_search_senechalelec(self):
        info_senechalelec = {"site":"Senechalelec","ref": self.ref, "item": "Not Found", "price": "Not Found", "link": "Not Found"}
        try:
            url = "https://www.senechalelec.com/fr/recherche?controller=search&search_query={0}".format(self.ref)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            info_senechalelec["item"] = soup.find("a", {"class": "product-name"}).text.strip()
            info_senechalelec["price"] = soup.find("span", {"class": "price product-price"}).text.strip().split()[
                0].replace(",", ".")
            info_senechalelec["link"] = url
        except:
            pass
        self.add(info_senechalelec)

    def get_search_123elec(self):
        info_123elec = {"site":"123elec","ref": self.ref, "item": "Not Found", "price": "Not Found", "link": "Not Found"}
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Chrome('driver/chromedriver', options=chrome_options)
            driver.get("https://www.123elec.com/recherche#/embedded/query={0}".format(self.ref))

            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "df-card__main"))))
            link = driver.current_url
            driver.quit()
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            ul = soup.find("ul", {"class": "product__refs"})
            li = ul.find_all("li")[1]
            reference = li.find("span").text.strip()
            if reference == self.ref.upper():
                info_123elec["item"] = soup.find("h1", {"class": "title-1"}).text.strip()
                info_123elec["price"] = soup.find("strong", {"class": "price"}).text.split()[0].replace(",", ".")
                info_123elec["link"] = link
        except:
            pass
        self.add(info_123elec)

    def get_search_leroymerlin(self):
        # Pour l'instant impossible il faut l'api sauf qu'il faut etre une entreprise
        # https://developer.leroymerlin.fr/dashboard/
        pass

    def get_search_eplanet(self):
        info_eplanet = {"site":"E-Planet","ref": self.ref, "item": "Not Found", "price": "Not Found", "link": "Not Found"}
        try:
            url = "https://www.e-planetelec.fr/jolisearch?s={0}".format(self.ref)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            link_projet = soup.find("div", {"class": "thumbnail-container"})
            link = link_projet.find("a").get("href")
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            reference = soup.find("p", {"class": "product_reference"}).text.strip().split()[-1]
            if reference == self.ref.upper():
                info_eplanet["item"] = soup.find("h1", {"class": "h1"}).text.strip()
                info_eplanet["price"] = soup.find("span", {"class": "price_ttc"}).text.strip().split()[0]
                info_eplanet["link"] = url
        except:
            pass
        self.add(info_eplanet)

    def get_search_elec44(self):
        info_elec44 = {"site":"Elec44","ref": self.ref, "item": "Not Found", "price": "Not Found", "link": "Not Found"}
        try:
            url = "https://elec44.fr/recherche?controller=search&s={0}".format(self.ref)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            reference = soup.find("h2", {"class": "h3 product-title"}).text.strip().split()[-1]
            if reference == self.ref.upper():
                info_elec44["item"] = soup.find("h2", {"class": "h3 product-title"}).text.strip()
                info_elec44["price"] = soup.find("span", {"class": "price"}).text.strip().split()[0]
                info_elec44["link"] = url
        except:
            pass
        self.add(info_elec44)

    def all_comparator(self, comparator):
        # TOTAL = 2
        comparator.get_search_senechalelec()
        comparator.get_search_123elec()
        comparator.get_search_eplanet()
        comparator.get_search_elec44()

#
# for i in range(total):
#     time.sleep(0.1)  # Simulation d'une opération qui prend du temps
#     progress_bar(i + 1, total, prefix='Progression:', suffix='Terminé', length=50)
# METTRE LA REFERENCE FABRIQUANT
# main("S530214")
