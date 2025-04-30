
import requests as r
from colorama import Fore, Back, Style
from time import sleep
from concurrent.futures import ThreadPoolExecutor

class ProxyList:

    def __init__(self, api: str, proxies_list: list, url: str) -> None:

        self.api: str = api
        self.proxies_list: list = proxies_list
        self.url = url

    def get_proxy_list(self) -> list:

        self.proxies_list = [proxy.strip() for proxy in r.get(self.api).text.split('\n') if proxy]

        return self.proxies_list
    
    

    def fetch_proxy_list(self):

        self.get_proxy_list()

        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        while True:

            print(Fore.CYAN + f'[+] Descansando da rotação de proxy por 10 segundos.')

            self.get_proxy_list()
            for i in range(0, len(self.proxies_list)):

                try:
                        
                    response = r.get(self.url, proxies={"http": self.proxies_list[i]}, headers=headers, timeout=10).status_code

                    if response == 200:
                        print(Fore.YELLOW +f'{self.proxies_list[i]}', Fore.GREEN + '[ONLINE]')

                except r.exceptions.RequestException as e:
                    print(Fore.YELLOW + f'{self.proxies_list[i]}', Fore.RED + '[OFFLINE]')

        sleep(10)

                

if __name__ == "__main__":

    proxies_list = []

    url = "http://127.0.0.1/"
    
    api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    
    proxy = ProxyList(api_url, proxies_list, url)
    
    proxy.fetch_proxy_list()