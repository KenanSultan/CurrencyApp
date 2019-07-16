import xml.etree.ElementTree as ET
from datetime import date
import requests

def listFromCbar(day):
    # url = f"https://www.cbar.az/currencies/{day}.xml"
    url = "https://www.cbar.az/currencies/"+day+".xml"

    result = requests.get(url)

    if result.status_code == 200:
        content = ET.fromstring(result.text)

        return content[1]

    return False