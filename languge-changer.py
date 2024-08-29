import json
from deep_translator import GoogleTranslator

# JSON dosyasını oku
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        print(f"Yüklendi: {data}")
        return data

# Çevrilmiş JSON verisini dosyaya yaz
def save_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"{file_path} dosyasına veri kaydedildi.")
    except Exception as e:
        print(f"Dosya kaydedilirken hata: {e}")

# JSON verilerini rekürsif olarak çeviren fonksiyon
def translate_json(data, translator, output_file, path=""):
    if isinstance(data, dict):
        translated_data = {}

        for key, value in data.items() :
            current_path = f"{path}.{key}" if path else key
            if key in ['description', 'portionDescription']:
                try:
                    translated_data[key] = translator.translate(value)
                    print(f"Çevirildi [{current_path}]: {value} -> {translated_data[key]}")
                except Exception as e:
                    print(f"Hata [{current_path}]: {e}")
                    translated_data[key] = value
            else:
                translated_data[key] = translate_json(value, translator, output_file, current_path)
        return translated_data
    elif isinstance(data, list):
        translated_list = []
        for index, item in enumerate(data):
            try:
                current_path = f"{path}[{index}]"
                translated_list.append(translate_json(item, translator, output_file, current_path))
                print(f"Listede çevirildi [{current_path}]: {item}")
            except Exception as e:
                print(f"Listede hata [{current_path}]: {e}")
                translated_list.append(item)
            # İlerlemeyi kaydet
            save_json(translated_list, output_file)
        return translated_list
    else:
        return data

# Ana fonksiyon
def main():
    # JSON dosyasını yükle
    input_file = 'data.json'
    output_file = 'data_hi_part1.json'

    data = load_json(input_file)

    # GoogleTranslator nesnesi oluştur
    translator = GoogleTranslator(source='auto', target='hi')

    # Verileri çevir ve kaydet
    translated_data = translate_json(data, translator, output_file)

    # Son olarak çevrilmiş veriyi yeni dosyaya kaydet
    save_json(translated_data, output_file)
    print(f'Çevrilmiş veri {output_file} dosyasına kaydedildi.')

if __name__ == "__main__":
    main()
