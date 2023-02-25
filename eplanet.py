import requests
from bs4 import BeautifulSoup
from database import Database
import sqlite3
import pandas as pd
database = Database()

def get_link_cat():
    link = []
    response = requests.get("https://www.e-planetelec.fr/")
    soup = BeautifulSoup(response.text, "html.parser")
    link_cat = soup.find("ul", {"id": "menu"}).find_all("a")
    for i in link_cat:
        link.append(i.get("href"))
    link = link[1:]
    return link

def get_link_product():
    link = get_link_cat()
    link_product = []
    for l in link:
        response = requests.get(l)
        soup = BeautifulSoup(response.text, "html.parser")
        if verify_page(soup) is not None:
            for i in range(1, int(verify_page(soup))):
                response = requests.get(l + "?page=" + str(i))
                soup = BeautifulSoup(response.text, "html.parser")
                produits = soup.find_all("div", {"class": "thumbnail-container"})
                for j in produits:
                    link_product.append(j.find("a").get("href"))
    print(len(link_product))
    return link_product

def get_info_product():
    link = ['https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2370-product.html', 'https://www.e-planetelec.fr'
    '/programme-plexo-composable-ip55/617-interrupteur-ou-va-et-vient-lumineux-etanche-plexo-composable-ip55-10ax'
    '-250v-gris.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2086-odace-touch-plaque-anthracite-2-postes'
    '-horiz-ou-vert-entraxe-71mm-s540804.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2371-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1090-voyant-led-lumineux-24v-dooxie-a-raccordement-par-montage-direct-2'
    '-fils-600143.html', 'https://www.e-planetelec.fr/prise-dooxie/1091-pret-a-poser-dooxie-creer-un-va-et-vient-avec'
    '-2-commandes-sans-fil-et-1-micromodule-livre-complet-blanc-600699.html',
    'https://www.e-planetelec.fr/programme-plexo-composable-ip55/621-pousssoir-no-gris-composable.html',
    'https://www.e-planetelec.fr/plaque-odace-touch/2087-plaque-aluminium-brosse-lisere-anthracite-odace-touch-2-post'
    '-horizvert-71mm-s540804j.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2372-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1093-pret-a-poser-dooxie-creer-une-prise-commandee-avec-1-prise-de'
    '-courant-et-1-commande-sans-fil-livre-complet-blanc-600694.html',
    'https://www.e-planetelec.fr/plaque-odace-touch/2088-odace-touch-plaque-miroir-brillant-fume-avec-lisere-anth'
    '-2postes-entraxe-71mm-s540804k1.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2373-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1094-pret-a-poser-dooxie-commander-un-volet-roulant-avec-1-commande'
    '-sans-fil-et-1-interrupteur-livre-complet-blanc-600696.html',
    'https://www.e-planetelec.fr/plaque-odace-touch/2089-odace-touch-plaque-bronze-brosse-lisere-anthracite-2-postes'
    '-horiz-vert-71mm-s540804l.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2374-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1645-transformeur-pour-realiser-5-fonctions-lumineuses-dooxie-one'
    '-600730.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2090-plaque-bois-frene-lisere-anthracite-odace'
    '-touch-2-postes-horizvert-71mm-s540804p3.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2375-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1686-prise-de-courant-2p-t-surface-dooxie-16a-finition-noir-emballage'
    '-blister-095275.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2091-plaque-bois-zebra-avec-lisere-anth-2'
    '-postes-horizvert-entraxe-71mm-s540804p4.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2376-product.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2379-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1673-interrupteur-ou-va-et-vient-dooxie-10ax-250v-finition-noir'
    '-emballage-blister-095260.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2092-plaque-pierre-galet-avec'
    '-lisere-anthracite-odace-touch-2-postes-horizvert-entraxe-71mm-s540804u.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2380-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1672-poussoir-simple-dooxie-6a-250v-finition-noir-emballage-blister'
    '-095264.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2093-plaque-ardoise-avec-lisere-anthracite-odace'
    '-touch-2-postes-horizvert-entraxe-71mm-s540804v.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2396-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1658-prise-telephone-en-t-dooxie-finition-noir-emballage-blister-095286'
    '.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2094-plaque-anthracite-odace-touch-3-postes-horiz-ou'
    '-vert-entraxe-71mm-s540806.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2095-plaque-aluminium-brosse'
    '-lisere-anthracite-odace-touch-3-postes-horizvert-71mm-s540806j.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2397-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1659-commande-de-volets-roulants-dooxie-finition-noir-emballage-blister'
    '-095272.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2096-plaque-miroir-brillant-fume-avec-lisere'
    '-anthracite-odace-touch-3-postes-entraxe-71mm-s540806k1.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2398-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1660-interrupteur-commande-vmc-dooxie-finition-noir-emballage-blister'
    '-095273.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2097-plaque-bronze-brosse-lisere-anthracite-odace'
    '-touch-3-postes-horizvert-71mm-s540806l.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2399-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1661-prise-tv-type-f-a-visser-dooxie-finition-noir-emballage-blister'
    '-095283.html', 'https://www.e-planetelec.fr/prise-dooxie/1663-prise-blindee-rj45-cat6-stp-dooxie-finition-noir'
    '-emballage-blister-095285.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2098-plaque-bois-zebra-avec'
    '-lisere-anthracite-odace-touch-3-postes-horizvert-entraxe-71mm-s540806p4.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2400-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1664-prise-haut-parleur-double-dooxie-finition-noir-emballage-blister'
    '-095289.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2099-plaque-pierre-galet-avec-lisere-anthracite'
    '-odace-touch-3-postes-horizvert-entraxe-71mm-s540806u.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2401-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1666-interrupteur-automatique-dooxie-2-fils-sans-neutre-finition-noir'
    '-emballage-blister-095271.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2100-odace-touch-plaque-ardoise'
    '-avec-lisere-anth-3-postes-horiz-vert-entraxe-71mm-s540806v.html',
    'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2402-product.html',
    'https://www.e-planetelec.fr/prise-dooxie/1667-poussoir-double-dooxie-6a-250v-finition-noir-emballage-blister'
    '-095265.html', 'https://www.e-planetelec.fr/plaque-dooxie/1095-plaque-carree-dooxie-1-poste-finition-blanc'
    '-600801.html', 'https://www.e-planetelec.fr/cadres-et-accessoires-asl/2197-product.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2200-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2187-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1096-lot-de-100-plaques-carrees-dooxie-1-poste-finition-blanc-600941'
    '.html', 'https://www.e-planetelec.fr/prise-dooxie/986-interrupteur-ou-va-et-vient-dooxie-blanc-600001.html',
    'https://www.e-planetelec.fr/cadres-et-accessoires-asl/2198-product.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2201-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2188-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1097-plaque-carree-dooxie-2-postes-finition-blanc-600802.html',
    'https://www.e-planetelec.fr/prise-dooxie/987-lot-de-50-interrupteurs-ou-va-et-vient-dooxie-blanc-600601.html',
    'https://www.e-planetelec.fr/cadres-et-accessoires-asl/2199-product.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2202-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2189-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1098-plaque-carree-dooxie-3-postes-finition-blanc-600803.html',
    'https://www.e-planetelec.fr/prise-dooxie/988-double-interrupteur-ou-va-et-vient-dooxie-blanc-600002.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2203-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2190-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1099-plaque-carree-dooxie-4-postes-finition-blanc-600804.html',
    'https://www.e-planetelec.fr/prise-dooxie/989-poussoir-simple-dooxie-blanc-600004.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2204-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2191-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1100-plaque-carree-dooxie-1-poste-finition-dune-600811.html',
    'https://www.e-planetelec.fr/prise-dooxie/990-poussoir-double-dooxie-blanc-600008.html',
    'https://www.e-planetelec.fr/prise-dooxie/991-poussoir-simple-avec-voyant-lumineux-dooxie-blanc-600016.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2205-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2192-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1101-plaque-carree-dooxie-2-postes-finition-dune-600812.html',
    'https://www.e-planetelec.fr/prise-dooxie/992-transformeur-pour-realiser-5-fonctions-dooxie-blanc-600031.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2206-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2193-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1102-plaque-carree-dooxie-3-postes-finition-dune-600813.html',
    'https://www.e-planetelec.fr/prise-dooxie/993-prise-de-courant-2p-t-surface-dooxie-16a-blanc-600335.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2207-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2194-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1103-plaque-carree-dooxie-4-postes-finition-dune-600814.html',
    'https://www.e-planetelec.fr/prise-dooxie/994-double-prise-de-courant-2p-t-surface-dooxie-16a-precablees-blanc'
    '-600332.html', 'https://www.e-planetelec.fr/appareillage-composable-asl/2208-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2195-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1104-plaque-carree-dooxie-1-poste-finition-plume-600821.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1105-plaque-carree-dooxie-2-postes-finition-plume-600822.html',
    'https://www.e-planetelec.fr/prise-dooxie/995-sortie-de-cable-ip21-dooxie-livree-complete-blanc-600323.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2209-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2196-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1106-plaque-carree-dooxie-3-postes-finition-plume-600823.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2353-poussoir-6a-appareillage-saillie-complet-blanc-086006'
    '.html', 'https://www.e-planetelec.fr/prise-dooxie/996-prise-blindee-rj45-cat6-stp-dooxie-blanc-600375.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2210-product.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/2354-prise-television-simple-male-appareillage-saillie'
    '-complet-blanc-086040.html', 'https://www.e-planetelec.fr/prise-dooxie/997-prise-tv-simple-etoile-blindee-dooxie'
    '-blanc-600351.html', 'https://www.e-planetelec.fr/appareillage-composable-asl/2211-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1107-plaque-carree-dooxie-4-postes-finition-plume-600824.html',
    'https://www.e-planetelec.fr/prise-dooxie/998-transformeur-pour-realiser-5-fonctions-dooxie-alu-600131.html',
    'https://www.e-planetelec.fr/appareillage-complet-asl/3037-va-et-vient-10a-appareillage-sailli-complet-blanc'
    '-086001.html', 'https://www.e-planetelec.fr/appareillage-composable-asl/2212-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1108-plaque-carree-dooxie-1-poste-finition-blanc-avec-bague-effet'
    '-chrome-600841.html', 'https://www.e-planetelec.fr/plaque-dooxie/1109-plaque-carree-dooxie-2-postes-finition'
    '-blanc-avec-bague-effet-chrome-600842.html',
    'https://www.e-planetelec.fr/prise-dooxie/999-interrupteur-ou-va-et-vient-dooxie-alu-600101.html',
    'https://www.e-planetelec.fr/appareillage-composable-asl/2213-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1110-plaque-carree-dooxie-3-postes-finition-blanc-avec-bague-effet'
    '-chrome-600843.html', 'https://www.e-planetelec.fr/prise-dooxie/1000-double-interrupteur-ou-va-et-vient-dooxie'
    '-finition-alu-600102.html', 'https://www.e-planetelec.fr/appareillage-composable-asl/2214-product.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1111-plaque-carree-dooxie-1-poste-finition-effet-aluminium-600851.html'
    '', 'https://www.e-planetelec.fr/prise-dooxie/1001-interrupteur-ou-va-et-vient-avec-voyant-lumineux-dooxie-blanc'
    '-600011.html', 'https://www.e-planetelec.fr/plaque-dooxie/1112-plaque-carree-dooxie-2-postes-finition-effet'
    '-aluminium-600852.html', 'https://www.e-planetelec.fr/prise-dooxie/1002-interrupteur-ou-va-et-vient-avec-voyant'
    '-lumineux-dooxie-alu-600111.html', 'https://www.e-planetelec.fr/plaque-dooxie/1113-plaque-carree-dooxie-3-postes'
    '-finition-effet-aluminium-600853.html',
    'https://www.e-planetelec.fr/prise-dooxie/1003-interrupteur-ou-va-et-vient-avec-voyant-temoin-dooxie-blanc-600009'
    '.html', 'https://www.e-planetelec.fr/plaque-dooxie/1114-plaque-carree-dooxie-4-postes-finition-effet-aluminium'
    '-600854.html', 'https://www.e-planetelec.fr/prise-dooxie/1004-interrupteur-ou-va-et-vient-avec-voyant-temoin'
    '-dooxie-alu-600109.html', 'https://www.e-planetelec.fr/plaque-dooxie/1115-plaque-carree-dooxie-1-poste-finition'
    '-effet-inox-brosse-600871.html', 'https://www.e-planetelec.fr/prise-dooxie/1005-permutateur-dooxie-blanc-600037'
    '.html', 'https://www.e-planetelec.fr/plaque-dooxie/1116-plaque-carree-dooxie-2-postes-finition-effet-inox-brosse'
    '-600872.html', 'https://www.e-planetelec.fr/prise-dooxie/1006-permutateur-dooxie-alu-600137.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1117-plaque-carree-dooxie-3-postes-finition-effet-inox-brosse-600873'
    '.html', 'https://www.e-planetelec.fr/prise-dooxie/1007-poussoir-simple-dooxie-alu-600104.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1118-plaque-carree-dooxie-1-poste-finition-effet-bois-ebene-600881'
    '.html', 'https://www.e-planetelec.fr/prise-dooxie/1008-poussoir-double-dooxie-alu-600108.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1119-plaque-carree-dooxie-2-postes-finition-effet-bois-ebene-600882'
    '.html', 'https://www.e-planetelec.fr/prise-dooxie/1009-poussoir-simple-avec-voyant-lumineux-dooxie-alu-600116'
    '.html', 'https://www.e-planetelec.fr/plaque-dooxie/1120-plaque-carree-dooxie-3-postes-finition-effet-bois-ebene'
    '-600883.html', 'https://www.e-planetelec.fr/prise-dooxie/1010-poussoir-simple-avec-voyant-lumineux-et-marquage'
    '-cadenas-dooxie-blanc-600017.html', 'https://www.e-planetelec.fr/prise-dooxie/1011-poussoir-simple-avec-voyant'
    '-lumineux-et-marquage-cadenas-dooxie-alu-600117.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1121-plaque-ronde-dooxie-1-poste-finition-blanc-600980.html',
    'https://www.e-planetelec.fr/prise-dooxie/1012-poussoir-simple-avec-voyant-lumineux-et-marquage-sonnette-dooxie'
    '-blanc-600018.html', 'https://www.e-planetelec.fr/plaque-dooxie/1122-plaque-ronde-dooxie-1-poste-finition-dune'
    '-600970.html', 'https://www.e-planetelec.fr/prise-dooxie/1013-poussoir-simple-avec-voyant-lumineux-et-marquage'
    '-sonnette-dooxie-alu-600118.html', 'https://www.e-planetelec.fr/plaque-dooxie/1123-plaque-ronde-dooxie-1-poste'
    '-finition-plume-600971.html', 'https://www.e-planetelec.fr/prise-dooxie/1014-interrupteur-a-badge-dooxie-blanc'
    '-600033.html', 'https://www.e-planetelec.fr/plaque-dooxie/1124-plaque-ronde-dooxie-1-poste-finition-blanc-avec'
    '-bague-effet-chrome-600973.html', 'https://www.e-planetelec.fr/plaque-dooxie/1125-plaque-ronde-dooxie-1-poste'
    '-finition-effet-aluminium-bague-effet-chrome-600975.html',
    'https://www.e-planetelec.fr/prise-dooxie/1015-interrupteur-a-badge-dooxie-alu-600133.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1126-plaque-ronde-dooxie-1-poste-finition-effet-inox-brosse-600978'
    '.html', 'https://www.e-planetelec.fr/prise-dooxie/1016-interrupteur-automatique-pour-minuterie-en-remplacement-d'
    '-un-poussoir-dooxie-blanc-600061.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1127-obturateur-dooxie-finition-blanc-600044.html',
    'https://www.e-planetelec.fr/prise-dooxie/1017-interrupteur-automatique-pour-minuterie-en-remplacement-d-un'
    '-poussoir-dooxie-alu-600161.html', 'https://www.e-planetelec.fr/plaque-dooxie/1128-plaque-carree-dooxie-1-poste'
    '-finition-blanc-avec-porte-etiquette-600942.html',
    'https://www.e-planetelec.fr/prise-dooxie/1018-interrupteur-automatique-dooxie-2-fils-sans-neutre-finition-blanc'
    '-600064.html', 'https://www.e-planetelec.fr/plaque-dooxie/1129-plaque-carree-dooxie-1-poste-avec-volet-ip44-ik07'
    '-600944.html', 'https://www.e-planetelec.fr/prise-dooxie/1019-interrupteur-automatique-dooxie-2-fils-sans-neutre'
    '-alu-600164.html', 'https://www.e-planetelec.fr/plaque-dooxie/1130-plaque-carree-speciale-dooxie-2-postes-avec'
    '-entraxe-57mm-finition-blanc-600807.html',
    'https://www.e-planetelec.fr/prise-dooxie/1020-variateur-toutes-lampes-dooxie-2-fils-sans-neutre-blanc-600060'
    '.html', 'https://www.e-planetelec.fr/plaque-dooxie/1665-plaque-carree-dooxie-2-postes-finition-noir-velours'
    '-600862.html', 'https://www.e-planetelec.fr/prise-dooxie/1021-variateur-toutes-lampes-dooxie-2-fils-sans-neutre'
    '-alu-600160.html', 'https://www.e-planetelec.fr/plaque-dooxie/1671-plaque-carree-dooxie-3-postes-finition-noir'
    '-velours-600863.html', 'https://www.e-planetelec.fr/prise-dooxie/1022-compensateur-actif-pour-commandes'
    '-eclairage-2-fils-sans-neutre-040149.html',
    'https://www.e-planetelec.fr/plaque-dooxie/1675-plaque-carree-dooxie-4-postes-finition-noir-velours-600864.html',
     'https://www.e-planetelec.fr/prise-dooxie/1023-interrupteur-vmc-dooxie-blanc-600007.html',
     'https://www.e-planetelec.fr/plaque-dooxie/1676-plaque-carree-dooxie-1-poste-finition-noir-velours-600861.html',
      'https://www.e-planetelec.fr/prise-dooxie/1024-interrupteur-vmc-dooxie-alu-600107.html',
      'https://www.e-planetelec.fr/prise-dooxie/1025-poussoir-commande-vmc-dooxie-blanc-600006.html',
      'https://www.e-planetelec.fr/plaque-dooxie/1662-plaque-ronde-dooxie-1-poste-finition-noir-velours-600976.html',
       'https://www.e-planetelec.fr/prise-dooxie/1026-poussoir-commande-vmc-dooxie-alu-600106.html',
       'https://www.e-planetelec.fr/prise-dooxie/1027-commande-de-volets-roulants-dooxie-blanc-600021.html',
       'https://www.e-planetelec.fr/prise-dooxie/1028-commande-de-volets-roulants-dooxie-alu-600121.html',
       'https://www.e-planetelec.fr/prise-dooxie/1029-lot-de-50-prises-de-courant-2p-t-surface-dooxie-16a-blanc'
       '-600635.html', 'https://www.e-planetelec.fr/prise-dooxie/1030-prise-de-courant-2p-t-surface-dooxie-16a-alu'
       '-600435.html', 'https://www.e-planetelec.fr/prise-dooxie/1031-prise-de-courant-2p-t-a-voyant-surface-dooxie'
       '-16a-blanc-600320.html', 'https://www.e-planetelec.fr/prise-dooxie/1032-prise-de-courant-2p-t-a-voyant'
       '-surface-dooxie-16a-alu-600420.html',
       'https://www.e-planetelec.fr/prise-dooxie/1033-double-prise-de-courant-2p-t-surface-dooxie-16a-precablees'
       '-finition-alu-600432.html', 'https://www.e-planetelec.fr/prise-dooxie/1034-triple-prise-de-courant-2p-t'
       '-surface-dooxie-16a-precablees-finition-blanc-600333.html',
       'https://www.e-planetelec.fr/prise-dooxie/1035-triple-prise-de-courant-2p-t-surface-dooxie-16a-precablees'
       '-finition-alu-600433.html', 'https://www.e-planetelec.fr/prise-dooxie/1036-prise-de-courant-easyreno-2p-t'
       '-dooxie-16a-finition-blanc-600328.html',
       'https://www.e-planetelec.fr/prise-dooxie/1037-prise-de-courant-easyreno-2p-t-dooxie-16a-finition-alu-600428'
       '.html', 'https://www.e-planetelec.fr/prise-dooxie/1038-double-prise-de-courant-compacte-monobloc-easyreno-2p'
       '-t-dooxie-16a-livree-avec-plaque-carree-blanche-600321.html',
       'https://www.e-planetelec.fr/prise-dooxie/1039-prise-de-courant-2p-t-a-puits-dooxie-16a-finition-blanc-600337'
       '.html', 'https://www.e-planetelec.fr/prise-dooxie/1040-prise-de-courant-2p-t-a-puits-dooxie-16a-finition-alu'
       '-600437.html', 'https://www.e-planetelec.fr/prise-dooxie/1041-sortie-de-cable-standard-dooxie-finition-blanc'
       '-600325.html', 'https://www.e-planetelec.fr/prise-dooxie/1042-sortie-de-cable-standard-dooxie-finition-alu'
       '-600425.html', 'https://www.e-planetelec.fr/prise-dooxie/1043-double-chargeur-usb-typea-dooxie-finition-blanc'
       '-600343.html', 'https://www.e-planetelec.fr/prise-dooxie/1044-double-chargeur-usb-typea-dooxie-finition-alu'
       '-600443.html', 'https://www.e-planetelec.fr/prise-dooxie/1045-double-chargeur-usb-1-typea-1-typec-dooxie'
       '-finition-blanc-600349.html', 'https://www.e-planetelec.fr/prise-dooxie/1046-double-chargeur-usb-1-typea-1'
       '-typec-dooxie-finition-alu-600449.html',
       'https://www.e-planetelec.fr/prise-dooxie/1047-prise-de-courant-2p-t-surface-module-de-charge-2-usb-typea'
       '-dooxie-precables-finition-blanc-600342.html',
       'https://www.e-planetelec.fr/prise-dooxie/1048-prise-de-courant-2p-t-surface-module-de-charge-2-usb-typea'
       '-dooxie-precables-finition-alu-600442.html',
       'https://www.e-planetelec.fr/prise-dooxie/1049-chargeur-a-induction-module-de-charge-usb-typea-dooxie-finition'
       '-metallisee-600348.html', 'https://www.e-planetelec.fr/prise-dooxie/1050-prise-tv-r-sat-1-cable-dooxie'
       '-finition-blanc-600353.html', 'https://www.e-planetelec.fr/prise-dooxie/1051-prise-tv-r-sat-1-cable-dooxie'
       '-finition-alu-600453.html', 'https://www.e-planetelec.fr/prise-dooxie/1052-prise-tv-simple-etoile-blindee'
       '-dooxie-finition-alu-600451.html',
       'https://www.e-planetelec.fr/prise-dooxie/1053-prise-tv-type-f-a-visser-dooxie-finition-blanc-600350.html',
       'https://www.e-planetelec.fr/prise-dooxie/1054-prise-tv-type-f-a-visser-dooxie-finition-alu-600450.html',
       'https://www.e-planetelec.fr/prise-dooxie/1055-prise-tv-sat-etoile-blindee-dooxie-finition-blanc-600356.html',
        'https://www.e-planetelec.fr/prise-dooxie/1056-prise-tv-sat-etoile-blindee-dooxie-finition-alu-600456.html',
        'https://www.e-planetelec.fr/prise-dooxie/1057-prise-tv-r-dooxie-finition-blanc-600354.html',
        'https://www.e-planetelec.fr/prise-dooxie/1058-prise-tv-r-dooxie-finition-alu-600454.html',
        'https://www.e-planetelec.fr/prise-dooxie/1059-prise-reseau-cable-aform-type-f-dooxie-a-etoile-blindee'
        '-finition-blanc-600357.html', 'https://www.e-planetelec.fr/prise-dooxie/1060-prise-reseau-cable-aform-type-f'
        '-dooxie-a-etoile-blindee-finition-alu-600457.html',
        'https://www.e-planetelec.fr/prise-dooxie/1061-prise-tv-rj45-cat6-stp-compacte-dooxie-finition-blanc-600352'
        '.html', 'https://www.e-planetelec.fr/prise-dooxie/1062-prise-tv-rj45-cat6-stp-compacte-dooxie-finition-alu'
        '-600452.html', 'https://www.e-planetelec.fr/prise-dooxie/1063-prise-tv-sat-rj45-cat6-stp-compacte-dooxie'
        '-finition-blanc-600358.html', 'https://www.e-planetelec.fr/prise-dooxie/1064-prise-tv-sat-rj45-cat6-stp'
        '-compacte-dooxie-finition-alu-600458.html',
        'https://www.e-planetelec.fr/prise-dooxie/1065-prise-blindee-rj45-cat6-stp-dooxie-finition-alu-600475.html',
        'https://www.e-planetelec.fr/prise-dooxie/1066-prise-blindee-rj45-cat6-ftp-dooxie-finition-blanc-600376.html'
        '', 'https://www.e-planetelec.fr/prise-dooxie/1067-prise-blindee-rj45-cat6-ftp-dooxie-finition-alu-600476'
        '.html', 'https://www.e-planetelec.fr/prise-dooxie/1068-prise-blindee-rj45-cat5e-ftp-dooxie-finition-blanc'
        '-600377.html', 'https://www.e-planetelec.fr/prise-dooxie/1069-prise-blindee-rj45-cat5e-ftp-dooxie-finition'
        '-alu-600477.html', 'https://www.e-planetelec.fr/prise-dooxie/1070-prise-hdmi-pre-connectorisee-dooxie'
        '-finition-blanc-600385.html', 'https://www.e-planetelec.fr/prise-dooxie/1072-prise-telephone-en-t-dooxie'
        '-finition-blanc-600368.html', 'https://www.e-planetelec.fr/prise-dooxie/1073-prise-telephone-en-t-dooxie'
        '-finition-alu-600468.html', 'https://www.e-planetelec.fr/prise-dooxie/1074-prise-haut-parleur-simple-dooxie'
        '-finition-blanc-600381.html', 'https://www.e-planetelec.fr/prise-dooxie/1075-prise-haut-parleur-simple'
        '-dooxie-finition-alu-600481.html',
        'https://www.e-planetelec.fr/prise-dooxie/1076-prise-haut-parleur-double-dooxie-finition-blanc-600382.html',
        'https://www.e-planetelec.fr/prise-dooxie/1077-prise-haut-parleur-double-dooxie-finition-alu-600482.html',
        'https://www.e-planetelec.fr/prise-dooxie/1078-griffe-rapido-profondeur-30mm-pour-fixation-des-appareils'
        '-dooxie-en-renovation-600047.html',
        'https://www.e-planetelec.fr/prise-dooxie/1079-griffe-rapido-profondeur-40mm-pour-fixation-des-appareils'
        '-dooxie-en-renovation-600049.html',
        'https://www.e-planetelec.fr/prise-dooxie/1080-griffe-rapido-profondeur-60mm-pour-fixation-des-appareils'
        '-dooxie-en-renovation-dans-carrelage-600048.html',
        'https://www.e-planetelec.fr/prise-dooxie/1081-cadre-saillie-1-poste-dooxie-finition-blanc-600041.html',
        'https://www.e-planetelec.fr/prise-dooxie/1082-cadre-saillie-1-poste-dooxie-finition-alu-600141.html',
        'https://www.e-planetelec.fr/prise-dooxie/1083-cadre-saillie-2-postes-dooxie-finition-blanc-600042.html',
        'https://www.e-planetelec.fr/prise-dooxie/1084-cadre-saillie-2-postes-dooxie-finition-alu-600142.html',
        'https://www.e-planetelec.fr/prise-dooxie/1085-obturateur-dooxie-finition-blanc-600044.html',
        'https://www.e-planetelec.fr/prise-dooxie/1086-obturateur-dooxie-finition-alu.html',
        'https://www.e-planetelec.fr/prise-dooxie/1087-chaussette-d-etancheite-a-l-air-dooxie-pour-installation-basse'
        '-consommation-600045.html', 'https://www.e-planetelec.fr/prise-dooxie/1088-voyant-led-lumineux-230v-dooxie-a'
        '-raccordement-par-montage-direct-2-fils-600043.html',
        'https://www.e-planetelec.fr/prise-dooxie/1089-voyant-led-temoin-230v-dooxie-a-raccordement-par-montage'
        '-direct-2-fils-600243.html', 'https://www.e-planetelec.fr/prise-dooxie/1090-voyant-led-lumineux-24v-dooxie-a'
        '-raccordement-par-montage-direct-2-fils-600143.html',
        'https://www.e-planetelec.fr/prise-dooxie/1091-pret-a-poser-dooxie-creer-un-va-et-vient-avec-2-commandes-sans'
        '-fil-et-1-micromodule-livre-complet-blanc-600699.html',
        'https://www.e-planetelec.fr/prise-dooxie/1093-pret-a-poser-dooxie-creer-une-prise-commandee-avec-1-prise-de'
        '-courant-et-1-commande-sans-fil-livre-complet-blanc-600694.html',
        'https://www.e-planetelec.fr/prise-dooxie/1094-pret-a-poser-dooxie-commander-un-volet-roulant-avec-1-commande'
        '-sans-fil-et-1-interrupteur-livre-complet-blanc-600696.html',
        'https://www.e-planetelec.fr/prise-dooxie/1645-transformeur-pour-realiser-5-fonctions-lumineuses-dooxie-one'
        '-600730.html', 'https://www.e-planetelec.fr/prise-dooxie/1686-prise-de-courant-2p-t-surface-dooxie-16a'
        '-finition-noir-emballage-blister-095275.html',
        'https://www.e-planetelec.fr/prise-dooxie/1673-interrupteur-ou-va-et-vient-dooxie-10ax-250v-finition-noir'
        '-emballage-blister-095260.html',
        'https://www.e-planetelec.fr/prise-dooxie/1672-poussoir-simple-dooxie-6a-250v-finition-noir-emballage-blister'
        '-095264.html', 'https://www.e-planetelec.fr/prise-dooxie/1658-prise-telephone-en-t-dooxie-finition-noir'
        '-emballage-blister-095286.html', 'https://www.e-planetelec.fr/prise-dooxie/1659-commande-de-volets-roulants'
        '-dooxie-finition-noir-emballage-blister-095272.html',
        'https://www.e-planetelec.fr/prise-dooxie/1660-interrupteur-commande-vmc-dooxie-finition-noir-emballage'
        '-blister-095273.html', 'https://www.e-planetelec.fr/prise-dooxie/1661-prise-tv-type-f-a-visser-dooxie'
        '-finition-noir-emballage-blister-095283.html',
        'https://www.e-planetelec.fr/prise-dooxie/1663-prise-blindee-rj45-cat6-stp-dooxie-finition-noir-emballage'
        '-blister-095285.html', 'https://www.e-planetelec.fr/prise-dooxie/1664-prise-haut-parleur-double-dooxie'
        '-finition-noir-emballage-blister-095289.html',
        'https://www.e-planetelec.fr/prise-dooxie/1666-interrupteur-automatique-dooxie-2-fils-sans-neutre-finition'
        '-noir-emballage-blister-095271.html',
        'https://www.e-planetelec.fr/prise-dooxie/1667-poussoir-double-dooxie-6a-250v-finition-noir-emballage-blister'
        '-095265.html', 'https://www.e-planetelec.fr/prise-dooxie/1668-sortie-de-cable-standard-dooxie-finition-noir'
        '-emballage-blister-095281.html',
        'https://www.e-planetelec.fr/plaque-dooxie/1095-plaque-carree-dooxie-1-poste-finition-blanc-600801.html',
        'https://www.e-planetelec.fr/prise-dooxie/986-interrupteur-ou-va-et-vient-dooxie-blanc-600001.html',
        'https://www.e-planetelec.fr/plaque-dooxie/1096-lot-de-100-plaques-carrees-dooxie-1-poste-finition-blanc'
        '-600941.html', 'https://www.e-planetelec.fr/prise-dooxie/987-lot-de-50-interrupteurs-ou-va-et-vient-dooxie'
        '-blanc-600601.html', 'https://www.e-planetelec.fr/plaque-dooxie/1097-plaque-carree-dooxie-2-postes-finition'
        '-blanc-600802.html', 'https://www.e-planetelec.fr/prise-dooxie/988-double-interrupteur-ou-va-et-vient-dooxie'
        '-blanc-600002.html', 'https://www.e-planetelec.fr/plaque-dooxie/1098-plaque-carree-dooxie-3-postes-finition'
        '-blanc-600803.html', 'https://www.e-planetelec.fr/plaque-dooxie/1099-plaque-carree-dooxie-4-postes-finition'
        '-blanc-600804.html', 'https://www.e-planetelec.fr/prise-dooxie/989-poussoir-simple-dooxie-blanc-600004.html'
        '', 'https://www.e-planetelec.fr/plaque-dooxie/1100-plaque-carree-dooxie-1-poste-finition-dune-600811.html',
        'https://www.e-planetelec.fr/prise-dooxie/990-poussoir-double-dooxie-blanc-600008.html',
        'https://www.e-planetelec.fr/plaque-dooxie/1101-plaque-carree-dooxie-2-postes-finition-dune-600812.html',
        'https://www.e-planetelec.fr/prise-dooxie/991-poussoir-simple-avec-voyant-lumineux-dooxie-blanc-600016.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1102-plaque-carree-dooxie-3-postes-finition-dune-600813.html',
         'https://www.e-planetelec.fr/prise-dooxie/992-transformeur-pour-realiser-5-fonctions-dooxie-blanc-600031'
         '.html', 'https://www.e-planetelec.fr/plaque-dooxie/1103-plaque-carree-dooxie-4-postes-finition-dune-600814'
         '.html', 'https://www.e-planetelec.fr/prise-dooxie/993-prise-de-courant-2p-t-surface-dooxie-16a-blanc-600335'
         '.html', 'https://www.e-planetelec.fr/plaque-dooxie/1104-plaque-carree-dooxie-1-poste-finition-plume-600821'
         '.html', 'https://www.e-planetelec.fr/prise-dooxie/994-double-prise-de-courant-2p-t-surface-dooxie-16a'
         '-precablees-blanc-600332.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1105-plaque-carree-dooxie-2-postes-finition-plume-600822.html',
         'https://www.e-planetelec.fr/prise-dooxie/995-sortie-de-cable-ip21-dooxie-livree-complete-blanc-600323.html'
         '', 'https://www.e-planetelec.fr/plaque-dooxie/1106-plaque-carree-dooxie-3-postes-finition-plume-600823.html'
         '', 'https://www.e-planetelec.fr/prise-dooxie/996-prise-blindee-rj45-cat6-stp-dooxie-blanc-600375.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1107-plaque-carree-dooxie-4-postes-finition-plume-600824.html',
         'https://www.e-planetelec.fr/prise-dooxie/997-prise-tv-simple-etoile-blindee-dooxie-blanc-600351.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1108-plaque-carree-dooxie-1-poste-finition-blanc-avec-bague-effet'
         '-chrome-600841.html', 'https://www.e-planetelec.fr/prise-dooxie/998-transformeur-pour-realiser-5-fonctions'
         '-dooxie-alu-600131.html', 'https://www.e-planetelec.fr/plaque-dooxie/1109-plaque-carree-dooxie-2-postes'
         '-finition-blanc-avec-bague-effet-chrome-600842.html',
         'https://www.e-planetelec.fr/prise-dooxie/999-interrupteur-ou-va-et-vient-dooxie-alu-600101.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1110-plaque-carree-dooxie-3-postes-finition-blanc-avec-bague'
         '-effet-chrome-600843.html', 'https://www.e-planetelec.fr/prise-dooxie/1000-double-interrupteur-ou-va-et'
         '-vient-dooxie-finition-alu-600102.html',
         'https://www.e-planetelec.fr/prise-dooxie/1001-interrupteur-ou-va-et-vient-avec-voyant-lumineux-dooxie-blanc'
         '-600011.html', 'https://www.e-planetelec.fr/plaque-dooxie/1111-plaque-carree-dooxie-1-poste-finition-effet'
         '-aluminium-600851.html', 'https://www.e-planetelec.fr/prise-dooxie/1002-interrupteur-ou-va-et-vient-avec'
         '-voyant-lumineux-dooxie-alu-600111.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1112-plaque-carree-dooxie-2-postes-finition-effet-aluminium'
         '-600852.html', 'https://www.e-planetelec.fr/prise-dooxie/1003-interrupteur-ou-va-et-vient-avec-voyant'
         '-temoin-dooxie-blanc-600009.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1113-plaque-carree-dooxie-3-postes-finition-effet-aluminium'
         '-600853.html', 'https://www.e-planetelec.fr/prise-dooxie/1004-interrupteur-ou-va-et-vient-avec-voyant'
         '-temoin-dooxie-alu-600109.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1114-plaque-carree-dooxie-4-postes-finition-effet-aluminium'
         '-600854.html', 'https://www.e-planetelec.fr/plaque-dooxie/1115-plaque-carree-dooxie-1-poste-finition-effet'
         '-inox-brosse-600871.html', 'https://www.e-planetelec.fr/prise-dooxie/1005-permutateur-dooxie-blanc-600037'
         '.html', 'https://www.e-planetelec.fr/plaque-dooxie/1116-plaque-carree-dooxie-2-postes-finition-effet-inox'
         '-brosse-600872.html', 'https://www.e-planetelec.fr/prise-dooxie/1006-permutateur-dooxie-alu-600137.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1117-plaque-carree-dooxie-3-postes-finition-effet-inox-brosse'
         '-600873.html', 'https://www.e-planetelec.fr/prise-dooxie/1007-poussoir-simple-dooxie-alu-600104.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1118-plaque-carree-dooxie-1-poste-finition-effet-bois-ebene'
         '-600881.html', 'https://www.e-planetelec.fr/prise-dooxie/1008-poussoir-double-dooxie-alu-600108.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1119-plaque-carree-dooxie-2-postes-finition-effet-bois-ebene'
         '-600882.html', 'https://www.e-planetelec.fr/plaque-dooxie/1119-plaque-carree-dooxie-2-postes-finition-effet'
         '-bois-ebene-600882.html', 'https://www.e-planetelec.fr/prise-dooxie/1010-poussoir-simple-avec-voyant'
         '-lumineux-et-marquage-cadenas-dooxie-blanc-600017.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1120-plaque-carree-dooxie-3-postes-finition-effet-bois-ebene'
         '-600883.html', 'https://www.e-planetelec.fr/plaque-dooxie/1121-plaque-ronde-dooxie-1-poste-finition-blanc'
         '-600980.html', 'https://www.e-planetelec.fr/prise-dooxie/1011-poussoir-simple-avec-voyant-lumineux-et'
         '-marquage-cadenas-dooxie-alu-600117.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1122-plaque-ronde-dooxie-1-poste-finition-dune-600970.html',
         'https://www.e-planetelec.fr/prise-dooxie/1012-poussoir-simple-avec-voyant-lumineux-et-marquage-sonnette'
         '-dooxie-blanc-600018.html', 'https://www.e-planetelec.fr/plaque-dooxie/1123-plaque-ronde-dooxie-1-poste'
         '-finition-plume-600971.html', 'https://www.e-planetelec.fr/prise-dooxie/1013-poussoir-simple-avec-voyant'
         '-lumineux-et-marquage-sonnette-dooxie-alu-600118.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1124-plaque-ronde-dooxie-1-poste-finition-blanc-avec-bague-effet'
         '-chrome-600973.html', 'https://www.e-planetelec.fr/prise-dooxie/1014-interrupteur-a-badge-dooxie-blanc'
         '-600033.html', 'https://www.e-planetelec.fr/plaque-dooxie/1125-plaque-ronde-dooxie-1-poste-finition-effet'
         '-aluminium-bague-effet-chrome-600975.html',
         'https://www.e-planetelec.fr/prise-dooxie/1015-interrupteur-a-badge-dooxie-alu-600133.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1126-plaque-ronde-dooxie-1-poste-finition-effet-inox-brosse'
         '-600978.html', 'https://www.e-planetelec.fr/prise-dooxie/1016-interrupteur-automatique-pour-minuterie-en'
         '-remplacement-d-un-poussoir-dooxie-blanc-600061.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1127-obturateur-dooxie-finition-blanc-600044.html',
         'https://www.e-planetelec.fr/prise-dooxie/1017-interrupteur-automatique-pour-minuterie-en-remplacement-d-un'
         '-poussoir-dooxie-alu-600161.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1128-plaque-carree-dooxie-1-poste-finition-blanc-avec-porte'
         '-etiquette-600942.html', 'https://www.e-planetelec.fr/prise-dooxie/1018-interrupteur-automatique-dooxie-2'
         '-fils-sans-neutre-finition-blanc-600064.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1129-plaque-carree-dooxie-1-poste-avec-volet-ip44-ik07-600944'
         '.html', 'https://www.e-planetelec.fr/prise-dooxie/1019-interrupteur-automatique-dooxie-2-fils-sans-neutre'
         '-alu-600164.html', 'https://www.e-planetelec.fr/plaque-dooxie/1130-plaque-carree-speciale-dooxie-2-postes'
         '-avec-entraxe-57mm-finition-blanc-600807.html',
         'https://www.e-planetelec.fr/prise-dooxie/1020-variateur-toutes-lampes-dooxie-2-fils-sans-neutre-blanc'
         '-600060.html', 'https://www.e-planetelec.fr/plaque-dooxie/1665-plaque-carree-dooxie-2-postes-finition-noir'
         '-velours-600862.html', 'https://www.e-planetelec.fr/prise-dooxie/1021-variateur-toutes-lampes-dooxie-2-fils'
         '-sans-neutre-alu-600160.html',
         'https://www.e-planetelec.fr/plaque-dooxie/1671-plaque-carree-dooxie-3-postes-finition-noir-velours-600863'
         '.html', 'https://www.e-planetelec.fr/prise-dooxie/1022-compensateur-actif-pour-commandes-eclairage-2-fils'
         '-sans-neutre-040149.html', 'https://www.e-planetelec.fr/prise-dooxie/1023-interrupteur-vmc-dooxie-blanc'
         '-600007.html', 'https://www.e-planetelec.fr/plaque-dooxie/1675-plaque-carree-dooxie-4-postes-finition-noir'
         '-velours-600864.html', 'https://www.e-planetelec.fr/prise-dooxie/1024-interrupteur-vmc-dooxie-alu-600107'
         '.html', 'https://www.e-planetelec.fr/plaque-dooxie/1676-plaque-carree-dooxie-1-poste-finition-noir-velours'
         '-600861.html', 'https://www.e-planetelec.fr/prise-dooxie/1025-poussoir-commande-vmc-dooxie-blanc-600006'
         '.html', 'https://www.e-planetelec.fr/plaque-dooxie/1662-plaque-ronde-dooxie-1-poste-finition-noir-velours'
         '-600976.html', 'https://www.e-planetelec.fr/prise-dooxie/1026-poussoir-commande-vmc-dooxie-alu-600106.html'
         '', 'https://www.e-planetelec.fr/prise-dooxie/1027-commande-de-volets-roulants-dooxie-blanc-600021.html',
         'https://www.e-planetelec.fr/prise-dooxie/1028-commande-de-volets-roulants-dooxie-alu-600121.html',
         'https://www.e-planetelec.fr/prise-dooxie/1029-lot-de-50-prises-de-courant-2p-t-surface-dooxie-16a-blanc'
         '-600635.html', 'https://www.e-planetelec.fr/prise-dooxie/1030-prise-de-courant-2p-t-surface-dooxie-16a-alu'
         '-600435.html', 'https://www.e-planetelec.fr/prise-dooxie/1031-prise-de-courant-2p-t-a-voyant-surface-dooxie'
         '-16a-blanc-600320.html', 'https://www.e-planetelec.fr/prise-dooxie/1032-prise-de-courant-2p-t-a-voyant'
         '-surface-dooxie-16a-alu-600420.html',
         'https://www.e-planetelec.fr/prise-dooxie/1033-double-prise-de-courant-2p-t-surface-dooxie-16a-precablees'
         '-finition-alu-600432.html', 'https://www.e-planetelec.fr/prise-dooxie/1034-triple-prise-de-courant-2p-t'
         '-surface-dooxie-16a-precablees-finition-blanc-600333.html',
         'https://www.e-planetelec.fr/prise-dooxie/1035-triple-prise-de-courant-2p-t-surface-dooxie-16a-precablees'
         '-finition-alu-600433.html', 'https://www.e-planetelec.fr/prise-dooxie/1036-prise-de-courant-easyreno-2p-t'
         '-dooxie-16a-finition-blanc-600328.html',
         'https://www.e-planetelec.fr/prise-dooxie/1037-prise-de-courant-easyreno-2p-t-dooxie-16a-finition-alu-600428'
         '.html', 'https://www.e-planetelec.fr/prise-dooxie/1038-double-prise-de-courant-compacte-monobloc-easyreno'
         '-2p-t-dooxie-16a-livree-avec-plaque-carree-blanche-600321.html',
         'https://www.e-planetelec.fr/prise-dooxie/1039-prise-de-courant-2p-t-a-puits-dooxie-16a-finition-blanc'
         '-600337.html', 'https://www.e-planetelec.fr/prise-dooxie/1040-prise-de-courant-2p-t-a-puits-dooxie-16a'
         '-finition-alu-600437.html', 'https://www.e-planetelec.fr/prise-dooxie/1041-sortie-de-cable-standard-dooxie'
         '-finition-blanc-600325.html', 'https://www.e-planetelec.fr/prise-dooxie/1042-sortie-de-cable-standard'
         '-dooxie-finition-alu-600425.html',
         'https://www.e-planetelec.fr/prise-dooxie/1043-double-chargeur-usb-typea-dooxie-finition-blanc-600343.html',
          'https://www.e-planetelec.fr/prise-dooxie/1044-double-chargeur-usb-typea-dooxie-finition-alu-600443.html',
          'https://www.e-planetelec.fr/prise-dooxie/1045-double-chargeur-usb-1-typea-1-typec-dooxie-finition-blanc'
          '-600349.html', 'https://www.e-planetelec.fr/prise-dooxie/1046-double-chargeur-usb-1-typea-1-typec-dooxie'
          '-finition-alu-600449.html', 'https://www.e-planetelec.fr/prise-dooxie/1047-prise-de-courant-2p-t-surface'
          '-module-de-charge-2-usb-typea-dooxie-precables-finition-blanc-600342.html',
          'https://www.e-planetelec.fr/prise-dooxie/1048-prise-de-courant-2p-t-surface-module-de-charge-2-usb-typea'
          '-dooxie-precables-finition-alu-600442.html',
          'https://www.e-planetelec.fr/prise-dooxie/1049-chargeur-a-induction-module-de-charge-usb-typea-dooxie'
          '-finition-metallisee-600348.html',
          'https://www.e-planetelec.fr/prise-dooxie/1050-prise-tv-r-sat-1-cable-dooxie-finition-blanc-600353.html',
          'https://www.e-planetelec.fr/prise-dooxie/1051-prise-tv-r-sat-1-cable-dooxie-finition-alu-600453.html',
          'https://www.e-planetelec.fr/prise-dooxie/1052-prise-tv-simple-etoile-blindee-dooxie-finition-alu-600451'
          '.html', 'https://www.e-planetelec.fr/prise-dooxie/1053-prise-tv-type-f-a-visser-dooxie-finition-blanc'
          '-600350.html', 'https://www.e-planetelec.fr/prise-dooxie/1054-prise-tv-type-f-a-visser-dooxie-finition-alu'
          '-600450.html', 'https://www.e-planetelec.fr/prise-dooxie/1055-prise-tv-sat-etoile-blindee-dooxie-finition'
          '-blanc-600356.html', 'https://www.e-planetelec.fr/prise-dooxie/1056-prise-tv-sat-etoile-blindee-dooxie'
          '-finition-alu-600456.html', 'https://www.e-planetelec.fr/prise-dooxie/1057-prise-tv-r-dooxie-finition'
          '-blanc-600354.html', 'https://www.e-planetelec.fr/prise-dooxie/1058-prise-tv-r-dooxie-finition-alu-600454'
          '.html', 'https://www.e-planetelec.fr/prise-dooxie/1059-prise-reseau-cable-aform-type-f-dooxie-a-etoile'
          '-blindee-finition-blanc-600357.html',
          'https://www.e-planetelec.fr/prise-dooxie/1060-prise-reseau-cable-aform-type-f-dooxie-a-etoile-blindee'
          '-finition-alu-600457.html', 'https://www.e-planetelec.fr/prise-dooxie/1061-prise-tv-rj45-cat6-stp-compacte'
          '-dooxie-finition-blanc-600352.html',
          'https://www.e-planetelec.fr/prise-dooxie/1062-prise-tv-rj45-cat6-stp-compacte-dooxie-finition-alu-600452'
          '.html', 'https://www.e-planetelec.fr/prise-dooxie/1063-prise-tv-sat-rj45-cat6-stp-compacte-dooxie-finition'
          '-blanc-600358.html', 'https://www.e-planetelec.fr/prise-dooxie/1064-prise-tv-sat-rj45-cat6-stp-compacte'
          '-dooxie-finition-alu-600458.html',
          'https://www.e-planetelec.fr/prise-dooxie/1065-prise-blindee-rj45-cat6-stp-dooxie-finition-alu-600475.html'
          '', 'https://www.e-planetelec.fr/prise-dooxie/1066-prise-blindee-rj45-cat6-ftp-dooxie-finition-blanc-600376'
          '.html', 'https://www.e-planetelec.fr/prise-dooxie/1067-prise-blindee-rj45-cat6-ftp-dooxie-finition-alu'
          '-600476.html', 'https://www.e-planetelec.fr/prise-dooxie/1068-prise-blindee-rj45-cat5e-ftp-dooxie-finition'
          '-blanc-600377.html', 'https://www.e-planetelec.fr/prise-dooxie/1069-prise-blindee-rj45-cat5e-ftp-dooxie'
          '-finition-alu-600477.html', 'https://www.e-planetelec.fr/prise-dooxie/1070-prise-hdmi-pre-connectorisee'
          '-dooxie-finition-blanc-600385.html',
          'https://www.e-planetelec.fr/prise-dooxie/1072-prise-telephone-en-t-dooxie-finition-blanc-600368.html',
          'https://www.e-planetelec.fr/prise-dooxie/1073-prise-telephone-en-t-dooxie-finition-alu-600468.html',
          'https://www.e-planetelec.fr/prise-dooxie/1074-prise-haut-parleur-simple-dooxie-finition-blanc-600381.html'
          '', 'https://www.e-planetelec.fr/prise-dooxie/1075-prise-haut-parleur-simple-dooxie-finition-alu-600481'
          '.html', 'https://www.e-planetelec.fr/prise-dooxie/1076-prise-haut-parleur-double-dooxie-finition-blanc'
          '-600382.html', 'https://www.e-planetelec.fr/prise-dooxie/1077-prise-haut-parleur-double-dooxie-finition'
          '-alu-600482.html', 'https://www.e-planetelec.fr/prise-dooxie/1078-griffe-rapido-profondeur-30mm-pour'
          '-fixation-des-appareils-dooxie-en-renovation-600047.html',
          'https://www.e-planetelec.fr/prise-dooxie/1079-griffe-rapido-profondeur-40mm-pour-fixation-des-appareils'
          '-dooxie-en-renovation-600049.html',
          'https://www.e-planetelec.fr/prise-dooxie/1080-griffe-rapido-profondeur-60mm-pour-fixation-des-appareils'
          '-dooxie-en-renovation-dans-carrelage-600048.html',
          'https://www.e-planetelec.fr/prise-dooxie/1081-cadre-saillie-1-poste-dooxie-finition-blanc-600041.html',
          'https://www.e-planetelec.fr/prise-dooxie/1082-cadre-saillie-1-poste-dooxie-finition-alu-600141.html',
          'https://www.e-planetelec.fr/prise-dooxie/1083-cadre-saillie-2-postes-dooxie-finition-blanc-600042.html',
          'https://www.e-planetelec.fr/prise-dooxie/1084-cadre-saillie-2-postes-dooxie-finition-alu-600142.html',
          'https://www.e-planetelec.fr/prise-dooxie/1085-obturateur-dooxie-finition-blanc-600044.html',
          'https://www.e-planetelec.fr/prise-dooxie/1086-obturateur-dooxie-finition-alu.html',
          'https://www.e-planetelec.fr/prise-dooxie/1087-chaussette-d-etancheite-a-l-air-dooxie-pour-installation'
          '-basse-consommation-600045.html',
          'https://www.e-planetelec.fr/prise-dooxie/1088-voyant-led-lumineux-230v-dooxie-a-raccordement-par-montage'
          '-direct-2-fils-600043.html', 'https://www.e-planetelec.fr/prise-dooxie/1089-voyant-led-temoin-230v-dooxie'
          '-a-raccordement-par-montage-direct-2-fils-600243.html',
          'https://www.e-planetelec.fr/prise-dooxie/1090-voyant-led-lumineux-24v-dooxie-a-raccordement-par-montage'
          '-direct-2-fils-600143.html', 'https://www.e-planetelec.fr/prise-dooxie/1091-pret-a-poser-dooxie-creer-un'
          '-va-et-vient-avec-2-commandes-sans-fil-et-1-micromodule-livre-complet-blanc-600699.html',
          'https://www.e-planetelec.fr/prise-dooxie/1093-pret-a-poser-dooxie-creer-une-prise-commandee-avec-1-prise'
          '-de-courant-et-1-commande-sans-fil-livre-complet-blanc-600694.html',
          'https://www.e-planetelec.fr/prise-dooxie/1094-pret-a-poser-dooxie-commander-un-volet-roulant-avec-1'
          '-commande-sans-fil-et-1-interrupteur-livre-complet-blanc-600696.html',
          'https://www.e-planetelec.fr/prise-dooxie/1645-transformeur-pour-realiser-5-fonctions-lumineuses-dooxie-one'
          '-600730.html', 'https://www.e-planetelec.fr/prise-dooxie/1686-prise-de-courant-2p-t-surface-dooxie-16a'
          '-finition-noir-emballage-blister-095275.html',
          'https://www.e-planetelec.fr/prise-dooxie/1673-interrupteur-ou-va-et-vient-dooxie-10ax-250v-finition-noir'
          '-emballage-blister-095260.html',
          'https://www.e-planetelec.fr/prise-dooxie/1672-poussoir-simple-dooxie-6a-250v-finition-noir-emballage'
          '-blister-095264.html', 'https://www.e-planetelec.fr/prise-dooxie/1658-prise-telephone-en-t-dooxie-finition'
          '-noir-emballage-blister-095286.html',
          'https://www.e-planetelec.fr/prise-dooxie/1659-commande-de-volets-roulants-dooxie-finition-noir-emballage'
          '-blister-095272.html', 'https://www.e-planetelec.fr/prise-dooxie/1660-interrupteur-commande-vmc-dooxie'
          '-finition-noir-emballage-blister-095273.html',
          'https://www.e-planetelec.fr/prise-dooxie/1661-prise-tv-type-f-a-visser-dooxie-finition-noir-emballage'
          '-blister-095283.html', 'https://www.e-planetelec.fr/prise-dooxie/1663-prise-blindee-rj45-cat6-stp-dooxie'
          '-finition-noir-emballage-blister-095285.html',
          'https://www.e-planetelec.fr/prise-dooxie/1664-prise-haut-parleur-double-dooxie-finition-noir-emballage'
          '-blister-095289.html', 'https://www.e-planetelec.fr/prise-dooxie/1666-interrupteur-automatique-dooxie-2'
          '-fils-sans-neutre-finition-noir-emballage-blister-095271.html',
          'https://www.e-planetelec.fr/prise-dooxie/1667-poussoir-double-dooxie-6a-250v-finition-noir-emballage'
          '-blister-095265.html', 'https://www.e-planetelec.fr/prise-dooxie/1668-sortie-de-cable-standard-dooxie'
          '-finition-noir-emballage-blister-095281.html',
          'https://www.e-planetelec.fr/prise-dooxie/1669-prise-tv-sat-etoile-blindee-dooxie-finition-noir-emballage'
          '-blister-095284.html', 'https://www.e-planetelec.fr/prise-dooxie/1670-prise-tv-etoile-blindee-dooxie'
          '-finition-noir-emballage-blister-095282.html',
          'https://www.e-planetelec.fr/prise-dooxie/1674-double-chargeur-usb-typea-dooxie-3a-finition-noir-emballage'
          '-blister-095287.html', 'https://www.e-planetelec.fr/prise-dooxie/1677-double-prise-de-courant-2p-t-surface'
          '-dooxie-16a-precablees-finition-noir-emballage-blister-095278.html',
          'https://www.e-planetelec.fr/prise-dooxie/1678-poussoir-simple-avec-voyant-lumineux-dooxie-6a-250v-finition'
          '-noir-emballage-blister-095267.html',
          'https://www.e-planetelec.fr/prise-dooxie/1679-prise-de-courant-2p-a-puits-dooxie-16a-finition-noir'
          '-emballage-blister-095274.html',
          'https://www.e-planetelec.fr/prise-dooxie/1680-prise-de-courant-2p-t-a-puits-dooxie-16a-finition-noir'
          '-emballage-blister-095276.html',
          'https://www.e-planetelec.fr/prise-dooxie/1681-triple-prise-de-courant-2p-t-surface-dooxie-16a-precablees'
          '-finition-noir-emballage-blister-095279.html',
          'https://www.e-planetelec.fr/prise-dooxie/1682-interrupteur-ou-va-et-vient-avec-voyant-temoin-dooxie-10ax'
          '-250v-finition-noir-emballage-blister-095263.html',
          'https://www.e-planetelec.fr/prise-dooxie/1683-prise-de-courant-easyreno-2p-t-faible-profondeur-dooxie-16a'
          '-finition-noir-emballage-blister-095277.html',
          'https://www.e-planetelec.fr/prise-dooxie/1684-interrupteur-ou-va-et-vient-10ax-bouton-poussoir-6a-dooxie'
          '-finition-noir-emballage-blister-095266.html',
          'https://www.e-planetelec.fr/prise-dooxie/1685-double-chargeur-usb-1-typea-1-typec-dooxie-3a-finition-noir'
          '-emballage-blister-095288.html',
          'https://www.e-planetelec.fr/prise-dooxie/1687-variateur-toutes-lampes-dooxie-2-fils-sans-neutre-finition'
          '-noir-emballage-blister-095270.html',
          'https://www.e-planetelec.fr/prise-dooxie/1688-kit-prise-de-courant-surface-module-de-charge-2-usb-typea'
          '-dooxie-2-4a-precables-finition-noir-300409.html',
          'https://www.e-planetelec.fr/prise-dooxie/1689-double-interrupteur-ou-va-et-vient-dooxie-10ax-250v-finition'
          '-noir-emballage-blister-095261.html',
          'https://www.e-planetelec.fr/prise-dooxie/1690-interrupteur-ou-va-et-vient-avec-voyant-lumineux-dooxie-10ax'
          '-250v-finition-noir-emballage-blister-095262.html',
          'https://www.e-planetelec.fr/prise-dooxie/1691-kit-double-prise-de-courant-2p-t-surface-dooxie-16a'
          '-precablees-finition-noir-300402.html',
          'https://www.e-planetelec.fr/prise-dooxie/1692-kit-triple-prise-de-courant-2p-t-surface-dooxie-16a'
          '-precablees-finition-noir-300406.html',
          'https://www.e-planetelec.fr/prise-dooxie/1693-double-chargeur-usb-typec-dooxie-3a-finition-noir-emballage'
          '-blister-095296.html', 'https://www.e-planetelec.fr/prise-dooxie/1737-prise-de-courant-2p-a-puits-dooxie'
          '-16a-finition-blanc-600334.html',
          'https://www.e-planetelec.fr/prise-dooxie/1738-prise-de-courant-2p-a-puits-dooxie-16a-finition-alu-600434'
          '.html', 'https://www.e-planetelec.fr/prise-dooxie/1749-sortie-de-cable-standard-dooxie-finition-blanc-ip44'
          '-600324.html', 'https://www.e-planetelec.fr/prise-dooxie/1790-prise-2pt-surface-avec-chargeur-usb-type-c'
          '-dooxie-livree-avec-support-blanc-600341.html',
          'https://www.e-planetelec.fr/prise-dooxie/1866-prise-rj45-cat-6a-stp-dooxie-blanc-600374.html',
          'https://www.e-planetelec.fr/prise-dooxie/1873-double-prise-rj45-cat6-stp-dooxie-blanc-600378.html',
          'https://www.e-planetelec.fr/prise-dooxie/1910-transformeur-pour-realiser-5-fonctions-dooxie-one-600731'
          '.html', 'https://www.e-planetelec.fr/prise-dooxie/2320-prise-de-courant-2pt-a-puits-dooxie-16a-ip44-livree'
          '-avec-plaque-carree-blanche-600344.html',
          'https://www.e-planetelec.fr/prise-dooxie/2321-interrupteur-ou-va-et-vient-dooxie-ip44-10ax-250v-livre-avec'
          '-plaque-carree-blanche-600013.html',
          'https://www.e-planetelec.fr/prise-dooxie/2684-poussoir-pour-commande-de-volets-roulants-dooxie-blanc'
          '-600022.html', 'https://www.e-planetelec.fr/prise-dooxie/3087-double-chargeur-usb-type-c-dooxie-finition'
          '-blanc-600345.html', 'https://www.e-planetelec.fr/prise-dooxie/3227-prise-de-courant-2pt-surface-chargeur'
          '-usb-type-c-finition-noir-emballage-blister-095280-legrand.html',
          'https://www.e-planetelec.fr/accessoires-ovalis-schneider/3207-ovalis-boite-support-36-mm-pour-montage-en'
          '-saillie-blanc-s320762.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3175-ovalis-prise'
          '-2pt-16a-affleurante-bornes-automatiques-antibacterien-s300052.html',
          'https://www.e-planetelec.fr/plaques-ovalis-schneider/3208-ovalis-plaque-de-finition-1-poste-antibacterien'
          '-s300702.html', 'https://www.e-planetelec.fr/plaque-odace-you/2014-odace-you-transparent-plaque-de'
          '-finition-support-blanc-1-poste-s520902w.html',
          'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2537-product.html',
          'https://www.e-planetelec.fr/plaque-odace-touch/160-plaque-odace-touch-aluminium-martele-1-poste-blanche'
          '-schneider-odace-s520802k.html',
          'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2221-product.html',
          'https://www.e-planetelec.fr/accessoires-ovalis-schneider/3217-ovalis-boite-support-36-mm-pour-montage-en'
          '-saillie-anthracite-s340762.html',
          'https://www.e-planetelec.fr/mecanisme-odace-blanc/1756-odace-prise-de-courant-2pt-affleurante-s520052'
          '-schneider.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/1887-prise-de-courant-2pt-alu-a-vis'
          '-connexion-rapide-speciale-renovation-s530049.html',
          'https://www.e-planetelec.fr/mecanisme-odace-anthracite/1798-odace-prise-de-courant-2pt-anthracite'
          '-affleurante-s540052.html', 'https://www.e-planetelec.fr/plaque-odace-styl/146-plaque-odace-styl-1-poste'
          '-blanche-schneider-odace-s520702.html',
          'https://www.e-planetelec.fr/cadres-et-accessoires/1803-alrea-sachet-de-10-ressorts-pour-transformation'
          '-interrupteur-en-poussoir-alb57944.html',
          'https://www.e-planetelec.fr/enjoliveur-odace/2451-odace-2-demi-enjoliveur-blanc-livre-avec-2-led-bleu-015'
          '-ma-connexion-par-cable-s520298.html',
          'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3176-ovalis-prise-de-courant-a-puits-2pt-16a'
          '-bornes-automatiques-antibacterien-s300059.html',
          'https://www.e-planetelec.fr/plaques-ovalis-schneider/3209-ovalis-plaque-de-finition-2-postes-horizontal'
          '-entraxe-71-mm-antibacterien-s300704.html',
          'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3162-ovalis-interrupteur-va-et-vient-10ax'
          '-antibacterien-s300204.html',
          'https://www.e-planetelec.fr/mecanisme-odace-blanc/109-pc-2pt-blanche-schneider-odace-s520059.html',
          'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2538-product.html',
          'https://www.e-planetelec.fr/plaque-odace-touch/161-plaque-odace-touch-aluminium-martele-2-postes-schneider'
          '-odace-s520804k.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2222-product'
          '.html', 'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2254-product.html',
          'https://www.e-planetelec.fr/appareillage-complet/1849-alrea-va-et-vient-avec-cadre-saillie-blanc-polaire'
          '-alb62051p.html', 'https://www.e-planetelec.fr/cadres-et-accessoires/1833-alrea-kit-voyant-demi-touche'
          '-lampe-a-neon-230v-1-5ma-blanc-polaire-alb61416p.html',
          'https://www.e-planetelec.fr/mecanisme-odace-alu/2590-prise-de-courant-affleurante-2pt-alu-a-vis-connexion'
          '-rapide-s530052.html', 'https://www.e-planetelec.fr/appareillage-composable/1805-alrea-va-et-vient-blanc'
          '-polaire-alb61051p.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2452-odace-blanc-enjoliveur-seul'
          '-va-et-vient-et-poussoir-s520604.html',
          'https://www.e-planetelec.fr/mecanisme-odace-anthracite/347-odace-prise-de-courant-2pt-anthracite-a-vis'
          '-connexion-rapide-s540059.html',
          'https://www.e-planetelec.fr/plaque-odace-styl/151-plaque-odace-styl-2-postes-blanche-schneider-odace'
          '-s520704.html', 'https://www.e-planetelec.fr/plaques-ovalis-schneider/3210-ovalis-plaque-de-finition-3'
          '-postes-horizontal-entraxe-71-mm-antibacterien-s300706.html',
          'https://www.e-planetelec.fr/mecanisme-odace-alu/1706-prise-de-courant-2pt-alu-a-vis-connexion-rapide'
          '-s530059.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3163-ovalis-interrupteur-2'
          '-boutons-pour-volet-roulant-6ax-antibacterien-s300208.html',
          'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2539-product.html',
          'https://www.e-planetelec.fr/plaques-ovalis-schneider/3199-ovalis-plaque-de-finition-1-poste-blanc-s320702'
          '.html', 'https://www.e-planetelec.fr/plaque-odace-touch/162-plaque-odace-touch-aluminium-martele-3-postes'
          '-schneider-odace-s520806k.html',
          'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2223-product.html',
          'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2255-product.html',
          'https://www.e-planetelec.fr/appareillage-complet/1850-alrea-poussoir-o-f-lumineux-faible-conso-avec-cadre'
          '-saillie-blanc-polaire-alb62052p.html',
          'https://www.e-planetelec.fr/cadres-et-accessoires/1834-alrea-kit-voyant-touche-lampe-a-neon-230v-1-5ma'
          '-blanc-polaire-alb61417p.html',
          'https://www.e-planetelec.fr/mecanisme-odace-blanc/1888-pc-2pt-blanche-special-renovation-schneider-odace'
          '-s520049.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/1890-odace-prise-de-courant-2pt'
          '-anthracite-a-vis-connexion-rapide-speciale-renovation-s540049.html',
          'https://www.e-planetelec.fr/appareillage-composable/1806-alrea-poussoir-o-f-lumineux-faible-conso-blanc'
          '-polaire-alb61052p.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2453-odace-blanc-enjoliveur-seul'
          '-double-va-et-vient-double-poussoir-vv-poussoir-s520614.html',
          'https://www.e-planetelec.fr/plaque-odace-styl/152-plaque-odace-styl-3-postes-blanche-schneider-odace'
          '-s520706.html', 'https://www.e-planetelec.fr/plaque-odace-touch/371-plaque-odace-touch-aluminium-martele-4'
          '-postes-schneider-odace-s520808k.html',
          'https://www.e-planetelec.fr/mecanisme-odace-alu/1750-odace-interrupteur-va-et-vient-alu-10a-connexion'
          '-rapide-s530204.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3164-ovalis-double-va-et'
          '-vient-10ax-antibacterien-s300214.html',
          'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2540-product.html',
          'https://www.e-planetelec.fr/plaque-odace-touch/371-plaque-odace-touch-aluminium-martele-4-postes-schneider'
          '-odace-s520808k.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/1750-odace-interrupteur-va-et'
          '-vient-alu-10a-connexion-rapide-s530204.html',
          'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3164-ovalis-double-va-et-vient-10ax-antibacterien'
          '-s300214.html', 'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2540-product.html',
          'https://www.e-planetelec.fr/plaques-ovalis-schneider/3200-ovalis-lot-de-360-plaques-de-finition-de-coloris'
          '-blanc-s320702p.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2224-product'
          '.html', 'https://www.e-planetelec.fr/plaque-odace-styl/264-plaque-odace-styl-3-postes-blanche-schneider'
          '-odace-s520706.html', 'https://www.e-planetelec.fr/appareillage-complet/1851-alrea-poussoir-a-fermeture'
          '-avec-cadre-saillie-blanc-polaire-alb62053p.html',
          'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2258-product.html',
          'https://www.e-planetelec.fr/cadres-et-accessoires/1836-alrea-lampe-neon-de-rechange-pour-commande'
          '-lumineuse-230v-0-5w-alb61422.html',
          'https://www.e-planetelec.fr/plaque-odace-styl/364-odace-styl-plaque-anthracite-1-poste-s540702.html',
          'https://www.e-planetelec.fr/appareillage-composable/1808-alrea-interrupteur-bipolaire-ou-permutateur-blanc'
          '-polaire-alb61054p.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2455-product.html',
          'https://www.e-planetelec.fr/mecanisme-odace-anthracite/350-odace-double-va-et-vient-anthracite-a-vis'
          '-connexion-rapide-s540214.html',
          'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3195-ovalis-prise-tv-simple-antibacterien-s300405'
          '.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/1707-double-va-et-vient-alu-a-vis-connexion'
          '-rapide-s530214.html', 'https://www.e-planetelec.fr/plaque-odace-you/2018-odace-you-transparent-plaque-de'
          '-finition-support-blanc-3-postes-entraxe-71mm-s520906w.html',
          'https://www.e-planetelec.fr/mecanisme-odace-blanc/112-double-va-et-vient-blanc-schneider-odace-s520214'
          '.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1966-odace-touch-plaque-de-finition-1-poste-blanc'
          '-ral9003-s520802.html', 'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2541-product.html',
          'https://www.e-planetelec.fr/plaques-ovalis-schneider/3201-ovalis-plaque-de-finition-2-postes-horizontal'
          '-entraxe-71-mm-blanc-s320704.html',
          'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2225-product.html',
          'https://www.e-planetelec.fr/appareillage-complet/1852-alrea-double-va-et-vient-avec-cadre-saillie-blanc'
          '-polaire-alb62056p.html', 'https://www.e-planetelec.fr/appareillage-complet/1853-alrea-va-et-vient'
          '-lumineux-forte-luminosite-avec-cadre-saillie-blanc-polaire-alb62057p.html',
          'https://www.e-planetelec.fr/cadres-et-accessoires/1837-alrea-lampe-neon-de-rechange-pour-commande'
          '-lumineuse-12v-0-4w-alb61423.html',
          'https://www.e-planetelec.fr/plaque-odace-styl/365-odace-styl-plaque-anthracite-2-postes-horiz-vert-entraxe'
          '-71mm-s540704.html', 'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2262-product.html',
          'https://www.e-planetelec.fr/plaque-odace-touch/1974-odace-touch-plaque-blanc-2-postes-horiz-ou-vert'
          '-entraxe-71mm-s520804.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/349-odace-poussoir'
          '-anthracite-10-a-a-vis-s540206.html',
          'https://www.e-planetelec.fr/appareillage-composable/1809-alrea-double-va-et-vient-blanc-polaire-alb61056p'
          '.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2456-product.html',
          'https://www.e-planetelec.fr/mecanisme-odace-alu/1751-odace-double-poussoir-alu-a-vis-connexion-rapide'
          '-s530216.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3184-ovalis-prise-rj45-cat6-stp'
          '-reseaux-vdi-grade-3-antibacterien-s300476.html',
          'https://www.e-planetelec.fr/mecanisme-odace-blanc/457-permutateur-schneider-odace-s520205.html',
          'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2542-product.html',
          'https://www.e-planetelec.fr/plaques-ovalis-schneider/3202-ovalis-lot-de-180-plaques-2-postes-horizontal'
          '-finition-de-coloris-blanc-s320704p.html',
          'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2226-product.html',
          'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2227-product.html',
          'https://www.e-planetelec.fr/appareillage-complet/1854-alrea-poussoir-avec-porte-etiquette-complet-blanc'
          '-polaire-alb62062p.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3139-ovalis-prise-de'
          '-courant-a-puits-2p-16a-bornes-vis-blanc-s320033.html',
          'https://www.e-planetelec.fr/cadres-et-accessoires/1838-alrea-lampe-neon-de-rechange-pour-commande'
          '-lumineuse-230v-1-5w-alb61424.html',
          'https://www.e-planetelec.fr/plaque-odace-styl/366-odace-styl-plaque-anthracite-3-postes-horiz-vert-entraxe'
          '-71mm-s540706.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/351-odace-double-poussoir'
          '-anthracite-a-vis-connexion-rapide-s540216.html',
          'https://www.e-planetelec.fr/appareillage-composable/1810-alrea-va-et-vient-lumineux-forte-luminosite-blanc'
          '-polaire-alb61057p.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2457-odace-touche-pour-commande'
          '-lumineuse-alu-livree-sans-led-s530297.html',
          'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2267-product.html',
          'https://www.e-planetelec.fr/mecanisme-odace-blanc/111-bouton-poussoir-blanc-schneider-odace-s520206.html',
           'https://www.e-planetelec.fr/plaque-odace-touch/1982-odace-touch-plaque-blanc-3-postes-horiz-ou-vert'
           '-entraxe-71mm-s520806.html', 'https://www.e-planetelec.fr/appareillage-complet/1854-alrea-poussoir-avec'
           '-porte-etiquette-complet-blanc-polaire-alb62062p.html',
           'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3139-ovalis-prise-de-courant-a-puits-2p-16a'
           '-bornes-vis-blanc-s320033.html',
           'https://www.e-planetelec.fr/appareillage-complet/1855-alrea-prise-de-courant-2p-connexion-a-vis-avec'
           '-cadre-saillie-blanc-polaire-alb62270p.html',
           'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3140-ovalis-prise-de-courant-2pt-16a-affleurante'
           '-bornes-automatiques-blanc-s320052.html',
           'https://www.e-planetelec.fr/cadres-et-accessoires/1839-alrea-cadre-saillie-standard-simple-62x62mm'
           '-profondeur-31mm-blanc-polaire-alb61441p.html',
           'https://www.e-planetelec.fr/plaque-odace-styl/367-odace-styl-plaque-anthracite-4-postes-horiz-vert'
           '-entraxe-71mm-s540708.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2146-odace-poussoir'
           '-anthracite-avec-porte-etiquette-a-vis-s540266.html',
           'https://www.e-planetelec.fr/appareillage-composable/1811-alrea-poussoir-a-fermeture-porte-etiquette-sans'
           '-lampe-blanc-polaire-alb61062p.html',
           'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2415-product.html',
           'https://www.e-planetelec.fr/mecanisme-odace-blanc/113-double-bouton-poussoir-blanc-schneider-odace'
           '-s520216.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/1752-odace-prise-rj45-alu-grade-3'
           '-multimedia-cat6-stp-s530476.html',
           'https://www.e-planetelec.fr/plaques-ovalis-schneider/3204-ovalis-plaque-de-finition-4-postes-horizontal'
           '-entraxe-71-mm-blanc-s320708.html',
           'https://www.e-planetelec.fr/plaque-odace-touch/1990-odace-touch-plaque-blanc-4-postes-horiz-ou-vert'
           '-entraxe-71mm-s520808.html',
           'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2228-product.html',
           'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2229-product.html',
           'https://www.e-planetelec.fr/appareillage-complet/1856-alrea-prise-de-courant-2p-t-complet-blanc-polaire'
           '-alb62272p.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3141-ovalis-prise-2pt-16a'
           '-affleurante-bornes-auto-blanc-griffes-montees-s320052c.html',
           'https://www.e-planetelec.fr/cadres-et-accessoires/1840-alrea-cadre-saillie-standard-double-62x124mm'
           '-profondeur-31mm-blanc-polaire-alb61442p.html',
           'https://www.e-planetelec.fr/mecanisme-odace-anthracite/352-odace-va-et-vient-poussoir-anthracite-10-a'
           '-s540285.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2459-product.html',
           'https://www.e-planetelec.fr/appareillage-composable/1812-alrea-poussoir-lumineux-a-ferm-porte-etiquette'
           '-forte-luminosite-blanc-polaire-alb61063p.html',
           'https://www.e-planetelec.fr/mecanisme-odace-blanc/139-va-et-vient-bouton-poussoir-blanc-schneider-odace'
           '.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/1754-odace-obturateur-alu-a-vis-s530666.html',
           'https://www.e-planetelec.fr/plaque-odace-touch/1967-odace-touch-plaque-aluminium-brosse-avec-lisere-blanc'
           '-1-poste-s520802j.html', 'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2420-product.html',
           'https://www.e-planetelec.fr/plaques-ovalis-schneider/3205-ovalis-plaque-de-finition-2-postes-vertical'
           '-entraxe-71-mm-blanc-s320724.html',
           'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2230-product.html',
           'https://www.e-planetelec.fr/appareillage-complet/1857-alrea-prise-de-courant-2p-t-connexion-rapide-cadre'
           '-saillie-blanc-polaire-alb62273p.html',
           'https://www.e-planetelec.fr/plaque-odace-touch/1975-odace-touch-plaque-aluminium-brosse-lisere-blanc-2'
           '-postes-horiz-vert-71mm-s520804j.html',
           'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3142-ovalis-lot-de-108-2pt-affleurantes-16a-blanc'
           '-sans-emballage-unitaire-s320052p.html',
           'https://www.e-planetelec.fr/cadres-et-accessoires/1841-alrea-diffuseur-voyant-de-balisage-rouge-alb61525'
           '.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/1909-odace-prise-alimentation-usb-alu-s530408'
           '.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1915-odace-styl-plaque-gris-1-poste-s520702a1.html'
           '', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/353-odace-poussoir-lumineux-anthracite-10-a-a'
           '-vis-led-bleu-015-ma-localisation-s540276.html',
           'https://www.e-planetelec.fr/enjoliveur-odace/2460-product.html',
           'https://www.e-planetelec.fr/appareillage-composable/1813-alrea-va-et-vient-bouton-poussoir-blanc-polaire'
           '-alb61081p.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/1575-va-et-vient-va-et-vient'
           '-lumineux-blanc-schneider-odace-s520273.html',
           'https://www.e-planetelec.fr/plaques-ovalis-schneider/3206-ovalis-plaque-de-finition-3-postes-vertical'
           '-entraxe-71-mm-blanc-s320726.html',
           'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2231-product.html',
           'https://www.e-planetelec.fr/appareillage-complet/1858-alrea-prise-de-courant-2p-connexion-rapide-avec'
           '-cadre-saillie-blanc-polaire-alb62274p.html',
           'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3143-ovalis-prise-de-courant-a-puits-2pt-16a'
           '-bornes-automatiques-blanc-s320059.html',
           'https://www.e-planetelec.fr/cadres-et-accessoires/1842-alrea-diffuseur-voyant-de-balisage-vert-alb61526'
           '.html', 'https://www.e-planetelec.fr/plaques-ovalis-schneider/3211-ovalis-plaque-de-finition-1-poste'
           '-anthracite-s340702.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1916-odace-styl-plaque-sable-1'
           '-poste-s520702b1.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/354-odace-va-et-vient'
           '-lumineux-anth-10-a-a-vis-led-orange-15-ma-local-ou-temoin-s540263.html',
           'https://www.e-planetelec.fr/enjoliveur-odace/2461-odace-alu-enjoliveur-seul-prise-television-simple'
           '-s530645.html', 'https://www.e-planetelec.fr/appareillage-composable/1814-alrea-double-poussoir-o-f-blanc'
           '-polaire-alb61083p.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1983-odace-touch-plaque'
           '-aluminium-brosse-lisere-blanc-3-postes-horiz-vert-71mm-s520806j.html',
           'https://www.e-planetelec.fr/mecanisme-odace-blanc/141-va-et-vient-lumineux-blanc-schneider-odace-s520263'
           '.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/2342-va-et-vient-bouton-poussoir-alu-schneider'
           '-odace-s530285.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1991-odace-touch-plaque-aluminium'
           '-brosse-lisere-blanc-4-postes-horiz-vert-71mm-s520808j.html',
           'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2232-product.html',
           'https://www.e-planetelec.fr/appareillage-complet/1859-alrea-prise-tv-simple-male-blindee-1-sortie-avec'
           '-cadre-saillie-blanc-polaire-alb62311p.html',
           'https://www.e-planetelec.fr/cadres-et-accessoires/1843-alrea-diffuseur-voyant-de-balisage-orange-alb61527'
           '.html', 'https://www.e-planetelec.fr/plaques-ovalis-schneider/3212-ovalis-plaque-de-finition-2-postes'
           '-horizontal-entraxe-71-mm-anthracite-s340704.html',
           'https://www.e-planetelec.fr/plaque-odace-styl/1917-odace-styl-plaque-bleu-cian-1-poste-s520702c.html',
           'https://www.e-planetelec.fr/enjoliveur-odace/2462-product.html',
           'https://www.e-planetelec.fr/appareillage-composable/1815-alrea-commande-vmc-sans-position-arret-blanc'
           '-polaire-alb61158p.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/140-bouton-poussoir-lumineux'
           '-blanc-schneider-odace-s520276.html',
           'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3218-ovalis-lot-de-108-2pt-a-puits-16a-blanc-sans'
           '-emballage-unitaire-s320059p.html',
           'https://www.e-planetelec.fr/mecanisme-odace-alu/2343-bouton-poussoir-alu-schneider-odace-s530206.html',
           'https://www.e-planetelec.fr/mecanisme-odace-blanc/1901-poussoir-blanc-avec-symbole-carillon-schneider'
           '-odace-s520246.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2233-product'
           '.html', 'https://www.e-planetelec.fr/appareillage-complet/1860-alrea-rj45-simple-categorie-6-utp-avec'
           '-cadre-saillie-blanc-polaire-alb62342p.html',
           'https://www.e-planetelec.fr/cadres-et-accessoires/1844-alrea-diffuseur-voyant-de-balisage-incolore'
           '-alb61528.html', 'https://www.e-planetelec.fr/plaques-ovalis-schneider/3213-ovalis-plaque-de-finition-3'
           '-postes-horizontal-entraxe-71-mm-anthracite-s340706.html',
           'https://www.e-planetelec.fr/plaque-odace-styl/1918-odace-styl-plaque-violine-1-poste-s520702d.html',
           'https://www.e-planetelec.fr/appareillage-composable/1816-alrea-interrupteur-volets-roulants-blanc-polaire'
           '-alb61197p.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3152-ovalis-combi-2pt-16a'
           '-affleurantechargeur-usb-c-105w-connex-auto-blanc-s320089.html',
           'https://www.e-planetelec.fr/plaque-odace-touch/1969-odace-touch-plaque-bronze-brosse-avec-lisere-blanc-1'
           '-poste-s520802l.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/2615-interrupteur-volets-roulants'
           '-odace-alu-s530208-schneider-electric.html',
           'https://www.e-planetelec.fr/mecanisme-odace-alu/3059-conjoncteur-en-t-alu-8-contacts-a-vis-odace-s530496'
           '.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1977-odace-touch-plaque-bronze-brosse-lisere'
           '-blanc-2-postes-horiz-vert-71mm-s520804l.html',
           'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3128-ovalis-interrupteur-va-et-vient-10ax-blanc'
           '-s320204.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2147-odace-poussoir-anthracite'
           '-10a-a-fermeture-symbole-carillon-s540246.html',
           'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2234-product.html',
           'https://www.e-planetelec.fr/appareillage-complet/1861-alrea-conjoncteur-telephonique-8-plots-avec-cadre'
           '-saillie-blanc-polaire-alb62366p.html',
           'https://www.e-planetelec.fr/cadres-et-accessoires/1845-alrea-lampe-e10-pour-voyant-de-balisage-12v-4w'
           '-incandescent-transp-alb61530.html',
           'https://www.e-planetelec.fr/plaques-ovalis-schneider/3214-ovalis-plaque-de-finition-4-postes-horizontal'
           '-entraxe-71-mm-anthracite-s340708.html',
           'https://www.e-planetelec.fr/plaque-odace-styl/1919-odace-styl-plaque-alu-1-poste-s520702e.html',
           'https://www.e-planetelec.fr/enjoliveur-odace/2464-odace-enjoliveur-anthracite-livre-sans-led-s540297.html'
           '', 'https://www.e-planetelec.fr/appareillage-composable/1817-alrea-poussoir-volets-roulants-blanc-polaire'
           '-alb61199p.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/1576-poussoir-porte-etiquette-blanc'
           '-schneider-odace-s520266.html',
           'https://www.e-planetelec.fr/mecanisme-odace-alu/3060-sortie-de-cable-20a-alu-schneider-odace-s530662.html'
           '', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/2524-variateur-de-lumiere-universel-en-2-ou-3-fils'
           '-3w-100wled-s520519.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3129-ovalis-lot-de'
           '-108-va-et-vient-10ax-blanc-sans-emballage-unitaire-s320204p.html',
           'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2235-product.html',
           'https://www.e-planetelec.fr/appareillage-complet/1862-alrea-obturateur-avec-cadre-saillie-blanc-polaire'
           '-alb62420p.html', 'https://www.e-planetelec.fr/cadres-et-accessoires/1846-alrea-lampe-e10-pour-voyant-de'
           '-balisage-24v-4w-incandescent-transp-alb61531.html',
           'https://www.e-planetelec.fr/plaques-ovalis-schneider/3215-ovalis-plaque-de-finition-2-postes-vertical'
           '-entraxe-71-mm-anthracite-s340724.html',
           'https://www.e-planetelec.fr/plaque-odace-styl/1920-odace-styl-plaque-ambre-1-poste-s520702g.html',
           'https://www.e-planetelec.fr/plaque-odace-touch/1985-odace-touch-plaque-bronze-brosse-lisere-blanc-3'
           '-postes-horiz-vert-71mm-s520806l.html',
           'https://www.e-planetelec.fr/enjoliveur-odace/2465-odace-2-demi-enjoliveur-anthracite-livre-sans-led'
           '-s540298.html', 'https://www.e-planetelec.fr/appareillage-composable/1818-alrea-prise-de-courant-2p'
           '-connexion-a-vis-blanc-polaire-alb61270p.html',
           'https://www.e-planetelec.fr/plaque-odace-touch/1993-odace-touch-plaque-bronze-brosse-lisere-blanc-4'
           '-postes-horiz-vert-71mm-s520808l.html',
           'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3130-ovalis-bouton-poussoir-a-fermeture-10a-blanc'
           '-s320206.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2236-product.html',
           'https://www.e-planetelec.fr/appareillage-complet/1863-alrea-double-prise-de-courant-2p-t-connexion-a-vis'
           '-avec-cadre-saillie-blanc-p-alb62472p.html',
           'https://www.e-planetelec.fr/cadres-et-accessoires/1847-alrea-lampe-e10-pour-voyant-de-balisage-240v-0-75w'
           '-incandescent-transp-alb61532.html',
           'https://www.e-planetelec.fr/plaques-ovalis-schneider/3216-ovalis-plaque-de-finition-3-postes-vertical'
           '-entraxe-71-mm-anthracite-s340726.html',
           'https://www.e-planetelec.fr/mecanisme-odace-anthracite/358-odace-interrupteur-vmc-anthracite-sans'
           '-position-arret-a-vis-s540233.html',
           'https://www.e-planetelec.fr/plaque-odace-styl/1921-odace-styl-plaque-vert-chartreuse-1-poste-s520702h'
           '.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2466-product.html',
           'https://www.e-planetelec.fr/appareillage-composable/1819-alrea-prise-de-courant-2p-t-connexion-a-vis'
           '-blanc-polaire-alb61272p.html', 'https://www.e-planetelec.fr/plaques-ovalis-schneider/2263-product.html',
            'https://www.e-planetelec.fr/mecanisme-odace-blanc/158-detecteur-de-presence-blanc-schneider-odace'
            '-s520524.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/370-interrupteur-volet-roulant'
            '-anthracite-montee-descente-stop-s540208.html',
            'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3131-ovalis-interrupteur-2-boutons-pour-volet'
            '-roulant-6ax-blanc-s320208.html',
            'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2237-product.html',
            'https://www.e-planetelec.fr/appareillage-complet/1864-alrea-double-prise-de-courant-2p-t-connexion'
            '-rapide-avec-cadre-saillie-blanc-p-alb62473p.html',
            'https://www.e-planetelec.fr/plaque-odace-styl/1922-odace-styl-plaque-gris-2-postes-horizontaux-ou'
            '-verticaux-entraxe-71mm-s520704a1.html',
            'https://www.e-planetelec.fr/enjoliveur-odace/2467-product.html',
            'https://www.e-planetelec.fr/plaque-odace-touch/1970-odace-touch-plaque-bois-nordique-avec-lisere-blanc-1'
            '-poste-s520802m.html', 'https://www.e-planetelec.fr/appareillage-composable/1820-alrea-prise-de-courant'
            '-2p-t-connexion-rapide-blanc-polaire-alb61273p.html',
            'https://www.e-planetelec.fr/mecanisme-odace-blanc/150-commande-de-vmc-sans-position-arret-blanc'
            '-schneider-odace-s520233.html',
            'https://www.e-planetelec.fr/plaques-ovalis-schneider/2264-product.html',
            'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2145-odace-interrupteur-vmc-anthracite-avec'
            '-position-arret-s540243.html',
            'https://www.e-planetelec.fr/plaque-odace-touch/1978-odace-touch-plaque-bois-nordique-lisere-blanc-2'
            '-postes-horiz-vert-71mm-s520804m.html',
            'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3132-ovalis-double-va-et-vient-10ax-blanc'
            '-s320214.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2238-product.html',
            'https://www.e-planetelec.fr/plaque-odace-styl/1923-odace-styl-plaque-sable-2-postes-horizontaux-ou'
            '-verticaux-entraxe-71mm-s520704b1.html',
            'https://www.e-planetelec.fr/enjoliveur-odace/2468-odace-anthracite-enjoliveur-seul-prise-television'
            '-simple-s540645.html', 'https://www.e-planetelec.fr/appareillage-composable/1821-alrea-prise-de-courant'
            '-2p-connexion-rapide-blanc-polaire-alb61274p.html',
            'https://www.e-planetelec.fr/appareillage-composable/1822-alrea-prise-tv-simple-male-blindee-1-sortie'
            '-blanc-polaire-alb61311p.html',
            'https://www.e-planetelec.fr/plaques-ovalis-schneider/2265-product.html',
            'https://www.e-planetelec.fr/mecanisme-odace-blanc/159-commande-de-volets-roulants-blanc-schneider-odace'
            '-s520208.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/356-odace-prise-tv-anthracite-a'
            '-vis-s540445.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3133-ovalis-lot-de-108'
            '-double-va-et-vient-10ax-blanc-sans-emballage-unitaire-s320214p.html',
            'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2239-product.html',
            'https://www.e-planetelec.fr/plaque-odace-touch/1986-odace-touch-plaque-bois-nordique-lisere-blanc-3'
            '-postes-horiz-vert-71mm-s520806m.html',
            'https://www.e-planetelec.fr/plaque-odace-styl/1924-odace-styl-plaque-bleu-cian-2-postes-horizontaux-ou'
            '-verticaux-entraxe-71mm-s520704c.html',
            'https://www.e-planetelec.fr/enjoliveur-odace/2469-product.html',
            'https://www.e-planetelec.fr/appareillage-composable/1823-alrea-embase-enjoliveur-prise-sat-type-f-500ma'
            '-telealim-blanc-polaire-alb61312p.html',
            'https://www.e-planetelec.fr/plaque-odace-touch/1994-odace-touch-plaque-bois-nordique-lisere-blanc-4'
            '-postes-horiz-vert-71mm-s520808m.html',
            'https://www.e-planetelec.fr/plaques-ovalis-schneider/2266-product.html',
            'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2218-mecanisme-odace-anthracite-prise-sat'
            '-schneider-odace-s420446.html',
            'https://www.e-planetelec.fr/mecanisme-odace-blanc/1878-poussoir-pour-volets-roulants-blanc-schneider'
            '-odace-s520207.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3134-ovalis-double'
            '-poussoir-fermeture-10ax-blanc-s320216.html',
            'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2240-product.html',
            'https://www.e-planetelec.fr/plaque-odace-styl/1925-odace-styl-plaque-violine-2-postes-horizontaux-ou'
            '-verticaux-entraxe-71mm-s520704d.html',
            'https://www.e-planetelec.fr/enjoliveur-odace/2470-product.html',
            'https://www.e-planetelec.fr/appareillage-composable/1824-alrea-prise-tv-fm-vr-sur-fm-blanc-polaire'
            '-alb61317p.html', 'https://www.e-planetelec.fr/plaques-ovalis-schneider/2299-product.html',
            'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3135-ovalis-poussoir-vmc-sans-arret-blanc'
            '-s320236.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2241-product.html',
            'https://www.e-planetelec.fr/mecanisme-odace-blanc/145-prise-rj-45-telephone-grade-1-blanc-schneider'
            '-odace-s520471.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1971-odace-touch-plaque-bois'
            '-naturel-avec-lisere-blanc-1-poste-s520802n.html',
            'https://www.e-planetelec.fr/mecanisme-odace-anthracite/1893-prise-conjoncteur-en-t-anthracite-schneider'
            '-odace-s540496.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1926-odace-styl-plaque-alu-2-postes'
            '-horiz-vert-entraxe-71mm-s520704e.html',
            'https://www.e-planetelec.fr/plaque-odace-styl/1927-odace-styl-plaque-ambre-2-postes-horizontaux-ou'
            '-verticaux-entraxe-71mm-s520704g.html',
            'https://www.e-planetelec.fr/mecanisme-odace-anthracite/368-odace-prise-rj45-anthracite-grade-1-telephone'
            '-cat-5-utp-a-vis-s540471.html',
            'https://www.e-planetelec.fr/appareillage-composable/1825-alrea-prise-tv-fm-sat500ma-3-ressorts-blanc'
            '-polaire-alb61322p.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1979-odace-touch-plaque-bois'
            '-naturel-lisere-blanc-2-postes-horiz-vert-71mm-s520804n.html',
            'https://www.e-planetelec.fr/plaques-ovalis-schneider/2416-product.html',
            'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3219-ovalis-interrupteur-va-et-vient-10ax'
            '-lumineux-ou-temoin-blanc-s320263.html',
            'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2242-product.html',
            'https://www.e-planetelec.fr/mecanisme-odace-blanc/147-prise-rj-45-telephone-informatique-grade-1-blanc'
            '-schneider-odace-s520475.html',
            'https://www.e-planetelec.fr/mecanisme-odace-blanc/1653-odace-prise-rj45-blanc-grade-3-multimedia-cat-6'
            '-stp-schneider-odace-s520476.html',
            'https://www.e-planetelec.fr/plaque-odace-styl/1928-odace-styl-plaque-vert-chartreuse-2-postes-horiz-ou'
            '-verticaux-entraxe-71mm-s520704h.html',
            'https://www.e-planetelec.fr/mecanisme-odace-anthracite/369-odace-prise-rj45-anth-grade-1-telephone'
            '-informatique-cat-6-utpa-vis-s540475.html',
            'https://www.e-planetelec.fr/appareillage-composable/1826-alrea-prise-tv-fm-deriv-vr-sur-tv-2-sorties'
            '-blanc-polaire-alb61324p.html',
            'https://www.e-planetelec.fr/plaques-ovalis-schneider/2417-product.html',
            'https://www.e-planetelec.fr/plaque-odace-touch/1987-odace-touch-plaque-bois-naturel-lisere-blanc-3'
            '-postes-horiz-vert-71mm-s520806n.html',
            'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3136-ovalis-poussoir-a-fermeture-avec-porte'
            '-etiquette-10ax-blanc-s320266.html',
            'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2243-product.html',
            'https://www.e-planetelec.fr/plaque-odace-styl/1929-odace-styl-plaque-gris-3-postes-horizontaux-ou'
            '-verticaux-entraxe-71mm-s520706a1.html',
            'https://www.e-planetelec.fr/mecanisme-odace-anthracite/1705-prise-rj45-anth-grade-2-ou-3-suivant-cablage'
            '-s540476.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1995-odace-touch-plaque-bois-naturel'
            '-lisere-blanc-4-postes-horiz-vert-71mm-s520808n.html',
            'https://www.e-planetelec.fr/appareillage-composable/1827-alrea-prise-tv-radio-1-entree-hertz-sat-3'
            '-sorties-tv-fm-sat-blanc-polaire-alb61329p.html',
            'https://www.e-planetelec.fr/plaques-ovalis-schneider/2418-product.html',
            'https://www.e-planetelec.fr/mecanisme-odace-blanc/1802-prise-rj-45-grade-3-blanc-schneider-odace-s520477'
            '.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3137-ovalis-poussoir-a-fermeture'
            '-lumineux-10ax-led-bleu-250v-blanc-s320276.html',
            'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2244-product.html',
            'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2245-product.html',
            'https://www.e-planetelec.fr/mecanisme-odace-blanc/2134-odace-prise-double-rj45-blanc-grade-3-multimedia'
            '-cat-6-stp-a-vis-s520486.html',
            'https://www.e-planetelec.fr/plaque-odace-styl/1930-odace-styl-plaque-sable-3-postes-horizontaux-ou'
            '-verticaux-entraxe-71mm-s520706b1.html',
            'https://www.e-planetelec.fr/appareillage-composable/1828-alrea-prise-rj45-simple-cat-6-utp-non-blindee'
            '-mecanisme-blanc-polaire-alb61342p.html',
            'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2169-odace-prise-usb-double-charge-rapide-type-ac'
            '-anthracite-18w-34a-s540219.html',
            'https://www.e-planetelec.fr/plaques-ovalis-schneider/2419-product.html',
            'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3138-ovalis-combine-va-et-vientpoussoir-10ax'
            '-blanc-s320285.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1972-odace-touch-plaque'
            '-translucide-blanc-1-poste-s520802r.html',
            'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2246-product.html',
            'https://www.e-planetelec.fr/plaque-odace-styl/1931-odace-styl-plaque-bleu-cian-3-postes-horizontaux-ou'
            '-verticaux-entraxe-71mm-s520706c.html',
            'https://www.e-planetelec.fr/plaque-odace-touch/1980-odace-touch-plaque-translucide-blanc-2-postes-horiz'
            '-vert-entraxe-71mm-s520804r.html',
            'https://www.e-planetelec.fr/appareillage-composable/1829-alrea-prise-rj45-simple-cat-5-utp-non-blindee'
            '-mecanisme-blanc-polaire-alb61343p.html',
            'https://www.e-planetelec.fr/mecanisme-odace-anthracite/360-odace-prise-alimentation-usb-5v-anthracite'
            '-s540408.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/541-prise-conjoncteur-en-t-schneider'
            '-odace-s520496.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3153-ovalis-double'
            '-chargeur-usb-ac-12w-blanc-s320401.html',
            'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2247-product.html',
            'https://www.e-planetelec.fr/plaque-odace-styl/1932-odace-styl-plaque-violine-3-postes-horizontaux-ou'
            '-verticaux-entraxe-71mm-s520706d.html',
            'https://www.e-planetelec.fr/appareillage-composable/1830-alrea-rj45-categorie-6-stp-blanc-polaire'
            '-alb61348p.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/143-prise-tv-blanc-schneider-odace'
            '-s520445.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/362-odace-prise-haut-parleur-1'
            '-sortie-anthracite-s540487.html',
            'https://www.e-planetelec.fr/plaque-odace-touch/1988-odace-touch-plaque-translucide-blanc-3-postes-horiz'
            '-vert-entraxe-71mm-s520806r.html',
            'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3154-ovalis-chargeur-usb-type-a-75w-c-45w-forte'
            '-puissance-type-c-blanc-s320403.html',
            'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3159-ovalis-prise-tv-simple-blanc-s320405.html',
             'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2248-product.html',
             'https://www.e-planetelec.fr/plaque-odace-touch/1996-odace-touch-plaque-translucide-blanc-4-postes-horiz'
             '-vert-entraxe-71mm-s520808r.html',
             'https://www.e-planetelec.fr/plaque-odace-styl/1933-odace-styl-plaque-alu-3-postes-horiz-vert-entraxe'
             '-71mm-s520706e.html', 'https://www.e-planetelec.fr/appareillage-composable/1831-alrea-conjoncteur'
             '-telephonique-8-plots-blanc-polaire-alb61366p.html',
             'https://www.e-planetelec.fr/mecanisme-odace-blanc/1889-prise-sat-a-vis-blanc-schneider-odace-s520446'
             '.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/363-odace-prise-haut-parleurs'
             '-anthracite-2-sorties-s540488.html',
             'https://www.e-planetelec.fr/plaque-odace-touch/1973-odace-touch-plaque-pierre-galet-1-poste-s520802u'
             '.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/1704-prise-tvfmsat-schneider-odace-s520460'
             '.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2249-product.html',
             'https://www.e-planetelec.fr/plaque-odace-styl/1934-odace-styl-plaque-ambre-3-postes-horizontaux-ou'
             '-verticaux-entraxe-71mm-s520706g.html',
             'https://www.e-planetelec.fr/mecanisme-odace-anthracite/357-odace-sortie-de-cable-anthracite-6-a-12-mm2'
             '-s540662.html', 'https://www.e-planetelec.fr/appareillage-composable/1832-alrea-prise-haut-parleur-1'
             '-sortie-blanc-ral9003-2-bornes-a-ressorts-alb61387p.html',
             'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3155-ovalis-chargeur-usb-c-65w-forte-puissance'
             '-pour-charge-app-mobiles-blanc-s320406.html',
             'https://www.e-planetelec.fr/mecanisme-odace-blanc/149-sortie-de-cable-20a-blanc-schneider-odace-s520662'
             '.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2250-product.html',
             'https://www.e-planetelec.fr/plaque-odace-touch/1981-odace-touch-plaque-pierre-galet-2-postes-horiz-vert'
             '-entraxe-71mm-s520804u.html',
             'https://www.e-planetelec.fr/mecanisme-odace-anthracite/361-odace-obturateur-anthracite-a-vis-s540666'
             '.html', 'https://www.e-planetelec.fr/appareillage-composable/1835-alrea-obturateur-blanc-polaire'
             '-alb61420p.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3156-ovalis-double-chargeur'
             '-usb-aa-105w-blanc-s320407.html',
             'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3160-ovalis-prise-tvr-blanc-s320451.html',
             'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2251-product.html',
             'https://www.e-planetelec.fr/plaque-odace-styl/1936-odace-styl-plaque-gris-4-postes-horizontaux-ou'
             '-verticaux-entraxe-71mm-s520708a1.html',
             'https://www.e-planetelec.fr/mecanisme-odace-blanc/256-obturateur-blanc-schneider-odace-s520666.html',
             'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2449-odace-permutateur-s540205.html',
             'https://www.e-planetelec.fr/plaque-odace-touch/1989-odace-touch-plaque-pierre-galet-3-postes-horiz-vert'
             '-entraxe-71mm-s520806u.html',
             'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3161-ovalis-prise-tvrsat-blanc-s320461.html',
             'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2529-variateur-de-lumiere-universel-en-2-ou-3'
             '-fils-3w-100wled-anthracite-s540519.html',
             'https://www.e-planetelec.fr/plaque-odace-touch/1997-odace-touch-plaque-pierre-galet-4-postes-horiz-vert'
             '-entraxe-71mm-s520808u.html',
             'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2252-product.html',
             'https://www.e-planetelec.fr/plaque-odace-styl/1937-odace-styl-plaque-sable-4-postes-horizontaux-ou'
             '-verticaux-entraxe-71mm-s520708b1.html',
             'https://www.e-planetelec.fr/mecanisme-odace-blanc/255-prise-alim-usb-5v-schneider-odace-s520408.html',
             'https://www.e-planetelec.fr/mecanisme-odace-blanc/1615-s520407-odace-double-chargeur-usb-21-a-blanc'
             '-schneider-electric.html',
             'https://www.e-planetelec.fr/plaque-odace-touch/1998-odace-touch-plaque-blanc-2-postes-verticaux-57mm'
             '-s520814.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3148-ovalis-prise-rj45-cat6'
             '-stp-reseaux-vdi-grade-3-blanc-s320476.html',
             'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2253-product.html',
             'https://www.e-planetelec.fr/plaque-odace-styl/1938-odace-styl-plaque-bleu-cian-4-postes-horizontaux-ou'
             '-verticaux-entraxe-71mm-s520708c.html',
             'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3149-ovalis-lot-de-108-rj45-cat6-stp-blanc-sans'
             '-emballage-unitaire-s320476p.html',
             'https://www.e-planetelec.fr/mecanisme-odace-blanc/2324-odace-prise-usb-double-charge-rapide-type-ac'
             '-blanc-18w-34a-s520219.html',
             'https://www.e-planetelec.fr/plaque-odace-styl/1939-odace-styl-plaque-violine-4-postes-horizontaux-ou'
             '-verticaux-entraxe-71mm-s520708d.html',
             'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2256-product.html',
             'https://www.e-planetelec.fr/plaque-odace-touch/1999-odace-touch-plaque-aluminium-brosse-avec-lisere'
             '-blanc-2-postes-verticaux-57mm-s520814j.html',
             'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3150-ovalis-prise-rj45-cat6a-grade-3-multimedia'
             '-longue-distance-blanc-s320477.html',
             'https://www.e-planetelec.fr/mecanisme-odace-blanc/444-prise-hdmi-schneider-odace-s520462.html',
             'https://www.e-planetelec.fr/plaque-odace-styl/1940-odace-styl-plaque-alu-4-postes-horiz-vert-entraxe'
             '-71mm-s520708e.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2257-product'
             '.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3151-ovalis-prise-haut-parleur-2'
             '-sorties-blanc-s320488.html',
             'https://www.e-planetelec.fr/plaque-odace-styl/1941-odace-styl-plaque-ambre-4-postes-horizontaux-ou'
             '-verticaux-entraxe-71mm-s520708g.html',
             'https://www.e-planetelec.fr/plaque-odace-touch/2007-odace-touch-plaque-aluminium-brosse-avec-lisere'
             '-blanc-3-postes-verticaux-57mm-s520816j.html',
             'https://www.e-planetelec.fr/mecanisme-odace-blanc/289-prise-hp-1-sortie-schneider-odace-s520487.html',
             'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2259-product.html',
             'https://www.e-planetelec.fr/plaque-odace-touch/2000-odace-touch-plaque-aluminium-martele-avec-lisere'
             '-blanc-2-postes-verticaux-57mm-s520814k.html',
             'https://www.e-planetelec.fr/plaque-odace-styl/1942-odace-styl-plaque-vert-chartreuse-4-postes-horiz-ou'
             '-verticaux-entraxe-71mm-s520708h.html',
             'https://www.e-planetelec.fr/mecanisme-odace-blanc/290-prise-hp-2-sorties-schneider-odace-s520488.html',
              'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2260-product.html',
              'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2300-product.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/378-boite-pour-montage-saillie-blanc-1-poste'
              '-schneider-odace-styl-s520762.html',
              'https://www.e-planetelec.fr/plaque-odace-touch/2008-odace-touch-plaque-aluminium-martele-avec-lisere'
              '-blanc-3-postes-verticaux-57mm-s520816k.html',
              'https://www.e-planetelec.fr/plaque-odace-styl/1943-odace-styl-pratic-plaque-blanc-support-telephone'
              '-mobile-1-poste-s520712.html',
              'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3158-ovalis-detecteur-de-presence-et-de'
              '-mouvement-toutes-charges-3-fils-blanc-s320523.html',
              'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3145-ovalis-sortie-de-cable-universelle-1620a'
              '-ip24d-blanc-s320644.html',
              'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2301-product.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/379-boite-pour-montage-saillie-blanc-2-postes'
              '-schneider-odace-styl-s520764.html',
              'https://www.e-planetelec.fr/plaque-odace-touch/2001-odace-touch-plaque-bronze-brosse-avec-lisere-blanc'
              '-2-postes-verticaux-57mm-s520814l.html',
              'https://www.e-planetelec.fr/plaque-odace-styl/1944-odace-styl-plaque-blanc-2-postes-verticaux-entraxe'
              '-57mm-s520714.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3146-ovalis-sortie-de'
              '-cable-16a-612mm-blanc-s320662.html',
              'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2302-product.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/422-ressorts-odace-sachets-10-pieces-schneider-odace'
              '-s520299.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2009-odace-touch-plaque-bronze-brosse'
              '-avec-lisere-blanc-3-postes-verticaux-57mm-s520816l.html',
              'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3147-ovalis-obturateur-blanc-s320666.html',
              'https://www.e-planetelec.fr/2303-product.html',
              'https://www.e-planetelec.fr/plaque-odace-touch/2002-odace-touch-plaque-bois-nordique-avec-lisere-blanc'
              '-2-postes-verticaux-57mm-s520814m.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/551-sachet-de-10-griffes-standard-schneider-odace'
              '-s520690.html', 'https://www.e-planetelec.fr/2304-product.html',
              'https://www.e-planetelec.fr/plaque-odace-touch/2010-odace-touch-plaque-bois-nordique-avec-lisere-blanc'
              '-3-postes-verticaux-57mm-s520816m.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/1904-voyant-led-bleu-a-clipser-schneider-odace'
              '-s520292.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3177-ovalis-prise-de-courant'
              '-a-puits-2p-16a-bornes-vis-anthracite-s340033.html',
              'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3178-ovalis-prise-de-courant-2pt-16a'
              '-affleurante-bornes-auto-anthracite-s340052.html',
              'https://www.e-planetelec.fr/plaque-odace-touch/2003-odace-touch-plaque-bois-naturel-avec-lisere-blanc'
              '-2-postes-verticaux-57mm-s520814n.html', 'https://www.e-planetelec.fr/2305-product.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/1905-enjoliveur-blanc-1-led-bleu-15ma-schneider'
              '-odace-s520297.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/157-voyant-led-orange'
              '-schneider-odace-s520290.html',
              'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3179-ovalis-prise-2pt-16a-affleurante-bornes'
              '-auto-anthracite-griffes-montees-s340052c.html', 'https://www.e-planetelec.fr/2306-product.html',
              'https://www.e-planetelec.fr/plaque-odace-styl/1949-odace-styl-plaque-alu-2-postes-verticaux-entraxe'
              '-57mm-s520714e.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2011-odace-touch-plaque-bois'
              '-naturel-avec-lisere-blanc-3-postes-verticaux-57mm-s520816n.html',
              'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3180-ovalis-prise-de-courant-a-puits-2pt-16a'
              '-bornes-automatiques-anthracite-s340059.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/283-voyant-led-bleu-schneider-odace-s520291.html',
              'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2307-product.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/2344-variateur-universel-a-poussoir-plus-link-blanc'
              '-schneider-odace-s520560.html',
              'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2308-product.html',
              'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3188-ovalis-combi-2pt-16a-affleurantechargeur'
              '-usb-c-105w-connex-auto-anth-s340089.html',
              'https://www.e-planetelec.fr/plaque-odace-touch/2012-odace-touch-plaque-translucide-blanc-3-postes'
              '-verticaux-entraxe-57mm-s520816r.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/2499-prise-tvfm-schneider-odace-s520451.html',
              'https://www.e-planetelec.fr/plaque-odace-styl/1952-odace-styl-plaque-blanc-3-postes-verticaux-entraxe'
              '-57mm-s520716.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3165-ovalis-interrupteur'
              '-va-et-vient-10ax-anthracite-s340204.html',
              'https://www.e-planetelec.fr/plaque-odace-touch/2005-odace-touch-plaque-pierre-galet-2-postes-verticaux'
              '-entraxe-57mm-s520814u.html',
              'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2309-product.html',
              'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2310-product.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/2500-prise-2p-a-vis-blanc-schneider-odace-s520033'
              '.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2013-odace-touch-plaque-pierre-galet-3-postes'
              '-verticaux-entraxe-57mm-s520816u.html',
              'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3166-ovalis-bouton-poussoir-a-fermeture-10a'
              '-anthracite-s340206.html',
              'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2311-product.html',
              'https://www.e-planetelec.fr/mecanisme-odace-blanc/2501-ronfleur-blanc-230v-a-vis-schneider-odace'
              '-s520685.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2030-odace-touch-plaque-de-finition-1'
              '-poste-alu-s530802.html',
              'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3167-ovalis-interrupteur-2-boutons-pour-volet'
              '-roulant-6ax-anthracite-s340208.html',
              'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2312-product.html',
              'https://www.e-planetelec.fr/plaque-odace-touch/2031-odace-touch-plaque-aluminium-brosse-avec-lisere'
              '-alu-1-poste-s530802j.html',
              'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3168-ovalis-double-va-et-vient-10ax-anthracite'
              '-s340214.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2313-product.html',
               'https://www.e-planetelec.fr/mecanisme-odace-blanc/2531-detecteur-de-presence-et-de-mouvement-blanc'
               '-toutes-charges-schneider-odace-s520523.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2032-odace-touch-plaque-aluminium-brosse-croco-avec'
               '-lisere-alu-1-poste-s530802j1.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3169-ovalis-double-poussoir-fermeture-10ax'
               '-anthracite-s340216.html',
               'https://www.e-planetelec.fr/plaque-odace-styl/1957-odace-styl-plaque-alu-3-postes-verticaux-entraxe'
               '-57mm-s520716e.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2314-product'
               '.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2033-odace-touch-plaque-aluminium-brillantt'
               '-fume-avec-lisere-alu-1-poste-s530802k1.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3170-ovalis-poussoir-vmc-sans-arret'
               '-anthracite-s340236.html',
               'https://www.e-planetelec.fr/mecanisme-odace-blanc/3041-odace-prise-de-courant-affleurante-usb-type-c'
               '-s520089-schneider.html',
               'https://www.e-planetelec.fr/mecanisme-odace-blanc/3042-odace-prise-usb-double-type-ac-s520401'
               '-schneider.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2315-product'
               '.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2034-odace-touch-plaque-wenge-avec-lisere-alu'
               '-1-poste-s530802p.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3171-ovalis-interrupteur-va-et-vient-10ax'
               '-lumineux-ou-temoin-anthracite-s340263.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2316-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2035-odace-touch-plaque-chene-astrakan-avec-lisere-alu'
               '-1-poste-s530802p1.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3172-ovalis-poussoir-a-fermeture-avec-porte'
               '-etiquette-10ax-anthracite-s340266.html',
               'https://www.e-planetelec.fr/plaque-odace-styl/1960-odace-styl-pratic-plaque-blanc-avec-crochet-multi'
               '-usage-1-poste-s520722.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2317-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2036-odace-touch-plaque-translucide-verre-avec-lisere'
               '-alu-1-poste-s530802s.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3173-ovalis-poussoir-a-fermeture-lumineux'
               '-10ax-led-bleu-250v-anthracite-s340276.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3174-ovalis-combine-va-et-vientpoussoir-10ax'
               '-anthracite-s340285.html',
               'https://www.e-planetelec.fr/plaque-odace-styl/1961-odace-styl-pratic-plaque-blanc-avec-porte'
               '-etiquette-1-poste-s520732.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2318-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2037-odace-touch-plaque-ardoise-avec-lisere-alu-1'
               '-poste-s530802v.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1962-odace-styl-pratic-plaque'
               '-blanc-porte-etiquette-avec-bloc-lumineux-1-poste-s520739.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2319-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2038-odace-touch-plaque-alu-2-postes-horiz-ou-vert'
               '-entraxe-71mm-s530804.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3189-ovalis-double-chargeur-usb-ac-12w'
               '-anthracite-s340401.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3190-ovalis-chargeur-usb-type-a-75w-c-45w'
               '-forte-puissance-type-c-anthracite-s340403.html',
               'https://www.e-planetelec.fr/plaque-odace-styl/1963-odace-styl-pratic-plaque-blanc-avec-pince-multi'
               '-usage-1-poste-s520742.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2581-ovalis-variateur-de-lumiere'
               '-universel-23-fils-3w-blanc-avec-plaque-s260519.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2039-odace-touch-plaque-aluminium-brosse-lisere-alu-2'
               '-post-horiz-vert-71mm-s530804j.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2358-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2040-odace-touch-plaque-aluminium-brosse-croco-avec'
               '-lisere-alu-2-postes-entraxe-71mm-s530804j1.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3196-ovalis-prise-tv-simple-anthracite'
               '-s340405.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1964-odace-styl-pratic-plaque-blanc'
               '-avec-couvercle-integre-pour-prise-1-poste-s520752.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2359-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2041-odace-touch-plaque-aluminium-brillant-fume-avec'
               '-lisere-alu-2postes-entraxe-71mm-s530804k1.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3191-ovalis-chargeur-usb-c-65w-forte'
               '-puissance-pour-charge-app-mobiles-anth-s340406.html',
               'https://www.e-planetelec.fr/plaque-odace-styl/1965-odace-styl-pratic-plaque-blanc-avec-couvercle'
               '-souple-translucide-1-poste-ip44-s520772.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2360-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2042-odace-touch-plaque-wenge-avec-lisere-alu-2-postes'
               '-horiz-ou-vert-entraxe-71mm-s530804p.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3192-ovalis-double-chargeur-usb-aa-105w'
               '-anthracite-s340407.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2361-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2043-odace-touch-plaque-chene-astrakan-avec-lisere-alu'
               '-2-postes-entraxe-71mm-s530804p1.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3197-ovalis-prise-tvr-anthracite-s340451.html'
               '', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2362-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2044-odace-touch-plaque-translucide-verre-avec-lisere'
               '-alu-2-postes-horiz-vert-71mm-s530804s.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3198-ovalis-prise-tvrsat-anthracite-s340461'
               '.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2363-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2045-odace-touch-plaque-ardoise-avec-lisere-alu-2'
               '-postes-horiz-vert-entraxe-71mm-s530804v.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3185-ovalis-prise-rj45-cat6-stp-reseaux-vdi'
               '-grade-3-anthracite-s340476.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2364-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2046-odace-touch-plaque-alu-3-postes-horiz-ou-vert'
               '-entraxe-71mm-s530806.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3186-ovalis-prise-rj45-cat6a-grade-3'
               '-multimedia-longue-distance-anth-s340477.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2365-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2047-odace-touch-plaque-aluminium-brosse-lisere-alu-3'
               '-post-horiz-vert-71mm-s530806j.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3187-ovalis-prise-haut-parleur-2-sorties'
               '-anthracite-s340488.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2366-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2048-odace-touch-plaque-aluminium-brosse-croco-avec'
               '-lisere-alu-3-postes-entraxe-71mm-s530806j1.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3194-ovalis-detecteur-de-presence-et-de'
               '-mouvement-toutes-charges-3-fils-anth-s340523.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2367-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2049-odace-touch-plaque-aluminium-brillant-fume-avec'
               '-lisere-alu-3postes-entraxe-71mm-s530806k1.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3181-ovalis-sortie-de-cable-universelle-1620a'
               '-ip24d-anthracite-s340644.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2368-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2050-odace-touch-plaque-wenge-avec-lisere-alu-3-postes'
               '-horiz-ou-vert-entraxe-71mm-s530806p.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2377-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3182-ovalis-sortie-de-cable-16a-612mm'
               '-anthracite-s340662.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2051-odace-touch-plaque-chene-astrakan-avec-lisere-alu'
               '-3-postes-entraxe-71mm-s530806p1.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2378-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3183-ovalis-obturateur-anthracite-s340666'
               '.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2052-odace-touch-plaque-translucide-verre'
               '-avec-lisere-alu-3-postes-horiz-vert-71mm-s530806s.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2381-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2268-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2053-odace-touch-plaque-ardoise-avec-lisere-alu-3'
               '-postes-horiz-vert-entraxe-71mm-s530806v.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2054-odace-touch-plaque-alu-4-postes-horiz-ou-vert'
               '-entraxe-71mm-s530808.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2382-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2269-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2055-odace-touch-plaque-aluminium-brosse-lisere-alu-4'
               '-post-horiz-vert-71mm-s530808j.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2383-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2055-odace-touch-plaque-aluminium-brosse-lisere-alu-4'
               '-post-horiz-vert-71mm-s530808j.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2056-odace-touch-plaque-aluminium-brosse-croco-avec'
               '-lisere-alu-4-postes-entraxe-71mm-s530808j1.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2384-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2271-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2057-odace-touch-plaque-aluminium-brillant-fume-avec'
               '-lisere-alu-4postes-entraxe-71mm-s530808k1.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2385-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2272-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2058-odace-touch-plaque-wenge-avec-lisere-alu-4-postes'
               '-horiz-ou-vert-entraxe-71mm-s530808p.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2386-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2273-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2059-odace-touch-plaque-chene-astrakan-avec-lisere-alu'
               '-4-postes-entraxe-71mm-s530808p1.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2387-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2274-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2060-odace-touch-plaque-translucide-verre-avec-lisere'
               '-alu-4-postes-horiz-vert-71mm-s530808s.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2388-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2275-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2061-odace-touch-plaque-ardoise-avec-lisere-alu-4'
               '-postes-horiz-vert-entraxe-71mm-s530808v.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2389-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2276-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2062-odace-touch-plaque-alu-2-postes-verticaux-entraxe'
               '-57mm-s530814.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2390-product'
               '.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2277-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2278-product.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2391-product.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2392-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2279-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2064-odace-touch-plaque-aluminium-brosse-croco-avec'
               '-lisere-alu-2-postes-entraxe-57mm-s530814j1.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2393-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2280-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2065-odace-touch-plaque-aluminium-brillant-fume-avec'
               '-lisere-alu-2postes-entraxe-57mm-s530814k1.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2394-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2281-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2066-odace-touch-plaque-wenge-avec-lisere-alu-2-postes'
               '-verticaux-entraxe-57mm-s530814p.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2395-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2282-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2067-odace-touch-plaque-chene-astrakan-avec-lisere-alu'
               '-2-postes-entraxe-57mm-s530814p1.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2283-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2068-odace-touch-plaque-2-postes-translucide-verre'
               '-avec-lisere-alu-57mm-vertical-s530814s.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2404-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2284-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2069-odace-touch-plaque-ardoise-avec-lisere-alu-2'
               '-postes-verticaux-entraxe-57mm-s530814v.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2405-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2285-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2070-odace-touch-plaque-alu-3-postes-verticaux-entraxe'
               '-57mm-s530816.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2406-product'
               '.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2286-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2071-odace-touch-plaque-aluminium-brosse-lisere-alu-3'
               '-postes-verticaux-entraxe-57mm-s530816j.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2407-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2072-odace-touch-plaque-aluminium-brosse-croco-avec'
               '-lisere-alu-3-postes-entraxe-57mm-s530816j1.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2408-product.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2287-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2073-odace-touch-plaque-aluminium-brillant-fume-avec'
               '-lisere-alu-3postes-entraxe-57mm-s530816k1.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2409-product.html',
               'https://www.e-planetelec.fr/2288-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2074-odace-touch-plaque-wenge-avec-lisere-alu-3-postes'
               '-verticaux-entraxe-57mm-s530816p.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2410-product.html',
               'https://www.e-planetelec.fr/2289-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2075-odace-touch-plaque-chene-astrakan-avec-lisere-alu'
               '-3-postes-entraxe-57mm-s530816p1.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2411-product.html',
               'https://www.e-planetelec.fr/2290-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2076-odace-touch-plaque-3-postes-translucide-verre'
               '-avec-lisere-alu-57mm-vertical-s530816s.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2412-product.html',
               'https://www.e-planetelec.fr/2291-product.html', 'https://www.e-planetelec.fr/2292-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2077-odace-touch-plaque-ardoise-avec-lisere-alu-3'
               '-postes-verticaux-entraxe-57mm-s530816v.html',
               'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2413-product.html',
               'https://www.e-planetelec.fr/2293-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2078-odace-touch-plaque-de-finition-1-poste-anthracite'
               '-s540802.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2414-product.html'
               '', 'https://www.e-planetelec.fr/2294-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2079-odace-touch-plaque-aluminium-brosse-avec-lisere'
               '-anthracite-1-poste-s540802j.html', 'https://www.e-planetelec.fr/2295-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2080-odace-touch-plaque-miroir-brillantt-fume-avec'
               '-lisere-anthracite-1-poste-s540802k1.html', 'https://www.e-planetelec.fr/2296-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2081-odace-touch-plaque-bronze-brosse-avec-lisere'
               '-anthracite-1-poste-s540802l.html', 'https://www.e-planetelec.fr/2297-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2082-odace-touch-plaque-bois-frene-avec-lisere'
               '-anthracite-1-poste-s540802p3.html', 'https://www.e-planetelec.fr/2298-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2083-odace-touch-plaque-bois-zebrano-avec-lisere'
               '-anthracite-1-poste-s540802p4.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2369-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2084-odace-touch-plaque-pierre-galet-avec-lisere'
               '-anthracite-1-poste-s540802u.html',
               'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2370-product.html',
               'https://www.e-planetelec.fr/plaque-odace-touch/2085-odace-touch-plaque-ardoise-avec-lisere-anthracite'
               '-1-poste-s540802v.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2371-product.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/2086-odace-touch-plaque-anthracite-2-postes-horiz-ou'
                '-vert-entraxe-71mm-s540804.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/2087-plaque-aluminium-brosse-lisere-anthracite-odace'
                '-touch-2-post-horizvert-71mm-s540804j.html',
                'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2372-product.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/2088-odace-touch-plaque-miroir-brillant-fume-avec'
                '-lisere-anth-2postes-entraxe-71mm-s540804k1.html',
                'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2373-product.html',
                'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2374-product.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/2089-odace-touch-plaque-bronze-brosse-lisere'
                '-anthracite-2-postes-horiz-vert-71mm-s540804l.html',
                'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2375-product.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/2090-plaque-bois-frene-lisere-anthracite-odace-touch'
                '-2-postes-horizvert-71mm-s540804p3.html',
                'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2376-product.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/2091-plaque-bois-zebra-avec-lisere-anth-2-postes'
                '-horizvert-entraxe-71mm-s540804p4.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/2092-plaque-pierre-galet-avec-lisere-anthracite-odace'
                '-touch-2-postes-horizvert-entraxe-71mm-s540804u.html',
                'https://www.e-planetelec.fr/plaque-odace-styl/146-plaque-odace-styl-1-poste-blanche-schneider-odace'
                '-s520702.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/1887-prise-de-courant-2pt-alu-a-vis'
                '-connexion-rapide-speciale-renovation-s530049.html',
                'https://www.e-planetelec.fr/enjoliveur-odace/2451-odace-2-demi-enjoliveur-blanc-livre-avec-2-led'
                '-bleu-015-ma-connexion-par-cable-s520298.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/160-plaque-odace-touch-aluminium-martele-1-poste'
                '-blanche-schneider-odace-s520802k.html',
                'https://www.e-planetelec.fr/plaque-odace-you/2014-odace-you-transparent-plaque-de-finition-support'
                '-blanc-1-poste-s520902w.html',
                'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2537-product.html',
                'https://www.e-planetelec.fr/mecanisme-odace-blanc/1756-odace-prise-de-courant-2pt-affleurante'
                '-s520052-schneider.html',
                'https://www.e-planetelec.fr/mecanisme-odace-anthracite/1798-odace-prise-de-courant-2pt-anthracite'
                '-affleurante-s540052.html',
                'https://www.e-planetelec.fr/mecanisme-odace-alu/2590-prise-de-courant-affleurante-2pt-alu-a-vis'
                '-connexion-rapide-s530052.html',
                'https://www.e-planetelec.fr/mecanisme-odace-anthracite/347-odace-prise-de-courant-2pt-anthracite-a'
                '-vis-connexion-rapide-s540059.html',
                'https://www.e-planetelec.fr/plaque-odace-styl/151-plaque-odace-styl-2-postes-blanche-schneider-odace'
                '-s520704.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2452-odace-blanc-enjoliveur-seul-va-et'
                '-vient-et-poussoir-s520604.html',
                'https://www.e-planetelec.fr/mecanisme-odace-blanc/109-pc-2pt-blanche-schneider-odace-s520059.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/161-plaque-odace-touch-aluminium-martele-2-postes'
                '-schneider-odace-s520804k.html',
                'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2538-product.html',
                'https://www.e-planetelec.fr/mecanisme-odace-blanc/1888-pc-2pt-blanche-special-renovation-schneider'
                '-odace-s520049.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/1890-odace-prise-de'
                '-courant-2pt-anthracite-a-vis-connexion-rapide-speciale-renovation-s540049.html',
                'https://www.e-planetelec.fr/plaque-odace-styl/152-plaque-odace-styl-3-postes-blanche-schneider-odace'
                '-s520706.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2453-odace-blanc-enjoliveur-seul'
                '-double-va-et-vient-double-poussoir-vv-poussoir-s520614.html',
                'https://www.e-planetelec.fr/mecanisme-odace-alu/1706-prise-de-courant-2pt-alu-a-vis-connexion-rapide'
                '-s530059.html', 'https://www.e-planetelec.fr/plaque-odace-touch/162-plaque-odace-touch-aluminium'
                '-martele-3-postes-schneider-odace-s520806k.html',
                'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2539-product.html',
                'https://www.e-planetelec.fr/mecanisme-odace-anthracite/348-odace-va-et-vient-anthracite-10-a-a-vis'
                '-s540204.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2454-odace-blanc-enjoliveur-seul-prise'
                '-television-simple-s520645.html',
                'https://www.e-planetelec.fr/mecanisme-odace-blanc/3109-va-et-vient-blanc-schneider-odace-s520204'
                '.html', 'https://www.e-planetelec.fr/plaque-odace-touch/371-plaque-odace-touch-aluminium-martele-4'
                '-postes-schneider-odace-s520808k.html',
                'https://www.e-planetelec.fr/mecanisme-odace-alu/1750-odace-interrupteur-va-et-vient-alu-10a'
                '-connexion-rapide-s530204.html',
                'https://www.e-planetelec.fr/plaque-odace-styl/264-plaque-odace-styl-3-postes-blanche-schneider-odace'
                '-s520706.html', 'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2540-product.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/1966-odace-touch-plaque-de-finition-1-poste-blanc'
                '-ral9003-s520802.html',
                'https://www.e-planetelec.fr/plaque-odace-styl/364-odace-styl-plaque-anthracite-1-poste-s540702.html'
                '', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/350-odace-double-va-et-vient-anthracite-a'
                '-vis-connexion-rapide-s540214.html',
                'https://www.e-planetelec.fr/mecanisme-odace-alu/1707-double-va-et-vient-alu-a-vis-connexion-rapide'
                '-s530214.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2455-product.html',
                'https://www.e-planetelec.fr/mecanisme-odace-blanc/112-double-va-et-vient-blanc-schneider-odace'
                '-s520214.html', 'https://www.e-planetelec.fr/plaque-odace-you/2018-odace-you-transparent-plaque-de'
                '-finition-support-blanc-3-postes-entraxe-71mm-s520906w.html',
                'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2541-product.html',
                'https://www.e-planetelec.fr/odace-sans-fil-sans-pile/2542-product.html',
                'https://www.e-planetelec.fr/plaque-odace-styl/365-odace-styl-plaque-anthracite-2-postes-horiz-vert'
                '-entraxe-71mm-s540704.html',
                'https://www.e-planetelec.fr/mecanisme-odace-anthracite/349-odace-poussoir-anthracite-10-a-a-vis'
                '-s540206.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1974-odace-touch-plaque-blanc-2'
                '-postes-horiz-ou-vert-entraxe-71mm-s520804.html',
                'https://www.e-planetelec.fr/enjoliveur-odace/2456-product.html',
                'https://www.e-planetelec.fr/mecanisme-odace-alu/1751-odace-double-poussoir-alu-a-vis-connexion'
                '-rapide-s530216.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/457-permutateur-schneider'
                '-odace-s520205.html',
                'https://www.e-planetelec.fr/plaque-odace-styl/366-odace-styl-plaque-anthracite-3-postes-horiz-vert'
                '-entraxe-71mm-s540706.html',
                'https://www.e-planetelec.fr/mecanisme-odace-anthracite/351-odace-double-poussoir-anthracite-a-vis'
                '-connexion-rapide-s540216.html',
                'https://www.e-planetelec.fr/mecanisme-odace-blanc/111-bouton-poussoir-blanc-schneider-odace-s520206'
                '.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2457-odace-touche-pour-commande-lumineuse-alu'
                '-livree-sans-led-s530297.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/1982-odace-touch-plaque-blanc-3-postes-horiz-ou-vert'
                '-entraxe-71mm-s520806.html',
                'https://www.e-planetelec.fr/plaque-odace-styl/366-odace-styl-plaque-anthracite-3-postes-horiz-vert'
                '-entraxe-71mm-s540706.html',
                'https://www.e-planetelec.fr/mecanisme-odace-blanc/113-double-bouton-poussoir-blanc-schneider-odace'
                '-s520216.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/1752-odace-prise-rj45-alu-grade-3'
                '-multimedia-cat6-stp-s530476.html',
                'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2146-odace-poussoir-anthracite-avec-porte'
                '-etiquette-a-vis-s540266.html',
                'https://www.e-planetelec.fr/plaque-odace-styl/367-odace-styl-plaque-anthracite-4-postes-horiz-vert'
                '-entraxe-71mm-s540708.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/1990-odace-touch-plaque-blanc-4-postes-horiz-ou-vert'
                '-entraxe-71mm-s520808.html',
                'https://www.e-planetelec.fr/mecanisme-odace-anthracite/352-odace-va-et-vient-poussoir-anthracite-10'
                '-a-s540285.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2459-product.html',
                'https://www.e-planetelec.fr/mecanisme-odace-blanc/139-va-et-vient-bouton-poussoir-blanc-schneider'
                '-odace.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/1754-odace-obturateur-alu-a-vis'
                '-s530666.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1967-odace-touch-plaque-aluminium'
                '-brosse-avec-lisere-blanc-1-poste-s520802j.html',
                'https://www.e-planetelec.fr/mecanisme-odace-anthracite/353-odace-poussoir-lumineux-anthracite-10-a-a'
                '-vis-led-bleu-015-ma-localisation-s540276.html',
                'https://www.e-planetelec.fr/plaque-odace-touch/1975-odace-touch-plaque-aluminium-brosse-lisere-blanc'
                '-2-postes-horiz-vert-71mm-s520804j.html',
                'https://www.e-planetelec.fr/mecanisme-odace-alu/1909-odace-prise-alimentation-usb-alu-s530408.html',
                 'https://www.e-planetelec.fr/plaque-odace-styl/1915-odace-styl-plaque-gris-1-poste-s520702a1.html',
                 'https://www.e-planetelec.fr/enjoliveur-odace/2460-product.html',
                 'https://www.e-planetelec.fr/mecanisme-odace-blanc/1575-va-et-vient-va-et-vient-lumineux-blanc'
                 '-schneider-odace-s520273.html',
                 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/354-odace-va-et-vient-lumineux-anth-10-a-a'
                 '-vis-led-orange-15-ma-local-ou-temoin-s540263.html',
                 'https://www.e-planetelec.fr/plaque-odace-styl/1916-odace-styl-plaque-sable-1-poste-s520702b1.html',
                  'https://www.e-planetelec.fr/enjoliveur-odace/2461-odace-alu-enjoliveur-seul-prise-television'
                  '-simple-s530645.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/141-va-et-vient-lumineux'
                  '-blanc-schneider-odace-s520263.html',
                  'https://www.e-planetelec.fr/plaque-odace-touch/1983-odace-touch-plaque-aluminium-brosse-lisere'
                  '-blanc-3-postes-horiz-vert-71mm-s520806j.html',
                  'https://www.e-planetelec.fr/mecanisme-odace-alu/2342-va-et-vient-bouton-poussoir-alu-schneider'
                  '-odace-s530285.html',
                  'https://www.e-planetelec.fr/plaque-odace-touch/1991-odace-touch-plaque-aluminium-brosse-lisere'
                  '-blanc-4-postes-horiz-vert-71mm-s520808j.html',
                  'https://www.e-planetelec.fr/mecanisme-odace-blanc/140-bouton-poussoir-lumineux-blanc-schneider'
                  '-odace-s520276.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1917-odace-styl-plaque-bleu'
                  '-cian-1-poste-s520702c.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2462-product.html',
                  'https://www.e-planetelec.fr/mecanisme-odace-alu/2343-bouton-poussoir-alu-schneider-odace-s530206'
                  '.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/1901-poussoir-blanc-avec-symbole'
                  '-carillon-schneider-odace-s520246.html',
                  'https://www.e-planetelec.fr/plaque-odace-styl/1918-odace-styl-plaque-violine-1-poste-s520702d.html'
                  '', 'https://www.e-planetelec.fr/plaque-odace-touch/1969-odace-touch-plaque-bronze-brosse-avec'
                  '-lisere-blanc-1-poste-s520802l.html',
                  'https://www.e-planetelec.fr/mecanisme-odace-alu/2615-interrupteur-volets-roulants-odace-alu'
                  '-s530208-schneider-electric.html',
                  'https://www.e-planetelec.fr/plaque-odace-touch/1977-odace-touch-plaque-bronze-brosse-lisere-blanc'
                  '-2-postes-horiz-vert-71mm-s520804l.html',
                  'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2147-odace-poussoir-anthracite-10a-a'
                  '-fermeture-symbole-carillon-s540246.html',
                  'https://www.e-planetelec.fr/plaque-odace-styl/1919-odace-styl-plaque-alu-1-poste-s520702e.html',
                  'https://www.e-planetelec.fr/enjoliveur-odace/2464-odace-enjoliveur-anthracite-livre-sans-led'
                  '-s540297.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/1576-poussoir-porte-etiquette'
                  '-blanc-schneider-odace-s520266.html',
                  'https://www.e-planetelec.fr/mecanisme-odace-alu/3059-conjoncteur-en-t-alu-8-contacts-a-vis-odace'
                  '-s530496.html', 'https://www.e-planetelec.fr/mecanisme-odace-alu/3060-sortie-de-cable-20a-alu'
                  '-schneider-odace-s530662.html',
                  'https://www.e-planetelec.fr/mecanisme-odace-blanc/2524-variateur-de-lumiere-universel-en-2-ou-3'
                  '-fils-3w-100wled-s520519.html',
                  'https://www.e-planetelec.fr/plaque-odace-styl/1920-odace-styl-plaque-ambre-1-poste-s520702g.html',
                   'https://www.e-planetelec.fr/enjoliveur-odace/2465-odace-2-demi-enjoliveur-anthracite-livre-sans'
                   '-led-s540298.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1985-odace-touch-plaque'
                   '-bronze-brosse-lisere-blanc-3-postes-horiz-vert-71mm-s520806l.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1993-odace-touch-plaque-bronze-brosse-lisere-blanc'
                   '-4-postes-horiz-vert-71mm-s520808l.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/358-odace-interrupteur-vmc-anthracite-sans'
                   '-position-arret-a-vis-s540233.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1921-odace-styl-plaque-vert-chartreuse-1-poste'
                   '-s520702h.html', 'https://www.e-planetelec.fr/enjoliveur-odace/2466-product.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/158-detecteur-de-presence-blanc-schneider-odace'
                   '-s520524.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/370-interrupteur-volet'
                   '-roulant-anthracite-montee-descente-stop-s540208.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1922-odace-styl-plaque-gris-2-postes-horizontaux-ou'
                   '-verticaux-entraxe-71mm-s520704a1.html',
                   'https://www.e-planetelec.fr/enjoliveur-odace/2467-product.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1970-odace-touch-plaque-bois-nordique-avec-lisere'
                   '-blanc-1-poste-s520802m.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2145-odace-interrupteur-vmc-anthracite'
                   '-avec-position-arret-s540243.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1978-odace-touch-plaque-bois-nordique-lisere-blanc'
                   '-2-postes-horiz-vert-71mm-s520804m.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1923-odace-styl-plaque-sable-2-postes-horizontaux'
                   '-ou-verticaux-entraxe-71mm-s520704b1.html',
                   'https://www.e-planetelec.fr/enjoliveur-odace/2468-odace-anthracite-enjoliveur-seul-prise'
                   '-television-simple-s540645.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/150-commande-de-vmc-sans-position-arret-blanc'
                   '-schneider-odace-s520233.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/159-commande-de-volets-roulants-blanc-schneider'
                   '-odace-s520208.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/356-odace-prise-tv'
                   '-anthracite-a-vis-s540445.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1986-odace-touch-plaque-bois-nordique-lisere-blanc'
                   '-3-postes-horiz-vert-71mm-s520806m.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1924-odace-styl-plaque-bleu-cian-2-postes'
                   '-horizontaux-ou-verticaux-entraxe-71mm-s520704c.html',
                   'https://www.e-planetelec.fr/enjoliveur-odace/2469-product.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1994-odace-touch-plaque-bois-nordique-lisere-blanc'
                   '-4-postes-horiz-vert-71mm-s520808m.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2218-mecanisme-odace-anthracite-prise-sat'
                   '-schneider-odace-s420446.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/1878-poussoir-pour-volets-roulants-blanc'
                   '-schneider-odace-s520207.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1925-odace-styl-plaque-violine-2-postes-horizontaux'
                   '-ou-verticaux-entraxe-71mm-s520704d.html',
                   'https://www.e-planetelec.fr/enjoliveur-odace/2470-product.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/145-prise-rj-45-telephone-grade-1-blanc'
                   '-schneider-odace-s520471.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1971-odace-touch-plaque-bois-naturel-avec-lisere'
                   '-blanc-1-poste-s520802n.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/1893-prise-conjoncteur-en-t-anthracite'
                   '-schneider-odace-s540496.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1926-odace-styl-plaque-alu-2-postes-horiz-vert'
                   '-entraxe-71mm-s520704e.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1979-odace-touch-plaque-bois-naturel-lisere-blanc'
                   '-2-postes-horiz-vert-71mm-s520804n.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/147-prise-rj-45-telephone-informatique-grade-1'
                   '-blanc-schneider-odace-s520475.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/368-odace-prise-rj45-anthracite-grade-1'
                   '-telephone-cat-5-utp-a-vis-s540471.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1927-odace-styl-plaque-ambre-2-postes-horizontaux'
                   '-ou-verticaux-entraxe-71mm-s520704g.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1928-odace-styl-plaque-vert-chartreuse-2-postes'
                   '-horiz-ou-verticaux-entraxe-71mm-s520704h.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1987-odace-touch-plaque-bois-naturel-lisere-blanc'
                   '-3-postes-horiz-vert-71mm-s520806n.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/1653-odace-prise-rj45-blanc-grade-3-multimedia'
                   '-cat-6-stp-schneider-odace-s520476.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/369-odace-prise-rj45-anth-grade-1'
                   '-telephone-informatique-cat-6-utpa-vis-s540475.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1929-odace-styl-plaque-gris-3-postes-horizontaux-ou'
                   '-verticaux-entraxe-71mm-s520706a1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1995-odace-touch-plaque-bois-naturel-lisere-blanc'
                   '-4-postes-horiz-vert-71mm-s520808n.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/1802-prise-rj-45-grade-3-blanc-schneider-odace'
                   '-s520477.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/1705-prise-rj45-anth'
                   '-grade-2-ou-3-suivant-cablage-s540476.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/2134-odace-prise-double-rj45-blanc-grade-3'
                   '-multimedia-cat-6-stp-a-vis-s520486.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1930-odace-styl-plaque-sable-3-postes-horizontaux'
                   '-ou-verticaux-entraxe-71mm-s520706b1.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2169-odace-prise-usb-double-charge-rapide'
                   '-type-ac-anthracite-18w-34a-s540219.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1972-odace-touch-plaque-translucide-blanc-1-poste'
                   '-s520802r.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1931-odace-styl-plaque-bleu-cian'
                   '-3-postes-horizontaux-ou-verticaux-entraxe-71mm-s520706c.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1980-odace-touch-plaque-translucide-blanc-2-postes'
                   '-horiz-vert-entraxe-71mm-s520804r.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/360-odace-prise-alimentation-usb-5v'
                   '-anthracite-s540408.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/541-prise-conjoncteur-en-t-schneider-odace'
                   '-s520496.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1932-odace-styl-plaque-violine-3'
                   '-postes-horizontaux-ou-verticaux-entraxe-71mm-s520706d.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/143-prise-tv-blanc-schneider-odace-s520445.html'
                   '', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/362-odace-prise-haut-parleur-1-sortie'
                   '-anthracite-s540487.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1988-odace-touch-plaque-translucide-blanc-3-postes'
                   '-horiz-vert-entraxe-71mm-s520806r.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/363-odace-prise-haut-parleurs-anthracite-2'
                   '-sorties-s540488.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/1889-prise-sat-a-vis-blanc-schneider-odace'
                   '-s520446.html', 'https://www.e-planetelec.fr/plaque-odace-touch/1996-odace-touch-plaque'
                   '-translucide-blanc-4-postes-horiz-vert-entraxe-71mm-s520808r.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1933-odace-styl-plaque-alu-3-postes-horiz-vert'
                   '-entraxe-71mm-s520706e.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/1704-prise-tvfmsat-schneider-odace-s520460.html'
                   '', 'https://www.e-planetelec.fr/plaque-odace-touch/1973-odace-touch-plaque-pierre-galet-1-poste'
                   '-s520802u.html', 'https://www.e-planetelec.fr/mecanisme-odace-anthracite/357-odace-sortie-de'
                   '-cable-anthracite-6-a-12-mm2-s540662.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1934-odace-styl-plaque-ambre-3-postes-horizontaux'
                   '-ou-verticaux-entraxe-71mm-s520706g.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/361-odace-obturateur-anthracite-a-vis'
                   '-s540666.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/149-sortie-de-cable-20a-blanc'
                   '-schneider-odace-s520662.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1981-odace-touch-plaque-pierre-galet-2-postes'
                   '-horiz-vert-entraxe-71mm-s520804u.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1936-odace-styl-plaque-gris-4-postes-horizontaux-ou'
                   '-verticaux-entraxe-71mm-s520708a1.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2449-odace-permutateur-s540205.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1989-odace-touch-plaque-pierre-galet-3-postes'
                   '-horiz-vert-entraxe-71mm-s520806u.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/256-obturateur-blanc-schneider-odace-s520666'
                   '.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1937-odace-styl-plaque-sable-4-postes'
                   '-horizontaux-ou-verticaux-entraxe-71mm-s520708b1.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-anthracite/2529-variateur-de-lumiere-universel-en-2'
                   '-ou-3-fils-3w-100wled-anthracite-s540519.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1997-odace-touch-plaque-pierre-galet-4-postes'
                   '-horiz-vert-entraxe-71mm-s520808u.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/255-prise-alim-usb-5v-schneider-odace-s520408'
                   '.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1938-odace-styl-plaque-bleu-cian-4-postes'
                   '-horizontaux-ou-verticaux-entraxe-71mm-s520708c.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/1615-s520407-odace-double-chargeur-usb-21-a'
                   '-blanc-schneider-electric.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1998-odace-touch-plaque-blanc-2-postes-verticaux'
                   '-57mm-s520814.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/2324-odace-prise-usb-double-charge-rapide-type'
                   '-ac-blanc-18w-34a-s520219.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1939-odace-styl-plaque-violine-4-postes-horizontaux'
                   '-ou-verticaux-entraxe-71mm-s520708d.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1940-odace-styl-plaque-alu-4-postes-horiz-vert'
                   '-entraxe-71mm-s520708e.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/444-prise-hdmi-schneider-odace-s520462.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/1999-odace-touch-plaque-aluminium-brosse-avec'
                   '-lisere-blanc-2-postes-verticaux-57mm-s520814j.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/289-prise-hp-1-sortie-schneider-odace-s520487'
                   '.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1941-odace-styl-plaque-ambre-4-postes'
                   '-horizontaux-ou-verticaux-entraxe-71mm-s520708g.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2007-odace-touch-plaque-aluminium-brosse-avec'
                   '-lisere-blanc-3-postes-verticaux-57mm-s520816j.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2000-odace-touch-plaque-aluminium-martele-avec'
                   '-lisere-blanc-2-postes-verticaux-57mm-s520814k.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/290-prise-hp-2-sorties-schneider-odace-s520488'
                   '.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1942-odace-styl-plaque-vert-chartreuse-4'
                   '-postes-horiz-ou-verticaux-entraxe-71mm-s520708h.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2008-odace-touch-plaque-aluminium-martele-avec'
                   '-lisere-blanc-3-postes-verticaux-57mm-s520816k.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1943-odace-styl-pratic-plaque-blanc-support'
                   '-telephone-mobile-1-poste-s520712.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/378-boite-pour-montage-saillie-blanc-1-poste'
                   '-schneider-odace-styl-s520762.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2001-odace-touch-plaque-bronze-brosse-avec-lisere'
                   '-blanc-2-postes-verticaux-57mm-s520814l.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1944-odace-styl-plaque-blanc-2-postes-verticaux'
                   '-entraxe-57mm-s520714.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/379-boite-pour-montage-saillie-blanc-2-postes'
                   '-schneider-odace-styl-s520764.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2009-odace-touch-plaque-bronze-brosse-avec-lisere'
                   '-blanc-3-postes-verticaux-57mm-s520816l.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/422-ressorts-odace-sachets-10-pieces-schneider'
                   '-odace-s520299.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/551-sachet-de-10-griffes'
                   '-standard-schneider-odace-s520690.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2002-odace-touch-plaque-bois-nordique-avec-lisere'
                   '-blanc-2-postes-verticaux-57mm-s520814m.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2010-odace-touch-plaque-bois-nordique-avec-lisere'
                   '-blanc-3-postes-verticaux-57mm-s520816m.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/1904-voyant-led-bleu-a-clipser-schneider-odace'
                   '-s520292.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2003-odace-touch-plaque-bois'
                   '-naturel-avec-lisere-blanc-2-postes-verticaux-57mm-s520814n.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/1905-enjoliveur-blanc-1-led-bleu-15ma-schneider'
                   '-odace-s520297.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/157-voyant-led-orange-schneider-odace-s520290'
                   '.html', 'https://www.e-planetelec.fr/plaque-odace-styl/1949-odace-styl-plaque-alu-2-postes'
                   '-verticaux-entraxe-57mm-s520714e.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2011-odace-touch-plaque-bois-naturel-avec-lisere'
                   '-blanc-3-postes-verticaux-57mm-s520816n.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/283-voyant-led-bleu-schneider-odace-s520291'
                   '.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/2344-variateur-universel-a-poussoir'
                   '-plus-link-blanc-schneider-odace-s520560.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2012-odace-touch-plaque-translucide-blanc-3-postes'
                   '-verticaux-entraxe-57mm-s520816r.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2005-odace-touch-plaque-pierre-galet-2-postes'
                   '-verticaux-entraxe-57mm-s520814u.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/2499-prise-tvfm-schneider-odace-s520451.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1952-odace-styl-plaque-blanc-3-postes-verticaux'
                   '-entraxe-57mm-s520716.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/2500-prise-2p-a-vis-blanc-schneider-odace'
                   '-s520033.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2013-odace-touch-plaque-pierre'
                   '-galet-3-postes-verticaux-entraxe-57mm-s520816u.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/2501-ronfleur-blanc-230v-a-vis-schneider-odace'
                   '-s520685.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2030-odace-touch-plaque-de'
                   '-finition-1-poste-alu-s530802.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2031-odace-touch-plaque-aluminium-brosse-avec'
                   '-lisere-alu-1-poste-s530802j.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/2531-detecteur-de-presence-et-de-mouvement'
                   '-blanc-toutes-charges-schneider-odace-s520523.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2032-odace-touch-plaque-aluminium-brosse-croco'
                   '-avec-lisere-alu-1-poste-s530802j1.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/3041-odace-prise-de-courant-affleurante-usb'
                   '-type-c-s520089-schneider.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1957-odace-styl-plaque-alu-3-postes-verticaux'
                   '-entraxe-57mm-s520716e.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2033-odace-touch-plaque-aluminium-brillantt-fume'
                   '-avec-lisere-alu-1-poste-s530802k1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2034-odace-touch-plaque-wenge-avec-lisere-alu-1'
                   '-poste-s530802p.html',
                   'https://www.e-planetelec.fr/mecanisme-odace-blanc/3042-odace-prise-usb-double-type-ac-s520401'
                   '-schneider.html', 'https://www.e-planetelec.fr/plaque-odace-touch/2035-odace-touch-plaque-chene'
                   '-astrakan-avec-lisere-alu-1-poste-s530802p1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2036-odace-touch-plaque-translucide-verre-avec'
                   '-lisere-alu-1-poste-s530802s.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1960-odace-styl-pratic-plaque-blanc-avec-crochet'
                   '-multi-usage-1-poste-s520722.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2037-odace-touch-plaque-ardoise-avec-lisere-alu-1'
                   '-poste-s530802v.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1961-odace-styl-pratic-plaque-blanc-avec-porte'
                   '-etiquette-1-poste-s520732.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2038-odace-touch-plaque-alu-2-postes-horiz-ou-vert'
                   '-entraxe-71mm-s530804.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1962-odace-styl-pratic-plaque-blanc-porte-etiquette'
                   '-avec-bloc-lumineux-1-poste-s520739.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2039-odace-touch-plaque-aluminium-brosse-lisere'
                   '-alu-2-post-horiz-vert-71mm-s530804j.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1963-odace-styl-pratic-plaque-blanc-avec-pince'
                   '-multi-usage-1-poste-s520742.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2040-odace-touch-plaque-aluminium-brosse-croco'
                   '-avec-lisere-alu-2-postes-entraxe-71mm-s530804j1.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1964-odace-styl-pratic-plaque-blanc-avec-couvercle'
                   '-integre-pour-prise-1-poste-s520752.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2041-odace-touch-plaque-aluminium-brillant-fume'
                   '-avec-lisere-alu-2postes-entraxe-71mm-s530804k1.html',
                   'https://www.e-planetelec.fr/plaque-odace-styl/1965-odace-styl-pratic-plaque-blanc-avec-couvercle'
                   '-souple-translucide-1-poste-ip44-s520772.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2042-odace-touch-plaque-wenge-avec-lisere-alu-2'
                   '-postes-horiz-ou-vert-entraxe-71mm-s530804p.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2043-odace-touch-plaque-chene-astrakan-avec-lisere'
                   '-alu-2-postes-entraxe-71mm-s530804p1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2044-odace-touch-plaque-translucide-verre-avec'
                   '-lisere-alu-2-postes-horiz-vert-71mm-s530804s.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2045-odace-touch-plaque-ardoise-avec-lisere-alu-2'
                   '-postes-horiz-vert-entraxe-71mm-s530804v.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2046-odace-touch-plaque-alu-3-postes-horiz-ou-vert'
                   '-entraxe-71mm-s530806.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2047-odace-touch-plaque-aluminium-brosse-lisere'
                   '-alu-3-post-horiz-vert-71mm-s530806j.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2048-odace-touch-plaque-aluminium-brosse-croco'
                   '-avec-lisere-alu-3-postes-entraxe-71mm-s530806j1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2049-odace-touch-plaque-aluminium-brillant-fume'
                   '-avec-lisere-alu-3postes-entraxe-71mm-s530806k1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2050-odace-touch-plaque-wenge-avec-lisere-alu-3'
                   '-postes-horiz-ou-vert-entraxe-71mm-s530806p.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2051-odace-touch-plaque-chene-astrakan-avec-lisere'
                   '-alu-3-postes-entraxe-71mm-s530806p1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2052-odace-touch-plaque-translucide-verre-avec'
                   '-lisere-alu-3-postes-horiz-vert-71mm-s530806s.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2053-odace-touch-plaque-ardoise-avec-lisere-alu-3'
                   '-postes-horiz-vert-entraxe-71mm-s530806v.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2054-odace-touch-plaque-alu-4-postes-horiz-ou-vert'
                   '-entraxe-71mm-s530808.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2055-odace-touch-plaque-aluminium-brosse-lisere'
                   '-alu-4-post-horiz-vert-71mm-s530808j.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2056-odace-touch-plaque-aluminium-brosse-croco'
                   '-avec-lisere-alu-4-postes-entraxe-71mm-s530808j1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2057-odace-touch-plaque-aluminium-brillant-fume'
                   '-avec-lisere-alu-4postes-entraxe-71mm-s530808k1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2058-odace-touch-plaque-wenge-avec-lisere-alu-4'
                   '-postes-horiz-ou-vert-entraxe-71mm-s530808p.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2059-odace-touch-plaque-chene-astrakan-avec-lisere'
                   '-alu-4-postes-entraxe-71mm-s530808p1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2060-odace-touch-plaque-translucide-verre-avec'
                   '-lisere-alu-4-postes-horiz-vert-71mm-s530808s.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2061-odace-touch-plaque-ardoise-avec-lisere-alu-4'
                   '-postes-horiz-vert-entraxe-71mm-s530808v.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2062-odace-touch-plaque-alu-2-postes-verticaux'
                   '-entraxe-57mm-s530814.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2064-odace-touch-plaque-aluminium-brosse-croco'
                   '-avec-lisere-alu-2-postes-entraxe-57mm-s530814j1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2065-odace-touch-plaque-aluminium-brillant-fume'
                   '-avec-lisere-alu-2postes-entraxe-57mm-s530814k1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2066-odace-touch-plaque-wenge-avec-lisere-alu-2'
                   '-postes-verticaux-entraxe-57mm-s530814p.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2067-odace-touch-plaque-chene-astrakan-avec-lisere'
                   '-alu-2-postes-entraxe-57mm-s530814p1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2068-odace-touch-plaque-2-postes-translucide-verre'
                   '-avec-lisere-alu-57mm-vertical-s530814s.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2069-odace-touch-plaque-ardoise-avec-lisere-alu-2'
                   '-postes-verticaux-entraxe-57mm-s530814v.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2070-odace-touch-plaque-alu-3-postes-verticaux'
                   '-entraxe-57mm-s530816.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2071-odace-touch-plaque-aluminium-brosse-lisere'
                   '-alu-3-postes-verticaux-entraxe-57mm-s530816j.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2072-odace-touch-plaque-aluminium-brosse-croco'
                   '-avec-lisere-alu-3-postes-entraxe-57mm-s530816j1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2073-odace-touch-plaque-aluminium-brillant-fume'
                   '-avec-lisere-alu-3postes-entraxe-57mm-s530816k1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2074-odace-touch-plaque-wenge-avec-lisere-alu-3'
                   '-postes-verticaux-entraxe-57mm-s530816p.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2075-odace-touch-plaque-chene-astrakan-avec-lisere'
                   '-alu-3-postes-entraxe-57mm-s530816p1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2076-odace-touch-plaque-3-postes-translucide-verre'
                   '-avec-lisere-alu-57mm-vertical-s530816s.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2077-odace-touch-plaque-ardoise-avec-lisere-alu-3'
                   '-postes-verticaux-entraxe-57mm-s530816v.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2078-odace-touch-plaque-de-finition-1-poste'
                   '-anthracite-s540802.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2079-odace-touch-plaque-aluminium-brosse-avec'
                   '-lisere-anthracite-1-poste-s540802j.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2080-odace-touch-plaque-miroir-brillantt-fume-avec'
                   '-lisere-anthracite-1-poste-s540802k1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2081-odace-touch-plaque-bronze-brosse-avec-lisere'
                   '-anthracite-1-poste-s540802l.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2082-odace-touch-plaque-bois-frene-avec-lisere'
                   '-anthracite-1-poste-s540802p3.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2083-odace-touch-plaque-bois-zebrano-avec-lisere'
                   '-anthracite-1-poste-s540802p4.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2084-odace-touch-plaque-pierre-galet-avec-lisere'
                   '-anthracite-1-poste-s540802u.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2085-odace-touch-plaque-ardoise-avec-lisere'
                   '-anthracite-1-poste-s540802v.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2086-odace-touch-plaque-anthracite-2-postes-horiz'
                   '-ou-vert-entraxe-71mm-s540804.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2087-plaque-aluminium-brosse-lisere-anthracite'
                   '-odace-touch-2-post-horizvert-71mm-s540804j.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2088-odace-touch-plaque-miroir-brillant-fume-avec'
                   '-lisere-anth-2postes-entraxe-71mm-s540804k1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2089-odace-touch-plaque-bronze-brosse-lisere'
                   '-anthracite-2-postes-horiz-vert-71mm-s540804l.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2090-plaque-bois-frene-lisere-anthracite-odace'
                   '-touch-2-postes-horizvert-71mm-s540804p3.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2091-plaque-bois-zebra-avec-lisere-anth-2-postes'
                   '-horizvert-entraxe-71mm-s540804p4.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2092-plaque-pierre-galet-avec-lisere-anthracite'
                   '-odace-touch-2-postes-horizvert-entraxe-71mm-s540804u.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2093-plaque-ardoise-avec-lisere-anthracite-odace'
                   '-touch-2-postes-horizvert-entraxe-71mm-s540804v.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2094-plaque-anthracite-odace-touch-3-postes-horiz'
                   '-ou-vert-entraxe-71mm-s540806.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2095-plaque-aluminium-brosse-lisere-anthracite'
                   '-odace-touch-3-postes-horizvert-71mm-s540806j.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2096-plaque-miroir-brillant-fume-avec-lisere'
                   '-anthracite-odace-touch-3-postes-entraxe-71mm-s540806k1.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2097-plaque-bronze-brosse-lisere-anthracite-odace'
                   '-touch-3-postes-horizvert-71mm-s540806l.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2098-plaque-bois-zebra-avec-lisere-anthracite'
                   '-odace-touch-3-postes-horizvert-entraxe-71mm-s540806p4.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2099-plaque-pierre-galet-avec-lisere-anthracite'
                   '-odace-touch-3-postes-horizvert-entraxe-71mm-s540806u.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2100-odace-touch-plaque-ardoise-avec-lisere-anth-3'
                   '-postes-horiz-vert-entraxe-71mm-s540806v.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2101-plaque-anthracite-4-postes-odace-touch-horiz'
                   '-ou-vert-entraxe-71mm-s540808.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2102-plaque-alminium-brosse-lisere-anthracite'
                   '-odace-touch-4-postes-horizvert-71mm-s540808j.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2104-plaque-pierre-galet-lisere-anthracite-odace'
                   '-touch-4-postes-horizvert-71mm-s540808u.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2105-plaque-ardoise-avec-lisere-anthracite-odace'
                   '-touch-4-postes-horizvert-entraxe-71mm-s540808v.html',
                   'https://www.e-planetelec.fr/plaque-odace-touch/2106-odace-touch-plaque-anthracite-2-postes'
                   '-verticaux-entraxe-57mm-s540814.html',
                   'https://www.e-planetelec.fr/accessoires-ovalis-schneider/3207-ovalis-boite-support-36-mm-pour'
                   '-montage-en-saillie-blanc-s320762.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3175-ovalis-prise-2pt-16a-affleurante'
                   '-bornes-automatiques-antibacterien-s300052.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3208-ovalis-plaque-de-finition-1-poste'
                   '-antibacterien-s300702.html',
                   'https://www.e-planetelec.fr/accessoires-ovalis-schneider/3217-ovalis-boite-support-36-mm-pour'
                   '-montage-en-saillie-anthracite-s340762.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2221-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3176-ovalis-prise-de-courant-a-puits-2pt'
                   '-16a-bornes-automatiques-antibacterien-s300059.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3209-ovalis-plaque-de-finition-2-postes'
                   '-horizontal-entraxe-71-mm-antibacterien-s300704.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2222-product.html',
                   'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2254-product.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3210-ovalis-plaque-de-finition-3-postes'
                   '-horizontal-entraxe-71-mm-antibacterien-s300706.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3162-ovalis-interrupteur-va-et-vient-10ax'
                   '-antibacterien-s300204.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2223-product.html',
                   'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2255-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3163-ovalis-interrupteur-2-boutons-pour'
                   '-volet-roulant-6ax-antibacterien-s300208.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3199-ovalis-plaque-de-finition-1-poste-blanc'
                   '-s320702.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2224-product'
                   '.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3164-ovalis-double-va-et-vient'
                   '-10ax-antibacterien-s300214.html',
                   'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2258-product.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3200-ovalis-lot-de-360-plaques-de-finition'
                   '-de-coloris-blanc-s320702p.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3195-ovalis-prise-tv-simple-antibacterien'
                   '-s300405.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2225-product'
                   '.html', 'https://www.e-planetelec.fr/plaques-ovalis-schneider/3201-ovalis-plaque-de-finition-2'
                   '-postes-horizontal-entraxe-71-mm-blanc-s320704.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2226-product.html',
                   'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2262-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3184-ovalis-prise-rj45-cat6-stp-reseaux'
                   '-vdi-grade-3-antibacterien-s300476.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3202-ovalis-lot-de-180-plaques-2-postes'
                   '-horizontal-finition-de-coloris-blanc-s320704p.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2227-product.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3203-ovalis-plaque-de-finition-3-postes'
                   '-horizontal-entraxe-71-mm-blanc-s320706.html',
                   'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2267-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3139-ovalis-prise-de-courant-a-puits-2p'
                   '-16a-bornes-vis-blanc-s320033.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2228-product.html',
                   'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2415-product.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3204-ovalis-plaque-de-finition-4-postes'
                   '-horizontal-entraxe-71-mm-blanc-s320708.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3140-ovalis-prise-de-courant-2pt-16a'
                   '-affleurante-bornes-automatiques-blanc-s320052.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2229-product.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3205-ovalis-plaque-de-finition-2-postes'
                   '-vertical-entraxe-71-mm-blanc-s320724.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3141-ovalis-prise-2pt-16a-affleurante'
                   '-bornes-auto-blanc-griffes-montees-s320052c.html',
                   'https://www.e-planetelec.fr/accessoires-ovalis-schneider/2420-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2230-product.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3206-ovalis-plaque-de-finition-3-postes'
                   '-vertical-entraxe-71-mm-blanc-s320726.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3142-ovalis-lot-de-108-2pt-affleurantes'
                   '-16a-blanc-sans-emballage-unitaire-s320052p.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3143-ovalis-prise-de-courant-a-puits-2pt'
                   '-16a-bornes-automatiques-blanc-s320059.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3211-ovalis-plaque-de-finition-1-poste'
                   '-anthracite-s340702.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2231-product.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3212-ovalis-plaque-de-finition-2-postes'
                   '-horizontal-entraxe-71-mm-anthracite-s340704.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3218-ovalis-lot-de-108-2pt-a-puits-16a'
                   '-blanc-sans-emballage-unitaire-s320059p.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2232-product.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3213-ovalis-plaque-de-finition-3-postes'
                   '-horizontal-entraxe-71-mm-anthracite-s340706.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3213-ovalis-plaque-de-finition-3-postes'
                   '-horizontal-entraxe-71-mm-anthracite-s340706.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3152-ovalis-combi-2pt-16a'
                   '-affleurantechargeur-usb-c-105w-connex-auto-blanc-s320089.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2234-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3128-ovalis-interrupteur-va-et-vient-10ax'
                   '-blanc-s320204.html', 'https://www.e-planetelec.fr/plaques-ovalis-schneider/3214-ovalis-plaque-de'
                   '-finition-4-postes-horizontal-entraxe-71-mm-anthracite-s340708.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2235-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3129-ovalis-lot-de-108-va-et-vient-10ax'
                   '-blanc-sans-emballage-unitaire-s320204p.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3215-ovalis-plaque-de-finition-2-postes'
                   '-vertical-entraxe-71-mm-anthracite-s340724.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2236-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3130-ovalis-bouton-poussoir-a-fermeture'
                   '-10a-blanc-s320206.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/3216-ovalis-plaque-de-finition-3-postes'
                   '-vertical-entraxe-71-mm-anthracite-s340726.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2237-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3131-ovalis-interrupteur-2-boutons-pour'
                   '-volet-roulant-6ax-blanc-s320208.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/2263-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2238-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3132-ovalis-double-va-et-vient-10ax-blanc'
                   '-s320214.html', 'https://www.e-planetelec.fr/plaques-ovalis-schneider/2264-product.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/2265-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2239-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3133-ovalis-lot-de-108-double-va-et-vient'
                   '-10ax-blanc-sans-emballage-unitaire-s320214p.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/2266-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2240-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3134-ovalis-double-poussoir-fermeture'
                   '-10ax-blanc-s320216.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/2299-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2241-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3135-ovalis-poussoir-vmc-sans-arret-blanc'
                   '-s320236.html', 'https://www.e-planetelec.fr/plaques-ovalis-schneider/2416-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2242-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3219-ovalis-interrupteur-va-et-vient-10ax'
                   '-lumineux-ou-temoin-blanc-s320263.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/2417-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2243-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3136-ovalis-poussoir-a-fermeture-avec'
                   '-porte-etiquette-10ax-blanc-s320266.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3137-ovalis-poussoir-a-fermeture-lumineux'
                   '-10ax-led-bleu-250v-blanc-s320276.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/2418-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2244-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3138-ovalis-combine-va-et-vientpoussoir'
                   '-10ax-blanc-s320285.html',
                   'https://www.e-planetelec.fr/plaques-ovalis-schneider/2419-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2245-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2246-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3153-ovalis-double-chargeur-usb-ac-12w'
                   '-blanc-s320401.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3154-ovalis-chargeur-usb-type-a-75w-c-45w'
                   '-forte-puissance-type-c-blanc-s320403.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2247-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2248-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3159-ovalis-prise-tv-simple-blanc-s320405'
                   '.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2249-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3155-ovalis-chargeur-usb-c-65w-forte'
                   '-puissance-pour-charge-app-mobiles-blanc-s320406.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2250-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3156-ovalis-double-chargeur-usb-aa-105w'
                   '-blanc-s320407.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2251-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3160-ovalis-prise-tvr-blanc-s320451.html'
                   '', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2252-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3161-ovalis-prise-tvrsat-blanc-s320461'
                   '.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3148-ovalis-prise-rj45-cat6-stp'
                   '-reseaux-vdi-grade-3-blanc-s320476.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2253-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3149-ovalis-lot-de-108-rj45-cat6-stp'
                   '-blanc-sans-emballage-unitaire-s320476p.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2256-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3150-ovalis-prise-rj45-cat6a-grade-3'
                   '-multimedia-longue-distance-blanc-s320477.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2257-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2259-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3151-ovalis-prise-haut-parleur-2-sorties'
                   '-blanc-s320488.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2260-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2300-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3158-ovalis-detecteur-de-presence-et-de'
                   '-mouvement-toutes-charges-3-fils-blanc-s320523.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2301-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3145-ovalis-sortie-de-cable-universelle'
                   '-1620a-ip24d-blanc-s320644.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2302-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3146-ovalis-sortie-de-cable-16a-612mm'
                   '-blanc-s320662.html', 'https://www.e-planetelec.fr/2303-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3147-ovalis-obturateur-blanc-s320666.html'
                   '', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3177-ovalis-prise-de-courant-a-puits'
                   '-2p-16a-bornes-vis-anthracite-s340033.html', 'https://www.e-planetelec.fr/2304-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3178-ovalis-prise-de-courant-2pt-16a'
                   '-affleurante-bornes-auto-anthracite-s340052.html',
                   'https://www.e-planetelec.fr/2305-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3179-ovalis-prise-2pt-16a-affleurante'
                   '-bornes-auto-anthracite-griffes-montees-s340052c.html',
                   'https://www.e-planetelec.fr/2306-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2307-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3180-ovalis-prise-de-courant-a-puits-2pt'
                   '-16a-bornes-automatiques-anthracite-s340059.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2308-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3188-ovalis-combi-2pt-16a'
                   '-affleurantechargeur-usb-c-105w-connex-auto-anth-s340089.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3165-ovalis-interrupteur-va-et-vient-10ax'
                   '-anthracite-s340204.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2309-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3166-ovalis-bouton-poussoir-a-fermeture'
                   '-10a-anthracite-s340206.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2310-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3167-ovalis-interrupteur-2-boutons-pour'
                   '-volet-roulant-6ax-anthracite-s340208.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2311-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3168-ovalis-double-va-et-vient-10ax'
                   '-anthracite-s340214.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2312-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3169-ovalis-double-poussoir-fermeture'
                   '-10ax-anthracite-s340216.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2313-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3170-ovalis-poussoir-vmc-sans-arret'
                   '-anthracite-s340236.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2314-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3171-ovalis-interrupteur-va-et-vient-10ax'
                   '-lumineux-ou-temoin-anthracite-s340263.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2315-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3172-ovalis-poussoir-a-fermeture-avec'
                   '-porte-etiquette-10ax-anthracite-s340266.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2316-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3173-ovalis-poussoir-a-fermeture-lumineux'
                   '-10ax-led-bleu-250v-anthracite-s340276.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2317-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3174-ovalis-combine-va-et-vientpoussoir'
                   '-10ax-anthracite-s340285.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2318-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3189-ovalis-double-chargeur-usb-ac-12w'
                   '-anthracite-s340401.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2319-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3190-ovalis-chargeur-usb-type-a-75w-c-45w'
                   '-forte-puissance-type-c-anthracite-s340403.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2581-ovalis-variateur-de'
                   '-lumiere-universel-23-fils-3w-blanc-avec-plaque-s260519.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2358-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3196-ovalis-prise-tv-simple-anthracite'
                   '-s340405.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3191-ovalis-chargeur-usb'
                   '-c-65w-forte-puissance-pour-charge-app-mobiles-anth-s340406.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2359-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3192-ovalis-double-chargeur-usb-aa-105w'
                   '-anthracite-s340407.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2360-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3197-ovalis-prise-tvr-anthracite-s340451'
                   '.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2361-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3198-ovalis-prise-tvrsat-anthracite'
                   '-s340461.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2362-product'
                   '.html', 'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3185-ovalis-prise-rj45-cat6-stp'
                   '-reseaux-vdi-grade-3-anthracite-s340476.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2363-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3186-ovalis-prise-rj45-cat6a-grade-3'
                   '-multimedia-longue-distance-anth-s340477.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2364-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2365-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3187-ovalis-prise-haut-parleur-2-sorties'
                   '-anthracite-s340488.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2366-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2367-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3194-ovalis-detecteur-de-presence-et-de'
                   '-mouvement-toutes-charges-3-fils-anth-s340523.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2368-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3181-ovalis-sortie-de-cable-universelle'
                   '-1620a-ip24d-anthracite-s340644.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2377-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3182-ovalis-sortie-de-cable-16a-612mm'
                   '-anthracite-s340662.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2378-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/3183-ovalis-obturateur-anthracite-s340666'
                   '.html', 'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2381-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2268-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2382-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2269-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2383-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2270-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2384-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2271-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2385-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2272-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2386-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2273-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2387-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2274-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2388-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2275-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2389-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2276-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2390-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2277-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2391-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2278-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2392-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2279-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2393-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2280-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2281-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2394-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2282-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2395-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2283-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2404-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2284-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2405-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2285-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2406-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2286-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2407-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2287-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2408-product.html',
                   'https://www.e-planetelec.fr/2288-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2409-product.html',
                   'https://www.e-planetelec.fr/2289-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2410-product.html',
                   'https://www.e-planetelec.fr/2290-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2411-product.html',
                   'https://www.e-planetelec.fr/2291-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2412-product.html',
                   'https://www.e-planetelec.fr/2292-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2413-product.html',
                   'https://www.e-planetelec.fr/2293-product.html',
                   'https://www.e-planetelec.fr/appareillage-complet-ovalis-schneider/2414-product.html',
                   'https://www.e-planetelec.fr/2294-product.html', 'https://www.e-planetelec.fr/2295-product.html',
                   'https://www.e-planetelec.fr/2296-product.html', 'https://www.e-planetelec.fr/2297-product.html',
                   'https://www.e-planetelec.fr/2298-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2369-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2370-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2371-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2372-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2373-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2374-product.html',
                   'https://www.e-planetelec.fr/mecanismes-ovalis-schneider/2375-product.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1803-alrea-sachet-de-10-ressorts-pour'
                   '-transformation-interrupteur-en-poussoir-alb57944.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1849-alrea-va-et-vient-avec-cadre-saillie-blanc'
                   '-polaire-alb62051p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1833-alrea-kit-voyant-demi-touche-lampe-a-neon'
                   '-230v-1-5ma-blanc-polaire-alb61416p.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1805-alrea-va-et-vient-blanc-polaire'
                   '-alb61051p.html', 'https://www.e-planetelec.fr/appareillage-complet/1850-alrea-poussoir-o-f'
                   '-lumineux-faible-conso-avec-cadre-saillie-blanc-polaire-alb62052p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1834-alrea-kit-voyant-touche-lampe-a-neon-230v'
                   '-1-5ma-blanc-polaire-alb61417p.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1806-alrea-poussoir-o-f-lumineux-faible-conso'
                   '-blanc-polaire-alb61052p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1851-alrea-poussoir-a-fermeture-avec-cadre'
                   '-saillie-blanc-polaire-alb62053p.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1807-alrea-poussoir-a-fermeture-blanc-polaire'
                   '-alb61053p.html', 'https://www.e-planetelec.fr/appareillage-complet/1852-alrea-double-va-et-vient'
                   '-avec-cadre-saillie-blanc-polaire-alb62056p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1836-alrea-lampe-neon-de-rechange-pour-commande'
                   '-lumineuse-230v-0-5w-alb61422.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1808-alrea-interrupteur-bipolaire-ou'
                   '-permutateur-blanc-polaire-alb61054p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1853-alrea-va-et-vient-lumineux-forte-luminosite'
                   '-avec-cadre-saillie-blanc-polaire-alb62057p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1837-alrea-lampe-neon-de-rechange-pour-commande'
                   '-lumineuse-12v-0-4w-alb61423.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1809-alrea-double-va-et-vient-blanc-polaire'
                   '-alb61056p.html', 'https://www.e-planetelec.fr/appareillage-composable/1810-alrea-va-et-vient'
                   '-lumineux-forte-luminosite-blanc-polaire-alb61057p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1854-alrea-poussoir-avec-porte-etiquette-complet'
                   '-blanc-polaire-alb62062p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1838-alrea-lampe-neon-de-rechange-pour-commande'
                   '-lumineuse-230v-1-5w-alb61424.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1811-alrea-poussoir-a-fermeture-porte'
                   '-etiquette-sans-lampe-blanc-polaire-alb61062p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1855-alrea-prise-de-courant-2p-connexion-a-vis'
                   '-avec-cadre-saillie-blanc-polaire-alb62270p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1839-alrea-cadre-saillie-standard-simple'
                   '-62x62mm-profondeur-31mm-blanc-polaire-alb61441p.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1812-alrea-poussoir-lumineux-a-ferm-porte'
                   '-etiquette-forte-luminosite-blanc-polaire-alb61063p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1856-alrea-prise-de-courant-2p-t-complet-blanc'
                   '-polaire-alb62272p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1840-alrea-cadre-saillie-standard-double'
                   '-62x124mm-profondeur-31mm-blanc-polaire-alb61442p.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1813-alrea-va-et-vient-bouton-poussoir-blanc'
                   '-polaire-alb61081p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1857-alrea-prise-de-courant-2p-t-connexion'
                   '-rapide-cadre-saillie-blanc-polaire-alb62273p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1841-alrea-diffuseur-voyant-de-balisage-rouge'
                   '-alb61525.html', 'https://www.e-planetelec.fr/cadres-et-accessoires/1842-alrea-diffuseur-voyant'
                   '-de-balisage-vert-alb61526.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1814-alrea-double-poussoir-o-f-blanc-polaire'
                   '-alb61083p.html', 'https://www.e-planetelec.fr/appareillage-complet/1858-alrea-prise-de-courant'
                   '-2p-connexion-rapide-avec-cadre-saillie-blanc-polaire-alb62274p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1859-alrea-prise-tv-simple-male-blindee-1-sortie'
                   '-avec-cadre-saillie-blanc-polaire-alb62311p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1843-alrea-diffuseur-voyant-de-balisage-orange'
                   '-alb61527.html', 'https://www.e-planetelec.fr/appareillage-composable/1815-alrea-commande-vmc'
                   '-sans-position-arret-blanc-polaire-alb61158p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1860-alrea-rj45-simple-categorie-6-utp-avec'
                   '-cadre-saillie-blanc-polaire-alb62342p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1844-alrea-diffuseur-voyant-de-balisage'
                   '-incolore-alb61528.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1816-alrea-interrupteur-volets-roulants-blanc'
                   '-polaire-alb61197p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1861-alrea-conjoncteur-telephonique-8-plots-avec'
                   '-cadre-saillie-blanc-polaire-alb62366p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1845-alrea-lampe-e10-pour-voyant-de-balisage'
                   '-12v-4w-incandescent-transp-alb61530.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1817-alrea-poussoir-volets-roulants-blanc'
                   '-polaire-alb61199p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1862-alrea-obturateur-avec-cadre-saillie-blanc'
                   '-polaire-alb62420p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1846-alrea-lampe-e10-pour-voyant-de-balisage'
                   '-24v-4w-incandescent-transp-alb61531.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1818-alrea-prise-de-courant-2p-connexion-a'
                   '-vis-blanc-polaire-alb61270p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1863-alrea-double-prise-de-courant-2p-t'
                   '-connexion-a-vis-avec-cadre-saillie-blanc-p-alb62472p.html',
                   'https://www.e-planetelec.fr/cadres-et-accessoires/1847-alrea-lampe-e10-pour-voyant-de-balisage'
                   '-240v-0-75w-incandescent-transp-alb61532.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1819-alrea-prise-de-courant-2p-t-connexion-a'
                   '-vis-blanc-polaire-alb61272p.html',
                   'https://www.e-planetelec.fr/appareillage-complet/1864-alrea-double-prise-de-courant-2p-t'
                   '-connexion-rapide-avec-cadre-saillie-blanc-p-alb62473p.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1820-alrea-prise-de-courant-2p-t-connexion'
                   '-rapide-blanc-polaire-alb61273p.html',
                   'https://www.e-planetelec.fr/appareillage-composable/1821-alrea-prise-de-courant-2p-connexion'
                   '-rapide-blanc-polaire-alb61274p.html',
                   'https://www.e-planetelec.fr/support-universel-pour-mecanismes-45x45/2663-adaptateur-pour-appareil'
                   '-a-encastrer-2-modules.html',
                   'https://www.e-planetelec.fr/plaques-de-finition-pour-appareillage-45x45/2664-plaque-simple-blanc'
                   '.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2619-double-allumage-2-modules-10ax-250v'
                   '-blanc.html', 'https://www.e-planetelec.fr/plaques-de-finition-pour-appareillage-45x45/2665'
                   '-plaque-simple-noir-mat.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2620-double-allumage-2-modules-10ax-250v-noir-mat'
                   '.html', 'https://www.e-planetelec.fr/plaques-de-finition-pour-appareillage-45x45/2666-plaque'
                   '-double-blanc.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2621-va-et-vient-2-modules'
                   '-10ax-250v-blanc.html',
                   'https://www.e-planetelec.fr/plaques-de-finition-pour-appareillage-45x45/2667-plaque-double-noir'
                   '-mat.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2622-va-et-vient-2-modules-10ax-250v'
                   '-noir-mat.html', 'https://www.e-planetelec.fr/plaques-de-finition-pour-appareillage-45x45/2668'
                   '-plaque-triple-blanc.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2623-va-et-vient-1-module-10ax-250v-blanc.html',
                   'https://www.e-planetelec.fr/plaques-de-finition-pour-appareillage-45x45/2669-plaque-triple-noir'
                   '-mat.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2624-va-et-vient-1-module-10ax-250v'
                   '-noir-mat.html', 'https://www.e-planetelec.fr/plaques-de-finition-pour-appareillage-45x45/2670'
                   '-plaque-quadruple-blanc.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2625-va-et-vient-lumineux-2-modules-10ax-250v-blanc'
                   '.html', 'https://www.e-planetelec.fr/plaques-de-finition-pour-appareillage-45x45/2671-plaque'
                   '-quadruple-noir-mat.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2626-va-et-vient-lumineux-2-modules-10ax-250v-noir'
                   '-mat.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2627-va-et-vient-lumineux-1-module-10ax'
                   '-250v-blanc.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2628-va-et-vient-lumineux-1'
                   '-module-10ax-250v-noir-mat.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2629-va-et-vient-temoin-2-modules-10ax-250v-blanc'
                   '.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2630-va-et-vient-temoin-2-modules-10ax-250v'
                   '-noir-mat.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2631-va-et-vient-temoin-1-module'
                   '-10ax-250v-blanc.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2632-va-et-vient-temoin-1-module-10ax-250v-noir-mat'
                   '.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2633-permutateur-2-modules-10ax-250v-blanc'
                   '.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2634-permutateur-2-modules-10ax-250v-noir'
                   '-mat.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2635-permutateur-1-module-10ax-250v'
                   '-blanc.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2636-permutateur-1-module-10ax-250v'
                   '-noir-mat.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2637-poussoir-a-bascule-2-modules'
                   '-10a-250v-blanc.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2638-poussoir-a-bascule-2-modules-10a-250v-noir-mat'
                   '.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2639-poussoir-a-bascule-1-module-10a-250v'
                   '-blanc.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2640-poussoir-a-bascule-1-module-10a'
                   '-250v-noir-mat.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2641-poussoir-a-bascule-avec'
                   '-symbole-sonnette-2-modules-10a-250v-blanc.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2642-poussoir-a-bascule-avec-symbole-sonnette-2'
                   '-modules-10a-250v-noir-mat.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2643-poussoir-a-bascule-lumineux-2-modules-10a-250v'
                   '-blanc.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2644-poussoir-a-bascule-lumineux-2'
                   '-modules-10a-250v-noir-mat.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2645-poussoir-a-bascule-lumineux-1-module-10a-250v'
                   '-blanc.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2646-poussoir-a-bascule-lumineux-1'
                   '-module-10a-250v-noir-mat.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2647-va-et-vient-a-cle-2-modules-10ax-250v-blanc'
                   '.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2648-va-et-vient-a-cle-2-modules-10ax-250v'
                   '-noir-mat.html', 'https://www.e-planetelec.fr/mecanismes-45x45/2649-balisage-led-blanc-avec'
                   '-batterie-2-modules-blanc.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2650-prise-hdmi-avec-connecteur-1-module-blanc.html'
                   '', 'https://www.e-planetelec.fr/mecanismes-45x45/2651-support-rj45-2-modules-blanc.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2652-support-rj45-2-modules-noir-mat.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2653-prise-tv-r-2-modules-blanc.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2654-prise-tv-r-2-modules-noir-mat.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2655-sortie-de-cables-2-modules-blanc.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2656-sortie-de-cables-2-modules-noir-mat.html',
                   'https://www.e-planetelec.fr/mecanismes-45x45/2657-prise-de-courant-2pt-2-modules-16a-250v-blanc'
                   '.html', 'https://www.e-planetelec.fr/-mecanismes-seuls/1491-mureva-styl-bouton-poussoir-porte'
                   '-etiquette-composable-ip55-ik08-gris-mur34029.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1483-mureva-styl-va-et-vient-saillie'
                   '-ip55-ik08-connexion-auto-gris-mur35021.html',
                   'https://www.e-planetelec.fr/-accessoires/1552-mureva-styl-lot-de-10-etiquettes-mur34004.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1519-mureva-styl-obturateur-pour-trou-de-fixation'
                   '-ip55-gris-mur34206.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2887-prise-de-courant-2pt-plexo'
                   '-composable-gris-069551l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2905-boitier-saillie-2-embouts-a-membrane'
                   '-1-entree-1-poste-plexo-anthracite-069601l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/2993-prise-de-courant-2pt-plexo'
                   '-complet-encastre-gris-069831l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1492-mureva-styl-double-va-et-vient-composable-ip55'
                   '-ik08-connexion-auto-gris-mur35019.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/591-2p-t-f-b-gris-saillie-legrand'
                   '-069731.html', 'https://www.e-planetelec.fr/-boites-et-cadres/1531-mureva-styl-boite-3-postes'
                   '-horizontale-saillie-ip55-ik08-gris-mur37713.html',
                   'https://www.e-planetelec.fr/-accessoires/1553-mureva-styl-enjoliveur-avec-symbole-sonnette-ip55'
                   '-ik08-gris-mur34201.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1489-mureva-styl-va-et-vient-complet'
                   '-saillie-ip55-ik08-connexion-auto-blanc-mur39021.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2906-boitier-saillie-a-embouts-2-postes'
                   '-horizontaux-et-verticaux-plexo-anthracite-069602l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1493-mureva-styl-permutateur-composable-ip55-ik08'
                   '-connexion-auto-gris-mur35020.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2889-prise-de-courant-2x2pt'
                   '-horizontale-plexo-composable-gris-069562l.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1510-mureva-styl-prise-courant-2p-t'
                   '-saillie-ip55-ik08-connexion-auto-gris-mur35031.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/631-va-et-vient-gris-saillie-legrand'
                   '-069711.html', 'https://www.e-planetelec.fr/-boites-et-cadres/1532-mureva-styl-boite-1-poste'
                   '-saillie-ip55-ik08-gris-mur37911.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/2986-interrupteur-ou-va-et-vient'
                   '-10ax-250v-plexo-complet-encastre-gris-069811l.html',
                   'https://www.e-planetelec.fr/-accessoires/1554-mureva-styl-enjoliveur-avec-symbole-lumiere-ip55'
                   '-ik08-gris-mur34202.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/2994-poussoir-no-lumineux-plexo'
                   '-complet-encastre-gris-069832l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2907-boitier-saillie-a-embouts-3-postes'
                   '-horizontaux-et-verticaux-plexo-anthracite-069603l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1494-mureva-styl-va-et-vient-lumineux-led'
                   '-composable-ip55-ik08-connex-auto-gris-mur35025.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2890-prise-de-courant-2x2pt-verticale'
                   '-plexo-composable-gris-069563l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2948-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-complet-saillie-gris-069711l.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1533-mureva-styl-boite-2-postes-verticale-saillie'
                   '-ip55-ik08-gris-mur37912.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1518-mureva-styl-prise-de-courant-2p-t'
                   '-saillie-ip55-ik08-connex-auto-blanc-mur39030.html',
                   'https://www.e-planetelec.fr/-accessoires/1555-mureva-styl-enjoliveur-porte-etiquette-lumineux'
                   '-ip55-ik08-gris-mur34203.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1495-mureva-styl-bouton-poussoir-composable-ip55'
                   '-ik08-connexion-auto-gris-mur35027.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2891-prise-de-courant-3x2pt'
                   '-horizontale-plexo-composable-gris-069564l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2909-support-plaque-encastre-1-poste'
                   '-plexo-anthracite-069606l.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1484-mureva-styl-double-va-et-vient'
                   '-saillie-ip55-ik08-connexion-auto-gris-mur35022.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1534-mureva-styl-boite-2-postes-horizontale-saillie'
                   '-ip55-ik08-gris-mur37914.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3003-sortie-de-cable-20a-avec'
                   '-bornier-plexo-complet-encastre-gris-069849l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2956-prise-de-courant-2pt-plexo'
                   '-complet-saillie-gris-069731l.html',
                   'https://www.e-planetelec.fr/-accessoires/1556-mureva-styl-enjoliveur-avec-lentille-ip55-ik08-gris'
                   '-mur34204.html', 'https://www.e-planetelec.fr/-accessoires/1557-mureva-styl-enjoliveur-2-demi'
                   '-touche-ip55-ik08-gris-mur34205.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2859-interrupteur-temporise-lumineux'
                   '-plexo-composable-gris-069504l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2964-prise-de-courant-2x2pt'
                   '-horizontale-plexo-complet-saillie-gris-069768l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1496-mureva-styl-interrupt-bipolaire-composable'
                   '-ip55-ik08-connex-auto-gris-mur35034.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2910-support-plaque-encastre-2-postes'
                   '-montage-horizontalvertical-plexo-anthracite-069607l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3002-sortie-de-cable-16a-plexo'
                   '-complet-encastre-gris-069848l.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1485-mureva-styl-va-et-vient'
                   '-lumineuxled-saillie-ip55-ik08-connex-auto-gris-mur35024.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1535-mureva-styl-boite-1-poste-saillie-ip55-ik08'
                   '-blanc-mur39911.html',
                   'https://www.e-planetelec.fr/-accessoires/1558-mureva-styl-enjoliveur-avec-symbole-sonnette-ip55'
                   '-ik08-blanc-mur39201.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2949-interrupteur-ou-va-et-vient'
                   '-temoin-10ax-250v-plexo-complet-saillie-gris-069712l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1497-mureva-styl-bouton-poussoir-volets-roulants'
                   '-composable-ip55-ik07-gris-mur35042.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2861-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-composable-gris-069511l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2949-interrupteur-ou-va-et-vient'
                   '-temoin-10ax-250v-plexo-complet-saillie-gris-069712l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1497-mureva-styl-bouton-poussoir-volets-roulants'
                   '-composable-ip55-ik07-gris-mur35042.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2861-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-composable-gris-069511l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2911-product.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1487-mureva-styl-bouton-poussoir'
                   '-lumineux-led-saillie-ip55-ik08-gris-mur35028.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1537-mureva-styl-boite-3-postes-horizontale-saillie'
                   '-ip55-ik08-blanc-mur39913.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/2990-poussoir-no-nf-lumineux-porte'
                   '-etiquette-plexo-complet-encastre-gris-069824l.html',
                   'https://www.e-planetelec.fr/-accessoires/1559-mureva-styl-enjoliveur-avec-symbole-lumiere-ip55'
                   '-ik08-blanc-mur39202.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2927-product.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2950-interrupteur-ou-va-et-vient'
                   '-lumineux-10ax-250v-plexo-complet-saillie-gris-069713l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1498-mureva-styl-bouton-poussoir-lumineux-led'
                   '-composable-ip55-ik08-gris-mur35127.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2862-interrupteur-ou-va-et-vient'
                   '-temoin-10ax-250v-plexo-composable-gris-069512l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3004-sortie-de-cable-20a-32a-plexo'
                   '-complet-encastre-gris-069850l.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1488-mureva-styl-interrupteur-bipolaire'
                   '-saillie-ip55-ik08-connex-auto-gris-mur35033.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1538-mureva-styl-boite-2-postes-horizontale-saillie'
                   '-ip55-ik08-blanc-mur39914.html',
                   'https://www.e-planetelec.fr/-accessoires/1560-mureva-styl-enjoliveur-porte-etiquette-lumineux'
                   '-ip55-ik08-blanc-mur39203.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2860-transformeur-reversible-plexo'
                   '-composable-gris-069506l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2951-commande-double-interrupteur-ou'
                   '-poussoir-plexo-complet-saillie-gris-069715l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1499-mureva-styl-dble-bouton-poussoir-lumineux-led'
                   '-composable-ip55-ik07-gris-mur35228.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2935-product.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1500-mureva-styl-double-bouton-poussoir-composable'
                   '-ip55-ik07-gris-mur35326.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2937-product.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2869-commande-double-interrupteur-ou'
                   '-poussoir-plexo-composable-gris-069525l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3007-prise-de-courant-2pt-plexo'
                   '-complet-encastre-anthracite-069860l.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1490-mureva-styl-bouton-poussoir'
                   '-complet-saillie-ip55-ik08-connex-auto-blanc-mur39026.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1539-mureva-styl-cadre-2-postes-horizontal-encastre'
                   '-ip55-ik08-gris-mur34101.html',
                   'https://www.e-planetelec.fr/-accessoires/1561-mureva-styl-enjoliveur-avec-lentille-ip55-ik08'
                   '-blanc-mur39204.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2952-transformeur-reversible-plexo'
                   '-complet-saillie-gris-069719l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2953-poussoir-no-plexo-complet'
                   '-saillie-gris-069720l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1501-mureva-styl-va-et-vient-composable-ip55-ik08'
                   '-connexion-auto-gris-mur37021.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2938-support-plaque-encastre-1-poste'
                   '-plexo-gris-069681l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3006-poussoir-no-nf-lumineux-porte'
                   '-etiquette-plexo-complet-encastre-anthracite-069854l.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1540-mureva-styl-cadre-1-poste-encastre-ip55-ik08'
                   '-gris-mur34107.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2872-poussoir'
                   '-no-temoin-plexo-composable-gris-069533l.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1511-mureva-styl-prise-courant-2p-t-va'
                   '-et-vient-verti-saillie-ip55-ik08-gris-mur36025.html',
                   'https://www.e-planetelec.fr/-accessoires/1562-mureva-styl-enjoliveur-2-demi-touche-ip55-ik08'
                   '-blanc-mur39205.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1502-mureva-styl-double-va-et-vient-composable-ip55'
                   '-ik08-blanc-mur39022.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2939-support-plaque-encastre-2-postes'
                   '-montage-horizontalvertical-plexo-gris-069683l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2955-poussoir-no-lumineux-plexo'
                   '-complet-saillie-gris-069722l.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1541-mureva-styl-cadre-3-postes-horizontal-encastre'
                   '-ip55-ik08-gris-mur34109.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3011-sortie-de-cable-16a-plexo'
                   '-complet-encastre-anthracite-069878l.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1512-mureva-styl-double-prise-2p-t'
                   '-precablee-horiz-saillie-ip55-ik08-gris-mur36028.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2863-interrupteur-ou-va-et-vient'
                   '-lumineux-10ax-250v-plexo-composable-gris-069513l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1503-mureva-styl-permutateur-composable-ip55-ik08'
                   '-connexion-auto-blanc-mur39023.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2940-support-plaque-encastre-3-postes'
                   '-montage-horizontalvertical-plexo-gris-069687l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2972-prise-de-courant-2pt-plexo'
                   '-complet-saillie-anthracite-069791l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2870-commande-double-interrupteur-ou'
                   '-poussoir-lumineux-plexo-composable-gris-069526l.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1542-mureva-styl-cadre-2-postes-vertical-encastre'
                   '-ip55-ik08-gris-mur34151.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3013-interrupteur-ou-va-et-vient'
                   '-10ax-250v-plexo-complet-encastre-anthracite-069881l.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1513-mureva-styl-double-pc-2p-t-schuko'
                   '-precablee-horiz-saillie-ip55-ik08-gris-mur36029.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1514-mureva-styl-prise-de-courant-2p-t'
                   '-a-vis-saillie-ip55-ik08-gris-mur36030.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2864-interrupteur-ou-va-et-vient'
                   '-temoin-sans-neutre-4ax-250v-plexo-composable-gris-069515l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2969-prise-de-courant-2x2pt'
                   '-horizontale-plexo-complet-saillie-anthracite-069788l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3018-sortie-de-cable-20a-avec'
                   '-bornier-plexo-complet-encastre-anthracite-069899l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1504-mureva-styl-va-et-vient-lumineux-led'
                   '-composable-ip55-ik08-blanc-mur39024.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2942-boitier-saillie-2-embouts-a-membrane'
                   '-1-entree-1-poste-plexo-blanc-069689l.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1543-mureva-styl-cadre-2-postes-horizontal-encastre'
                   '-ip55-ik08-blanc-mur39101.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1515-mureva-styl-prise-de-courant-2p-t'
                   '-schuko-saillie-ip55-ik08-gris-mur36034.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2867-permutateur-plexo-composable'
                   '-gris-069521l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2957-interrupteur-ou-va-et-vient'
                   '-lumineux10ax-250v-plexo-complet-saillie-anthracite-069736l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1505-mureva-styl-bouton-poussoir-composable-ip55'
                   '-ik08-connexion-auto-blanc-mur39027.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2943-boitier-saillie-a-embouts-2-postes'
                   '-horizontaux-et-verticaux-plexo-blanc-069690l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3009-poussoir-no-nf-lumineux-porte'
                   '-etiquette-plexo-complet-encastre-blanc-069864l.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1544-mureva-styl-cadre-1-poste-encastre-ip55-ik08'
                   '-blanc-mur39107.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1516-mureva-styl-triple-pc-2p-t-horiz'
                   '-precablee-saillie-ip55-ik08-gris-mur36037.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2971-poussoir-no-plexo-complet'
                   '-saillie-anthracite-069790l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2941-boitier-saillie-a-embouts-3-postes'
                   '-horizontaux-et-verticaux-plexo-blanc-069688l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1506-mureva-styl-interrupteur-bipolaire-composable'
                   '-ip55-ik08-blanc-mur39033.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1545-mureva-styl-cadre-1-poste-a-griffes-encastre'
                   '-ip55-ik08-blanc-mur39108.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3014-sortie-de-cable-16a-plexo'
                   '-complet-encastre-blanc-069888l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2877-double-va-et-vient-pour-volets'
                   '-roulants-plexo-composable-gris-069538l.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1517-mureva-styl-3-pc-2p-t-schuko-horiz'
                   '-precablees-saillie-ip55-ik08-gris-mur36038.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2865-interrupteur-crepusculaire-plexo'
                   '-composable-neutre-069517l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/587-va-et-vient-gris-encastre'
                   '-legrand-69811.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1507-mureva-styl-bouton-poussoir-lumineux-led'
                   '-composable-ip55-ik08-blanc-mur39127.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2944-support-plaque-encastre-1-poste'
                   '-plexo-blanc-069692l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2962-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-complet-saillie-anthracite-069761l.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1546-mureva-styl-cadre-3-postes-horizontal-encastre'
                   '-ip55-ik08-blanc-mur39109.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1547-mureva-styl-cadre-2-postes-vertical-encastre'
                   '-ip55-ik08-blanc-mur39151.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2968-poussoir-no-lumineux-plexo'
                   '-complet-saillie-anthracite-069782l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2866-detecteur-de-mouvement-sans'
                   '-neutre-plexo-composable-transparent-069520l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1508-mureva-styl-bouton-poussoir-porte-etiquette'
                   '-composable-ip55-ik08-blanc-mur39129.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1525-mureva-styl-interrupteur-temporise'
                   '-led-saillie-ip55-ik08-gris-mur35067.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2945-support-plaque-encastre-2-postes'
                   '-montage-horizontalvertical-plexo-blanc-069694l.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1566-mureva-styl-entree-de-cable-triple-ip55-gris'
                   '-mur35007.html', 'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2954-interrupteur'
                   '-ou-va-et-vient-temoin-10ax-250v-plexo-complet-saillie-anthracite-069721l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2868-detecteur-de-mouvement-avec'
                   '-neutre-plexo-composable-transparent-069522l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1509-mureva-styl-va-et-vient-composable-ip55-ik08'
                   '-connexion-auto-blanc-mur39723.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1526-mureva-styl-interrupteur-temporise'
                   '-led-saillie-ip55-ik08-blanc-mur39067.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2947-support-plaque-encastre-3-postes'
                   '-montage-horizontalvertical-plexo-blanc-069698l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/652-plexo-double-va-et-vient'
                   '-encastre-blanc-legrand-069855.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1567-mureva-styl-entree-de-cable-simple-ip55-gris'
                   '-mur35008.html', 'https://www.e-planetelec.fr/-mecanismes-seuls/1520-mureva-styl-prise-de-courant'
                   '-2p-t-composable-ip55-ik08-connex-auto-gris-mur36133.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1698-mureva-styl-double-prise-2p-t'
                   '-precablee-horiz-saillie-ip55-ik08-blanc-mur36027.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2871-interrupteur-bipolaire-plexo'
                   '-composable-gris-069530l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2965-commande-double-interrupteur-ou'
                   '-poussoir-plexo-complet-saillie-anthracite-069775l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/652-plexo-double-va-et-vient'
                   '-encastre-blanc-legrand-069855.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1568-mureva-styl-entree-de-cable-triple-ip55-blanc'
                   '-mur39007.html', 'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2970-transformeur'
                   '-reversible-plexo-complet-saillie-anthracite-069789l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/3005-support-plaque-encastre-2-postes'
                   '-montage-horizontalvertical-plexo-sable-069853l.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1699-mureva-styl-triple-pc-2p-t-horiz'
                   '-precablee-saillie-ip55-ik08-blanc-mur36039.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2873-interrupteur-a-cles-ronis-2'
                   '-positions-plexo-composable-gris-069534l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/594-plexo-va-et-vient-blanc-encastre'
                   '-legrand-069851.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1569-mureva-styl-entree-de-cable-simple-ip55-blanc'
                   '-mur39008.html', 'https://www.e-planetelec.fr/-mecanismes-seuls/1522-mureva-styl-sortie-de-cable'
                   '-composable-ip55-ik08-connexion-auto-gris-mur37931.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/3008-boitier-saillie-2-embouts-a-membrane'
                   '-1-entree-1-poste-plexo-sable-069863l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2874-interrupteur-a-cles-ronis-3'
                   '-positions-plexo-composable-gris-069535l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2967-prise-de-courant-2pt-plexo'
                   '-complet-saillie-blanc-069781l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/596-plexo-poussoir-nonf-lumineux'
                   '-porte-etiquette-blanc-legrand-069864.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1570-mureva-styl-joint-complementaire-ip55-mur34007'
                   '.html', 'https://www.e-planetelec.fr/-mecanismes-seuls/1523-mureva-styl-prise-de-courant-2p-t-a'
                   '-vis-composable-ip55-ik08-gris-mur38030.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2959-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-complet-saillie-blanc-069751l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/3010-boitier-saillie-a-embouts-2-postes'
                   '-horizontaux-et-verticaux-plexo-sable-069867l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2875-poussoir-no-nf-lumineux-plexo'
                   '-composable-gris-069536l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/595-plexo-2pt-fb-blanc-encastre'
                   '-legrand-069870.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1524-mureva-styl-prise-courant-2p-t-composable-ip55'
                   '-ik08-connex-auto-blanc-mur39133.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2960-commande-double-interrupteur-ou'
                   '-poussoir-plexo-complet-saillie-blanc-069755l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2876-obturateur-plexo-composable-gris'
                   '-069537l.html', 'https://www.e-planetelec.fr/programme-plexo-accessoires/2928-product.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2961-poussoir-no-plexo-complet'
                   '-saillie-blanc-069760l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1527-mureva-styl-arret-d-urgence-a-cle-composable'
                   '-ip55-ik08-jaune-mur35052.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2878-double-poussoir-pour-volets'
                   '-roulants-plexo-composable-gris-069539l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2930-boitier-saillie-a-presse-etoupe-1'
                   '-entree-iso20-1-poste-plexo-gris-069656l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2855-rehausse-plexo-1-poste-inox-pour'
                   '-fixation-sur-panneau-sandwich-069492l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2963-poussoir-no-lumineux-plexo'
                   '-complet-saillie-blanc-069762l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1528-mureva-styl-arret-d-urgence-1-4-tour'
                   '-composable-ip55-ik08-jaune-mur35053.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2879-poussoir-no-plexo-composable'
                   '-gris-069540l.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2880-poussoir'
                   '-no-nf-plexo-composable-gris-069541l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2856-voyant-bleu-plexo-basse-tension-12v'
                   '-a-48v-069495l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1529-mureva-styl-interrupteur-a-cle-3-positions'
                   '-composable-ip55-ik08-gris-mur35061.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2966-prise-de-courant-2pt-plexo'
                   '-complet-saillie-sable-069776l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2881-poussoir-no-lumineux-plexo'
                   '-composable-gris-069542l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2976-lot-de-3-prises-2-va-et-vient'
                   '-commande-double-plexo-saillie-anthracite-069798l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2857-voyant-lumineux-bleu-plexo-230v'
                   '-069496l.html', 'https://www.e-planetelec.fr/-mecanismes-seuls/1530-mureva-styl-interrupteur-a'
                   '-cle-2-positions-composable-ip55-ik08-gris-mur35062.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2882-poussoir-no-nf-lumineux-porte'
                   '-etiquette-plexo-composable-gris-069544l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/590-poussoir-no-gris-saillie-legrand'
                   '-069720.html', 'https://www.e-planetelec.fr/programme-plexo-accessoires/2858-voyant-temoin-bleu'
                   '-plexo-230v-069498l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2883-coup-de-poing-d-urgence-plexo'
                   '-composable-grisjaune-069547l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2899-diffuseur-pour-voyant-de-balisage'
                   '-plexo-incolore-069588l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/588-va-et-vient-lumineux-gris-saillie'
                   '-legrand-069713.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1549-mureva-styl-adaptateur-pour-fonction-45x45'
                   '-composable-ip55-ik07-gris-mur35110.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2884-coup-de-poing-d-urgence'
                   '-deverrouillage-a-cle-plexo-composable-grisjaune-069548l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2900-diffuseur-pour-voyant-de-balisage'
                   '-plexo-vert-069589l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/589-double-va-et-vient-gris-saillie'
                   '-legrand-069715.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2885-coup-de-poing-d-urgence'
                   '-deverrouillage-14-tour-plexo-composable-grisjaune-069549l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2901-diffuseur-pour-voyant-de-balisage'
                   '-plexo-orange-069590l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1551-mureva-styl-adaptateur-pour-fonction-45x45'
                   '-composable-ip55-ik07-blanc-mur39110.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2886-sortie-de-cable-16a-plexo'
                   '-composable-gris-069550l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2902-diffuseur-pour-voyant-de-balisage'
                   '-plexo-rouge-069591l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1563-mureva-styl-voyant-de-balisage-a-composer-ip55'
                   '-mur34526.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2888-prise-de'
                   '-courant-2pt-a-detrompage-plexo-composable-gris-069553l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1564-mureva-styl-lampe-pour-voyant-de-balisage-ip55'
                   '-mur34555.html', 'https://www.e-planetelec.fr/programme-plexo-accessoires/2929-embout-presse'
                   '-etoupe-plexo-multi-cable-pg16-gris-069653l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2975-griffes-longues-et-entretoise-plexo'
                   '-069797l.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2892-prise-de'
                   '-courant-differentielle-plexo-composable-gris-069567l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1565-mureva-styl-lampe-led-pour-voyant-de-balisage'
                   '-ip55-mur34556.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2974-griffes-standard-et-entretoise-plexo'
                   '-069796l.html', 'https://www.e-planetelec.fr/-mecanismes-seuls/1896-mureva-styl-sortie-de-cable'
                   '-composable-ip55-ik08-connexion-auto-blanc-mur37933.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2893-adaptateur-plexo-pour-osmoz'
                   '-composable-gris-069568l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2958-piquet-de-jardin-plexo-avec-2-prises'
                   '-precablees-anthracite-069749l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2894-adaptateur-plexo-verrouillable-a'
                   '-volet-transparent-pour-mosaic-composable-gris-069579l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2895-adaptateur-plexo-a-volet'
                   '-transparent-pour-mosaic-composable-gris-069580l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2896-adaptateur-plexo-pour-prise-rj45'
                   '-mosaic-composable-gris-069581l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2897-adaptateur-plexo-pour-mosaic'
                   '-composable-gris-069582l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2898-voyant-de-balisage-et'
                   '-signalisation-plexo-composable-grisblanc-069583l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2908-interrupteur-temporise-lumineux'
                   '-plexo-composable-blanc-069604l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2912-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-composable-blanc-069611l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2913-interrupteur-ou-va-et-vient'
                   '-temoin-10ax-250v-plexo-composable-blanc-069612l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2914-interrupteur-ou-va-et-vient'
                   '-lumineux-10ax-250v-plexo-composable-blanc-069613l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2915-poussoir-no-nf-lumineux-plexo'
                   '-composable-blanc-069616l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2916-transformeur-reversible-plexo'
                   '-composable-blanc-069618l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2917-prise-de-courant-2pt-plexo'
                   '-composable-blanc-069621l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2918-commande-double-interrupteur-ou'
                   '-poussoir-plexo-composable-blanc-069625l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2919-double-va-et-vient-pour-volets'
                   '-roulants-plexo-composable-blanc-069629l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2920-poussoir-no-plexo-composable'
                   '-blanc-069630l.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2921-poussoir'
                   '-no-lumineux-plexo-composable-blanc-069632l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2922-prise-de-courant-2x2pt'
                   '-horizontale-plexo-composable-blanc-069642l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2923-prise-de-courant-2x2pt-verticale'
                   '-plexo-composable-blanc-069643l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2924-prise-de-courant-3x2pt'
                   '-horizontale-plexo-composable-blanc-069644l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2946-adaptateur-plexo-a-volet'
                   '-transparent-pour-mosaic-composable-blanc-069695l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2977-transformeur-reversible-plexo'
                   '-composable-anthracite-069800l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2978-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-composable-anthracite-069801l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2979-interrupteur-ou-va-et-vient'
                   '-temoin-10ax-250v-plexo-composable-anthracite-069802l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2980-interrupteur-ou-va-et-vient'
                   '-lumineux-10ax-250v-plexo-composable-anthracite-069803l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2981-interrupteur-temporise-lumineux'
                   '-plexo-composable-anthracite-069804l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2982-commande-double-interrupteur-ou'
                   '-poussoir-plexo-composable-anthracite-069805l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2985-poussoir-no-plexo-composable'
                   '-anthracite-069810l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2987-poussoir-no-lumineux-plexo'
                   '-composable-anthracite-069813l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2988-poussoir-no-nf-lumineux-plexo'
                   '-composable-anthracite-069816l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2991-interrupteur-bipolaire-plexo'
                   '-composable-anthracite-069827l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2995-obturateur-plexo-composable'
                   '-anthracite-069837l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/591-2p-t-f-b-gris-saillie-legrand'
                   '-069731.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2887-prise-de-courant'
                   '-2pt-plexo-composable-gris-069551l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2905-boitier-saillie-2-embouts-a-membrane'
                   '-1-entree-1-poste-plexo-anthracite-069601l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/2993-prise-de-courant-2pt-plexo'
                   '-complet-encastre-gris-069831l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2906-boitier-saillie-a-embouts-2-postes'
                   '-horizontaux-et-verticaux-plexo-anthracite-069602l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2889-prise-de-courant-2x2pt'
                   '-horizontale-plexo-composable-gris-069562l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/2986-interrupteur-ou-va-et-vient'
                   '-10ax-250v-plexo-complet-encastre-gris-069811l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/631-va-et-vient-gris-saillie-legrand'
                   '-069711.html', 'https://www.e-planetelec.fr/programme-plexo-complet-encastre/2994-poussoir-no'
                   '-lumineux-plexo-complet-encastre-gris-069832l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2907-boitier-saillie-a-embouts-3-postes'
                   '-horizontaux-et-verticaux-plexo-anthracite-069603l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2890-prise-de-courant-2x2pt-verticale'
                   '-plexo-composable-gris-069563l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2948-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-complet-saillie-gris-069711l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2891-prise-de-courant-3x2pt'
                   '-horizontale-plexo-composable-gris-069564l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2909-support-plaque-encastre-1-poste'
                   '-plexo-anthracite-069606l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3003-sortie-de-cable-20a-avec'
                   '-bornier-plexo-complet-encastre-gris-069849l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2956-prise-de-courant-2pt-plexo'
                   '-complet-saillie-gris-069731l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2859-interrupteur-temporise-lumineux'
                   '-plexo-composable-gris-069504l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2964-prise-de-courant-2x2pt'
                   '-horizontale-plexo-complet-saillie-gris-069768l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2910-support-plaque-encastre-2-postes'
                   '-montage-horizontalvertical-plexo-anthracite-069607l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3002-sortie-de-cable-16a-plexo'
                   '-complet-encastre-gris-069848l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2949-interrupteur-ou-va-et-vient'
                   '-temoin-10ax-250v-plexo-complet-saillie-gris-069712l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2861-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-composable-gris-069511l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2911-product.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/2989-poussoir-no-plexo-complet'
                   '-encastre-gris-069820l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2927-product.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2950-interrupteur-ou-va-et-vient'
                   '-lumineux-10ax-250v-plexo-complet-saillie-gris-069713l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2862-interrupteur-ou-va-et-vient'
                   '-temoin-10ax-250v-plexo-composable-gris-069512l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/2990-poussoir-no-nf-lumineux-porte'
                   '-etiquette-plexo-complet-encastre-gris-069824l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2860-transformeur-reversible-plexo'
                   '-composable-gris-069506l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2951-commande-double-interrupteur-ou'
                   '-poussoir-plexo-complet-saillie-gris-069715l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2935-product.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3004-sortie-de-cable-20a-32a-plexo'
                   '-complet-encastre-gris-069850l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2952-transformeur-reversible-plexo'
                   '-complet-saillie-gris-069719l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2937-product.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2869-commande-double-interrupteur-ou'
                   '-poussoir-plexo-composable-gris-069525l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3007-prise-de-courant-2pt-plexo'
                   '-complet-encastre-anthracite-069860l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2872-poussoir-no-temoin-plexo'
                   '-composable-gris-069533l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2953-poussoir-no-plexo-complet'
                   '-saillie-gris-069720l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2938-support-plaque-encastre-1-poste'
                   '-plexo-gris-069681l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3006-poussoir-no-nf-lumineux-porte'
                   '-etiquette-plexo-complet-encastre-anthracite-069854l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3011-sortie-de-cable-16a-plexo'
                   '-complet-encastre-anthracite-069878l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2863-interrupteur-ou-va-et-vient'
                   '-lumineux-10ax-250v-plexo-composable-gris-069513l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2939-support-plaque-encastre-2-postes'
                   '-montage-horizontalvertical-plexo-gris-069683l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2955-poussoir-no-lumineux-plexo'
                   '-complet-saillie-gris-069722l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3013-interrupteur-ou-va-et-vient'
                   '-10ax-250v-plexo-complet-encastre-anthracite-069881l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2940-support-plaque-encastre-3-postes'
                   '-montage-horizontalvertical-plexo-gris-069687l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2972-prise-de-courant-2pt-plexo'
                   '-complet-saillie-anthracite-069791l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2870-commande-double-interrupteur-ou'
                   '-poussoir-lumineux-plexo-composable-gris-069526l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2864-interrupteur-ou-va-et-vient'
                   '-temoin-sans-neutre-4ax-250v-plexo-composable-gris-069515l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2969-prise-de-courant-2x2pt'
                   '-horizontale-plexo-complet-saillie-anthracite-069788l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3018-sortie-de-cable-20a-avec'
                   '-bornier-plexo-complet-encastre-anthracite-069899l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2942-boitier-saillie-2-embouts-a-membrane'
                   '-1-entree-1-poste-plexo-blanc-069689l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2867-permutateur-plexo-composable'
                   '-gris-069521l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2957-interrupteur-ou-va-et-vient'
                   '-lumineux10ax-250v-plexo-complet-saillie-anthracite-069736l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2943-boitier-saillie-a-embouts-2-postes'
                   '-horizontaux-et-verticaux-plexo-blanc-069690l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3009-poussoir-no-nf-lumineux-porte'
                   '-etiquette-plexo-complet-encastre-blanc-069864l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2971-poussoir-no-plexo-complet'
                   '-saillie-anthracite-069790l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2941-boitier-saillie-a-embouts-3-postes'
                   '-horizontaux-et-verticaux-plexo-blanc-069688l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/3014-sortie-de-cable-16a-plexo'
                   '-complet-encastre-blanc-069888l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2877-double-va-et-vient-pour-volets'
                   '-roulants-plexo-composable-gris-069538l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/587-va-et-vient-gris-encastre'
                   '-legrand-69811.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2865-interrupteur-crepusculaire-plexo'
                   '-composable-neutre-069517l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2944-support-plaque-encastre-1-poste'
                   '-plexo-blanc-069692l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2962-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-complet-saillie-anthracite-069761l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2968-poussoir-no-lumineux-plexo'
                   '-complet-saillie-anthracite-069782l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2866-detecteur-de-mouvement-sans'
                   '-neutre-plexo-composable-transparent-069520l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2945-support-plaque-encastre-2-postes'
                   '-montage-horizontalvertical-plexo-blanc-069694l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2954-interrupteur-ou-va-et-vient'
                   '-temoin-10ax-250v-plexo-complet-saillie-anthracite-069721l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2868-detecteur-de-mouvement-avec'
                   '-neutre-plexo-composable-transparent-069522l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2947-support-plaque-encastre-3-postes'
                   '-montage-horizontalvertical-plexo-blanc-069698l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/652-plexo-double-va-et-vient'
                   '-encastre-blanc-legrand-069855.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2871-interrupteur-bipolaire-plexo'
                   '-composable-gris-069530l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2965-commande-double-interrupteur-ou'
                   '-poussoir-plexo-complet-saillie-anthracite-069775l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/3015-support-plaque-encastre-1-poste'
                   '-plexo-sable-069890l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2970-transformeur-reversible-plexo'
                   '-complet-saillie-anthracite-069789l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/3005-support-plaque-encastre-2-postes'
                   '-montage-horizontalvertical-plexo-sable-069853l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/594-plexo-va-et-vient-blanc-encastre'
                   '-legrand-069851.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2873-interrupteur-a-cles-ronis-2'
                   '-positions-plexo-composable-gris-069534l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2967-prise-de-courant-2pt-plexo'
                   '-complet-saillie-blanc-069781l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/3008-boitier-saillie-2-embouts-a-membrane'
                   '-1-entree-1-poste-plexo-sable-069863l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/596-plexo-poussoir-nonf-lumineux'
                   '-porte-etiquette-blanc-legrand-069864.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2874-interrupteur-a-cles-ronis-3'
                   '-positions-plexo-composable-gris-069535l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-encastre/595-plexo-2pt-fb-blanc-encastre'
                   '-legrand-069870.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2959-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-complet-saillie-blanc-069751l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/3010-boitier-saillie-a-embouts-2-postes'
                   '-horizontaux-et-verticaux-plexo-sable-069867l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2875-poussoir-no-nf-lumineux-plexo'
                   '-composable-gris-069536l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2960-commande-double-interrupteur-ou'
                   '-poussoir-plexo-complet-saillie-blanc-069755l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2876-obturateur-plexo-composable-gris'
                   '-069537l.html', 'https://www.e-planetelec.fr/programme-plexo-accessoires/2928-product.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2878-double-poussoir-pour-volets'
                   '-roulants-plexo-composable-gris-069539l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2930-boitier-saillie-a-presse-etoupe-1'
                   '-entree-iso20-1-poste-plexo-gris-069656l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2961-poussoir-no-plexo-complet'
                   '-saillie-blanc-069760l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2879-poussoir-no-plexo-composable'
                   '-gris-069540l.html', 'https://www.e-planetelec.fr/programme-plexo-accessoires/2855-rehausse-plexo'
                   '-1-poste-inox-pour-fixation-sur-panneau-sandwich-069492l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2963-poussoir-no-lumineux-plexo'
                   '-complet-saillie-blanc-069762l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2880-poussoir-no-nf-plexo-composable'
                   '-gris-069541l.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2880-poussoir'
                   '-no-nf-plexo-composable-gris-069541l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2856-voyant-bleu-plexo-basse-tension-12v'
                   '-a-48v-069495l.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2881-poussoir'
                   '-no-lumineux-plexo-composable-gris-069542l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/2976-lot-de-3-prises-2-va-et-vient'
                   '-commande-double-plexo-saillie-anthracite-069798l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2857-voyant-lumineux-bleu-plexo-230v'
                   '-069496l.html', 'https://www.e-planetelec.fr/programme-plexo-accessoires/2858-voyant-temoin-bleu'
                   '-plexo-230v-069498l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/590-poussoir-no-gris-saillie-legrand'
                   '-069720.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2882-poussoir-no-nf'
                   '-lumineux-porte-etiquette-plexo-composable-gris-069544l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/588-va-et-vient-lumineux-gris-saillie'
                   '-legrand-069713.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2883-coup-de-poing-d-urgence-plexo'
                   '-composable-grisjaune-069547l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2899-diffuseur-pour-voyant-de-balisage'
                   '-plexo-incolore-069588l.html',
                   'https://www.e-planetelec.fr/programme-plexo-complet-saillie/589-double-va-et-vient-gris-saillie'
                   '-legrand-069715.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2884-coup-de-poing-d-urgence'
                   '-deverrouillage-a-cle-plexo-composable-grisjaune-069548l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2900-diffuseur-pour-voyant-de-balisage'
                   '-plexo-vert-069589l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2885-coup-de-poing-d-urgence'
                   '-deverrouillage-14-tour-plexo-composable-grisjaune-069549l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2901-diffuseur-pour-voyant-de-balisage'
                   '-plexo-orange-069590l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2886-sortie-de-cable-16a-plexo'
                   '-composable-gris-069550l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2902-diffuseur-pour-voyant-de-balisage'
                   '-plexo-rouge-069591l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2929-embout-presse-etoupe-plexo-multi'
                   '-cable-pg16-gris-069653l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2888-prise-de-courant-2pt-a'
                   '-detrompage-plexo-composable-gris-069553l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2892-prise-de-courant-differentielle'
                   '-plexo-composable-gris-069567l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2975-griffes-longues-et-entretoise-plexo'
                   '-069797l.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2893-adaptateur'
                   '-plexo-pour-osmoz-composable-gris-069568l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2974-griffes-standard-et-entretoise-plexo'
                   '-069796l.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2894-adaptateur'
                   '-plexo-verrouillable-a-volet-transparent-pour-mosaic-composable-gris-069579l.html',
                   'https://www.e-planetelec.fr/programme-plexo-accessoires/2958-piquet-de-jardin-plexo-avec-2-prises'
                   '-precablees-anthracite-069749l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2895-adaptateur-plexo-a-volet'
                   '-transparent-pour-mosaic-composable-gris-069580l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2896-adaptateur-plexo-pour-prise-rj45'
                   '-mosaic-composable-gris-069581l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2897-adaptateur-plexo-pour-mosaic'
                   '-composable-gris-069582l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2898-voyant-de-balisage-et'
                   '-signalisation-plexo-composable-grisblanc-069583l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2908-interrupteur-temporise-lumineux'
                   '-plexo-composable-blanc-069604l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2912-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-composable-blanc-069611l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2913-interrupteur-ou-va-et-vient'
                   '-temoin-10ax-250v-plexo-composable-blanc-069612l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2914-interrupteur-ou-va-et-vient'
                   '-lumineux-10ax-250v-plexo-composable-blanc-069613l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2915-poussoir-no-nf-lumineux-plexo'
                   '-composable-blanc-069616l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2916-transformeur-reversible-plexo'
                   '-composable-blanc-069618l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2917-prise-de-courant-2pt-plexo'
                   '-composable-blanc-069621l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2918-commande-double-interrupteur-ou'
                   '-poussoir-plexo-composable-blanc-069625l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2919-double-va-et-vient-pour-volets'
                   '-roulants-plexo-composable-blanc-069629l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2920-poussoir-no-plexo-composable'
                   '-blanc-069630l.html', 'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2921-poussoir'
                   '-no-lumineux-plexo-composable-blanc-069632l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2922-prise-de-courant-2x2pt'
                   '-horizontale-plexo-composable-blanc-069642l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2923-prise-de-courant-2x2pt-verticale'
                   '-plexo-composable-blanc-069643l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2924-prise-de-courant-3x2pt'
                   '-horizontale-plexo-composable-blanc-069644l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2946-adaptateur-plexo-a-volet'
                   '-transparent-pour-mosaic-composable-blanc-069695l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2977-transformeur-reversible-plexo'
                   '-composable-anthracite-069800l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2978-interrupteur-ou-va-et-vient-10ax'
                   '-250v-plexo-composable-anthracite-069801l.html',
                   'https://www.e-planetelec.fr/programme-plexo-composable-ip55/2979-interrupteur-ou-va-et-vient'
                   '-temoin-10ax-250v-plexo-composable-anthracite-069802l.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1491-mureva-styl-bouton-poussoir-porte-etiquette'
                   '-composable-ip55-ik08-gris-mur34029.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1483-mureva-styl-va-et-vient-saillie'
                   '-ip55-ik08-connexion-auto-gris-mur35021.html',
                   'https://www.e-planetelec.fr/-accessoires/1552-mureva-styl-lot-de-10-etiquettes-mur34004.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1519-mureva-styl-obturateur-pour-trou-de-fixation'
                   '-ip55-gris-mur34206.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1492-mureva-styl-double-va-et-vient-composable-ip55'
                   '-ik08-connexion-auto-gris-mur35019.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1531-mureva-styl-boite-3-postes-horizontale-saillie'
                   '-ip55-ik08-gris-mur37713.html',
                   'https://www.e-planetelec.fr/-accessoires/1553-mureva-styl-enjoliveur-avec-symbole-sonnette-ip55'
                   '-ik08-gris-mur34201.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1489-mureva-styl-va-et-vient-complet'
                   '-saillie-ip55-ik08-connexion-auto-blanc-mur39021.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1493-mureva-styl-permutateur-composable-ip55-ik08'
                   '-connexion-auto-gris-mur35020.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1510-mureva-styl-prise-courant-2p-t'
                   '-saillie-ip55-ik08-connexion-auto-gris-mur35031.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1532-mureva-styl-boite-1-poste-saillie-ip55-ik08'
                   '-gris-mur37911.html', 'https://www.e-planetelec.fr/-accessoires/1554-mureva-styl-enjoliveur-avec'
                   '-symbole-lumiere-ip55-ik08-gris-mur34202.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1494-mureva-styl-va-et-vient-lumineux-led'
                   '-composable-ip55-ik08-connex-auto-gris-mur35025.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1533-mureva-styl-boite-2-postes-verticale-saillie'
                   '-ip55-ik08-gris-mur37912.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1518-mureva-styl-prise-de-courant-2p-t'
                   '-saillie-ip55-ik08-connex-auto-blanc-mur39030.html',
                   'https://www.e-planetelec.fr/-accessoires/1555-mureva-styl-enjoliveur-porte-etiquette-lumineux'
                   '-ip55-ik08-gris-mur34203.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1495-mureva-styl-bouton-poussoir-composable-ip55'
                   '-ik08-connexion-auto-gris-mur35027.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1484-mureva-styl-double-va-et-vient'
                   '-saillie-ip55-ik08-connexion-auto-gris-mur35022.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1534-mureva-styl-boite-2-postes-horizontale-saillie'
                   '-ip55-ik08-gris-mur37914.html',
                   'https://www.e-planetelec.fr/-accessoires/1556-mureva-styl-enjoliveur-avec-lentille-ip55-ik08-gris'
                   '-mur34204.html', 'https://www.e-planetelec.fr/-accessoires/1557-mureva-styl-enjoliveur-2-demi'
                   '-touche-ip55-ik08-gris-mur34205.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1496-mureva-styl-interrupt-bipolaire-composable'
                   '-ip55-ik08-connex-auto-gris-mur35034.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1485-mureva-styl-va-et-vient'
                   '-lumineuxled-saillie-ip55-ik08-connex-auto-gris-mur35024.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1535-mureva-styl-boite-1-poste-saillie-ip55-ik08'
                   '-blanc-mur39911.html',
                   'https://www.e-planetelec.fr/-accessoires/1558-mureva-styl-enjoliveur-avec-symbole-sonnette-ip55'
                   '-ik08-blanc-mur39201.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1497-mureva-styl-bouton-poussoir-volets-roulants'
                   '-composable-ip55-ik07-gris-mur35042.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1486-mureva-styl-bouton-poussoir'
                   '-saillie-ip55-ik08-connexion-auto-gris-mur35026.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1536-mureva-styl-boite-2-postes-verticale-saillie'
                   '-ip55-ik08-blanc-mur39912.html',
                   'https://www.e-planetelec.fr/-accessoires/1559-mureva-styl-enjoliveur-avec-symbole-lumiere-ip55'
                   '-ik08-blanc-mur39202.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1498-mureva-styl-bouton-poussoir-lumineux-led'
                   '-composable-ip55-ik08-gris-mur35127.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1487-mureva-styl-bouton-poussoir'
                   '-lumineux-led-saillie-ip55-ik08-gris-mur35028.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1537-mureva-styl-boite-3-postes-horizontale-saillie'
                   '-ip55-ik08-blanc-mur39913.html',
                   'https://www.e-planetelec.fr/-accessoires/1560-mureva-styl-enjoliveur-porte-etiquette-lumineux'
                   '-ip55-ik08-blanc-mur39203.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1499-mureva-styl-dble-bouton-poussoir-lumineux-led'
                   '-composable-ip55-ik07-gris-mur35228.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1488-mureva-styl-interrupteur-bipolaire'
                   '-saillie-ip55-ik08-connex-auto-gris-mur35033.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1538-mureva-styl-boite-2-postes-horizontale-saillie'
                   '-ip55-ik08-blanc-mur39914.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1490-mureva-styl-bouton-poussoir'
                   '-complet-saillie-ip55-ik08-connex-auto-blanc-mur39026.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1539-mureva-styl-cadre-2-postes-horizontal-encastre'
                   '-ip55-ik08-gris-mur34101.html',
                   'https://www.e-planetelec.fr/-accessoires/1561-mureva-styl-enjoliveur-avec-lentille-ip55-ik08'
                   '-blanc-mur39204.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1500-mureva-styl-double-bouton-poussoir-composable'
                   '-ip55-ik07-gris-mur35326.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1540-mureva-styl-cadre-1-poste-encastre-ip55-ik08'
                   '-gris-mur34107.html', 'https://www.e-planetelec.fr/-appareillage-saillie-complet/1511-mureva-styl'
                   '-prise-courant-2p-t-va-et-vient-verti-saillie-ip55-ik08-gris-mur36025.html',
                   'https://www.e-planetelec.fr/-accessoires/1562-mureva-styl-enjoliveur-2-demi-touche-ip55-ik08'
                   '-blanc-mur39205.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1501-mureva-styl-va-et-vient-composable-ip55-ik08'
                   '-connexion-auto-gris-mur37021.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1541-mureva-styl-cadre-3-postes-horizontal-encastre'
                   '-ip55-ik08-gris-mur34109.html',
                   'https://www.e-planetelec.fr/-appareillage-saillie-complet/1512-mureva-styl-double-prise-2p-t'
                   '-precablee-horiz-saillie-ip55-ik08-gris-mur36028.html',
                   'https://www.e-planetelec.fr/-mecanismes-seuls/1502-mureva-styl-double-va-et-vient-composable-ip55'
                   '-ik08-blanc-mur39022.html',
                   'https://www.e-planetelec.fr/-boites-et-cadres/1542-mureva-styl-cadre-2-postes-vertical-encastre'
                   '-ip55-ik08-gris-mur34151.html',
                   'https://www.e-planetelec.fr/sortie-de-cable/154-sortie-de-cable-32a-legrand.html',
                   'https://www.e-planetelec.fr/accessoires-pour-pose-de-boitiers/254-multifix-gabarit-de-marquage-et'
                   '-niveau-imt35043.html',
                   'https://www.e-planetelec.fr/boite-d-encastrement/114-boite-d-encastrement-1-poste-diam68mm.html',
                    'https://www.e-planetelec.fr/boitier-multimedia-pour-installation-audio-video/2618-boitier'
                    '-multimedia-a-encastrer-avec-porte-2x8-modules.html',
                    'https://www.e-planetelec.fr/boites-d-encastrement-a-sceller/3097-boite-maconnerie-diam-67-prof'
                    '-40-52103-eur-ohm.html',
                    'https://www.e-planetelec.fr/outillage/277-scie-cloche-multi-materiaux-diam-68.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement/115-boite-d-encastrement-2-postes-diam67mm'
                    '-entraxe-71mm.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement-bbc/2685-boite-d-encastrement-bbc-1-poste'
                    '-080021-legrand.html',
                    'https://www.e-planetelec.fr/dcl/1779-kit-point-de-centre-dcl-air-metic-diam67-douille-e27-53064'
                    '.html', 'https://www.e-planetelec.fr/mecanisme-odace-blanc/149-sortie-de-cable-20a-blanc'
                    '-schneider-odace-s520662.html',
                    'https://www.e-planetelec.fr/outillage/3057-scie-cloche-eco-diametre-85mm-eur-ohm-52406.html',
                    'https://www.e-planetelec.fr/boites-d-encastrement-a-sceller/3098-boite-maconnerie-1-poste'
                    '-75x75mm-prof-40-52105-eur-ohm.html',
                    'https://www.e-planetelec.fr/dcl/1608-kit-point-de-centre-bbc-diametre-68-p36859.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement/116-boite-d-encastrement-3-postes-diam67mm'
                    '-entraxe-71mm.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement-bbc/2686-boite-d-encastrement-bbc-2-postes'
                    '-080022-legrand.html',
                    'https://www.e-planetelec.fr/sortie-de-cable/1647-sortie-de-cable-2032a-p11032-sib.html',
                    'https://www.e-planetelec.fr/sortie-de-cable/1724-eur-ohm-60092-sortie-de-cable-20-32a.html',
                    'https://www.e-planetelec.fr/boites-d-encastrement-a-sceller/3100-boite-maconnerie-2-postes-prof'
                    '-40-horvert-52115-eur-ohm.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement-bbc/2687-boite-d-encastrement-bbc-3-postes'
                    '-080023-legrand.html',
                    'https://www.e-planetelec.fr/dcl/120-kit-dcl-bbc-point-de-centre-diametre-67mm-fiche-douille-e27'
                    '-capri-723552.html',
                    'https://www.e-planetelec.fr/dcl/1712-boite-d-applique-dcl-air-metic-diam-54-53074.html',
                    'https://www.e-planetelec.fr/boites-d-encastrement-a-sceller/3101-boite-maconnerie-3-postes-prof'
                    '-40-horvert-52117-eur-ohm.html',
                    'https://www.e-planetelec.fr/sortie-de-cable/1792-cadre-saillie-1-poste-pour-socle-et-sortie-de'
                    '-cables-100x100x36mm-055849.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement-bbc/2688-boite-d-encastrement-bbc-4-postes'
                    '-080024-legrand.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement/1655-boite-d-encastrement-1-poste-imt35915'
                    '-schneider-electric.html',
                    'https://www.e-planetelec.fr/dcl/1713-kit-applique-e27-dcl-air-metic-diam-67-douille-e27-53077'
                    '.html', 'https://www.e-planetelec.fr/boite-d-encastrement-bbc/1744-eur-ohm-52061-boite-1-poste'
                    '-etanche-a-l-air-67-mm-p40-mm.html',
                    'https://www.e-planetelec.fr/sortie-de-cable/2331-eur-ohm-60091-sortie-de-cable-1020a.html',
                    'https://www.e-planetelec.fr/boites-d-encastrement-a-sceller/3099-boite-maconnerie-1-poste-pour'
                    '-2032a-prof-40-52109-eur-ohm.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement/1656-boite-d-encastrement-2-postes-imt35925'
                    '-schneider-electric.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement/1694-boite-d-encastrement-3-postes-imt35935'
                    '-schneider-electric.html',
                    'https://www.e-planetelec.fr/sortie-de-cable/229-sortie-de-cable-1020a-p11016-sib.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement-bbc/1745-eur-ohm-52064-boite-d-encastrement'
                    '-etanche-2p-h-v-xl-air-metic-vis-prof-40mm.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement/1695-boite-d-encastrement-4-postes-imt35945'
                    '-schneider-electric.html',
                    'https://www.e-planetelec.fr/dcl/1600-douille-e27-a-vis-fiche-p11127.html',
                    'https://www.e-planetelec.fr/sortie-de-cable/2617-blm-605200-sortie-de-cable-20a.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement-bbc/1746-eur-ohm-52066-boite-d-encastrement'
                    '-etanche-3p-h-v-xl-air-metic-vis-prof-40mm.html',
                    'https://www.e-planetelec.fr/mecanisme-odace-alu/3060-sortie-de-cable-20a-alu-schneider-odace'
                    '-s530662.html', 'https://www.e-planetelec.fr/boite-d-encastrement/2113-boite-d-encastrement-2'
                    '-postes-entraxe-57-mm-alb71333-schneider-electric.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement-bbc/1747-eur-ohm-52068-boite-d-encastrement'
                    '-etanche-4p-h-v-xl-air-metic-vis-prof-40mm.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement/2114-boite-d-encastrement-3-postes-entraxe-57'
                    '-mm-alb71337-schneider-electric.html',
                    'https://www.e-planetelec.fr/dcl/1778-kit-couvercle-dcl-o120-piton-100-douille-e27-53052.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement-bbc/117-boite-d-encastrement-1-poste-diam67mm'
                    '-bbc-imt35001.html',
                    'https://www.e-planetelec.fr/dcl/1903-kit-point-de-centre-dcl-saillie-douille-e27-53098.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement-bbc/118-boite-d-encastrement-2-postes-diam67mm'
                    '-bbc-imt35000.html', 'https://www.e-planetelec.fr/dcl/1911-couvercle-dcl-applique-diam-88-53041'
                    '.html', 'https://www.e-planetelec.fr/boite-d-encastrement-bbc/119-boite-d-encastrement-3-postes'
                    '-diam67mm-bbc-imt35031.html',
                    'https://www.e-planetelec.fr/boite-d-encastrement-bbc/253-boite-d-encastrement-4-postes-diam67mm'
                    '-bbc-imt35033.html', 'https://www.e-planetelec.fr/detecteur-de-mouvements-mural/225-detecteur-de'
                    '-mouvement-200-niko-351-03160.html',
                    'https://www.e-planetelec.fr/lampes-a-poser/2445-antoine-lampe-a-poser.html#/144'
                    '-couleur_du_cable_d_alimentation-chanvre',
                    'https://www.e-planetelec.fr/detecteurs-de-mouvements/228-telecommande-p-ir-niko-351-25320.html',
                     'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1299-zoom-14w-1450lm-3000k-matt'
                     '-white-30280143.html',
                     'https://www.e-planetelec.fr/luminaire-suspendu/1339-zoom-pendant-12w-1150lm-40-3000k-white'
                     '-30530123w.html', 'https://www.e-planetelec.fr/-accessoires/1634-boite-de-connexion-luminaire'
                     '-2e1s.html', 'https://www.e-planetelec.fr/lampe-a-poser/3220-lampe-a-poser-et-portable-yoru'
                     '-coloris-noir-arkos.html',
                     'https://www.e-planetelec.fr/applique-murale/1742-sarlam-applique-ip44-led-prismaline-sans'
                     '-interrupteur-sl189800.html',
                     'https://www.e-planetelec.fr/lampes-a-poser/2446-ariane-lampe-a-poser.html#/144'
                     '-couleur_du_cable_d_alimentation-chanvre',
                     'https://www.e-planetelec.fr/lampes-a-suspendre/2448-albatros-suspension-bois.html#/141'
                     '-couleur_du_cable_d_alimentation-blanc/147-diametre_suspension-65cm',
                     'https://www.e-planetelec.fr/selection-professionnelle/284-encastre-595x595-leds-ip54-40w-panel'
                     '-led.html#/122-couleur_eclairage-3000k_blanc_chaud',
                     'https://www.e-planetelec.fr/-accessoires/1914-protection-de-spot-eur-ohm-52139.html',
                     'https://www.e-planetelec.fr/projecteur-portatif/2115-projecteur-portatif-25w-led-avec-pc-2p-t'
                     '-et-prise-usb-plwork25w.html',
                     'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1300-zoom-14w-1500lm-4000k-matt'
                     '-white-30280144.html',
                     'https://www.e-planetelec.fr/detecteur-de-mouvements-mural/2135-detecteur-de-mouvement-exterieur'
                     '-180-niko-350-20058.html',
                     'https://www.e-planetelec.fr/etanche-led/2485-luminaire-profiles-lineaire-led-tp-strong-48w'
                     '-4000k-kanlux-33170.html',
                     'https://www.e-planetelec.fr/luminaire-suspendu/1340-zoom-pendant-12w-1150lm-40-3000k-black'
                     '-30530123n.html', 'https://www.e-planetelec.fr/hublot-led/2510--plafonnier-rond-beno-led-24w-nw'
                     '-o-gr-33341.html', 'https://www.e-planetelec.fr/detecteur-de-mouvements-360/2511-detecteur-de'
                     '-mouvement-pir-merge-jq-kanlux-07691.html',
                     'https://www.e-planetelec.fr/lampe-a-poser/3222--lampe-a-poser-et-portable-yoru-coloris-blanc'
                     '-arkos.html', 'https://www.e-planetelec.fr/ampoule-led/2594-led-gu10-6w-3000k-38.html',
                     'https://www.e-planetelec.fr/downlight-led/1870-flat-top-elecman.html#/122-couleur_eclairage'
                     '-3000k_blanc_chaud/134-puissance_led-6w',
                     'https://www.e-planetelec.fr/lampes-a-poser/2447-archimede-lampe-a-poser.html#/144'
                     '-couleur_du_cable_d_alimentation-chanvre',
                     'https://www.e-planetelec.fr/applique-murale/1902-applique-ip44-led-prismaline-avec-interrupteur'
                     '-tactile-avec-led-700lm-sl189801.html',
                     'https://www.e-planetelec.fr/projecteur-portatif/2116-projecteur-portatif-45w-led-avec-2-pc-2pt'
                     '-plwork45w.html', 'https://www.e-planetelec.fr/lampes-a-suspendre/2476-albert-suspension-bois'
                     '.html', 'https://www.e-planetelec.fr/spot-led/539-kit-spot-gu10-led-blanc-fix-avec-lampe-6w'
                     '.html', 'https://www.e-planetelec.fr/-accessoires/2120-brassard-lumineux-led-running-pl8710499'
                     '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1301-zoom-14w-1450lm-3000k'
                     '-matt-black-30290143.html',
                     'https://www.e-planetelec.fr/etanche-led/2484-luminaire-profiles-lineaire-led-tp-strong-75w'
                     '-4000k-kanlux-33171.html',
                     'https://www.e-planetelec.fr/detecteur-de-mouvements-mural/2140-detecteur-de-mouvement-exterieur'
                     '-180-noir-niko-350-20158.html',
                     'https://www.e-planetelec.fr/spot-led-downlight/1733-delta-6w-3000k-white-31000063w.html',
                     'https://www.e-planetelec.fr/hublot-led/2166-hublot-led-25w-ip65-ik10-4000k.html',
                     'https://www.e-planetelec.fr/luminaire-suspendu/1341-belly-250mm-e27-white-30432500w.html',
                     'https://www.e-planetelec.fr/applique-murale/1291-wide-18w-600mm-1500lm-4000k-30220184.html',
                     'https://www.e-planetelec.fr/detecteur-de-mouvements-360/227-detecteur-swiss-garde-360-presence'
                     '-mini-niko-351-25480.html',
                     'https://www.e-planetelec.fr/etanche-led/1869-etanche-tubulaire-slim-led-ip67-ik10-tubiled-30w'
                     '.html', 'https://www.e-planetelec.fr/ampoule-led/2596-led-gu10-6w-4000k-38.html',
                     'https://www.e-planetelec.fr/lampes-a-suspendre/2474-azur-suspension-bois.html',
                     'https://www.e-planetelec.fr/projecteur-portatif/2117-projecteur-portatif-30w-ip65-2600-lumens'
                     '-pl56010.html', 'https://www.e-planetelec.fr/-accessoires/2121-lampe-frontale-led-3w-200-lumens'
                     '-plled26.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1302-zoom-14w'
                     '-1500lm-4000k-matt-black-30290144.html',
                     'https://www.e-planetelec.fr/detecteur-esylux/3086-product.html',
                     'https://www.e-planetelec.fr/luminaire-hublot/1262-blok-round-led-ip65-7w-550lm-4000k-30170074'
                     '.html', 'https://www.e-planetelec.fr/downlight-led/3096-flat-top-square-18w-1440lm-4000k'
                     '-30890184.html', 'https://www.e-planetelec.fr/spot-led-downlight/1734-delta-6w-3000k-black'
                     '-31000063n.html', 'https://www.e-planetelec.fr/luminaire-suspendu/1342-belly-250mm-e27-black'
                     '-white-30432500nw.html',
                     'https://www.e-planetelec.fr/luminaire-suspendu/1343-belly-250mm-e27-black-gold-30432500ng.html'
                     '', 'https://www.e-planetelec.fr/detecteur-esylux/3084-product.html',
                     'https://www.e-planetelec.fr/detecteurs-de-mouvements/1604-boite-de-montage-en-saillie-ronde-351'
                     '-25420.html', 'https://www.e-planetelec.fr/etanche-led/583-etanche-tubulaire-led-ip67-ik10'
                     '-tubiled-40w.html#/123-couleur_eclairage-4000k_blanc_neutre/133-diffuseur-transparent',
                     'https://www.e-planetelec.fr/reglette-etanche/1286-line-5w-311mm-500lm-4000k-30110054.html',
                     'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1303-zoom-25w-2200lm-3000k-matt'
                     '-white-30280253.html',
                     'https://www.e-planetelec.fr/luminaire-hublot/1263-surf-14w-300mm-1100lm-3000k-30380143.html',
                     'https://www.e-planetelec.fr/luminaires-exterieurs/1373-rook-round-led-ip65-7w-525lm-4000k'
                     '-anthracite-30670074a.html',
                     'https://www.e-planetelec.fr/luminaire-suspendu/1343-belly-250mm-e27-black-gold-30432500ng.html'
                     '', 'https://www.e-planetelec.fr/applique-murale/1292-wide-36w-1200mm-3000lm-4000k-30220364.html'
                     '', 'https://www.e-planetelec.fr/detecteur-de-mouvements-360/267-detecteur-de-mouvement-360-16m'
                     '-230v-a-encastrer-niko-351-25340.html',
                     'https://www.e-planetelec.fr/ampoule-led/2598-led-gu10-75w-2700k-38.html',
                     'https://www.e-planetelec.fr/detecteur-esylux/3083-product.html',
                     'https://www.e-planetelec.fr/detecteur-de-mouvements-360/1602-detecteur-de-mouvement-230-vac-360'
                     '-1-canal-30-m-a-encastrer-rond-351-25065.html',
                     'https://www.e-planetelec.fr/reglette-etanche/1287-line-9w-572mm-900lm-4000k-30110094.html',
                     'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1304-zoom-25w-2300lm-4000k-matt'
                     '-white-30280254.html',
                     'https://www.e-planetelec.fr/luminaire-hublot/1264-surf-14w-300mm-1150lm-4000k-30380144.html',
                     'https://www.e-planetelec.fr/applique-murale/1357-pixel-7w-420lm-3000k-white-30590073w.html',
                     'https://www.e-planetelec.fr/ampoule-led/2579-led-gu10-75w-3000k-38.html',
                     'https://www.e-planetelec.fr/luminaires-exterieurs/1375-rook-round-single-ip54-gu10-1x50w'
                     '-anthracite-30680010a.html',
                     'https://www.e-planetelec.fr/luminaire-suspendu/1344-belly-330mm-e27-white-30433300w.html',
                     'https://www.e-planetelec.fr/ampoule-led/441-pack-10-ampoules-led-gu10-75w.html',
                     'https://www.e-planetelec.fr/detecteur-de-mouvements-360/1601-detecteur-de-mouvement-230-vac-360'
                     '-1-canal-30-m-montage-en-saillie-351-25050.html',
                     'https://www.e-planetelec.fr/lampes-a-suspendre/2479-ariel-suspension-bois.html',
                     'https://www.e-planetelec.fr/etanche-led/1418-hydra-led-60w-ip65-1500mm-6000lm-4000k-30022604'
                     '.html', 'https://www.e-planetelec.fr/reglette-etanche/1288-line-12w-872mm-1200lm-4000k-30110124'
                     '.html', 'https://www.e-planetelec.fr/detecteur-esylux/3117-telecommande-pour-detecteur-de'
                     '-mouvements-esylux-em10425509-remote-control-mdipdi.html',
                     'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1305-zoom-25w-2200lm-3000k-matt'
                     '-black-30290253.html',
                     'https://www.e-planetelec.fr/luminaire-hublot/1265-surf-18w-340mm-1400lm-3000k-30380183.html',
                     'https://www.e-planetelec.fr/applique-murale/1358-pixel-7w-420lm-3000k-black-30590073n.html',
                     'https://www.e-planetelec.fr/luminaires-exterieurs/1374-rook-round-led-ip65-14w-1050lm-4000k'
                     '-anthracite-30670144a.html',
                     'https://www.e-planetelec.fr/luminaire-suspendu/1345-belly-330mm-e27-black-white-30433300nw.html'
                     '', 'https://www.e-planetelec.fr/etanche-led/1412-hydra-led-30w-ip65-1500mm-3000lm-4000k'
                     '-30021304.html', 'https://www.e-planetelec.fr/spot-led-downlight/1173-man-fix-50w-gu10-matt'
                     '-white-30340010.html',
                     'https://www.e-planetelec.fr/reglette-etanche/1289-line-16w-1172mm-1600lm-4000k-30110164.html',
                     'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1306-zoom-25w-2300lm-4000k-matt'
                     '-black-30290254.html',
                     'https://www.e-planetelec.fr/luminaire-hublot/1266-surf-18w-340mm-1450lm-4000k-30380184.html',
                     'https://www.e-planetelec.fr/applique-murale/1359-miral-ip44-20w-1400lm-3000k-30730203.html',
                     'https://www.e-planetelec.fr/luminaires-exterieurs/1376-rook-round-double-ip54-gu10-2x50w'
                     '-anthracite-30680020a.html',
                     'https://www.e-planetelec.fr/ampoule-led/2593-led-gu10-75w-4000k-38.html',
                     'https://www.e-planetelec.fr/luminaire-suspendu/1346-belly-330mm-e27-black-gold-30433300ng.html'
                     '', 'https://www.e-planetelec.fr/lampes-a-suspendre/2475-ava-suspension-bois.html',
                     'https://www.e-planetelec.fr/detecteur-esylux/3081-product.html',
                     'https://www.e-planetelec.fr/detecteur-esylux/3085-product.html',
                     'https://www.e-planetelec.fr/ampoule-led/2186-led-gu10-dimmable-75w-38.html',
                     'https://www.e-planetelec.fr/spot-led-downlight/1174-man-fix-50w-gu10-nickel-satin-30340020.html'
                     '', 'https://www.e-planetelec.fr/reglette-etanche/1290-line-accessories-kit-30110000.html',
                     'https://www.e-planetelec.fr/luminaire-hublot/1267-surf-sensor-24w-1560lm-3000k-30380243s.html',
                      'https://www.e-planetelec.fr/applique-murale/1360-tulip-ip44-12w-840lm-3000k-30720123.html',
                      'https://www.e-planetelec.fr/luminaire-suspendu/1347-iris-290mm-e27-black-30432900n.html',
                      'https://www.e-planetelec.fr/detecteur-esylux/3085-product.html',
                      'https://www.e-planetelec.fr/spot-led-downlight/1175-man-tilt-50w-gu10-matt-white-30340030.html'
                      '', 'https://www.e-planetelec.fr/ampoule-led/2592-led-gu10-dimmable-75w-38-3000k.html',
                      'https://www.e-planetelec.fr/luminaire-hublot/1268-surf-sensor-24w-1680lm-4000k-30380244s.html'
                      '', 'https://www.e-planetelec.fr/applique-murale/1361-wally-round-single-1x50w-gu10-matt-white'
                      '-30510150w.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1378-rook-square-double'
                      '-ip54-gu10-2x50w-anthracite-30680040a.html',
                      'https://www.e-planetelec.fr/luminaire-suspendu/1348-iris-290mm-e27-black-gold-30432900ng.html'
                      '', 'https://www.e-planetelec.fr/detecteur-esylux/3082-product.html',
                      'https://www.e-planetelec.fr/spot-led-downlight/1176-man-tilt-50w-gu10-nickel-satin-30340040'
                      '.html', 'https://www.e-planetelec.fr/luminaire-hublot/1271-kamel-ip65-20w-1700lm-4000k-white'
                      '-30600204w.html', 'https://www.e-planetelec.fr/applique-murale/1362-wally-round-single-1x50w'
                      '-gu10-matt-black-30510150n.html',
                      'https://www.e-planetelec.fr/luminaires-exterieurs/1379-alpha-ip65-6w-400lm-3000k-white'
                      '-30620063w.html', 'https://www.e-planetelec.fr/ampoule-led/425-ampoule-vintage-standard-e27'
                      '.html', 'https://www.e-planetelec.fr/luminaire-suspendu/1349-iris-290mm-e27-brass-30432900br'
                      '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1177-man-square-tilt-50w-gu10-matt'
                      '-white-30340050.html',
                      'https://www.e-planetelec.fr/luminaire-hublot/1272-kamel-ip65-20w-1700lm-4000k-anthracite'
                      '-30600204a.html', 'https://www.e-planetelec.fr/applique-murale/1363-wally-round-double-2x50w'
                      '-gu10-matt-white-30510250w.html',
                      'https://www.e-planetelec.fr/luminaires-exterieurs/1380-alpha-ip65-6w-400lm-3000k-anthracite'
                      '-30620063a.html', 'https://www.e-planetelec.fr/luminaire-suspendu/1350-iris-375mm-e27-black'
                      '-30433750n.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1311-reflector'
                      '-zoom-15-14w-30281400.html',
                      'https://www.e-planetelec.fr/spot-led-downlight/1178-man-square-tilt-50w-gu10-nickel-satin'
                      '-30340060.html', 'https://www.e-planetelec.fr/luminaire-hublot/1273-kamel-ip65-sensor-20w'
                      '-1700lm-4000k-white-30600204ws.html',
                      'https://www.e-planetelec.fr/applique-murale/1364-wally-round-double-2x50w-gu10-matt-black'
                      '-30510250n.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1381-alpha-ip65-6w-450lm'
                      '-4000k-white-30620064w.html',
                      'https://www.e-planetelec.fr/luminaire-suspendu/1351-iris-375mm-e27-black-gold-30433750ng.html'
                      '', 'https://www.e-planetelec.fr/spot-led-downlight/1171-foc-ip65-8w-640lm-3000k-dimmable'
                      '-30750083.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1312-reflector'
                      '-zoom-24-14w-30291400.html',
                      'https://www.e-planetelec.fr/luminaire-hublot/1274-kamel-ip65-sensor-20w-1700lm-4000k'
                      '-anthracite-30600204as.html',
                      'https://www.e-planetelec.fr/applique-murale/1365-wally-square-single-1x50w-gu10-matt-white'
                      '-30520150w.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1382-alpha-ip65-6w-450lm'
                      '-4000k-anthracite-30620064a.html',
                      'https://www.e-planetelec.fr/luminaire-suspendu/1352-iris-375mm-e27-brass-30433750br.html',
                      'https://www.e-planetelec.fr/spot-led-downlight/1172-foc-ip65-8w-680lm-4000k-dimmable-30750084'
                      '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1313-reflector-zoom-15-25w'
                      '-30280015.html', 'https://www.e-planetelec.fr/applique-murale/1366-wally-square-single-1x50w'
                      '-gu10-matt-black-30520150n.html',
                      'https://www.e-planetelec.fr/luminaires-exterieurs/1383-alpha-ip65-12w-780lm-3000k-white'
                      '-30620123w.html',
                      'https://www.e-planetelec.fr/luminaire-suspendu/1353-up-200mm-e27-white-30432000w.html',
                      'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1314-reflector-zoom-24-25w-30280024'
                      '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1179-cobby-7w-550lm-3000k-matt-white'
                      '-30390073.html', 'https://www.e-planetelec.fr/ampoule-led/439-ampoule-smd-led-12w-e27.html'
                      '#/128-reference_lampe-10010122_12w_2700k',
                      'https://www.e-planetelec.fr/luminaire-hublot/1276-kamel-ip65-30w-2500lm-4000k-anthracite'
                      '-30600304a.html', 'https://www.e-planetelec.fr/applique-murale/1367-wally-square-double-2x50w'
                      '-gu10-matt-white-30520250w.html',
                      'https://www.e-planetelec.fr/luminaires-exterieurs/1384-alpha-ip65-12w-780lm-3000k-anthracite'
                      '-30620123a.html',
                      'https://www.e-planetelec.fr/luminaire-suspendu/1354-up-200mm-e27-black-30432000n.html',
                      'https://www.e-planetelec.fr/luminaire-suspendu/1355-up-200mm-e27-brass-30432000br.html',
                      'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1315-reflector-zoom-15-40w-30290015'
                      '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1180-cobby-7w-575lm-4000k-matt-white'
                      '-30390074.html', 'https://www.e-planetelec.fr/luminaire-hublot/1277-kamel-ip65-sensor-30w'
                      '-2500lm-4000k-white-30600304ws.html',
                      'https://www.e-planetelec.fr/applique-murale/1368-wally-square-double-2x50w-gu10-matt-black'
                      '-30520250n.html', 'https://www.e-planetelec.fr/ampoule-led/550-lampe-led-8w-e27-a60.html',
                      'https://www.e-planetelec.fr/luminaires-exterieurs/1385-alpha-ip65-12w-840lm-4000k-white'
                      '-30620124w.html', 'https://www.e-planetelec.fr/luminaire-suspendu/1356-up-200mm-e27-copper'
                      '-30432000c.html', 'https://www.e-planetelec.fr/ampoule-led/1739-ampoule-smd-led-9w-2700k-e27'
                      '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1316-reflector-zoom-24-40w'
                      '-30290024.html', 'https://www.e-planetelec.fr/spot-led-downlight/1181-ringo-7w-590lm-3000k'
                      '-30150073.html', 'https://www.e-planetelec.fr/reglette-etanche/1410-hydra-led-25w-ip65-1200mm'
                      '-2500lm-4000k-30021254.html',
                      'https://www.e-planetelec.fr/luminaire-hublot/1278-kamel-ip65-sensor-30w-2500lm-4000k'
                      '-anthracite-30600304as.html',
                      'https://www.e-planetelec.fr/luminaires-exterieurs/1369-mask-ip65-10w-750lm-3000k-white'
                      '-30660103w.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1386-alpha-ip65-12w-840lm'
                      '-4000k-anthracite-30620124a.html',
                      'https://www.e-planetelec.fr/luminaires-exterieurs/1387-alpha-ip65-16w-1040lm-3000k-white'
                      '-30620163w.html', 'https://www.e-planetelec.fr/luminaire-suspendu/1473-clap-9w-30700009.html',
                       'https://www.e-planetelec.fr/ampoule-led/1740-ampoule-smd-led-9w-4000k-e27.html',
                       'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1317-track-230v-3l-n-surface-2mt'
                       '-white-30440002w.html',
                       'https://www.e-planetelec.fr/spot-led-downlight/1182-ringo-7w-650lm-4000k-30150074.html',
                       'https://www.e-planetelec.fr/luminaire-hublot/1283-pascal-18w-1440lm-3000-4000-6000k-30710180'
                       '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1370-mask-ip65-10w-750lm-3000k'
                       '-anthracite-30660103a.html',
                       'https://www.e-planetelec.fr/luminaires-exterieurs/1371-mask-ip65-10w-800lm-4000k-white'
                       '-30660104w.html',
                       'https://www.e-planetelec.fr/luminaires-exterieurs/1388-alpha-ip65-16w-1040lm-3000k-anthracite'
                       '-30620163a.html',
                       'https://www.e-planetelec.fr/luminaire-suspendu/1474-clap-display-7w-30700007.html',
                       'https://www.e-planetelec.fr/ampoule-led/2441-lampe-lino-s19-led-7w-4000k-700lm.html',
                       'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1318-track-230v-3l-n-surface-2mt'
                       '-black-30440002n.html',
                       'https://www.e-planetelec.fr/spot-led-downlight/1183-ringo-10w-950lm-3000k-30150103.html',
                       'https://www.e-planetelec.fr/luminaires-exterieurs/1372-mask-ip65-10w-800lm-4000k-anthracite'
                       '-30660104a.html',
                       'https://www.e-planetelec.fr/luminaires-exterieurs/1389-alpha-ip65-16w-1120lm-4000k-white'
                       '-30620164w.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1319-track-230v'
                       '-3l-n-surface-3mt-white-30440003w.html',
                       'https://www.e-planetelec.fr/spot-led-downlight/1184-ringo-10w-1000lm-4000k-30150104.html',
                       'https://www.e-planetelec.fr/luminaires-exterieurs/1390-alpha-ip65-16w-1120lm-4000k-anthracite'
                       '-30620164a.html', 'https://www.e-planetelec.fr/applique-murale/2440-sarlam-applique-standard'
                       '-ip24-et-ik04-avec-interrupteur-et-prise-rasoir-189869.html',
                       'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1320-track-230v-3l-n-surface-3mt'
                       '-black-30440003n.html',
                       'https://www.e-planetelec.fr/luminaires-exterieurs/1391-kat-ip65-3w-3000k-150lm-white'
                       '-30630033w.html',
                       'https://www.e-planetelec.fr/applique-murale/3038-wide-36w-ip44-1200mm-3000lm-4000k-30980364'
                       '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1321-track-230v-live-end'
                       '-connector-white-30440010w.html',
                       'https://www.e-planetelec.fr/luminaire-hublot/1617-blok-oval-guard-ip44-e27-30180008.html',
                       'https://www.e-planetelec.fr/luminaires-exterieurs/1392-kat-ip65-3w-3000k-150lm-anthracite'
                       '-30630033a.html',
                       'https://www.e-planetelec.fr/spot-led-downlight/1187-steam-7w-ip65-595lm-3000k-30050073.html',
                        'https://www.e-planetelec.fr/reglette-etanche/1416-hydra-led-50w-ip65-1200mm-5000lm-4000k'
                        '-30022504.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1322-track-230v'
                        '-live-end-connector-black-30440010n.html',
                        'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1323-track-230v-central-connector'
                        '-white-30440011w.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1393-kat-ip65-3w-4000k-180lm-white'
                        '-30630034w.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1188-steam-square-7w-ip65-595lm-3000k'
                        '-30060073.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1324-track-230v'
                        '-central-connector-black-30440011n.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1394-kat-ip65-3w-4000k-180lm-anthracite'
                        '-30630034a.html',
                        'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1325-track-230v-universal-angle'
                        '-white-30440012w.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1395-kat-ip65-9w-3000k-450lm-white'
                        '-30630093w.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1191-loop-50w-gu10-30350010.html',
                        'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1326-track-230v-universal-angle'
                        '-black-30440012n.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1396-kat-ip65-9w-3000k-450lm-anthracite'
                        '-30630093a.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1192-loop-square-50w-gu10-30350020.html',
                        'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1327-track-230v-90-angle-white'
                        '-30440013w.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1397-kat-ip65-9w-4000k-520lm-white'
                        '-30630094w.html',
                        'https://www.e-planetelec.fr/reglette-etanche/1422-hydra-led-60w-ip65-1500mm-6000lm-4000k'
                        '-linkable-30022604lk.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1193-loop-rectangular-50w-gu10-30350030.html'
                        '', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1328-track-230v-90-angle'
                        '-black-30440013n.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1398-kat-ip65-9w-4000k-520lm-anthracite'
                        '-30630094a.html',
                        'https://www.e-planetelec.fr/reglette-etanche/1468-planet-2-150w-19500lm-120-4000k-30701504'
                        '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1423-flash-10w-ip65-750lm-3000k'
                        '-30240103.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1194-magnum-30w-2400lm-3000k-white-30570303w'
                        '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1329-track-230v-t-joint'
                        '-white-30440016w.html',
                        'https://www.e-planetelec.fr/reglette-etanche/1469-planet-2-200w-26000lm-120-4000k-30702004'
                        '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1424-flash-10w-ip65-800lm-4000k'
                        '-30240104.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1195-magnum-30w-2400lm-3000k-black-30570303n'
                        '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1330-track-230v-t-joint'
                        '-black-30440016n.html',
                        'https://www.e-planetelec.fr/reglette-etanche/1470-planet-2-60-beam-angle-lens-150w-30700000'
                        '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1425-flash-20w-ip65-1500lm-3000k'
                        '-30240203.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1196-magnum-30w-2500lm-4000k-white-30570304w'
                        '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1331-track-230v'
                        '-suspension-kit-white-30440017w.html',
                        'https://www.e-planetelec.fr/reglette-etanche/1471-planet-2-60-beam-angle-lens-200w-30700001'
                        '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1426-flash-20w-ip65-1600lm-4000k'
                        '-30240204.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1197-magnum-30w-2500lm-4000k-black-30570304n'
                        '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1332-track-230v'
                        '-suspension-kit-black-30440017n.html',
                        'https://www.e-planetelec.fr/reglette-etanche/1472-planet-2-surface-fixed-bracket-30700002'
                        '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1427-flash-30w-ip65-2250lm-3000k'
                        '-30240303.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1198-magnum-30w-2400lm-3000k-white-1-10v-dimm'
                        '-30580303w.html',
                        'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1333-track-230v-contact-mini'
                        '-joint-white-30445000w.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1428-flash-30w-ip65-2400lm-4000k-30240304'
                        '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1199-magnum-30w-2400lm-3000k-black-1'
                        '-10v-dimm-30580303n.html',
                        'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1334-track-230v-contact-mini'
                        '-joint-black-30445000n.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1429-flash-50w-ip65-3750lm-3000k-30240503'
                        '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1200-magnum-30w-2500lm-4000k-white-1'
                        '-10v-dimm-30580304w.html',
                        'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1335-track-230v-closing-end-white'
                        '-30445001w.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1430-flash-50w-ip65-4000lm-4000k-30240504'
                        '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1336-track-230v-closing'
                        '-end-black-30445001n.html',
                        'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1337-track-230v-mechanical-mini'
                        '-joint-white-30440018w.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1431-flash-100w-ip65-7500lm-3000k-30241003'
                        '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1338-track-230v'
                        '-mechanical-mini-joint-black-30440018n.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1432-flash-100w-ip65-8000lm-4000k-30241004'
                        '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1433-flash-150w-ip65-11250lm'
                        '-3000k-30241503.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1205-magnum-30w-2500lm-4000k-black-dali-push'
                        '-dimm-30760304n.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1434-flash-150w-ip65-12000lm-4000k'
                        '-30241504.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1206-magnum-60w-4800lm-3000k-white-30570603w'
                        '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1435-flash-200w-ip65-15000lm'
                        '-3000k-30242003.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1436-flash-200w-ip65-16000lm-4000k'
                        '-30242004.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1207-magnum-60w-4800lm-3000k-black-30570603n'
                        '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1437-flash-300w-ip65-24000lm'
                        '-4000k-30243004.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1437-flash-300w-ip65-24000lm-4000k'
                        '-30243004.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1209-magnum-60w-5000lm-4000k-black-30570604n'
                        '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1438-flash-400w-ip65-32000lm'
                        '-4000k-30244004.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1210-magnum-60w-4800lm-3000k-white-1-10v-dimm'
                        '-30580603w.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1211-magnum-60w-4800lm-3000k-black-1-10v-dimm'
                        '-30580603n.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1212-magnum-60w-5000lm-4000k-white-1-10v-dimm'
                        '-30580604w.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1213-magnum-60w-5000lm-4000k-black-1-10v-dimm'
                        '-30580604n.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1214-magnum-60w-4800lm-3000k-white-dali-push'
                        '-dimm-30760603w.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1215-magnum-60w-4800lm-3000k-black-dali-push'
                        '-dimm-30760603n.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1450-tuck-ip65-30w-2400lm-4000k-white'
                        '-30260304.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1216-magnum-60w-5000lm-4000k-white-dali-push'
                        '-dimm-30760604w.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1217-magnum-60w-5000lm-4000k-black-dali-push'
                        '-dimm-30760604n.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1218-magnum-15-reflector-30570300.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1219-magnum-24-reflector-30570301.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1220-petit-2w-ip44-240lm-3000k-30310023.html'
                        '', 'https://www.e-planetelec.fr/spot-led-downlight/1221-petit-square-2w-ip44-240lm-3000k'
                        '-30320023.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1456-vega-ip65-10w-800lm'
                        '-4000k-white-30650104w.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1222-petit-rectangular-4w-480lm-3000k'
                        '-30320043.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1457-vega-ip65-10w-800lm'
                        '-4000k-black-30650104n.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1458-vega-ip65-30w-2400lm-4000k-white'
                        '-30650304w.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1223-nest-50w-gu10-30330010.html',
                        'https://www.e-planetelec.fr/luminaires-exterieurs/1459-vega-ip65-30w-2400lm-4000k-black'
                        '-30650304n.html',
                        'https://www.e-planetelec.fr/spot-led-downlight/1224-nest-asymmetric-50w-gu10-30330020.html',
                         'https://www.e-planetelec.fr/luminaires-exterieurs/1460-vega-ip65-50w-4000lm-4000k-white'
                         '-30650504w.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1225-rot-7-5w-850lm-3000k-30420073.html',
                         'https://www.e-planetelec.fr/luminaires-exterieurs/1461-vega-ip65-50w-4000lm-4000k-black'
                         '-30650504n.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1226-rot-7-5w-875lm-4000k-30420074.html',
                         'https://www.e-planetelec.fr/luminaires-exterieurs/1462-vega-ip65-100w-8000lm-4000k-white'
                         '-30651004w.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1227-rot-17w-1650lm-3000k-30420173.html',
                         'https://www.e-planetelec.fr/luminaires-exterieurs/1463-vega-ip65-100w-8000lm-4000k-black'
                         '-30651004n.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1228-rot-17w-1750lm-4000k-30420174.html',
                         'https://www.e-planetelec.fr/luminaires-exterieurs/1464-vega-ip65-150w-12000lm-4000k-white'
                         '-30651504w.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1229-rot-32w-3150lm-3000k-30420323.html',
                         'https://www.e-planetelec.fr/luminaires-exterieurs/1465-vega-ip65-150w-12000lm-4000k-black'
                         '-30651504n.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1230-rot-32w-3250lm-4000k-30420324.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1231-swing-35w-4000k-3850lm-30410354.html',
                         'https://www.e-planetelec.fr/luminaires-exterieurs/1466-vega-ip65-200w-16000lm-4000k-white'
                         '-30652004w.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1232-sixty-40w-no-flickering-3400lm-3000k'
                         '-30140403.html',
                         'https://www.e-planetelec.fr/luminaires-exterieurs/1467-vega-ip65-200w-16000lm-4000k-black'
                         '-30652004n.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1233-sixty-40w-no-flickering-3600lm-4000k'
                         '-30140404.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1234-sixty-40w-no-flickering-3400lm-3000k-1'
                         '-10v-dimm-30770403.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1235-sixty-40w-no-flickering-3600lm-4000k-1'
                         '-10v-dimm-30770404.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1236-sixty-40w-no-flickering-3400lm-3000k'
                         '-dali-push-dimm-30780403.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1237-sixty-40w-no-flickering-3600lm-4000k'
                         '-dali-push-dimm-30780404.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1238-suspension-kit-sixty-hydra-30021000'
                         '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1239-sixty-surface-kit-30140000'
                         '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1240-moon-9w-500lm-3000k-30560093'
                         '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1241-moon-24w-1600lm-3000k-30560243'
                         '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1299-zoom-14w-1450lm'
                         '-3000k-matt-white-30280143.html',
                         'https://www.e-planetelec.fr/lampe-a-poser/3220-lampe-a-poser-et-portable-yoru-coloris-noir'
                         '-arkos.html', 'https://www.e-planetelec.fr/-accessoires/1634-boite-de-connexion-luminaire'
                         '-2e1s.html', 'https://www.e-planetelec.fr/luminaire-suspendu/1339-zoom-pendant-12w-1150lm'
                         '-40-3000k-white-30530123w.html',
                         'https://www.e-planetelec.fr/selection-professionnelle/284-encastre-595x595-leds-ip54-40w'
                         '-panel-led.html#/122-couleur_eclairage-3000k_blanc_chaud',
                         'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1300-zoom-14w-1500lm-4000k-matt'
                         '-white-30280144.html',
                         'https://www.e-planetelec.fr/lampe-a-poser/3222--lampe-a-poser-et-portable-yoru-coloris'
                         '-blanc-arkos.html',
                         'https://www.e-planetelec.fr/luminaire-suspendu/1340-zoom-pendant-12w-1150lm-40-3000k-black'
                         '-30530123n.html',
                         'https://www.e-planetelec.fr/etanche-led/2485-luminaire-profiles-lineaire-led-tp-strong-48w'
                         '-4000k-kanlux-33170.html',
                         'https://www.e-planetelec.fr/applique-murale/1742-sarlam-applique-ip44-led-prismaline-sans'
                         '-interrupteur-sl189800.html',
                         'https://www.e-planetelec.fr/hublot-led/2510--plafonnier-rond-beno-led-24w-nw-o-gr-33341'
                         '.html', 'https://www.e-planetelec.fr/-accessoires/1914-protection-de-spot-eur-ohm-52139'
                         '.html', 'https://www.e-planetelec.fr/projecteur-portatif/2115-projecteur-portatif-25w-led'
                         '-avec-pc-2p-t-et-prise-usb-plwork25w.html',
                         'https://www.e-planetelec.fr/projecteur-portatif/2116-projecteur-portatif-45w-led-avec-2-pc'
                         '-2pt-plwork45w.html',
                         'https://www.e-planetelec.fr/-accessoires/2120-brassard-lumineux-led-running-pl8710499.html'
                         '', 'https://www.e-planetelec.fr/hublot-led/2166-hublot-led-25w-ip65-ik10-4000k.html',
                         'https://www.e-planetelec.fr/spot-led/539-kit-spot-gu10-led-blanc-fix-avec-lampe-6w.html',
                         'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1301-zoom-14w-1450lm-3000k-matt'
                         '-black-30290143.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1733-delta-6w-3000k-white-31000063w.html',
                         'https://www.e-planetelec.fr/etanche-led/2484-luminaire-profiles-lineaire-led-tp-strong-75w'
                         '-4000k-kanlux-33171.html',
                         'https://www.e-planetelec.fr/luminaire-suspendu/1341-belly-250mm-e27-white-30432500w.html',
                         'https://www.e-planetelec.fr/downlight-led/1870-flat-top-elecman.html#/122-couleur_eclairage'
                         '-3000k_blanc_chaud/134-puissance_led-6w',
                         'https://www.e-planetelec.fr/applique-murale/1902-applique-ip44-led-prismaline-avec'
                         '-interrupteur-tactile-avec-led-700lm-sl189801.html',
                         'https://www.e-planetelec.fr/ampoule-led/2594-led-gu10-6w-3000k-38.html',
                         'https://www.e-planetelec.fr/ampoule-led/2596-led-gu10-6w-4000k-38.html',
                         'https://www.e-planetelec.fr/projecteur-portatif/2117-projecteur-portatif-30w-ip65-2600'
                         '-lumens-pl56010.html',
                         'https://www.e-planetelec.fr/-accessoires/2121-lampe-frontale-led-3w-200-lumens-plled26.html'
                         '', 'https://www.e-planetelec.fr/downlight-led/3096-flat-top-square-18w-1440lm-4000k'
                         '-30890184.html',
                         'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1302-zoom-14w-1500lm-4000k-matt'
                         '-black-30290144.html',
                         'https://www.e-planetelec.fr/spot-led-downlight/1734-delta-6w-3000k-black-31000063n.html',
                         'https://www.e-planetelec.fr/luminaire-hublot/1262-blok-round-led-ip65-7w-550lm-4000k'
                         '-30170074.html',
                         'https://www.e-planetelec.fr/luminaire-suspendu/1342-belly-250mm-e27-black-white-30432500nw'
                         '.html', 'https://www.e-planetelec.fr/etanche-led/1869-etanche-tubulaire-slim-led-ip67-ik10'
                         '-tubiled-30w.html',
                         'https://www.e-planetelec.fr/applique-murale/1291-wide-18w-600mm-1500lm-4000k-30220184.html'
                         '', 'https://www.e-planetelec.fr/ampoule-led/2598-led-gu10-75w-2700k-38.html',
                         'https://www.e-planetelec.fr/etanche-led/583-etanche-tubulaire-led-ip67-ik10-tubiled-40w'
                         '.html#/123-couleur_eclairage-4000k_blanc_neutre/133-diffuseur-transparent',
                         'https://www.e-planetelec.fr/reglette-etanche/1286-line-5w-311mm-500lm-4000k-30110054.html',
                          'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1303-zoom-25w-2200lm-3000k-matt'
                          '-white-30280253.html',
                          'https://www.e-planetelec.fr/luminaire-hublot/1263-surf-14w-300mm-1100lm-3000k-30380143'
                          '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1373-rook-round-led-ip65-7w'
                          '-525lm-4000k-anthracite-30670074a.html',
                          'https://www.e-planetelec.fr/luminaire-suspendu/1343-belly-250mm-e27-black-gold-30432500ng'
                          '.html', 'https://www.e-planetelec.fr/applique-murale/1292-wide-36w-1200mm-3000lm-4000k'
                          '-30220364.html',
                          'https://www.e-planetelec.fr/reglette-etanche/1287-line-9w-572mm-900lm-4000k-30110094.html'
                          '', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1304-zoom-25w-2300lm-4000k'
                          '-matt-white-30280254.html',
                          'https://www.e-planetelec.fr/luminaire-hublot/1264-surf-14w-300mm-1150lm-4000k-30380144'
                          '.html', 'https://www.e-planetelec.fr/applique-murale/1357-pixel-7w-420lm-3000k-white'
                          '-30590073w.html',
                          'https://www.e-planetelec.fr/luminaires-exterieurs/1375-rook-round-single-ip54-gu10-1x50w'
                          '-anthracite-30680010a.html',
                          'https://www.e-planetelec.fr/ampoule-led/2579-led-gu10-75w-3000k-38.html',
                          'https://www.e-planetelec.fr/reglette-etanche/1287-line-9w-572mm-900lm-4000k-30110094.html'
                          '', 'https://www.e-planetelec.fr/reglette-etanche/1288-line-12w-872mm-1200lm-4000k-30110124'
                          '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1305-zoom-25w-2200lm'
                          '-3000k-matt-black-30290253.html',
                          'https://www.e-planetelec.fr/luminaire-hublot/1265-surf-18w-340mm-1400lm-3000k-30380183'
                          '.html', 'https://www.e-planetelec.fr/applique-murale/1358-pixel-7w-420lm-3000k-black'
                          '-30590073n.html',
                          'https://www.e-planetelec.fr/luminaires-exterieurs/1374-rook-round-led-ip65-14w-1050lm'
                          '-4000k-anthracite-30670144a.html',
                          'https://www.e-planetelec.fr/luminaire-suspendu/1345-belly-330mm-e27-black-white-30433300nw'
                          '.html', 'https://www.e-planetelec.fr/ampoule-led/441-pack-10-ampoules-led-gu10-75w.html',
                          'https://www.e-planetelec.fr/etanche-led/1418-hydra-led-60w-ip65-1500mm-6000lm-4000k'
                          '-30022604.html',
                          'https://www.e-planetelec.fr/spot-led-downlight/1173-man-fix-50w-gu10-matt-white-30340010'
                          '.html', 'https://www.e-planetelec.fr/reglette-etanche/1289-line-16w-1172mm-1600lm-4000k'
                          '-30110164.html',
                          'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1306-zoom-25w-2300lm-4000k-matt'
                          '-black-30290254.html',
                          'https://www.e-planetelec.fr/luminaire-hublot/1266-surf-18w-340mm-1450lm-4000k-30380184'
                          '.html', 'https://www.e-planetelec.fr/applique-murale/1359-miral-ip44-20w-1400lm-3000k'
                          '-30730203.html',
                          'https://www.e-planetelec.fr/luminaires-exterieurs/1376-rook-round-double-ip54-gu10-2x50w'
                          '-anthracite-30680020a.html',
                          'https://www.e-planetelec.fr/ampoule-led/2593-led-gu10-75w-4000k-38.html',
                          'https://www.e-planetelec.fr/luminaire-suspendu/1346-belly-330mm-e27-black-gold-30433300ng'
                          '.html', 'https://www.e-planetelec.fr/etanche-led/1412-hydra-led-30w-ip65-1500mm-3000lm'
                          '-4000k-30021304.html',
                          'https://www.e-planetelec.fr/spot-led-downlight/1174-man-fix-50w-gu10-nickel-satin-30340020'
                          '.html', 'https://www.e-planetelec.fr/reglette-etanche/1290-line-accessories-kit-30110000'
                          '.html', 'https://www.e-planetelec.fr/luminaire-hublot/1267-surf-sensor-24w-1560lm-3000k'
                          '-30380243s.html',
                          'https://www.e-planetelec.fr/applique-murale/1360-tulip-ip44-12w-840lm-3000k-30720123.html'
                          '', 'https://www.e-planetelec.fr/luminaires-exterieurs/1377-rook-square-single-ip54-gu10'
                          '-1x50w-anthracite-30680030a.html',
                          'https://www.e-planetelec.fr/luminaire-suspendu/1347-iris-290mm-e27-black-30432900n.html',
                          'https://www.e-planetelec.fr/ampoule-led/2186-led-gu10-dimmable-75w-38.html',
                          'https://www.e-planetelec.fr/spot-led-downlight/1175-man-tilt-50w-gu10-matt-white-30340030'
                          '.html', 'https://www.e-planetelec.fr/ampoule-led/2592-led-gu10-dimmable-75w-38-3000k.html'
                          '', 'https://www.e-planetelec.fr/luminaire-hublot/1268-surf-sensor-24w-1680lm-4000k'
                          '-30380244s.html',
                          'https://www.e-planetelec.fr/applique-murale/1361-wally-round-single-1x50w-gu10-matt-white'
                          '-30510150w.html',
                          'https://www.e-planetelec.fr/luminaires-exterieurs/1378-rook-square-double-ip54-gu10-2x50w'
                          '-anthracite-30680040a.html',
                          'https://www.e-planetelec.fr/luminaire-suspendu/1348-iris-290mm-e27-black-gold-30432900ng'
                          '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1176-man-tilt-50w-gu10-nickel'
                          '-satin-30340040.html',
                          'https://www.e-planetelec.fr/luminaire-hublot/1271-kamel-ip65-20w-1700lm-4000k-white'
                          '-30600204w.html',
                          'https://www.e-planetelec.fr/applique-murale/1362-wally-round-single-1x50w-gu10-matt-black'
                          '-30510150n.html',
                          'https://www.e-planetelec.fr/luminaires-exterieurs/1379-alpha-ip65-6w-400lm-3000k-white'
                          '-30620063w.html',
                          'https://www.e-planetelec.fr/ampoule-led/425-ampoule-vintage-standard-e27.html',
                          'https://www.e-planetelec.fr/luminaire-suspendu/1349-iris-290mm-e27-brass-30432900br.html',
                           'https://www.e-planetelec.fr/spot-led-downlight/1177-man-square-tilt-50w-gu10-matt-white'
                           '-30340050.html',
                           'https://www.e-planetelec.fr/luminaire-hublot/1272-kamel-ip65-20w-1700lm-4000k-anthracite'
                           '-30600204a.html',
                           'https://www.e-planetelec.fr/applique-murale/1363-wally-round-double-2x50w-gu10-matt-white'
                           '-30510250w.html',
                           'https://www.e-planetelec.fr/luminaires-exterieurs/1380-alpha-ip65-6w-400lm-3000k'
                           '-anthracite-30620063a.html',
                           'https://www.e-planetelec.fr/luminaire-suspendu/1350-iris-375mm-e27-black-30433750n.html',
                            'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1311-reflector-zoom-15-14w'
                            '-30281400.html',
                            'https://www.e-planetelec.fr/spot-led-downlight/1178-man-square-tilt-50w-gu10-nickel'
                            '-satin-30340060.html',
                            'https://www.e-planetelec.fr/luminaire-hublot/1273-kamel-ip65-sensor-20w-1700lm-4000k'
                            '-white-30600204ws.html',
                            'https://www.e-planetelec.fr/applique-murale/1364-wally-round-double-2x50w-gu10-matt'
                            '-black-30510250n.html',
                            'https://www.e-planetelec.fr/luminaires-exterieurs/1381-alpha-ip65-6w-450lm-4000k-white'
                            '-30620064w.html',
                            'https://www.e-planetelec.fr/luminaire-suspendu/1351-iris-375mm-e27-black-gold-30433750ng'
                            '.html', 'https://www.e-planetelec.fr/luminaire-hublot/1274-kamel-ip65-sensor-20w-1700lm'
                            '-4000k-anthracite-30600204as.html',
                            'https://www.e-planetelec.fr/applique-murale/1365-wally-square-single-1x50w-gu10-matt'
                            '-white-30520150w.html',
                            'https://www.e-planetelec.fr/luminaires-exterieurs/1382-alpha-ip65-6w-450lm-4000k'
                            '-anthracite-30620064a.html',
                            'https://www.e-planetelec.fr/luminaire-suspendu/1352-iris-375mm-e27-brass-30433750br.html'
                            '', 'https://www.e-planetelec.fr/spot-led-downlight/1171-foc-ip65-8w-640lm-3000k-dimmable'
                            '-30750083.html',
                            'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1312-reflector-zoom-24-14w'
                            '-30291400.html',
                            'https://www.e-planetelec.fr/applique-murale/1366-wally-square-single-1x50w-gu10-matt'
                            '-black-30520150n.html',
                            'https://www.e-planetelec.fr/luminaires-exterieurs/1383-alpha-ip65-12w-780lm-3000k-white'
                            '-30620123w.html',
                            'https://www.e-planetelec.fr/luminaire-suspendu/1353-up-200mm-e27-white-30432000w.html',
                            'https://www.e-planetelec.fr/spot-led-downlight/1172-foc-ip65-8w-680lm-4000k-dimmable'
                            '-30750084.html',
                            'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1313-reflector-zoom-15-25w'
                            '-30280015.html',
                            'https://www.e-planetelec.fr/spot-led-downlight/1179-cobby-7w-550lm-3000k-matt-white'
                            '-30390073.html',
                            'https://www.e-planetelec.fr/ampoule-led/439-ampoule-smd-led-12w-e27.html#/128'
                            '-reference_lampe-10010122_12w_2700k',
                            'https://www.e-planetelec.fr/luminaire-hublot/1276-kamel-ip65-30w-2500lm-4000k-anthracite'
                            '-30600304a.html',
                            'https://www.e-planetelec.fr/applique-murale/1367-wally-square-double-2x50w-gu10-matt'
                            '-white-30520250w.html',
                            'https://www.e-planetelec.fr/luminaires-exterieurs/1384-alpha-ip65-12w-780lm-3000k'
                            '-anthracite-30620123a.html',
                            'https://www.e-planetelec.fr/luminaire-suspendu/1354-up-200mm-e27-black-30432000n.html',
                            'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1314-reflector-zoom-24-25w'
                            '-30280024.html',
                            'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1315-reflector-zoom-15-40w'
                            '-30290015.html',
                            'https://www.e-planetelec.fr/spot-led-downlight/1180-cobby-7w-575lm-4000k-matt-white'
                            '-30390074.html',
                            'https://www.e-planetelec.fr/luminaire-hublot/1277-kamel-ip65-sensor-30w-2500lm-4000k'
                            '-white-30600304ws.html',
                            'https://www.e-planetelec.fr/applique-murale/1368-wally-square-double-2x50w-gu10-matt'
                            '-black-30520250n.html',
                            'https://www.e-planetelec.fr/ampoule-led/550-lampe-led-8w-e27-a60.html',
                            'https://www.e-planetelec.fr/luminaires-exterieurs/1385-alpha-ip65-12w-840lm-4000k-white'
                            '-30620124w.html',
                            'https://www.e-planetelec.fr/luminaire-suspendu/1355-up-200mm-e27-brass-30432000br.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1316-reflector-zoom-24-40w'
                             '-30290024.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1181-ringo-7w-590lm-3000k-30150073.html'
                             '', 'https://www.e-planetelec.fr/reglette-etanche/1410-hydra-led-25w-ip65-1200mm-2500lm'
                             '-4000k-30021254.html',
                             'https://www.e-planetelec.fr/luminaire-hublot/1278-kamel-ip65-sensor-30w-2500lm-4000k'
                             '-anthracite-30600304as.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1369-mask-ip65-10w-750lm-3000k-white'
                             '-30660103w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1386-alpha-ip65-12w-840lm-4000k'
                             '-anthracite-30620124a.html',
                             'https://www.e-planetelec.fr/ampoule-led/1739-ampoule-smd-led-9w-2700k-e27.html',
                             'https://www.e-planetelec.fr/luminaire-suspendu/1356-up-200mm-e27-copper-30432000c.html'
                             '', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1317-track-230v-3l-n'
                             '-surface-2mt-white-30440002w.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1182-ringo-7w-650lm-4000k-30150074.html'
                             '', 'https://www.e-planetelec.fr/luminaire-hublot/1283-pascal-18w-1440lm-3000-4000-6000k'
                             '-30710180.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1370-mask-ip65-10w-750lm-3000k'
                             '-anthracite-30660103a.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1387-alpha-ip65-16w-1040lm-3000k'
                             '-white-30620163w.html',
                             'https://www.e-planetelec.fr/ampoule-led/1740-ampoule-smd-led-9w-4000k-e27.html',
                             'https://www.e-planetelec.fr/luminaire-suspendu/1473-clap-9w-30700009.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1318-track-230v-3l-n-surface'
                             '-2mt-black-30440002n.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1183-ringo-10w-950lm-3000k-30150103.html'
                             '', 'https://www.e-planetelec.fr/ampoule-led/2441-lampe-lino-s19-led-7w-4000k-700lm.html'
                             '', 'https://www.e-planetelec.fr/luminaires-exterieurs/1371-mask-ip65-10w-800lm-4000k'
                             '-white-30660104w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1388-alpha-ip65-16w-1040lm-3000k'
                             '-anthracite-30620163a.html',
                             'https://www.e-planetelec.fr/luminaire-suspendu/1474-clap-display-7w-30700007.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1319-track-230v-3l-n-surface'
                             '-3mt-white-30440003w.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1184-ringo-10w-1000lm-4000k-30150104'
                             '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1184-ringo-10w-1000lm-4000k'
                             '-30150104.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1372-mask-ip65-10w-800lm-4000k'
                             '-anthracite-30660104a.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1390-alpha-ip65-16w-1120lm-4000k'
                             '-anthracite-30620164a.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1320-track-230v-3l-n-surface'
                             '-3mt-black-30440003n.html',
                             'https://www.e-planetelec.fr/applique-murale/2440-sarlam-applique-standard-ip24-et-ik04'
                             '-avec-interrupteur-et-prise-rasoir-189869.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1391-kat-ip65-3w-3000k-150lm-white'
                             '-30630033w.html',
                             'https://www.e-planetelec.fr/applique-murale/3038-wide-36w-ip44-1200mm-3000lm-4000k'
                             '-30980364.html',
                             'https://www.e-planetelec.fr/luminaire-hublot/1617-blok-oval-guard-ip44-e27-30180008'
                             '.html', 'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1321-track-230v'
                             '-live-end-connector-white-30440010w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1392-kat-ip65-3w-3000k-150lm'
                             '-anthracite-30630033a.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1187-steam-7w-ip65-595lm-3000k-30050073'
                             '.html', 'https://www.e-planetelec.fr/reglette-etanche/1416-hydra-led-50w-ip65-1200mm'
                             '-5000lm-4000k-30022504.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1322-track-230v-live-end'
                             '-connector-black-30440010n.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1393-kat-ip65-3w-4000k-180lm-white'
                             '-30630034w.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1188-steam-square-7w-ip65-595lm-3000k'
                             '-30060073.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1323-track-230v-central'
                             '-connector-white-30440011w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1394-kat-ip65-3w-4000k-180lm'
                             '-anthracite-30630034a.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1324-track-230v-central'
                             '-connector-black-30440011n.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1325-track-230v-universal'
                             '-angle-white-30440012w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1395-kat-ip65-9w-3000k-450lm-white'
                             '-30630093w.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1326-track-230v-universal'
                             '-angle-black-30440012n.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1396-kat-ip65-9w-3000k-450lm'
                             '-anthracite-30630093a.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1191-loop-50w-gu10-30350010.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1327-track-230v-90-angle'
                             '-white-30440013w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1397-kat-ip65-9w-4000k-520lm-white'
                             '-30630094w.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1192-loop-square-50w-gu10-30350020.html'
                             '', 'https://www.e-planetelec.fr/spot-led-downlight/1193-loop-rectangular-50w-gu10'
                             '-30350030.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1328-track-230v-90-angle'
                             '-black-30440013n.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1398-kat-ip65-9w-4000k-520lm'
                             '-anthracite-30630094a.html',
                             'https://www.e-planetelec.fr/reglette-etanche/1422-hydra-led-60w-ip65-1500mm-6000lm'
                             '-4000k-linkable-30022604lk.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1194-magnum-30w-2400lm-3000k-white'
                             '-30570303w.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1329-track-230v-t-joint'
                             '-white-30440016w.html',
                             'https://www.e-planetelec.fr/reglette-etanche/1468-planet-2-150w-19500lm-120-4000k'
                             '-30701504.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1423-flash-10w-ip65-750lm-3000k'
                             '-30240103.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1424-flash-10w-ip65-800lm-4000k'
                             '-30240104.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1195-magnum-30w-2400lm-3000k-black'
                             '-30570303n.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1330-track-230v-t-joint'
                             '-black-30440016n.html',
                             'https://www.e-planetelec.fr/reglette-etanche/1469-planet-2-200w-26000lm-120-4000k'
                             '-30702004.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1425-flash-20w-ip65-1500lm-3000k'
                             '-30240203.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1196-magnum-30w-2500lm-4000k-white'
                             '-30570304w.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1331-track-230v-suspension'
                             '-kit-white-30440017w.html',
                             'https://www.e-planetelec.fr/reglette-etanche/1470-planet-2-60-beam-angle-lens-150w'
                             '-30700000.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1426-flash-20w-ip65-1600lm-4000k'
                             '-30240204.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1197-magnum-30w-2500lm-4000k-black'
                             '-30570304n.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1332-track-230v-suspension'
                             '-kit-black-30440017n.html',
                             'https://www.e-planetelec.fr/reglette-etanche/1471-planet-2-60-beam-angle-lens-200w'
                             '-30700001.html',
                             'https://www.e-planetelec.fr/reglette-etanche/1472-planet-2-surface-fixed-bracket'
                             '-30700002.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1427-flash-30w-ip65-2250lm-3000k'
                             '-30240303.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1427-flash-30w-ip65-2250lm-3000k'
                             '-30240303.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1198-magnum-30w-2400lm-3000k-white-1-10v'
                             '-dimm-30580303w.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1199-magnum-30w-2400lm-3000k-black-1-10v'
                             '-dimm-30580303n.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1334-track-230v-contact-mini'
                             '-joint-black-30445000n.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1428-flash-30w-ip65-2400lm-4000k'
                             '-30240304.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1200-magnum-30w-2500lm-4000k-white-1-10v'
                             '-dimm-30580304w.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1335-track-230v-closing-end'
                             '-white-30445001w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1429-flash-50w-ip65-3750lm-3000k'
                             '-30240503.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1430-flash-50w-ip65-4000lm-4000k'
                             '-30240504.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1336-track-230v-closing-end'
                             '-black-30445001n.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1431-flash-100w-ip65-7500lm-3000k'
                             '-30241003.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1337-track-230v-mechanical'
                             '-mini-joint-white-30440018w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1432-flash-100w-ip65-8000lm-4000k'
                             '-30241004.html',
                             'https://www.e-planetelec.fr/spots-sur-rails-et-accessoires/1338-track-230v-mechanical'
                             '-mini-joint-black-30440018n.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1433-flash-150w-ip65-11250lm-3000k'
                             '-30241503.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1205-magnum-30w-2500lm-4000k-black-dali'
                             '-push-dimm-30760304n.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1434-flash-150w-ip65-12000lm-4000k'
                             '-30241504.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1206-magnum-60w-4800lm-3000k-white'
                             '-30570603w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1435-flash-200w-ip65-15000lm-3000k'
                             '-30242003.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1207-magnum-60w-4800lm-3000k-black'
                             '-30570603n.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1436-flash-200w-ip65-16000lm-4000k'
                             '-30242004.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1208-magnum-60w-5000lm-4000k-white'
                             '-30570604w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1437-flash-300w-ip65-24000lm-4000k'
                             '-30243004.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1209-magnum-60w-5000lm-4000k-black'
                             '-30570604n.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1438-flash-400w-ip65-32000lm-4000k'
                             '-30244004.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1210-magnum-60w-4800lm-3000k-white-1-10v'
                             '-dimm-30580603w.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1211-magnum-60w-4800lm-3000k-black-1-10v'
                             '-dimm-30580603n.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1212-magnum-60w-5000lm-4000k-white-1-10v'
                             '-dimm-30580604w.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1213-magnum-60w-5000lm-4000k-black-1-10v'
                             '-dimm-30580604n.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1214-magnum-60w-4800lm-3000k-white-dali'
                             '-push-dimm-30760603w.html',
                             'https://www.e-planetelec.fr/luminaires-exterieurs/1450-tuck-ip65-30w-2400lm-4000k-white'
                             '-30260304.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1215-magnum-60w-4800lm-3000k-black-dali'
                             '-push-dimm-30760603n.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1216-magnum-60w-5000lm-4000k-white-dali'
                             '-push-dimm-30760604w.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1217-magnum-60w-5000lm-4000k-black-dali'
                             '-push-dimm-30760604n.html',
                             'https://www.e-planetelec.fr/spot-led-downlight/1218-magnum-15-reflector-30570300.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1219-magnum-24-reflector-30570301.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1220-petit-2w-ip44-240lm-3000k'
                              '-30310023.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1221-petit-square-2w-ip44-240lm-3000k'
                              '-30320023.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1456-vega-ip65-10w-800lm-4000k-white'
                              '-30650104w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1222-petit-rectangular-4w-480lm-3000k'
                              '-30320043.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1457-vega-ip65-10w-800lm-4000k-black'
                              '-30650104n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1223-nest-50w-gu10-30330010.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1458-vega-ip65-30w-2400lm-4000k'
                              '-white-30650304w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1224-nest-asymmetric-50w-gu10-30330020'
                              '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1459-vega-ip65-30w-2400lm'
                              '-4000k-black-30650304n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1225-rot-7-5w-850lm-3000k-30420073.html'
                              '', 'https://www.e-planetelec.fr/luminaires-exterieurs/1460-vega-ip65-50w-4000lm-4000k'
                              '-white-30650504w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1226-rot-7-5w-875lm-4000k-30420074.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1226-rot-7-5w-875lm-4000k-30420074'
                              '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/1462-vega-ip65-100w-8000lm'
                              '-4000k-white-30651004w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1227-rot-17w-1650lm-3000k-30420173.html'
                              '', 'https://www.e-planetelec.fr/luminaires-exterieurs/1463-vega-ip65-100w-8000lm-4000k'
                              '-black-30651004n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1228-rot-17w-1750lm-4000k-30420174.html'
                              '', 'https://www.e-planetelec.fr/luminaires-exterieurs/1464-vega-ip65-150w-12000lm'
                              '-4000k-white-30651504w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1229-rot-32w-3150lm-3000k-30420323.html'
                              '', 'https://www.e-planetelec.fr/luminaires-exterieurs/1465-vega-ip65-150w-12000lm'
                              '-4000k-black-30651504n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1230-rot-32w-3250lm-4000k-30420324.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1231-swing-35w-4000k-3850lm'
                              '-30410354.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1466-vega-ip65-200w-16000lm-4000k'
                              '-white-30652004w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1232-sixty-40w-no-flickering-3400lm'
                              '-3000k-30140403.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1467-vega-ip65-200w-16000lm-4000k'
                              '-black-30652004n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1233-sixty-40w-no-flickering-3600lm'
                              '-4000k-30140404.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1234-sixty-40w-no-flickering-3400lm'
                              '-3000k-1-10v-dimm-30770403.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1235-sixty-40w-no-flickering-3600lm'
                              '-4000k-1-10v-dimm-30770404.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1236-sixty-40w-no-flickering-3400lm'
                              '-3000k-dali-push-dimm-30780403.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1237-sixty-40w-no-flickering-3600lm'
                              '-4000k-dali-push-dimm-30780404.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1238-suspension-kit-sixty-hydra'
                              '-30021000.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1239-sixty-surface-kit-30140000.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1240-moon-9w-500lm-3000k-30560093.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1241-moon-24w-1600lm-3000k-30560243'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1242-moon-24w-1700lm-4000k'
                              '-30560244.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1243-tango-32w-2450lm-3000k-30100323'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1244-tango-32w-2560lm-4000k'
                              '-30100324.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1245-sindra-18w-1900lm-3000k-30740183'
                              '.html', 'https://www.e-planetelec.fr/luminaires-exterieurs/3224-projecteur-led'
                              '-floodlight-50w-access-epl7913.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1246-sindra-18w-2050lm-4000k-30740184'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1247-flat-6w-450lm-3000k'
                              '-30070063.html',
                              'https://www.e-planetelec.fr/-accessoires/3225-detecteur-pir-clipsable-pour-floodlight'
                              '-access.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1248-flat-6w-480lm-4000k-30070064.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1249-flat-18w-1350lm-3000k-30070183'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1250-flat-18w-1440lm-4000k'
                              '-30070184.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1252-flat-24w-1800lm-3000k-30070243'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1253-flat-24w-1900lm-4000k'
                              '-30070244.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1254-flat-square-18w-1350lm-3000k'
                              '-30080183.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1255-flat-square-18w-1440lm-4000k'
                              '-30080184.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1257-flat-surface-18w-1440lm-4000k'
                              '-30090184.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1258-flat-surface-18w-1440lm-6000k'
                              '-30090186.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1259-flat-square-surface-18w-1440lm'
                              '-4000k-30270184.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1260-flat-square-surface-18w-1440lm'
                              '-6000k-30270186.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1293-pukhet-surface-downlight-9w-800lm'
                              '-3000k-white-30550093w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1294-pukhet-surface-downlight-9w-800lm'
                              '-3000k-black-30550093n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1295-pukhet-surface-downlight-9w-850lm'
                              '-4000k-white-30550094w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1296-pukhet-surface-downlight-9w-850lm'
                              '-4000k-black-30550094n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1297-zoom-surface-12w-1150lm-40-3000k'
                              '-white-30540123w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1298-zoom-surface-12w-1150lm-40-3000k'
                              '-black-30540123n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1592-downlight-led-extra-plat-6w-3000k'
                              '-nled9403e-3k.html',
                              'https://www.e-planetelec.fr/spot-led/539-kit-spot-gu10-led-blanc-fix-avec-lampe-6w'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1733-delta-6w-3000k-white'
                              '-31000063w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1734-delta-6w-3000k-black-31000063n'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1173-man-fix-50w-gu10-matt'
                              '-white-30340010.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1174-man-fix-50w-gu10-nickel-satin'
                              '-30340020.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1175-man-tilt-50w-gu10-matt-white'
                              '-30340030.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1176-man-tilt-50w-gu10-nickel-satin'
                              '-30340040.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1177-man-square-tilt-50w-gu10-matt'
                              '-white-30340050.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1178-man-square-tilt-50w-gu10-nickel'
                              '-satin-30340060.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1171-foc-ip65-8w-640lm-3000k-dimmable'
                              '-30750083.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1172-foc-ip65-8w-680lm-4000k-dimmable'
                              '-30750084.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1179-cobby-7w-550lm-3000k-matt-white'
                              '-30390073.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1180-cobby-7w-575lm-4000k-matt-white'
                              '-30390074.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1181-ringo-7w-590lm-3000k-30150073.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1182-ringo-7w-650lm-4000k-30150074'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1183-ringo-10w-950lm-3000k'
                              '-30150103.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1184-ringo-10w-1000lm-4000k-30150104'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1187-steam-7w-ip65-595lm-3000k'
                              '-30050073.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1188-steam-square-7w-ip65-595lm-3000k'
                              '-30060073.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1191-loop-50w-gu10-30350010.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1192-loop-square-50w-gu10-30350020.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1193-loop-rectangular-50w-gu10'
                              '-30350030.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1194-magnum-30w-2400lm-3000k-white'
                              '-30570303w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1195-magnum-30w-2400lm-3000k-black'
                              '-30570303n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1196-magnum-30w-2500lm-4000k-white'
                              '-30570304w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1197-magnum-30w-2500lm-4000k-black'
                              '-30570304n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1198-magnum-30w-2400lm-3000k-white-1'
                              '-10v-dimm-30580303w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1199-magnum-30w-2400lm-3000k-black-1'
                              '-10v-dimm-30580303n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1200-magnum-30w-2500lm-4000k-white-1'
                              '-10v-dimm-30580304w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1205-magnum-30w-2500lm-4000k-black-dali'
                              '-push-dimm-30760304n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1206-magnum-60w-4800lm-3000k-white'
                              '-30570603w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1207-magnum-60w-4800lm-3000k-black'
                              '-30570603n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1208-magnum-60w-5000lm-4000k-white'
                              '-30570604w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1209-magnum-60w-5000lm-4000k-black'
                              '-30570604n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1210-magnum-60w-4800lm-3000k-white-1'
                              '-10v-dimm-30580603w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1211-magnum-60w-4800lm-3000k-black-1'
                              '-10v-dimm-30580603n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1212-magnum-60w-5000lm-4000k-white-1'
                              '-10v-dimm-30580604w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1213-magnum-60w-5000lm-4000k-black-1'
                              '-10v-dimm-30580604n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1214-magnum-60w-4800lm-3000k-white-dali'
                              '-push-dimm-30760603w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1215-magnum-60w-4800lm-3000k-black-dali'
                              '-push-dimm-30760603n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1216-magnum-60w-5000lm-4000k-white-dali'
                              '-push-dimm-30760604w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1217-magnum-60w-5000lm-4000k-black-dali'
                              '-push-dimm-30760604n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1218-magnum-15-reflector-30570300.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1219-magnum-24-reflector-30570301'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1220-petit-2w-ip44-240lm-3000k'
                              '-30310023.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1221-petit-square-2w-ip44-240lm-3000k'
                              '-30320023.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1222-petit-rectangular-4w-480lm-3000k'
                              '-30320043.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1223-nest-50w-gu10-30330010.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1224-nest-asymmetric-50w-gu10-30330020'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1225-rot-7-5w-850lm-3000k'
                              '-30420073.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1226-rot-7-5w-875lm-4000k-30420074.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1227-rot-17w-1650lm-3000k-30420173'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1228-rot-17w-1750lm-4000k'
                              '-30420174.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1229-rot-32w-3150lm-3000k-30420323.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1230-rot-32w-3250lm-4000k-30420324'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1231-swing-35w-4000k-3850lm'
                              '-30410354.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1232-sixty-40w-no-flickering-3400lm'
                              '-3000k-30140403.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1233-sixty-40w-no-flickering-3600lm'
                              '-4000k-30140404.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1234-sixty-40w-no-flickering-3400lm'
                              '-3000k-1-10v-dimm-30770403.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1235-sixty-40w-no-flickering-3600lm'
                              '-4000k-1-10v-dimm-30770404.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1236-sixty-40w-no-flickering-3400lm'
                              '-3000k-dali-push-dimm-30780403.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1237-sixty-40w-no-flickering-3600lm'
                              '-4000k-dali-push-dimm-30780404.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1238-suspension-kit-sixty-hydra'
                              '-30021000.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1239-sixty-surface-kit-30140000.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1240-moon-9w-500lm-3000k-30560093.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1241-moon-24w-1600lm-3000k-30560243'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1242-moon-24w-1700lm-4000k'
                              '-30560244.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1243-tango-32w-2450lm-3000k-30100323'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1244-tango-32w-2560lm-4000k'
                              '-30100324.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1245-sindra-18w-1900lm-3000k-30740183'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1246-sindra-18w-2050lm-4000k'
                              '-30740184.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1247-flat-6w-450lm-3000k-30070063.html'
                              '', 'https://www.e-planetelec.fr/spot-led-downlight/1248-flat-6w-480lm-4000k-30070064'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1249-flat-18w-1350lm-3000k'
                              '-30070183.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1250-flat-18w-1440lm-4000k-30070184'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1252-flat-24w-1800lm-3000k'
                              '-30070243.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1253-flat-24w-1900lm-4000k-30070244'
                              '.html', 'https://www.e-planetelec.fr/spot-led-downlight/1254-flat-square-18w-1350lm'
                              '-3000k-30080183.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1255-flat-square-18w-1440lm-4000k'
                              '-30080184.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1257-flat-surface-18w-1440lm-4000k'
                              '-30090184.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1258-flat-surface-18w-1440lm-6000k'
                              '-30090186.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1259-flat-square-surface-18w-1440lm'
                              '-4000k-30270184.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1260-flat-square-surface-18w-1440lm'
                              '-6000k-30270186.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1293-pukhet-surface-downlight-9w-800lm'
                              '-3000k-white-30550093w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1294-pukhet-surface-downlight-9w-800lm'
                              '-3000k-black-30550093n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1295-pukhet-surface-downlight-9w-850lm'
                              '-4000k-white-30550094w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1296-pukhet-surface-downlight-9w-850lm'
                              '-4000k-black-30550094n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1297-zoom-surface-12w-1150lm-40-3000k'
                              '-white-30540123w.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1298-zoom-surface-12w-1150lm-40-3000k'
                              '-black-30540123n.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1592-downlight-led-extra-plat-6w-3000k'
                              '-nled9403e-3k.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1593-downlight-led-extra-plat-6w-4000k'
                              '-nled9403e-4k.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1594-downlight-led-extra-plat-12w-3000k'
                              '-nled9404e-3k.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1595-downlight-led-extra-plat-12w-4000k'
                              '-nled9404e-4k.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1597-downlight-led-extra-plat-18w-4000k'
                              '-nled9406e-4k.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1598-downlight-led-extra-plat-24w-3000k'
                              '-nled9408e-3k.html',
                              'https://www.e-planetelec.fr/spot-led-downlight/1599-downlight-led-extra-plat-24w-4000k'
                              '-nled9408e-4k.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1373-rook-round-led-ip65-7w-525lm'
                              '-4000k-anthracite-30670074a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1375-rook-round-single-ip54-gu10'
                              '-1x50w-anthracite-30680010a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1374-rook-round-led-ip65-14w-1050lm'
                              '-4000k-anthracite-30670144a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1376-rook-round-double-ip54-gu10'
                              '-2x50w-anthracite-30680020a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1377-rook-square-single-ip54-gu10'
                              '-1x50w-anthracite-30680030a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1378-rook-square-double-ip54-gu10'
                              '-2x50w-anthracite-30680040a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1379-alpha-ip65-6w-400lm-3000k-white'
                              '-30620063w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1380-alpha-ip65-6w-400lm-3000k'
                              '-anthracite-30620063a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1381-alpha-ip65-6w-450lm-4000k-white'
                              '-30620064w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1382-alpha-ip65-6w-450lm-4000k'
                              '-anthracite-30620064a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1383-alpha-ip65-12w-780lm-3000k'
                              '-white-30620123w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1384-alpha-ip65-12w-780lm-3000k'
                              '-anthracite-30620123a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1385-alpha-ip65-12w-840lm-4000k'
                              '-white-30620124w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1386-alpha-ip65-12w-840lm-4000k'
                              '-anthracite-30620124a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1387-alpha-ip65-16w-1040lm-3000k'
                              '-white-30620163w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1388-alpha-ip65-16w-1040lm-3000k'
                              '-anthracite-30620163a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1389-alpha-ip65-16w-1120lm-4000k'
                              '-white-30620164w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1390-alpha-ip65-16w-1120lm-4000k'
                              '-anthracite-30620164a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1391-kat-ip65-3w-3000k-150lm-white'
                              '-30630033w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1392-kat-ip65-3w-3000k-150lm'
                              '-anthracite-30630033a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1393-kat-ip65-3w-4000k-180lm-white'
                              '-30630034w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1394-kat-ip65-3w-4000k-180lm'
                              '-anthracite-30630034a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1395-kat-ip65-9w-3000k-450lm-white'
                              '-30630093w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1396-kat-ip65-9w-3000k-450lm'
                              '-anthracite-30630093a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1397-kat-ip65-9w-4000k-520lm-white'
                              '-30630094w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1398-kat-ip65-9w-4000k-520lm'
                              '-anthracite-30630094a.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1423-flash-10w-ip65-750lm-3000k'
                              '-30240103.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1424-flash-10w-ip65-800lm-4000k'
                              '-30240104.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1425-flash-20w-ip65-1500lm-3000k'
                              '-30240203.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1426-flash-20w-ip65-1600lm-4000k'
                              '-30240204.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1427-flash-30w-ip65-2250lm-3000k'
                              '-30240303.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1428-flash-30w-ip65-2400lm-4000k'
                              '-30240304.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1429-flash-50w-ip65-3750lm-3000k'
                              '-30240503.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1430-flash-50w-ip65-4000lm-4000k'
                              '-30240504.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1431-flash-100w-ip65-7500lm-3000k'
                              '-30241003.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1432-flash-100w-ip65-8000lm-4000k'
                              '-30241004.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1433-flash-150w-ip65-11250lm-3000k'
                              '-30241503.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1434-flash-150w-ip65-12000lm-4000k'
                              '-30241504.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1435-flash-200w-ip65-15000lm-3000k'
                              '-30242003.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1436-flash-200w-ip65-16000lm-4000k'
                              '-30242004.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1437-flash-300w-ip65-24000lm-4000k'
                              '-30243004.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1438-flash-400w-ip65-32000lm-4000k'
                              '-30244004.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1450-tuck-ip65-30w-2400lm-4000k'
                              '-white-30260304.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1456-vega-ip65-10w-800lm-4000k-white'
                              '-30650104w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1457-vega-ip65-10w-800lm-4000k-black'
                              '-30650104n.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1458-vega-ip65-30w-2400lm-4000k'
                              '-white-30650304w.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1459-vega-ip65-30w-2400lm-4000k'
                              '-black-30650304n.html',
                              'https://www.e-planetelec.fr/luminaires-exterieurs/1460-vega-ip65-50w-4000lm-4000k'
                              '-white-30650504w.html',
                              'https://www.e-planetelec.fr/cordons-de-brassage-rj45/2348-cordon-de-brassage-rj45-05m'
                              '.html', 'https://www.e-planetelec.fr/cordons-hdmi/285-cordon-hdmi.html',
                              'https://www.e-planetelec.fr/coffret-de-communication-grade-3/3118-tdc-delta-initial'
                              '-grd-3-4-rj45-quadrupleur-q199-michaud.html',
                              'https://www.e-planetelec.fr/antenne-reception-satellite/2434-antenne-satellite-plate'
                              '-sedea-769921.html',
                              'https://www.e-planetelec.fr/repartiteur-tv/1728-kit-repartiteur-tv-sur-rj45-2-sorties'
                              '-go187.html',
                              'https://www.e-planetelec.fr/cable-tv-coaxial/2437-cable-coaxial-17-vatca-triple'
                              '-blindage-25ml-032075.html',
                              'https://www.e-planetelec.fr/cordons-hdmi/286-cordon-hdmi.html',
                              'https://www.e-planetelec.fr/cordons-balun/1868-cordon-de-brassage-1-embout-coaxial-et'
                              '-1-embout-rj45-413206-legrand.html',
                              'https://www.e-planetelec.fr/cordons-balun/2332-cordon-balun-05m-rj45prise-f.html',
                              'https://www.e-planetelec.fr/coffret-de-communication-grade-2/3079-tableau-de'
                              '-communication-neo-grd2tvgrd3-quad-lb204-michaud.html',
                              'https://www.e-planetelec.fr/gamme-terrestre-tnt/2433-antenne-tv-tnt-hd-exterieure'
                              '-amplifiee-flagtv-hd-40-db-sedea-340105.html',
                              'https://www.e-planetelec.fr/repartiteur-tv/1729-kit-repartiteur-tv-sur-rj45-4-sorties'
                              '-go188.html',
                              'https://www.e-planetelec.fr/cable-tv-coaxial/2438-cable-coaxial-17-vatca-triple'
                              '-blindage-50ml-032078.html',
                              'https://www.e-planetelec.fr/cordons-hdmi/287-cordon-hdmi.html',
                              'https://www.e-planetelec.fr/coffret-de-communication-grade-3/537-coffret-de'
                              '-communication-grade-3-4-rj45.html',
                              'https://www.e-planetelec.fr/cordons-balun/2333-cordon-balun-25m-rj45prise-tv.html',
                              'https://www.e-planetelec.fr/coffret-de-communication-grade-3/3231-coffret-vdi-13'
                              '-modules-1rangee-switch5-ports-poe-grade-3tv-r9h13401vdixs-schneider-electric.html',
                              'https://www.e-planetelec.fr/cable-et-connectique-tv/2436-boite-de-50-connecteurs'
                              '-premium-f-males-a-visser-pour-cables-17-et-19-vpatc-059069.html',
                              'https://www.e-planetelec.fr/repartiteur-tv/1730-amplificateur-tnt-sat-sur-rj45-4'
                              '-sorties-go165.html',
                              'https://www.e-planetelec.fr/cordons-hdmi/1900-cordon-hdmi-20-10ml.html',
                              'https://www.e-planetelec.fr/repartiteur-tv/1635-vre-200-rep-2-directions-0144882r13'
                              '.html', 'https://www.e-planetelec.fr/cordons-balun/2334-cordon-balun-2m-rj45prise-f'
                              '.html', 'https://www.e-planetelec.fr/coffret-de-communication-grade-3/3232-coffret-vdi'
                              '-13-modules-2-rangees-switch5-ports-poe-grade-3tv-r9h13402vdixs-schneider-electric'
                              '.html', 'https://www.e-planetelec.fr/cable-et-connectique-tv/2439-connecteur-premium-f'
                              '-males-a-visser-pour-cables-17-et-19-vpatc-a-l-unite-059069-1.html',
                              'https://www.e-planetelec.fr/coffret-de-communication-grade-1/380-legrand-413208.html',
                               'https://www.e-planetelec.fr/cable-et-connectique-tv/2580-boite-de-50-connecteurs-f'
                               '-males-a-compression-953017-k05.html',
                               'https://www.e-planetelec.fr/repartiteur-tv/1636-vre-300-rep-3-directions-0144883r13'
                               '.html', 'https://www.e-planetelec.fr/coffret-de-communication-grade-3/3233-coffret'
                               '-vdi-18-modules-2-rangees-switch5-ports-poe-grade-3tv-r9h18402vdixs-schneider'
                               '-electric.html',
                               'https://www.e-planetelec.fr/coffret-de-communication-grade-1/265-coffret-de'
                               '-communication-basique-13-modules-413218-legrand.html',
                               'https://www.e-planetelec.fr/repartiteur-tv/1637-vre-400-rep-4-directions-0144884r13'
                               '.html', 'https://www.e-planetelec.fr/coffret-de-communication-grade-1/266-coffret-de'
                               '-communication-basique-13-modules-413219-legrand.html',
                               'https://www.e-planetelec.fr/coffret-de-communication-grade-2/1477-coffret-basique'
                               '-grade-2-tv-drivia-13-4-prises-rj45-stp-repartiteur-tv-2-sorties-413248.html',
                               'https://www.e-planetelec.fr/coffret-de-communication-grade-2/3230-coffret-vdi-13'
                               '-modules-1rangee-grade-2-r9h13401vdim-schneider-electric.html',
                               'https://www.e-planetelec.fr/repartiteur-tv/1638-vre-600-rep-6-directions-0144885r13'
                               '.html', 'https://www.e-planetelec.fr/repartiteur-tv/1639-vre-800-rep-8-directions'
                               '-0144886r13.html',
                               'https://www.e-planetelec.fr/support-box-internet/1478-support-box-operateur-adsl-et'
                               '-fibre-avec-1-prise-2p-t-413149.html',
                               'https://www.e-planetelec.fr/support-box-internet/538-tablette-support-box-internet'
                               '-pour-gtl.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/2532-module-de'
                               '-brassage-blinde-cat-6a-stp-avec-connecteur-lcs3-1-module-413104.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/2326-support-pour-4'
                               '-connecteurs-rj45-lcs-pour-coffret-de-communication-413180.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/2325-connecteur-rj45'
                               '-categorie6-stp-413183.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/536-embase-rj45'
                               '-cat6a-sftp-10-gbits.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/1908-dti-precable'
                               '-2rj45.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/2616-connecteurs'
                               '-rj45-sachet-de-4-connecteurs-cat6a-stp-grade-2-tv-go181.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/2029-kit-pt-home-diy'
                               '-rallonge-fibre-optique-de-30m-avec-accessoires.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/2482-connecteur-rj45'
                               '-categorie-6-blinde-stp-vdib1772xb01.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/2481-support-pour-4'
                               '-connecteurs-rj45-vdir312011.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/2347-lexcom-home'
                               '-switch-informatique-1-gbits-5-ports-5-cordons-support-vdir323005.html',
                               'https://www.e-planetelec.fr/accessoires-coffret-de-communication/2605-support-rj45'
                               '-vdir380005-schneider-electric.html',
                               'https://www.e-planetelec.fr/manchons-icta/1606-manchons-clipsables-icta-diam-20'
                               '-p03020.html',
                               'https://www.e-planetelec.fr/conduit-ik-nf-c-14-100/105-icta-3522-diametre-40-ik10'
                               '-25ml.html', 'https://www.e-planetelec.fr/gaine-icta/2173-product.html',
                               'https://www.e-planetelec.fr/syt-awg20/2428-syt-5-paires-910-awg20.html',
                               'https://www.e-planetelec.fr/cable-electrique-rigide-r2v/377-u1000-r2v-3g15-mm'
                               '-couronne-de-50-ml.html',
                               'https://www.e-planetelec.fr/cable-telephone/664-cable-telephone-serie-298-4p-100'
                               '-metres.html',
                               'https://www.e-planetelec.fr/cable-tv-coaxial/669-cable-tv-coaxial-17-vatc.html',
                               'https://www.e-planetelec.fr/manchons-icta/1607-manchons-clipsables-icta-reducteur'
                               '-diam-25-20-p03026.html',
                               'https://www.e-planetelec.fr/conduit-ik-nf-c-14-100/106-icta-3522-diametre-63-ik10'
                               '-25ml.html',
                               'https://www.e-planetelec.fr/cable-informatique-grade-3-sat/1906-cable-residentiel'
                               '-grade-3-tv-couronne-de-100ml.html',
                               'https://www.e-planetelec.fr/gaines-electriques-icta-prefilees/175-gaine-prefilee'
                               '-3g15mm-100-metres.html', 'https://www.e-planetelec.fr/gaine-icta/2174-product.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2576-tm'
                                '-221x125-w0-moulure-tm-optima-08800-iboco.html',
                                'https://www.e-planetelec.fr/trifils-ho7-v-u/240-trifil-h07v-u-3g25mm-100-metres.html'
                                '', 'https://www.e-planetelec.fr/syt-awg20/2430-syt-3-paires-910-awg20-couronne-de'
                                '-100ml.html',
                                'https://www.e-planetelec.fr/cable-informatique-rj45/243-cable-4putp-cat6-couronne-de'
                                '-100ml.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2547-tm'
                                '-321x125-w0-moulure-tm-optima-08802-iboco.html',
                                'https://www.e-planetelec.fr/manchons-icta/1632-manchons-clipsables-icta-diam-25'
                                '-p03025.html',
                                'https://www.e-planetelec.fr/conduit-ik-nf-c-14-100/107-janojet-3522-diametre-75-ik10'
                                '-25ml.html',
                                'https://www.e-planetelec.fr/cable-electrique-rigide-r2v/2170-u1000-r2v-3g25-mm'
                                '-couronne-de-50-ml.html',
                                'https://www.e-planetelec.fr/gaines-electriques-icta-prefilees/177-gaine-prefilee'
                                '-3g25mm-100-metres.html',
                                'https://www.e-planetelec.fr/gaine-icta/2175-product.html',
                                'https://www.e-planetelec.fr/trifils-ho7-v-u/241-trifil-h07v-u-3g15mm-100-metres.html'
                                '', 'https://www.e-planetelec.fr/cable-tv-coaxial/2437-cable-coaxial-17-vatca-triple'
                                '-blindage-25ml-032075.html',
                                'https://www.e-planetelec.fr/cable-tv-coaxial/2438-cable-coaxial-17-vatca-triple'
                                '-blindage-50ml-032078.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2567-tm'
                                '-341x16-w0-moulure-tm-optima-08804-iboco.html',
                                'https://www.e-planetelec.fr/conduit-ik-nf-c-14-100/108-icta-3522-diametre-90-ik10'
                                '-25ml.html',
                                'https://www.e-planetelec.fr/gaines-electriques-icta-prefilees/179-gaine-prefilee-tv'
                                '-coaxial-17-vatc-100-metres.html',
                                'https://www.e-planetelec.fr/gaine-icta/2176-product.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2548-tm'
                                '-521x20-w0-moulure-tm-optima-08808-iboco.html',
                                'https://www.e-planetelec.fr/conduit-ik-nf-c-14-100/234-icta-3522-diametre-110-ik10'
                                '-25ml.html', 'https://www.e-planetelec.fr/gaine-icta/2177-product.html',
                                'https://www.e-planetelec.fr/gaine-icta/62-icta-standard-diametre-16mm-courants-forts'
                                '-legrand-06616.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2549-aim'
                                '-32x125-w0-angle-interieur-moulure-08830-iboco.html',
                                'https://www.e-planetelec.fr/gaines-electriques-icta-prefilees/3036-gaine-prefilee'
                                '-grade-3-sat-2200-mhz-100-metres.html',
                                'https://www.e-planetelec.fr/gaine-icta/63-icta-standard-diametre-20mm-courants-forts'
                                '-legrand-06620.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2550-aem'
                                '-32x125-w0-angle-exterieur-moulure-08831-iboco.html',
                                'https://www.e-planetelec.fr/gaine-icta/64-icta-standard-diametre-25mm-courants-forts'
                                '-legrand-06625.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2551-apm'
                                '-32x125-w0-angle-plat-moulure-08832-iboco.html',
                                'https://www.e-planetelec.fr/conduit-ik-nf-c-14-100/3089-hekachoc-3522-ik10-diametre'
                                '-40-couronne-de-25ml.html',
                                'https://www.e-planetelec.fr/gaine-icta/65-icta-standard-diametre-32mm-courants-forts'
                                '-legrand-06632.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2552-gm'
                                '-32x125-w0-joint-de-couvercle-moulu-08833-iboco.html',
                                'https://www.e-planetelec.fr/conduit-ik-nf-c-14-100/3090-hekachoc-3522-ik10-diametre'
                                '-63-couronne-de-25ml.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2553-im'
                                '-32x125-w0-te-de-derivation-moulure-08834-iboco.html',
                                'https://www.e-planetelec.fr/conduit-ik-nf-c-14-100/3091-hekachoc-3522-ik10-diametre'
                                '-90-couronne-de-25ml.html',
                                'https://www.e-planetelec.fr/conduit-ik-nf-c-14-100/3092-hekachoc-3522-ik10-diametre'
                                '-110-couronne-de-25ml.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2554-lm'
                                '-32x125-w0-embout-moulure-08835-iboco.html',
                                'https://www.e-planetelec.fr/moulures-goulottes-et-plinthes-electriques/2556-sms-o'
                                '-125-w0-boitier-appareillage-sailli-08818-iboco.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-pavillonnaires/2349-51019-boite'
                                '-derivation-pavillonaire-pour-combles-etanche-a-l-air-210x210x85.html',
                                'https://www.e-planetelec.fr/barrettes-de-connexion-a-vis/2599-barrette-laiton-noire'
                                '-10-mm.html',
                                'https://www.e-planetelec.fr/materiel-incorporation-beton/2487-sib-top-irl-25-p02225'
                                '.html', 'https://www.e-planetelec.fr/mise-a-la-terre/13-cuivre-nu-25mm.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-etanches/1716-boite-etanche-carree'
                                '-ip55-105x105x55-960-50034.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-pavillonnaires/2355-51022-boite'
                                '-derivation-pavillonaire-pour-combles-etanche-a-l-air-160x160x65mm.html',
                                'https://www.e-planetelec.fr/colliers-embases-de-fixation/386-schneider-enn47942'
                                '-mureva-fix-colliers-d-installation-194x9.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-rigides/1718-eur-ohm'
                                '-70052-boite-de-100-connecteurs-transparents-2-entrees.html',
                                'https://www.e-planetelec.fr/materiel-incorporation-beton/2488-distancier-horizontal'
                                '-p0104210.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-souples-rigides/1482'
                                '-connecteurs-a-leviers-5-trous-p07315.html',
                                'https://www.e-planetelec.fr/mise-a-la-terre/14-barette-de-coupure-de-terre.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-encastrees/1727-eur-ohm-51018-boite'
                                '-de-derivation-encastre-etanche-a-l-air-140x140x50.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-etanches/1715-boite-etanche-carree'
                                '-ip55-80x80x45-960-50033.html',
                                'https://www.e-planetelec.fr/colliers-embases-de-fixation/387-schneider-enn47962'
                                '-mureva-fix-colliers-d-installation-273x9.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-rigides/1719-eur-ohm'
                                '-70053-boite-de-100-connecteurs-transparents-3-entrees.html',
                                'https://www.e-planetelec.fr/materiel-incorporation-beton/2489-couvercle-de-pose'
                                '-p0102001.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-souples-rigides/1481'
                                '-connecteurs-a-leviers-3-trous-p07313.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-encastrees/1725-eur-ohm-51014-boite'
                                '-de-derivation-encastre-etanche-a-l-air-170x110x40.html',
                                'https://www.e-planetelec.fr/mise-a-la-terre/15-piquet-de-terre-1ml.html',
                                'https://www.e-planetelec.fr/edf-colonne-montante/174-repartiteur-de-terre-3138'
                                '-beromet.html',
                                'https://www.e-planetelec.fr/colliers-embases-de-fixation/2112-schneider-47992-mureva'
                                '-fix-colliers-d-installation-370x9.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-etanches/1714-boite-etanche-ronde'
                                '-ip55-diam-60x40mm-960-50031.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-rigides/1720-eur-ohm'
                                '-70054-boite-de-100-connecteurs-transparents-4-entrees.html',
                                'https://www.e-planetelec.fr/materiel-incorporation-beton/2490-anneau-a-vis-universel'
                                '-p01052.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-souples-rigides/1480'
                                '-connecteurs-a-leviers-2-trous-p07312.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-encastrees/1726-eur-ohm-51016-boite'
                                '-de-derivation-encastre-etanche-a-l-air-250x190x50.html',
                                'https://www.e-planetelec.fr/mise-a-la-terre/2154-repartiteur-de-terre-3139-beromet'
                                '.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-etanches/1717-boite-etanche-carree'
                                '-ip55-155x110x80-960-50036.html',
                                'https://www.e-planetelec.fr/colliers-embases-de-fixation/388-schneider-imt47006'
                                '-mureva-fix-embase-avec-cheville-.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-rigides/1721-eur-ohm'
                                '-70055-boite-de-100-connecteurs-transparents-5-entrees.html',
                                'https://www.e-planetelec.fr/materiel-incorporation-beton/2491-anneau-a-vis-universel'
                                '-p01052.html',
                                'https://www.e-planetelec.fr/colliers-embases-de-fixation/389-schneider-enn47933'
                                '-instacables-diametre-16-32-gris.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-etanches/534-schneider-enn05004'
                                '-boite-de-derivation-a-embouts-80x80x45-gris.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-rigides/1722-eur-ohm'
                                '-70058-boite-de-50-connecteurs-transparents-8-entrees.html',
                                'https://www.e-planetelec.fr/materiel-incorporation-beton/2492-distancier-vertical'
                                '-p01042.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-etanches/535-schneider-enn05005'
                                '-boite-de-derivation-a-embouts-105x105x55-gris.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-rigides/1723-eur-ohm'
                                '-70069-blister-de-100-connecteurs-transparents-10-entrees.html',
                                'https://www.e-planetelec.fr/materiel-incorporation-beton/2493-distancier-horizontal'
                                '-entraxe-100-p0104300.html',
                                'https://www.e-planetelec.fr/colliers-embases-de-fixation/1755--enn47995-mureva-fix'
                                '-embase-universelle-pour-collier-d-installation.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-encastrees/2515-eur-ohm-51016-boite'
                                '-de-derivation-encastre-etanche-a-l-air-250x190x50.html',
                                'https://www.e-planetelec.fr/materiel-incorporation-beton/2494-boite-32a-couvercle'
                                '-imperdable-p0110013.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-rigides/1577-bornes-de'
                                '-connexion-automatique-2-trous-rouge-p07132.html',
                                'https://www.e-planetelec.fr/materiel-incorporation-beton/2495-pa-92-piton-m5-lame'
                                '-rigide-p0039934.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-rigides/1578-bornes-de'
                                '-connexion-automatique-3-trous-orange-p07133.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-rigides/1579-bornes-de'
                                '-connexion-automatique-4-trous-jaune-p07134.html',
                                'https://www.e-planetelec.fr/materiel-incorporation-beton/2496-couvercle-universel'
                                '-diametre-150mm-p0039070.html',
                                'https://www.e-planetelec.fr/bornes-de-connexion-rapides-fils-rigides/1580-bornes-de'
                                '-connexion-automatique-5-trous-gris-p07135.html',
                                'https://www.e-planetelec.fr/boites-de-derivation-etanches/2528-fixation-pour-boite'
                                '-de-derivation-sur-chemin-de-cables-43614.html',
                                'https://www.e-planetelec.fr/atlantic/3245-accessio-digital-2-radiateur-chaleur-douce'
                                '-2000w-atlantic.html',
                                'https://www.e-planetelec.fr/plancher-rayonnant-electrique/31-plancher-rayonnant'
                                '-electrique-ks-thermor.html#/43-largeur_de_trame-60_cm/45-puissance_trame-150w',
                                'https://www.e-planetelec.fr/thermostats-et-gestionnaires-d-energie/250-calybox-230'
                                '-gestionnaire-d-energie-delta-dore.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/3228-vmc-octeo-simple'
                                '-flux-hygro-ecowatt-607611-unelvent.html',
                                'https://www.e-planetelec.fr/plancher-rayonnant-electrique/33-realisation-d-etude-de'
                                '-dimensionnement.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/3229-vmc-octeo-simple'
                                '-flux-hygro-607711-unelvent.html',
                                'https://www.e-planetelec.fr/thermostat-connecte/1882-thermostat-d-ambiance-myneo'
                                '-stat-blanc-neomitis.html',
                                'https://www.e-planetelec.fr/plancher-rayonnant-electrique/34-thermostat-d-ambiance'
                                '-digital-ks-thermor.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1757-rayonnant-intelligent-et'
                                '-connecte-tatou-horizontal-300w-blanc-666416.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/3043-unelvent-vmc-ozeo'
                                '-ecowatt-604611.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/2129-unelvent-vmc-ozeo'
                                '-st-2-604711.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1758-rayonnant-intelligent-et'
                                '-connecte-tatou-horizontal-500w-blanc-666417.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/1696-kit-easy-home-hygro'
                                '-classic-aldes-11033031.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1759-rayonnant-intelligent-et'
                                '-connecte-tatou-horizontal-750w-blanc-666418.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/564-kit-easyhome-auto'
                                '-grilles-de-ventilation-colorline-aldes-11026033.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1760-rayonnant-intelligent-et'
                                '-connecte-tatou-horizontal-1000w-blanc-666419.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/653-gaine-isolee'
                                '-diametre-80.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1761-rayonnant-intelligent-et'
                                '-connecte-tatou-horizontal-1250w-blanc-666421.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/654-gaine-isolee'
                                '-diametre-125.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1762-rayonnant-intelligent-et'
                                '-connecte-tatou-horizontal-1500w-blanc-666422.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/655-gaine-isolee'
                                '-diametre-160.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1763-rayonnant-intelligent-et'
                                '-connecte-tatou-horizontal-2000w-blanc-666423.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/2130-unelvent-bouche'
                                '-salle-de-bains-850195-.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1764-rayonnant-intelligent-et'
                                '-connecte-tatou-vertical-1000w-blanc-666424.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1765-rayonnant-intelligent-et'
                                '-connecte-tatou-vertical-1500w-blanc-666425.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/3047-unelvent-bouche'
                                '-hygroreglable-sdbwc-detection-presence-a-piles-5-4030-d80-858056.html',
                                'https://www.e-planetelec.fr/radiateurs-fluide-caloporteur/1876-myneo-fluid'
                                '-anthracite-neomitis.html#/74-puissance-600w',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/2131-unelvent-bouche-wc'
                                '-858322.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1766-rayonnant-intelligent-et'
                                '-connecte-tatou-vertical-2000w-blanc-666426.html',
                                'https://www.e-planetelec.fr/radiateurs-fluide-caloporteur/1879-myneo-fluid-blanc'
                                '-neomitis.html#/74-puissance-600w',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/3044-gaine-souple-pvc'
                                '-standard-diametre-80-longueur-6m-une810196.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1769-rayonnant-digital-solius'
                                '-horizontal-500w-blanc-423533.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/3045-gaine-souple-pvc'
                                '-standard-diametre-125-longueur-6m-une810198.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1770-rayonnant-digital-solius'
                                '-horizontal-750w-blanc-423534.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/2421-manchon-raccord'
                                '-male-spiraclim-mrt-80-diametre-80mm-unv860355.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1771-rayonnant-digital-solius'
                                '-horizontal-1000w-blanc-423535.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/2422-manchon-raccord'
                                '-male-spiraclim-mrt-125-diametre-125mm-unv860353.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1772-rayonnant-digital-solius'
                                '-horizontal-1250w-blanc-423966.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/2423-manchon-raccord'
                                '-male-spiraclim-mrt-160-diametre-160mm-unv860354.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1773-rayonnant-digital-solius'
                                '-horizontal-1500w-blanc-423967.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/2508-extracteur-d-air'
                                '-cyklon-eol100b-kanlux-70911.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1774-rayonnant-digital-solius'
                                '-horizontal-2000w-blanc-423968.html',
                                'https://www.e-planetelec.fr/ventilation-mecanique-controlee/2509-extracteur-d-air'
                                '-cyklon-eol100ht-kanlux-70936.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1775-rayonnant-digital-solius'
                                '-vertical-1000w-blanc-423539.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1776-rayonnant-digital-solius'
                                '-vertical-1500w-blanc-423540.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1780-rayonnant-solius-horizontal'
                                '-500w-blanc-542405.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1781-rayonnant-solius-horizontal'
                                '-750w-blanc-542407.html',
                                'https://www.e-planetelec.fr/panneaux-rayonnants/1782-rayonnant-solius-horizontal'
                                '-1000w-blanc-542410.html']
    for l in link:
        try:
            response = requests.get(l)
            soup = BeautifulSoup(response.text, "html.parser")
            name = soup.find("h1", {"itemprop": "name"}).text.strip()
            ref = soup.find("p", {"class": "product_reference"}).text.strip().split(": ")[1]
            price = soup.find("span", {"itemprop": "price"}).text.strip().split(" ")[0].replace(",", ".").split("€")[0]
            info_produit = (3, ref, name, price, l)
            if database.search_item(3, ref) is False:
                database.insert_data(info_produit)
        except Exception as exception:
            print(exception)
            pass

def verify_page(soup):
    pages = []
    try:
        page = soup.find("ul", {"class": "page-list clearfix text-sm-center"}).find_all("a")
        for i in page:
            pages.append(i.text.strip())
        return pages[-2]
    except:
        return None


# cxn = sqlite3.connect('produits.db')
# wb = pd.read_excel('PRODUIT.xlsx',sheet_name = 'produits')
# wb.to_sql(name='PRODUIT',con=cxn,if_exists='replace',index=True)
# cxn.commit()
# cxn.close()