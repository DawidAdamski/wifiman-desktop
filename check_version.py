import requests
from bs4 import BeautifulSoup
import re
import sys

def get_version_bs4():
    url = "https://ui.com/download/app/wifiman-desktop"
    # Musimy podać User-Agent, bo bez tego UI.com od razu wali 403
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Błąd statusu: {response.status_code}", file=sys.stderr)
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Szukamy wszystkich linków, które prowadzą do pliku .deb
        links = soup.find_all('a', href=re.compile(r'wifiman-desktop-.*-amd64\.deb'))
        
        for link in links:
            href = link.get('href')
            # Wyciągamy wersję z linku za pomocą regex
            match = re.search(r'wifiman-desktop-([\d\.]+)-amd64\.deb', href)
            if match:
                return match.group(1)
                
    except Exception as e:
        print(f"Błąd: {e}", file=sys.stderr)
        
    return None

if __name__ == "__main__":
    version = get_version_bs4()
    if version:
        print(version)
        sys.exit(0)
    else:
        sys.exit(1)

