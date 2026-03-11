from playwright.sync_api import sync_playwright
#from scrapers.sysco import SyscoScraper
from scrapers.intermarcher import IntermarcherScraper


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled","--no-sandbox", "--disable-dev-shm-usage"]
        )

        # Créer un nouveau contexte de navigateur avec des paramètres personnalisés
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="fr-FR",
            timezone_id="Europe/Paris"
        )

        page = context.new_page()

        # Changez variable "Fournisseur" pour tester différents scrapers
        Fournisseur = "Intermarcher" 
        
        if Fournisseur == "Intermarcher": # OK
            scraper = IntermarcherScraper(page)
            scraper.run()
            scraper.save_to_csv("donnees_supermarches/donnees_intermarcher.csv")

        browser.close()

if __name__ == "__main__":
    main()