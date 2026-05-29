import time
from .base import BaseScraper


class SuperUScraper(BaseScraper):

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
        ],
        "charcuterie-traiteur": [
            "aperitif",
            "charcuterie-traditionnelle",
            "charcuterie",
            "traiteur-traditionnel",
            "salades-et-entrees",
            "pate-a-tarte-et-autre-pate",
            "pizza-quiche-pates-fraiches-crepe",
            "vegetal",
            "plats-cuisines-et-snacking",
            "cuisine-du-monde"
        ],
        "produits-laitiers-oeufs-et-fromages": [
            "beurres-cremes-et-oeufs",
            "laits",
            "fromages-a-deguster",
            "fromages-a-cuisiner-aperitifs-et-rapes",
            "yaourts-et-fromages-blancs",
            "desserts-et-compotes",
            "pate-a-tarte-et-autre-pate",
            "le-vegetal",
            "jus-de-fruits-et-legumes-frais"
        ],
        "surgeles": [
            "surgeles-bio",
            "glaces-et-sorbets",
            "desserts-viennoiseries-et-fruits",
            "aperitifs-entrees-et-snacks",
            "pizzas-quiches-et-tartes",
            "plats-cuisines",
            "legumes-surgeles",
            "pommes-de-terre-et-frites",
            "viandes",
            "poissons-et-fruits-de-mer",
            "produits-du-monde"
        ],
        "epicerie-salee": [
            "aperitifs-et-chips",
            "riz-purees-feculents",
            "pates",
            "conserves-de-poissons-et-viandes",
            "conserves-de-legumes",
            "plats-cuisines",
            "produits-du-monde",
            "assaisonnements-et-condiments",
            "sauces-et-bouillons",
            "soupes-et-croutons"
        ],
        "epicerie-sucree": [
            "cafes",
            "thes-et-chocolats-en-poudre",
            "petit-dejeuner",
            "pate-a-tartiner-confiture-et-miel",
            "biscuits",
            "gateaux-moelleux",
            "tablettes-et-chocolat",
            "bonbons",
            "sucre-farine-patisserie",
            "compotes-et-desserts"
        ],
        "pains-viennoiseries-et-patisseries": [
            "pains-du-fournil",
            "pains-de-mie-pains-pre-emballes",
            "viennoiseries-et-brioches",
            "patisseries-fraiches",
            "gateaux-moelleux-et-biscuiterie",
            "le-bio"
        ],
        "boissons-sans-alcool": [
            "eaux",
            "sodas-et-boissons-aux-fruits",
            "jus-de-fruits-et-de-legumes",
            "sirops-et-concentres",
            "laits-et-boissons-vegetales",
            "cafes",
            "thes-et-chocolats-en-poudre",
            "bieres-et-aperitifs-sans-alcool"
        ],
        "nutrition-et-regimes-alimentaires": [
            "vegetal",
            "nutrition-quotidienne",
            "sans-gluten",
            "sans-sucres-sans-sucres-ajoutes"
        ],
        "univers-bebe": [
            "bebe-bio",
            "laits-et-petit-dejeuner",
            "repas",
            "desserts-gouters",
            "couches-culottes",
            "toilette-soins-bebe",
            "equipements-et-accessoires-bebe"
        ],
        "hygiene-et-beaute": [
            "hygiene-et-soin-du-corps",
            "soin-des-cheveux",
            "dentaire",
            "soin-du-visage",
            "solaire-et-brumisateur",
            "papiers-cotons",
            "hygiene-intime",
            "hygiene-soin-homme",
            "maquillage",
            "parapharmacie"
        ],
        "entretien-et-nettoyage": [
            "papier-toilette-essuie-tout-mouchoirs",
            "lessives-et-soin-du-linge",
            "nettoyants",
            "accessoires-pour-le-menage",
            "vaisselle",
            "sacs-emballages",
            "essuyage",
            "desodorisant",
            "cirage",
            "insectes-allume-feux"
        ]
    }

    def run(self):
        print("🚚 Scraping SuperU...")
        seen_refs = set()

        self.page.goto("https://www.coursesu.com/drive-superu-talantarandes",
                        wait_until="domcontentloaded", timeout=30000)
        
        self.accept_cookies()

        for category, subcategories in self.categories.items():
            for subcategory in subcategories:

                print(f"\n🔍 Categorie: {category} ➔ Subcategorie: {subcategory}")
                url = f"https://www.coursesu.com/c/{category}/{subcategory}"

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

                    self.scroll_to_load_all_products(category, subcategory, seen_refs)

                except Exception as e:
                    print(f"❌ Erreur sur {category}/{subcategory}")
                    print(e)
                    continue

        print(f"\n✅ {len(self.data)} produits récupérés au total")

    def accept_cookies(self):
        print("🍪 Tentative d'acceptation des cookies...")
        try:
            self.page.wait_for_selector("#footer_tc_privacy_button", timeout=5000)
            btn = self.page.locator("#footer_tc_privacy_button")
            btn.click()
            print("✅ Cookies acceptés via bouton ID")
            self.page.wait_for_timeout(1000)
        except Exception:
            try:
                self.page.get_by_role("button", name="Accepter & Fermer").click(timeout=2000)
                print("✅ Cookies acceptés via Role Name")
            except Exception:
                print("ℹ️ Aucun pop-up de cookies trouvé ou déjà accepté.")

    def scroll_to_load_all_products(self, category, subcategory, seen_refs):
        print("⬇️ Chargement progressif des produits...")

        no_new_products = 0
        last_seen_count = 0

        while True:
            # Récupération des données des produits actuellement chargés par JavaScript
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
