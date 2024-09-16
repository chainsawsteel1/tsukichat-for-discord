import logging
logger = logging.getLogger(__name__)

import json
import re
import urllib.parse
import urllib.request
from collections import OrderedDict

class Converter:
    hiragana_map = OrderedDict()
    
    @staticmethod
    def is_initialized():
        return bool(Converter.hiragana_map)

    @staticmethod
    def init_map(resource_name):
        try:
            with open(resource_name, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        parts = line.strip().split(':')
                        romaji = parts[0]
                        hiragana = parts[1]
                        back = parts[2] if len(parts) == 3 else '0'
                        Converter.hiragana_map[romaji] = [hiragana, back]
        except FileNotFoundError:
            print(f"Could not find resource: {resource_name}")
        except Exception as e:
            print(f"Error reading resource: {e}")

    @staticmethod
    def romaji_to_hiragana(romaji):
        if not Converter.is_initialized():
            raise Exception("Converter not initialized")

        hiragana = []
        i = 0
        while i < len(romaji):
            found = False
            for j in range(4, 0, -1):
                if i + j <= len(romaji):
                    substring = romaji[i:i + j]
                    if substring in Converter.hiragana_map:
                        hiragana.append(Converter.hiragana_map[substring][0])
                        i += j + int(Converter.hiragana_map[substring][1])
                        found = True
                        break
            if not found:
                hiragana.append(romaji[i])
                i += 1
        return ''.join(hiragana)

    @staticmethod
    def hiragana_to_japanese(hiragana):
        try:
            url = f"https://www.google.com/transliterate?langpair=ja-Hira|ja&text={urllib.parse.quote(hiragana)}"
            with urllib.request.urlopen(url) as response:
                content = response.read().decode('utf-8')
                json_array = json.loads(content)
                result = ''.join([item[1][0] for item in json_array])
                return re.sub(r'([！-～])', lambda m: chr(ord(m.group(0)) - 0xFEE0), result)
        except Exception as e:
            print(f"Error during conversion to Japanese: {e}")
            return f"{hiragana} ```変換出来ませんでした```"

    @staticmethod
    def romaji_to_japanese(romaji):
        return Converter.hiragana_to_japanese(Converter.romaji_to_hiragana(romaji))
