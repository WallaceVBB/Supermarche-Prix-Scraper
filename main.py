from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp
from scrapers.superu import SuperUScraper


def main():
    sb = sb_cdp.Chrome()
    endpoint_url = sb.get_endpoint_url()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)

        context = browser.contexts[0]

        page = context.new_page()

        # Bloquer les ressources inutiles pour accélérer le chargement
        page.route(
            "**/*",
            lambda route: route.abort()
            if route.request.resource_type in [
                "image",
                "media",
                "font"
            ]
            else route.continue_()
        )
        

        # Changez variable "Fournisseur" pour tester différents scrapers
        Fournisseur = "SuperU" 
        
        if Fournisseur == "SuperU":
            try:
                scraper = SuperUScraper(page)
                scraper.run()
                scraper.save_to_csv("donnees_supermarches/donnees_superu.csv")
            except Exception as e:
                print(f"❌ Erro: {e}")
                page.screenshot(path="error_superu.png", full_page=True)
        
        browser.close()

if __name__ == "__main__":
    main()
