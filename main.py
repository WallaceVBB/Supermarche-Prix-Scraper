from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp
from scrapers.superu import SuperUScraper
import random


'''USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]'''

def main():
    sb = sb_cdp.Chrome()
    endpoint_url = sb.get_endpoint_url()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)

        context = browser.contexts[0]

        page = context.new_page()
        

        # Changez variable "Fournisseur" pour tester différents scrapers
        Fournisseur = "SuperU" 
        
        if Fournisseur == "SuperU": # OK
            try:
                scraper = SuperUScraper(page)
                scraper.run()
                page.screenshot(path="verif_superu.png", full_page=True)
                scraper.save_to_csv("donnees_supermarches/donnees_superu.csv")
            except Exception as e:
                print(f"❌ Erro: {e}")
                page.screenshot(path="error_superu.png", full_page=True)
        
        context.tracing.stop(path="trace.zip")
        browser.close()

if __name__ == "__main__":
    main()
