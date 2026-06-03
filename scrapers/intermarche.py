from .base import BaseScraper


class IntermarcheScraper(BaseScraper):

    categories = {
        "bio": [
            "du-bio-pour-bebe/6866",
            "fruits-et-legumes-bio/8637",
            "produits-frais-bio/6961",
            "surgeles-bio/6867",
            "epicerie-salee-bio/6962",
            "epicerie-sucree-bio/6963",
            "vrac-bio/16368",
            "saveurs-du-monde-bio/17629",
            "boissons-bio/6964",
            "hygiene-et-soin-bio/6965",
            "entretien-ecologique/6966"
        ],
        "fruits-et-legumes": [
            "fruits/7569",
            "legumes/7570",
            "fruits-et-legumes-decoupes/16210",
            "gazpachos-et-legumes-cuisines/16211",
            "jus-de-fruits-frais/7572",
            "fruits-et-legumes-secs/7573"
        ],
        "viandes-et-poissons": [
            "viandes-et-poissons-bio/9587",
            "special-barbecue/9589",
            "viandes-a-la-coupe/9588",
            "poissonnerie-a-la-coupe/16953",
            "boucherie/9590",
            "volaille/9591",
            "poissonnerie/9592",
            "traiteur-de-la-mer/9593",
            "sushi-et-maki-traditionnel/sauces/17606"
        ],
        "charcuterie": [
            "charcuterie-bio/15406",
            "charcuterie-a-la-coupe/15499",
            "saucissons-salamis-et-chorizos/15391",
            "jambons-blancs-et-rotis/15392",
            "jambons-de-volaille-et-rotis/15393",
            "jambons-crus/15394",
            "lardons-des-et-bacons/15395",
            "saucisses-knacks-et-boudins/15396",
            "pates-rillettes-et-foies-gras/15388",
            "sales-et-fumes/15710",
            "produits-tripiers/15498",
            "halal/16955"
        ],
        "traiteur": [
            "traiteur-bio/9625",
            "traiteur-a-la-coupe/13023",
            "salades-preparees-et-taboules/9628",
            "entrees-aperitifs-et-tartinables/10272",
            "snacking-et-pause-dejeuner/9631",
            "plats-cuisines-et-cuisines-du-monde/10266",
            "pizzas-quiches-et-tartes/9632",
            "burgers-et-croques/17055",
            "pates-fraiches-gnocchis-et-quenelles/9629",
            "cordons-bleus-nuggets-et-grignottes/9633",
            "pates-a-tarte-et-a-pizza/9630",
            "traiteur-vegetal/14777"
        ],
        "pains-et-patisseries": [
            "pains-et-patisseries-bio/9677",
            "pains-frais/9678",
            "pains-de-table-et-a-cuire/17324",
            "pains-de-mie-et-toasts/9679",
            "pains-sandwichs-et-burgers/16435",
            "viennoiseries-et-brioches-fraiches/9680",
            "patisseries/9681"
        ],
        "yaourts-et-desserts": [
            "yaourts-et-desserts-bio/16779",
            "brebis-chevres-et-vegetal/16788",
            "yaourts-blancs-natures/16780",
            "yaourts-fruites/16778",
            "yaourts-aromatises/16781",
            "skyrs-fromage-blancs-et-petits-suisses/16784",
            "bien-etre-bifidus-et-alleges/16802",
            "yaourts-a-boire-et-boissons-lactees/17554",
            "desserts-patissiers-et-italiens/16786",
            "flans-cremes-aux-oeufs-riz-au-lait/16791",
            "mousses-et-liegeois/16793",
            "cremes-desserts-et-petits-pots/16792",
            "compotes-fraiches-et-desserts-aux-fruits/16790",
            "yaourts-et-desserts-enfants/16789"
        ],
        "fromages-cremerie-et-oeufs": [
            "fromages-cremerie-et-oeufs-bio/7581",
            "fromages-de-degustation/16816",
            "fromages-a-cuisiner-et-aperitifs/16817",
            "laits-et-boissons-lactees/7577",
            "oeufs/16773",
            "cremes-et-sauces/15055",
            "beurres-et-margarines/7578",
            "boissons-vegetales/15161"
        ],
        "surgeles": [
            "surgeles-bio/7090",
            "glaces-et-sorbets/6776",
            "aperitifs-entrees-et-snacking/6770",
            "pizzas/6771",
            "plats-cuisines/6772",
            "legumes/16416",
            "pommes-de-terre-et-frites/16408",
            "viandes/6774",
            "poissons-et-fruits-de-mer/6775",
            "desserts-et-patisseries/6777",
            "saveurs-du-monde/16297"
        ],
        "saveurs-du-monde": [
            "saveurs-asiatiques/17409",
            "saveurs-mexicaines/17410",
            "saveurs-italiennes/17411",
            "saveurs-portugaises/17412",
            "saveurs-orientales/17413",
            "saveurs-americaines/17506",
            "autres-saveurs-du-monde/17414"
        ],
        "epicerie-sucree": [
            "epicerie-sucree-bio/7610",
            "petit-dejeuner/7604",
            "cafes-et-filtres/7605",
            "the-infusion-et-boisson-chocolatee/7606",
            "confiseries-et-chocolats/7603",
            "biscuits/7602",
            "gateaux-moelleux/14897",
            "pains-de-mie-et-toasts/16429",
            "pains-sandwichs-et-burgers/16430",
            "compotes-et-fruits-au-sirop/14884",
            "farine-et-patisserie/7607",
            "sucre-et-edulcorant/7608",
            "nutrition-et-dietetique/9248"
        ],
        "epicerie-salee": [
            "epicerie-salee-bio/7599",
            "aperitifs-et-chips/7600",
            "pates-et-sauces/17011",
            "riz-purees-et-feculents/7593",
            "pates-rillettes-et-foies-gras/17725",
            "plats-cuisines/14037",
            "conserves-de-legumes/14038",
            "conserves-de-poissons/14039",
            "sel-huile-epices-et-bouillons/7595",
            "sauces/7597",
            "soupes-et-croutons/7596",
            "nutrition-et-dietetique/9247"
        ],
        "eaux-sodas-et-jus": [
            "eaux-sodas-et-jus-bio/16577",
            "thes-glaces/16442",
            "sirops-et-concentres/15449",
            "eaux-plates/15384",
            "eaux-gazeuses/15471",
            "jus-de-fruits-et-legumes/15463",
            "jus-frais-et-soupes-fraiches/15473",
            "colas-et-boissons-gazeuses/15454",
            "boissons-aux-fruits/15451",
            "cafes-et-thes/15429"
        ]
    }

    def run(self):
        print("🚚 Scraping Intermarché...")
        seen_refs = set()

        self.page.goto("https://www.intermarche.com/magasins/10718/fontaine-les-dijon-21121/infos-pratiques",
                        wait_until="domcontentloaded", timeout=30000)

        self.accept_cookies()

        self.access_shop()

        for category, subcategories in self.categories.items():
            for subcategory in subcategories:

                print(f"\n🔍 Categorie: {category} ➔ Subcategorie: {subcategory}")
                url = f"https://www.intermarche.com/rayons/{category}/{subcategory}"

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

    def access_shop (self):
        print("🏪 Accès à la boutique spécifique...")
        try:
            self.page.wait_for_selector("a:has-text('Faire mes courses')", timeout=5000)
            self.page.click("a:has-text('Faire mes courses')")
            print("✅ Accès à la boutique réussi")
            self.page.wait_for_timeout(2000)
        except Exception:
            print("❌ Bouton d'accès à la boutique non trouvé ou déjà sur la boutique.")

    def accept_cookies(self):
        print("🍪 Tentative d'acceptation des cookies...")
        try:
            self.page.wait_for_selector("#didomi-notice-agree-button", timeout=5000)
            btn = self.page.locator("#didomi-notice-agree-button")
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
                        // Product title
                        const titleEl = e.querySelector('.stime-product--details__title');
                        // Product price
                        const priceEl = e.querySelector('.text-title2.font-bold') || e.querySelector('.font-brand');
                        // Product unit price (e.g., "2,29 €/Pièce")
                        const unitEl = e.querySelector('.stime-product--details__packaging');
                        let unitText = unitEl ? unitEl.textContent.trim() : null;
                        if (unitText && unitText.includes('•')) {
                            unitText = unitText.split('•')[1].trim(); // Pega só o "2,29 €/Pièce"
                        }
                        // Product origin                                                    
                        const orgEl = e.querySelector('.text-pays');
                        
                        return {
                            reference: ref,
                            designation: titleEl ? titleEl.textContent.trim() : null,
                            url_product: titleEl && titleEl.getAttribute('href') ? 'https://www.coursesu.com' + titleEl.getAttribute('href') : null,
                            prix: priceEl ? priceEl.getAttribute('data-item-price') : null,
                            prix_kg: unitText,
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
