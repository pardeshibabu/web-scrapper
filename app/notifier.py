class Notifier:
    def notify(self, count):
        raise NotImplementedError

class ConsoleNotifier(Notifier):
    def notify(self, count):
        print(f"Scraping complete. {count} products scraped.")
