import time
from .base import BaseScraper


class ShopScraper(BaseScraper): # TODO: Replace

    # TODO: Replace
    categories = {
        "fruits-et-legumes": [
            "fruits-et-legumes-bio",
            "fruits",
            "legumes",
            "prets-a-consommer",
            "jus-de-fruits-et-legumes-frais"
        ],
        "viandes-poissons": [
            "tout-pour-le-barbecue",
            "prepare-sur-place-par-nos-bouchers",
            "boucherie",
            "volaille",
            "prepare-sur-place-par-nos-poissonniers",
            "poissonnerie",
            "traiteur-de-la-mer"
        ]
    }

    def run(self):
        print("🚚 Scraping Shop...") # TODO: Replace
        seen_refs = set()

        self.page.goto("https://www.shop_link",
                        wait_until="domcontentloaded", timeout=30000) # TODO: Replace
        
        self.accept_cookies()

        for category, subcategories in self.categories.items():
            for subcategory in subcategories:

                print(f"\n🔍 Categorie: {category} ➔ Subcategorie: {subcategory}")
                url = f"https://www.shop_link/c/{category}/{subcategory}" # TODO: Replace

                try:
                    self.page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=30000
                    )

                    self.page.wait_for_selector(
                        ".product-tile",
                        timeout=10000
                    )

                    self.scroll_to_load_all_products(category, subcategory, seen_refs) # TODO : Replace by click_to_load_all_products if the site has a "Load more" button

                except Exception as e:
                    print(f"❌ Erreur sur {category}/{subcategory}")
                    print(e)
                    continue

        print(f"\n✅ {len(self.data)} produits récupérés au total")

    def accept_cookies(self):
        print("🍪 Tentative d'acceptation des cookies...")
        try:
            self.page.wait_for_selector("locator", timeout=5000) # TODO: Replace locator
            btn = self.page.locator("locator") # TODO: Replace locator
            btn.click()
            print("✅ Cookies accepted")
            self.page.wait_for_timeout(1000)
        except Exception:
            try:
                self.page.get_by_role("button", name="Accepter & Fermer").click(timeout=2000)
                print("✅ Cookies acceptés via Role Name")
            except Exception:
                print("ℹ️ Aucun pop-up de cookies trouvé ou déjà accepté.")

# Scroll method
    def scroll_to_load_all_products(self, category, subcategory, seen_refs):
        print("⬇️ Chargement progressif des produits...")

        no_new_products = 0
        last_seen_count = 0

        while True:
            # Récupération des données des produits actuellement chargés par JavaScript
            products_data = self.page.locator(".correct_selector").evaluate_all("""
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
                            url_product: titleEl && titleEl.getAttribute('href') ? 'https://www.shop_link.com' + titleEl.getAttribute('href') : null,
                            prix: priceEl ? priceEl.getAttribute('data-item-price') : null,
                            prix_kg: unitEl ? unitEl.textContent.trim() : null,
                            origine: orgEl ? orgEl.textContent.trim() : null
                        };
                    });
                }
            """) # TODO: Replace selectors and https

            for p in products_data:
                ref = p["reference"]
                if not ref or ref in seen_refs:
                    continue

                seen_refs.add(ref)
                
                # On insère les catégories, subcatégories et le fournisseur dans les données du produit
                p["categorie"] = category
                p["sub_categorie"] = subcategory
                p["Fournisseur"] = "SuperU"
                
                self.data.append(p)
                print(f"-> {p['designation']}")

            if len(seen_refs) == last_seen_count:
                no_new_products += 1
            else:
                no_new_products = 0

            last_seen_count = len(seen_refs)

            if no_new_products >= 8: 
                print("✅ Fin du chargement de la sous-catégorie")
                break

            try:
                self.page.locator(".product-tile").last.scroll_into_view_if_needed()
            except Exception:
                self.page.evaluate("window.scrollBy(0, 700)")

            self.page.wait_for_timeout(900)

#Click method
    def click_to_load_all_products(self, category, subcategory, seen_refs):
        print("⬇️ Chargement de tous os produtos via bouton...")

        button_selector = "button:has-text('AFFICHEZ PLUS DE PRODUITS')" # TODO: Replace selector
        
        clicks = 0
        while True:
            try:
                # Create a locator for the button
                more_products_button = self.page.locator(button_selector)
                
                # Verify if the button exists and can be clicked
                if more_products_button.count() > 0 and more_products_button.is_visible():
                    
                    # Scroll to the button to ensure it's in view before clicking
                    more_products_button.scroll_into_view_if_needed()
                    
                    # Click the button to load more products
                    more_products_button.click(timeout=5000)
                    clicks += 1
                    print(f"   ➔ Click sur 'Plus de produits' ({clicks})")
                    
                    # Wait a moment for new products to load after the click
                    self.page.wait_for_timeout(1200)
                else:
                    # Se o botão sumiu ou chegou ao fim, saímos do loop de cliques
                    print("✅ All the products should be loaded.")
                    break
                    
            except Exception as e:
                # Se der erro ao clicar (ex: o botão ficou desabilitado), encerra os cliques
                print("ℹ️ End of clicks or button not found.")
                break

        # --- FASE 2: EXTRAÇÃO DOS DADOS (UMA ÚNICA VEZ) ---
        print("⚡ Extraction des données en cours...")
        
        # Executa o evaluate_all para pegar tudo o que foi carregado de uma vez só
        products_data = self.page.locator(".product-tile").evaluate_all("""
            (els) => {
                return els.map(e => {
                    const ref = e.getAttribute('data-itemid') || e.getAttribute('id');
                    const titleEl = e.querySelector('.product-name .name-link');
                    const priceEl = e.querySelector('.sale-price');
                    const unitEl = e.querySelector('.unit-info');
                    const orgEl = e.querySelector('.product-origine');
                    
                    return {
                        reference: ref,
                        designation: titleEl ? titleEl.textContent.trim() : null,
                        url_product: titleEl && titleEl.getAttribute('href') ? 'https://www.shop_link.com' + titleEl.getAttribute('href') : null,
                        prix: priceEl ? priceEl.getAttribute('data-item-price') : priceEl.textContent.trim() : null,
                        prix_kg: unitEl ? unitEl.textContent.trim() : null,
                        origine: orgEl ? orgEl.textContent.trim() : null
                    };
                });
            }
        """)

        for p in products_data:
            ref = p["reference"]
            if not ref or ref in seen_refs:
                continue

            seen_refs.add(ref)
            
            p["categoria"] = category
            p["sub_categoria"] = subcategory
            p["Fournisseur"] = "ShopName" # TODO: Replace
            
            self.data.append(p)
            print(f"-> {p['designation']}")

        print(f"✅ Fin du chargement de la sous-catégorie. Total vistos: {len(seen_refs)}")