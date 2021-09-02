from datetime import datetime
from colorama import Fore
from time import perf_counter
import requests
import argparse
import asyncio


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', action = "store", type = str, required = True, help = "URL or Domain")
    parser.add_argument('--port', action = "store", type = int, required = False, help = "Server's html port that you want to scan, default = 80", default = 80)
    parser.add_argument('--wordlist', action = "store", type = str, required = True, help = "Wordlist's location")
    parser.add_argument('--extensions', action= "store", type = str, required = False, help = "Extensions that you want to scan, deafult = html,php,js", default = "html,php,js")
    parser.add_argument('--ssl', action = argparse.BooleanOptionalAction, type = bool, required = False, help = "If website has ssl write --ssl, if not write --no-ssl, default = --no-ssl", default = False)
    args = parser.parse_args()
    return args

async def get_request(host, port, k, header):
    try:
        r = k[0]
        k.pop(0)
        req = requests.get(f"{host}:{port}/{r}", headers=header)
        if req.ok:
            print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*]        {Fore.BLUE}/{r}             {Fore.MAGENTA}size:{len(req.text)}")
    except KeyboardInterrupt:
        exit()
    except:
        return
        
async def main():
    args = parse_args()
    k = args.extensions.split(",")
    l = list()
    p = list()

    if args.ssl:
        h = f"https://{args.host}"
    else:
        h = f"http://{args.host}"

    header = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Encoding' : 'gzip, deflate, br',
            'Content-Language' : 'en-US;en;q=0.5',
            'Upgrade-Insecure-Requests' : '1',
            'Referer' : h,
            'DNT' : '1',
            'Language' : 'en-US'
    }
    with open(args.wordlist) as f:
        c = f.readlines()
        for i in c:
            i = i.replace("\n", "")
            l.append(i)
            for a in k:
                p.append(i + f".{a}")
        f.close()

    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*] {Fore.BLUE}HOST = {Fore.CYAN}{h}")
    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*] {Fore.BLUE}PORT = {Fore.CYAN}{args.port}")
    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*] {Fore.BLUE}WORDLIST = {Fore.CYAN}{args.wordlist}")
    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*] {Fore.BLUE}EXTENSIONS = {Fore.CYAN}{args.extensions}")
    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*] {Fore.BLUE}SSL = {Fore.CYAN}{args.ssl}\n\n")

    start = perf_counter()

    for i in range(len(p)):
        await asyncio.gather(get_request(h, args.port, l, header))
        await asyncio.gather(get_request(h, args.port, p, header))

    end = perf_counter()
    
    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*]{Fore.GREEN} OPERATION COMPLETED IN {end-start} SECONDS{Fore.WHITE}")

if __name__ == "__main__":
    asyncio.run(main())
