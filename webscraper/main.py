import io
import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'watchBrands')))

from citizen import citizen_watches
from orient import orient_watches
from seiko import seiko_watches
from timex import timex_watches

if __name__ == "__main__":
    watches = {"Brands" : {"Citizen" : citizen_watches(), "Orient" : orient_watches(), "Seiko" : seiko_watches(), "Timex" : timex_watches()}}
    with open('watches.json', 'w', encoding='utf-8') as f:
        json.dump(watches, f, ensure_ascii=False, indent=4)