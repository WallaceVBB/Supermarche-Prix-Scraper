from abc import ABC, abstractmethod
import pandas as pd

class BaseScraper(ABC):

    def __init__(self, page):
        self.page = page
        self.data = []

    @abstractmethod
    def run(self):
        pass

    def save_to_csv(self, filename):
        df = pd.DataFrame(self.data)
        df.to_csv(filename, sep=";", index=False)
        print(f"💾 Données sauvegardées dans {filename}")