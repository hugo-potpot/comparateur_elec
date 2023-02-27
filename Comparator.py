import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from database import Database


class Comparator:
    data = Database()

    def __init__(self, ref):
        self.ref = ref.upper()
        self.tmp = []

    def getData(self):
        return self.tmp

    def getBestPrice(self,ref):
        return self.data.best_price(ref)

    def get_search_senechalelec(self):
        info_tmp = {"site":"Senechalelec","ref": self.ref, "item": "Not Found", "price": "Not Found", "link": "Not Found"}
        info_senechalelec = (1, self.ref, "Not Found", "Not Found", "Not Found")
        try:
            url = "https://www.senechalelec.com/fr/recherche?controller=search&search_query={0}".format(self.ref)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            info_senechalelec = info_senechalelec[:2] + (soup.find("a", {"class": "product-name"}).text.strip(),) + info_senechalelec[3:]
            info_senechalelec = info_senechalelec[:3] + (soup.find("span", {"class": "price product-price"}).text.strip().split()[0].replace(",", "."),) + info_senechalelec[4:]
            info_senechalelec = info_senechalelec[:4] + (url,) + info_senechalelec[5:]
            info_tmp["item"] = soup.find("a", {"class": "product-name"}).text.strip()
            info_tmp["price"] = soup.find("span", {"class": "price product-price"}).text.strip().split()[
                0].replace(",", ".")
            info_tmp["link"] = url
        except:
            pass
        finally:
            if info_tmp['item'] != "Not Found":
                self.check_data(1, "Senechalelec", info_senechalelec)
        self.tmp.append(info_tmp)

    def get_search_123elec(self):
        #id_site = 2
        info_tmp = {"site":"123Elec","ref": self.ref, "item": "Not Found", "price": "Not Found", "link": "Not Found"}
        info_123elec = (2, self.ref, "Not Found", "Not Found", "Not Found")
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Chrome(options=chrome_options)
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
                info_123elec = info_123elec[:2] + (soup.find("h1", {"class": "title-1"}).text.strip(),) + info_123elec[3:]
                info_123elec = info_123elec[:3] + (soup.find("strong", {"class": "price"}).text.split()[0].replace(",", "."),) + info_123elec[4:]
                info_123elec = info_123elec[:4] + (link,) + info_123elec[5:]
                info_tmp["item"] = soup.find("h1", {"class": "title-1"}).text.strip()
                info_tmp["price"] = soup.find("strong", {"class": "price"}).text.split()[0].replace(",", ".")
                info_tmp["link"] = link
        except Exception as exception:
            print(exception)
        finally:
            if info_tmp['item'] != "Not Found":
                self.check_data(2, "123ELec", info_123elec)
        self.tmp.append(info_tmp)

    def get_search_eplanet(self):
        #id_site = 3
        info_tmp = {"site":"E-PlanetElec","ref": self.ref, "item": "Not Found", "price": "Not Found", "link": "Not Found"}
        info_eplanet = (3, self.ref, "Not Found", "Not Found", "Not Found")
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
                info_eplanet = info_eplanet[:2] + (soup.find("h1", {"class": "h1"}).text.strip(),) + info_eplanet[3:]
                info_eplanet = info_eplanet[:3] + (soup.find("span", {"class": "price_ttc"}).text.strip().split()[0].replace(",", "."),) + info_eplanet[4:]
                info_eplanet = info_eplanet[:4] + (url,) + info_eplanet[5:]
                info_tmp["item"] = soup.find("h1", {"class": "h1"}).text.strip()
                info_tmp["price"] = soup.find("span", {"class": "price_ttc"}).text.strip().split()[0].replace(",", ".")
                info_tmp["link"] = url
        except:
            pass
        finally:
            if info_tmp['item'] != "Not Found":
                self.check_data(3, "E-Planetelec", info_eplanet)
        self.tmp.append(info_tmp)

    def get_search_elec44(self):
        #id_site = 4
        info_tmp = {"site":"Elec44","ref": self.ref, "item": "Not Found", "price": "Not Found", "link": "Not Found"}
        info_elec44 = (4, self.ref, "Not Found", "Not Found", "Not Found")
        try:
            url = "https://elec44.fr/recherche?controller=search&s={0}".format(self.ref)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            reference = soup.find("h2", {"class": "h3 product-title"}).text.strip().split()[-1]
            if reference == self.ref.upper():
                info_elec44 = info_elec44[:2] + (soup.find("h2", {"class": "h3 product-title"}).text.strip(),) + info_elec44[3:]
                info_elec44 = info_elec44[:3] + (soup.find("span", {"class": "price"}).text.strip().split()[0].replace(",", "."),) + info_elec44[4:]
                info_elec44 = info_elec44[:4] + (url,) + info_elec44[5:]
                info_tmp["item"] = soup.find("h2", {"class": "h3 product-title"}).text.strip()
                info_tmp["price"] = soup.find("span", {"class": "price"}).text.strip().split()[0].replace(",", ".")
                info_tmp["link"] = url
        except:
            pass
        finally:
            if info_tmp['item'] != "Not Found":
                self.check_data(4, "Elec44", info_elec44)
        self.tmp.append(info_tmp)

    def check_data(self, id_site,nom_site, info):
        exist_item = self.data.search_item(id_site, self.ref)
        exist_site = self.data.search_site(nom_site)
        if exist_site == False:
            self.data.insert_site(nom_site)
        if exist_item:
            self.data.update(info)
        else:
            self.data.insert_data(info)

    def all_comparator(self, comparator, eleccheck):
        # TOTAL = 4
        if not eleccheck:
            comparator.get_search_senechalelec()
            comparator.get_search_eplanet()
            comparator.get_search_elec44()
        else:
            comparator.get_search_senechalelec()
            comparator.get_search_123elec()
            comparator.get_search_eplanet()
            comparator.get_search_elec44()

    def get_info_page(self):
        url = "https://www.123elec.com/recherche#/embedded/query=s530214"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        with open("test.html", "w") as file:
            file.write(str(soup))

#
# for i in range(total):
#     time.sleep(0.1)  # Simulation d'une opération qui prend du temps
#     progress_bar(i + 1, total, prefix='Progression:', suffix='Terminé', length=50)
# METTRE LA REFERENCE FABRIQUANT
# main("S530214"