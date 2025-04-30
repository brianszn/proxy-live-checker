import requests as r
from colorama import Fore
from time import sleep
from concurrent.futures import ThreadPoolExecutor

class ProxyList:

    def __init__(self, api: str, proxies_list: list, url: str) -> None:
        self.api: str = api
        self.proxies_list: list = proxies_list
        self.url = url

    def get_proxy_list(self):
        self.proxies_list = [proxy.strip() for proxy in r.get(self.api).text.split('\n') if proxy]
        return self.proxies_list
    
    def check_proxy(self, proxy: str) -> None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        try:
            response = r.get(self.url, proxies={"http": proxy}, headers=headers, timeout=10).status_code
            if response == 200:
                print(Fore.YELLOW + f'{proxy}', Fore.GREEN + '[ONLINE]')
            else:
                print(Fore.YELLOW + f'{proxy}', Fore.RED + '[OFFLINE]')
        except r.exceptions.RequestException as e:
            print(Fore.YELLOW + f'{proxy}', Fore.RED + '[OFFLINE]')

    def fetch_proxy_list(self):
        
        while True:
            print(Fore.CYAN + f'[+] Descansando da rotação de proxy por 10 segundos.')
            self.get_proxy_list()

            # Usando ThreadPoolExecutor para verificar os proxies em paralelo
            with ThreadPoolExecutor(max_workers=30) as executor:
                executor.map(self.check_proxy, self.proxies_list)

            sleep(10)  # Pausa para evitar sobrecarregar a API e dar tempo para novas atualizações de proxies

if __name__ == "__main__":
    proxies_list = []
    url = "http://127.0.0.1/"
    api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"

    proxy = ProxyList(api_url, proxies_list, url)
    proxy.fetch_proxy_list()
