import time
from .base import BaseScraper


class AgidraScraper(BaseScraper):

    categories = {
        "epicerie-salee": [
            "fournisseur-aperitifs-biscuits-sales-et-chips/famille-2-2.html",
            "fournisseur-assaisonnements-et-condiments/famille-3-2.html",
            "fournisseur-cereales/famille-13-2.html",
            "fournisseur-conserves-de-legumes/famille-12-2.html",
            "fournisseur-conserves-terre-et-mer/famille-11-2.html",
            "fournisseur-epices-et-herbes-aromatiques/famille-15-2.html",
            "fournisseur-legumes-secs/famille-17-2.html",
            "fournisseur-olives-et-tartinables/famille-19-2.html",
            "fournisseur-pates/famille-47-2.html",
            "plats-cuisines/famille-89-2.html",
            "fournisseur-riz/famille-24-2.html",
            "fournisseur-soupes/famille-25-2.html"
        ],
        "epicerie-sucree": [
            "fournisseur-aides-a-la-patisserie/famille-1-3.html",
            "fournisseur-biscuits-gateaux/famille-5-3.html",
            "fournisseur-bonbons-et-confiseries/famille-7-3.html",
            "fournisseur-cafes-et-chocolats/famille-8-3.html",
            "fournisseur-chocolats/famille-9-3.html",
            "fournisseur-confitures-miels-et-pates-a-tartiner/famille-10-3.html",
            "fournisseur-desserts/famille-14-3.html",
            "fournisseur-fruits-secs/famille-16-3.html",
            "fournisseur-pains-et-viennoiseries/famille-20-3.html",
            "fournisseur-thes-et-infusions/famille-26-3.html"
        ],
        "boissons": [
            "fournisseur-boissons-aux-fruits/famille-55-1.html",
            "fournisseur-boissons-vegetales/famille-31-1.html",
            "fournisseur-cafes-et-chocolats/famille-8-1.html",
            "fournisseur-jus-de-fruits-et-legumes/famille-27-1.html",
            "fournisseur-sirops/famille-60-1.html",
            "fournisseur-sodas-et-limonades/famille-30-1.html",
            "fournisseur-thes-et-infusions/famille-26-1.html"
        ]
    }

    def run(self):
        print("🚚 Scraping Agidra...") 
        seen_refs = set()

        self.page.goto("https://www.agidra.com",
                        wait_until="domcontentloaded", timeout=30000)
        
        self.accept_cookies()

        for category, subcategories in self.categories.items():
            for subcategory in subcategories:

                print(f"\n🔍 Categorie: {category} ➔ Subcategorie: {subcategory}")
                url = f"https://www.agidra.com/c/{category}/{subcategory}"

                try:
                    self.page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=30000
                    )

                    self.page.wait_for_selector(
                        "article.vignetteProduit",
                        timeout=10000
                    )

                    self.click_to_load_all_products(category, subcategory, seen_refs)

                except Exception as e:
                    print(f"❌ Erreur sur {category}/{subcategory}")
                    print(e)
                    continue

        print(f"\n✅ {len(self.data)} produits récupérés au total")

    def accept_cookies(self):
        print("🍪 Tentative d'acceptation des cookies...")
        try:
            self.page.wait_for_selector(".highlight-button", timeout=5000)
            btn = self.page.locator(".highlight-button")
            btn.click()
            print("✅ Cookies accepted")
            self.page.wait_for_timeout(1000)
        except Exception:
            try:
                self.page.get_by_role("button", name="Accepter & Fermer").click(timeout=2000)
                print("✅ Cookies acceptés via Role Name")
            except Exception:
                print("ℹ️ Aucun pop-up de cookies trouvé ou déjà accepté.")

#Click method
    def click_to_load_all_products(self, category, subcategory, seen_refs):
        print("⬇️ Chargement de tous os produtos via bouton...")

        #button_selector = self.page.locator(".plusproduit")
        
        clicks = 0
        while True:
            try:
                # Create a locator for the button
                more_products_button = self.page.locator(".plusproduit")
                
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
                print("ℹ️ End of clicks or button not found.")
                break

        print("✅ Extraction des données en cours...")
        
        products_data = self.page.locator("article.vignetteProduit").evaluate_all("""
                    (els) => {
                        return els.map(e => {
                            const linkEl = e.querySelector('a');
                            const url = linkEl ? linkEl.getAttribute('href') : null;

                            const refEl = e.querySelector('.boutonVignette');
                            const ref = refEl ? refEl.getAttribute('data-produit-id') : null;

                            const titleEl = e.querySelector('.libelleProduit.hidden-xs');
                            const title = titleEl ? titleEl.textContent.trim() : null;

                            const priceEl = e.querySelector('.prix');
                            let price = null;
                            if (priceEl) {
                                price = priceEl.textContent.replace('€ HT/KG', '').trim();
                            }

                            const unitEl = e.querySelector('.zoneRef.hidden-xs');
                            let unit = null;

                            if (unitEl) {
                                const rawText = unitEl.textContent.trim();
                                
                                const match = rawText.match(/(\d+[\d,.]*\s*€)/);
                                
                                if (match) {
                                    unit = match[0];
                                }
                            }

                            return {
                                reference: ref,
                                designation: title,
                                prix: price,
                                prix_kg: unit,
                                url_product: url ? 'https://www.agidra.com/' + url : null,
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
            p["Fournisseur"] = "Agidra"
            
            self.data.append(p)
            print(f"-> {p['designation']}")

        print(f"✅ Fin du chargement de la sous-catégorie. Total vistos: {len(seen_refs)}")