import time
from .base import BaseScraper


class SuperUScraper(BaseScraper):

    sections = ["fruits-et-legumes","viandes-poissons",
                "charcuterie-traiteur","produits-laitiers-oeufs-et-fromages",
                "surgeles", "epicerie-salee",
                "epicerie-sucree", "pains-viennoiseries-et-patisseries",
                "boissons-sans-alcool", "bio",
                "nutrition-et-regimes-alimentaires", "univers-bebe",
                "hygiene-et-beaute", "entretien-et-nettoyage"]
    
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

                #self.scroll_to_load_all_products()

                self.scroll_to_load_all_products(section,seen_refs)

            except Exception as e:

                print(f"❌ Erreur section {section}")
                print(e)

                continue

        print(f"\n✅ {len(self.data)} produits récupérés")

    def extract_product(self, product, current_section):

        data = {
            "designation": None,
            "reference": None,
            "section": current_section,
            "prix": None,
            "prix_kg": None,
            "origine": None,
            "Fournisseur": "SuperU",
            "url_product": None
        }

        # Référence
        data["reference"] = product.get(
            "data-itemid"
        )

        # Désignation
        title = product.select_one(
            ".product-name .name-link"
        )

        if title:
            data["designation"] = (
                title.get_text(strip=True)
            )

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
        price = product.select_one(
            ".sale-price"
        )

        if price:

            data["prix"] = (
                price.get(
                    "data-item-price"
                )
            )

        # Prix/kg
        unit_price = product.select_one(
            ".unit-info"
        )

        if unit_price:

            data["prix_kg"] = (
                unit_price.get_text(strip=True)
            )

        # Origine
        origine = product.select_one(
            ".product-origine"
        )

        if origine:

            data["origine"] = (
                origine.get_text(strip=True)
            )

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

    def scroll_to_load_all_products(self, section, seen_refs):
        print("⬇️ Chargement progressif des produits...")

        no_new_products = 0
        last_seen_count = 0

        while True:
            # Extração direta no JavaScript
            products_data = self.page.locator(".product-tile").evaluate_all("""
                (els) => {
                    return els.map(e => {
                        const ref = e.getAttribute('data-itemid');
                        const titleEl = e.querySelector('.product-name .name-link');
                        const priceEl = e.querySelector('.sale-price');
                        const unitEl = e.querySelector('.unit-info');
                        const orgEl = e.querySelector('.product-origine');
                        
                        return {
                            reference: ref,
                            designation: titleEl ? titleEl.textContent.trim() : null,
                            url_product: titleEl && titleEl.getAttribute('href') ? 'https://www.coursesu.com' + titleEl.getAttribute('href') : null,
                            prix: priceEl ? priceEl.getAttribute('data-item-price') : null,
                            prix_kg: unitEl ? unitEl.textContent.trim() : null,
                            origine: orgEl ? orgEl.textContent.trim() : null
                        };
                    });
                }
            """)

            print(f"📦 Produits actuellement dans le DOM: {len(products_data)}")

            # 2. Processamento ultra rápido dos dicionários em Python
            for p in products_data:
                ref = p["reference"]
                if not ref or ref in seen_refs:
                    continue

                seen_refs.add(ref)
                
                # Adiciona os metadados diretamente no dicionário vindo do JS
                p["section"] = section
                p["Fournisseur"] = "SuperU"
                
                self.data.append(p)
                print(f"-> {p['designation']}")

            # Verica se novos produtos foram carregados comparando o número de referências vistas
            if len(seen_refs) == last_seen_count:
                no_new_products += 1
            else:
                no_new_products = 0

            last_seen_count = len(seen_refs)

            # Se não surgirem novos produtos após algumas tentativas, encerra a seção
            if no_new_products >= 10: 
                print("✅ Fin du chargement détectée")
                break

            # Rola até o último elemento renderizado para ativar o infinite scroll
            try:
                self.page.locator(".product-tile").last.scroll_into_view_if_needed()
            except Exception:
                # Fallback de segurança caso o locator falhe por um milissegundo
                self.page.evaluate("window.scrollBy(0, 800)")

            # Tempo para o site carregar mais dados
            self.page.wait_for_timeout(1000)
