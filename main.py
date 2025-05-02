import requests as r
from colorama import Fore, Back, Style
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import sys


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

                with open("live-proxy.txt", "a") as f:
                    f.write(f"[free-proxy][http] ➔ {proxy} ➔ [ifconfig.me] ➔ {response.text} [ONLINE]\n")
                

        except r.exceptions.RequestException as e:
            pass

        

    def fetch_proxy_list(self, arg_function, threads: int) -> None: # Aqui uso o ThreadPoolExecutor

        self.get_proxy_list()

            # Usando ThreadPoolExecutor para verificar os proxies em paralelo
        with ThreadPoolExecutor(max_workers=int(threads)) as executor:
            executor.map(arg_function, self.proxies_list)

    def main(self):
        def ban():
            banner = r"""

        ▗▄▄▖  ▗▄▖ ▗▖ ▗▖  ▗▖▗▄▄▖ ▗▖ ▗▖ ▗▄▄▖    ▗▖    ▗▄▖ ▗▄▄▖  ▗▄▄▖
        ▐▌ ▐▌▐▌ ▐▌▐▌  ▝▚▞▘ ▐▌ ▐▌▐▌ ▐▌▐▌       ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌   
        ▐▛▀▘ ▐▌ ▐▌▐▌   ▐▌  ▐▛▀▘ ▐▌ ▐▌ ▝▀▚▖    ▐▌   ▐▛▀▜▌▐▛▀▚▖ ▝▀▚▖
        ▐▌   ▝▚▄▞▘▐▙▄▄▖▐▌  ▐▌   ▝▚▄▞▘▗▄▄▞▘    ▐▙▄▄▖▐▌ ▐▌▐▙▄▞▘▗▄▄▞▘  presents.
                                                                
                    live http proxy searcher, by sxdv.
                    github: @brianszn
                    Use: python3 main.py 'threads number'

            """
            return banner
        print(ban())
        try:
            if sys.argv[1]:
                pass
        except IndexError as e:
            print("\nUse: python3 main.py 'threads number'")
            sys.exit()       
        sleep(5)       
        self.fetch_proxy_list(proxy.test_proxy_list, sys.argv[1])
        print(Fore.YELLOW +f'file: live-proxy.txt has been created.')


if __name__ == "__main__":

    proxies_list = []
    url = "http://127.0.0.1/"
    api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    proxy = ProxyList(api_url, proxies_list, url)

    proxy.main()
      