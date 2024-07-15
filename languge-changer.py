import json
from deep_translator import GoogleTranslator

# JSON dosyasını oku
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# JSON verilerini rekürsif olarak çeviren fonksiyon
def translate_json(data, translator):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'description':
                data[key] = translator.translate(value)
            elif key == 'foodNutrients':
                data[key] = translate_json(value, translator)
            else:
                data[key] = translate_json(value, translator)
        return data
    elif isinstance(data, list):
        return [translate_json(item, translator) for item in data]
    elif isinstance(data, str):
        return data  # stringleri direk döndür
    else:
        return data

# Belirtilen alanları çeviren fonksiyon
def translate_nutrients(data, translator):
    for nutrient in data:
        if 'nutrient' in nutrient and 'name' in nutrient['nutrient']:
            nutrient['nutrient']['name'] = translator.translate(nutrient['nutrient']['name'])
    return data

# Çevrilmiş JSON verisini dosyaya yaz
def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Ana fonksiyon
def main():
    # JSON dosyasını yükle
    input_file = 'data.json'
    output_file = 'translated_data_3.json'

    data = load_json(input_file)

    # GoogleTranslator nesnesi oluştur
    translator = GoogleTranslator(source='auto', target='tr')

    # Verileri çevir
    translated_data = translate_json(data, translator)
    for item in translated_data:
        if 'foodNutrients' in item:
            item['foodNutrients'] = translate_nutrients(item['foodNutrients'], translator)

    # Çevrilmiş veriyi yeni dosyaya kaydet
    save_json(translated_data, output_file)
    print(f'Çevrilmiş veri {output_file} dosyasına kaydedildi.')

if __name__ == "__main__":
    main()
