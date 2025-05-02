
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
    
    def test_proxy_list(self, proxy: str) -> None:  

        # Necessita de um argumento, para receber apenas 1 proxy, pois servirá de iterador no executor.map().

        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        try:    

            response = r.get('http://ifconfig.me/ip', proxies={"http": proxy}, headers=headers, timeout=10)
            if response.status_code == 200:

                print(Fore.YELLOW +f'[free-proxy] ➔ {proxy}\n[ifconfig.me] ➔ {response.text} ', Fore.GREEN + '[ONLINE]\n')

        except r.exceptions.RequestException as e:
            pass

    def fetch_proxy_list(self, arg_function): # Aqui uso o ThreadPoolExecutor

        while True:

            print(Fore.CYAN + f'[+] Descansando da rotação de proxy por 10 segundos.')

            self.get_proxy_list()

            # Usando ThreadPoolExecutor para verificar os proxies em paralelo
            with ThreadPoolExecutor(max_workers=100) as executor:
                executor.map(arg_function, self.proxies_list)  # Aqui ele recebe nosso método, e utiilza o 2º param, para pegar cada item e jogar no 1º param.

            sleep(10)


if __name__ == "__main__":

    proxies_list = []
    url = "http://127.0.0.1/"
    api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"

    proxy = ProxyList(api_url, proxies_list, url)
    proxy.fetch_proxy_list(proxy.test_proxy_list)