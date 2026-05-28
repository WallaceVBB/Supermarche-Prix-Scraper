import time
from bs4 import BeautifulSoup
from .base import BaseScraper


class SuperUScraper(BaseScraper):

    sections = {"fruits-et-legumes"}

    def run(self):

        print("🚚 Scraping SuperU...")
        
        seen_refs = set()

        self.page.goto("https://www.coursesu.com/drive-superu-talantarandes",
                       wait_until="domcontentloaded",timeout=30000)
        
        self.accept_cookies()

        for section in self.sections:

            print(f"\n🔍 Section : {section}")

            url = f"https://www.coursesu.com/c/{section}"

            try:

                self.page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=30000
                )

                #self.accept_cookies()

                self.page.wait_for_selector(
                    ".product-tile",
                    timeout=10000
                )

                self.scroll_to_load_all_products()

            except Exception as e:

                print(f"❌ Erreur section {section}")
                print(e)

                continue

            # =========================
            # HTML COMPLET
            # =========================

            html = self.page.content()

            soup = BeautifulSoup(html, "html.parser")

            products = soup.select(".product-tile")

            print(f"📦 {len(products)} produits trouvés")

            for product in products:

                try:

                    ref = product.get("data-itemid")

                    if ref in seen_refs:
                        continue

                    seen_refs.add(ref)

                    product_data = self.extract_product(
                        product,
                        section
                    )

                    self.data.append(product_data)

                except Exception as e:

                    print("⚠️ Erreur extraction produit")
                    print(e)

        print(f"\n✅ {len(self.data)} produits récupérés")

    def scroll_to_load_all_products(self):
            print("⬇️ Chargement progressif des produits...")
            
            # Distance de scroll à chaque étape (en pixels)
            scroll_step = 250 
            # Temps d'attente entre chaque scroll pour laisser le temps au contenu de se charger (en secondes)
            scroll_delay = 0.5 
            
            last_height = self.page.evaluate("document.body.scrollHeight")
            current_position = 0

            while True:
                # Scroll vers le bas
                current_position += scroll_step
                self.page.evaluate(f"window.scrollTo(0, {current_position})")
                
                # Petite pause pour s'assurer que le "lazy loading" se déclenche
                time.sleep(scroll_delay)
                
                # Vérifie si le scroll_step était trop court et si nous devons descendre encore
                new_height = self.page.evaluate("document.body.scrollHeight")
                
                # Si la hauteur de la page n'a pas augmenté, cela signifie que nous avons atteint le bas
                if current_position >= new_height:
                    # Dernière vérification si la langeur de la page a augmenter depuis
                    time.sleep(2)
                    final_height = self.page.evaluate("document.body.scrollHeight")
                    if final_height == new_height:
                        break
                    else:
                        last_height = final_height

            # Revient au debut pour garantir que le scraper capture tous les produits
            self.page.evaluate("window.scrollTo(0, 0)")
            print("✅ Tous les produits sont chargés et visibles")

    def extract_product(self, product, current_section):

        data = {
            "designation": None,
            "reference": None,
            "url_product": None,
            "section": current_section,
            "prix": None,
            "prix_kg": None,
            "origine": None,
            "Fournisseur": "SuperU"
        }

        # Référence
        data["reference"] = product.get("data-itemid")

        # Désignation
        title = product.select_one(
            ".product-name .name-link"
        )

        if title:
            data["designation"] = title.get_text(strip=True)

        # URL
        link = product.select_one(
            "a.product-tile-link"
        )

        if link and link.get("href"):

            data["url_product"] = (
                "https://www.coursesu.com"
                + link.get("href")
            )

        # Prix
        price = product.select_one(".sale-price")

        if price:
            data["prix"] = price.get_text(strip=True)

        # Prix/kg
        unit_price = product.select_one(".unit-info")

        if unit_price:
            data["prix_kg"] = unit_price.get_text(strip=True)

        # Origine
        origine = product.select_one(".product-origine")

        if origine:
            data["origine"] = origine.get_text(strip=True)

        return data

    def accept_cookies(self):
        print("🍪 Tentative d'acceptation des cookies...")
        try:
            # Attente que le bouton d'acceptation des cookies soit visible
            self.page.wait_for_selector("#footer_tc_privacy_button", timeout=5000)
            
            # Nous essayons de cliquer sur le bouton d'acceptation des cookies via son selector
            btn = self.page.locator("#footer_tc_privacy_button")
            
            btn.click()
            print("✅ Cookies acceptés via bouton ID")

                
            # Petite pause pour s'assurer que le pop-up est bien fermé avant de continuer
            self.page.wait_for_timeout(1000)

        except Exception as e:
            try:
                self.page.get_by_role("button", name="Accepter & Fermer").click(timeout=2000)
                print("✅ Cookies acceptés via Role Name")
            except:
                print("ℹ️ Aucun pop-up de cookies trouvé ou déjà accepté.")
