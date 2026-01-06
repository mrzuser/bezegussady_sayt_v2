from flask import Flask, render_template, request

app = Flask(__name__)

# --- TERCÜMELER (TRANSLATIONS) ---
TRANSLATIONS = {
    'tm': {
        'home': 'Baş Sahypa',
        'products': 'Satlyk Harytlar',
        'catalog': 'Katalog',
        'design': 'Dizaýn we Taslama',
        'contact': 'Habarlaşmak',
        'view_details': 'Giňişleýin Gör',
        'hero_title': 'Bezeg Ussady',
        'hero_subtitle': 'Siz arzuw ediň, biz çyzaly we ýasaly!',
        'hero_btn': 'Işlerimizi Görüň',
        'catalog_title': 'Katalog',
        'catalog_subtitle': 'Bölümi saýlaň we ähli işlerimizi görüň',
        'design_title': 'Ilki Çyzýarys, Soňra Ýasaýarys',
        'design_subtitle': 'Siziň islegleriňiz, biziň hünärimiz',
        'design_service': 'Dizaýn we Taslama',
        'design_desc': 'Siz bize jaýyňyzyň ölçeglerini beriň, biz size 3D dizaýnyny taýýarlap bereliň.',
        'design_list_1': 'Takyk ölçeg we dizaýn',
        'design_list_2': '3D Render',
        'design_list_3': 'Ýokary hilli gurnamak',
        'real_work': 'Taýýar Önümler (Bitirilen Işler)',
        'real_work_desc': 'Biz diňe dizaýn etmän, eýsem şol dizaýny durmuşa geçirýäris.',
        'footer_title': 'Biz bilen habarlaşyň',
        'rights': 'Ähli hukuklar goralan',
        'price_currency': 'TMT',
        'exclusive_products': 'Eksklýuziw mebeller we taýýar önümler',
        'products_empty': 'Bu kategoriýada heniz haryt ýok.',
        'back_to_catalog': 'Kataloga Dolanmak',
        'whatsapp_order': 'WHATSAPP-DAN SARGYT ET'
    },
    'ru': {
        'home': 'Главная',
        'products': 'Товары',
        'catalog': 'Каталог',
        'design': 'Дизайн и Проекты',
        'contact': 'Контакты',
        'view_details': 'Подробнее',
        'hero_title': 'Bezeg Ussady',
        'hero_subtitle': 'Вы мечтаете, мы проектируем и создаем!',
        'hero_btn': 'Наши Работы',
        'catalog_title': 'Каталог',
        'catalog_subtitle': 'Выберите раздел и посмотрите все наши работы',
        'design_title': 'Сначала Рисуем, Потом Создаем',
        'design_subtitle': 'Ваши желания, наш профессионализм',
        'design_list_1': 'Точные замеры и дизайн',
        'design_list_2': '3D Рендер',
        'design_list_3': 'Качественная установка',
        'design_service': 'Дизайн и Проектирование',
        'design_desc': 'Предоставьте нам размеры вашего помещения, и мы подготовим для вас 3D-дизайн.',
        'real_work': 'Готовые Изделия (Выполненные Работы)',
        'real_work_desc': 'Мы не только проектируем, но и воплощаем этот дизайн в жизнь.',
        'footer_title': 'Свяжитесь с нами',
        'rights': 'Все права защищены',
        'price_currency': 'ТМТ',
        'exclusive_products': 'Эксклюзивная мебель и готовые изделия',
        'products_empty': 'В этой категории пока нет товаров.',
        'back_to_catalog': 'Вернуться в Каталог',
        'whatsapp_order': 'ЗАКАЗАТЬ ЧЕРЕЗ WHATSAPP'
    }
}

# --- VERİ YAPILARI ---
# Genişletilmiş Ürün Veritabanı
# Genişletilmiş Ürün Veritabanı
PRODUCTS = [
    # Gapy (Kapı)
    {
        "id": "mdf-gapy", 
        "name_tm": "MDF Gapy (Eksklýuziw)", 
        "name_ru": "МДФ Дверь (Эксклюзив)", 
        "price": 1200, 
        "images": ["/static/images/MDF_Gapy1_esasy.jpg", "/static/images/gapy2.jpg", "/static/images/gapy3.jpg"], 
        "url": "/haryt/mdf-gapy", 
        "category": "gapy",
        "features": {
            "tm": [
                "Material: 100% MDF",
                "Ölçeg: 210x90 sm (Standart)",
                "Reňk: Goýy Şokolad / Islege görä",
                "Görnüş: Modern / Klassik"
            ],
            "ru": [
                "Материал: 100% МДФ",
                "Размер: 210x90 см (Стандарт)",
                "Цвет: Темный Шоколад / По желанию",
                "Стиль: Модерн / Классика"
            ]
        }
    },
    {
        "id": "gapy-classic", 
        "name_tm": "Klassiki Agaç Gapy", 
        "name_ru": "Классическая Деревянная Дверь", 
        "price": 1800, 
        "images": ["/static/images/gapy2.jpg", "/static/images/MDF_Gapy1_esasy.jpg", "/static/images/gapy3.jpg"], 
        "url": "/haryt/gapy-classic", 
        "category": "gapy",
        "features": {
            "tm": ["Material: Arassa Agaç", "Ölçeg: 210x90 sm", "Reňk: Açyk Agaç", "Gapy Tutawaçlary: Bürünç"],
            "ru": ["Материал: Натуральное Дерево", "Размер: 210x90 см", "Цвет: Светлое Дерево", "Ручки: Бронза"]
        }
    },
    {
        "id": "gapy-modern", 
        "name_tm": "Modern Ak Gapy", 
        "name_ru": "Современная Белая Дверь", 
        "price": 1400, 
        "images": ["/static/images/gapy3.jpg", "/static/images/gapy2.jpg", "/static/images/MDF_Gapy1_esasy.jpg"], 
        "url": "/haryt/gapy-modern", 
        "category": "gapy",
        "features": {
            "tm": ["Material: MDF + Emal", "Ölçeg: 210x80 sm", "Reňk: Ak Matowy", "Dizaýn: Minimalistik"],
            "ru": ["Материал: МДФ + Эмаль", "Размер: 210x80 см", "Цвет: Белый Матовый", "Дизайн: Минимализм"]
        }
    },
    
    # Ofis
    {
        "id": "ofis-stol", 
        "name_tm": "Ofis Stoly (Modern)", 
        "name_ru": "Офисный Стол (Модерн)", 
        "price": 1500, 
        "images": ["/static/images/Ofis_Stol1_esasy.jpg", "/static/images/ofis_mebel1_2.jpg", "/static/images/ofis_mebel1_3.jpg"], 
        "url": "/haryt/ofis-stol", 
        "category": "ofis",
        "features": {
            "tm": ["Material: Laminat DSP", "Ölçeg: 160x80x75 sm", "Aýratynlyk: Kabel geçelgesi bar", "Reňk: Antrasit / Dub"],
            "ru": ["Материал: ЛДСП", "Размер: 160x80x75 см", "Особенность: Кабель-канал", "Цвет: Антрацит / Дуб"]
        }
    },
    {
        "id": "ofis-kreslo", 
        "name_tm": "Ergonomik Kreslo", 
        "name_ru": "Эргономичное Кресло", 
        "price": 2500, 
        "images": ["/static/images/ofis_mebel1_2.jpg", "/static/images/Ofis_Stol1_esasy.jpg", "/static/images/ofis_mebel1_3.jpg"], 
        "url": "/haryt/ofis-kreslo", 
        "category": "ofis",
        "features": {
            "tm": ["Material: Deri / Tor", "Mehanizm: Multi-blok", "Göterijilik: 120 kg çenli", "Reňk: Gara"],
            "ru": ["Материал: Кожа / Сетка", "Механизм: Мульти-блок", "Нагрузка: до 120 кг", "Цвет: Черный"]
        }
    },
    {
        "id": "ofis-shkaf", 
        "name_tm": "Ofis Şkafy", 
        "name_ru": "Офисный Шкаф", 
        "price": 3000, 
        "images": ["/static/images/ofis_mebel1_3.jpg", "/static/images/Ofis_Stol1_esasy.jpg", "/static/images/ofis_mebel1_2.jpg"], 
        "url": "/haryt/ofis-shkaf", 
        "category": "ofis",
        "features": {
            "tm": ["Material: MDF", "Ölçeg: 200x90x40 sm", "Gapy Sany: 2", "Tekjeler: Sazlanýan"],
            "ru": ["Материал: МДФ", "Размер: 200x90x40 см", "Дверей: 2", "Полки: Регулируемые"]
        }
    },

    # Aşhana
    {
        "id": "ashana-lux", 
        "name_tm": "Aşhana Mebeli (Lux)", 
        "name_ru": "Кухонная Мебель (Lux)", 
        "price": 5000, 
        "images": ["/static/images/ashana1.jpg", "/static/images/ashana2.jpg", "/static/images/ashana3.jpg"], 
        "url": "/haryt/ashana-lux", 
        "category": "ashana",
        "features": {
            "tm": ["Material: Akril / MDF", "Stoleşnisa: Emeli Daş", "Furnitura: Blum (Awstriýa)", "Reňk: Ak / Altyn"],
            "ru": ["Материал: Акрил / МДФ", "Столешница: Искусственный камень", "Фурнитура: Blum (Австрия)", "Цвет: Белый / Золото"]
        }
    },
    {
        "id": "ashana-modern", 
        "name_tm": "Modern Aşhana", 
        "name_ru": "Современная Кухня", 
        "price": 4500, 
        "images": ["/static/images/ashana2.jpg", "/static/images/ashana1.jpg", "/static/images/ashana3.jpg"], 
        "url": "/haryt/ashana-modern", 
        "category": "ashana",
        "features": {
            "tm": ["Material: Plastik", "Stoleşnisa: Egger", "Reňk: Agymtyl çal", "Görnüş: Burçlaýyn"],
            "ru": ["Материал: Пластик", "Столешница: Egger", "Цвет: Светло-серый", "Тип: Угловая"]
        }
    },
    {
        "id": "ashana-compact", 
        "name_tm": "Kiçi Aşhana Toplumy", 
        "name_ru": "Малый Кухонный Набор", 
        "price": 3500, 
        "images": ["/static/images/ashana3.jpg", "/static/images/ashana1.jpg", "/static/images/ashana2.jpg"], 
        "url": "/haryt/ashana-compact", 
        "category": "ashana",
        "features": {
            "tm": ["Material: DSP", "Uzynlyk: 2.4 metr", "Reňk: Hoz", "Komplektasiýa: Çanak goşulan"],
            "ru": ["Материал: ДСП", "Длина: 2.4 метра", "Цвет: Орех", "Комплектация: Мойка включена"]
        }
    },

    # Ýatylýan Otag (Yatak Odası)
    {
        "id": "yatylyan-classic", 
        "name_tm": "Ýatylýan Otag (Classic)", 
        "name_ru": "Спальня (Классика)", 
        "price": 8500, 
        "images": ["/static/images/yatylyan1_1.jpg", "/static/images/yatylyan1_2.jpg", "/static/images/yatylyan1_1.jpg"], 
        "url": "/haryt/yatylyan-classic", 
        "category": "yatylyan",
        "features": {
            "tm": ["Toplum: Krowat, Şkaf, Tizleme", "Krowat Ölçegi: 180x200 sm", "Material: MDF Boýagly", "Aýna: Bar"],
            "ru": ["Набор: Кровать, Шкаф, Трюмо", "Размер кровати: 180x200 см", "Материал: МДФ Крашенный", "Зеркало: Есть"]
        }
    },
    {
        "id": "yatylyan-modern", 
        "name_tm": "Modern Döwrebap Ýatak", 
        "name_ru": "Современная Кровать", 
        "price": 7000, 
        "images": ["/static/images/yatylyan1_2.jpg", "/static/images/yatylyan1_1.jpg", "/static/images/yatylyan1_2.jpg"], 
        "url": "/haryt/yatylyan-modern", 
        "category": "yatylyan",
        "features": {
            "tm": ["Krowat Ölçegi: 160x200 sm", "Material: Ýumşak örtük (Barhat)", "Täzeçillik: Ýokary galdyrylýan mehanizm", "Reňk: Çal"],
            "ru": ["Размер кровати: 160x200 см", "Материал: Мягкая обивка (Бархат)", "Особенность: Подъемный механизм", "Цвет: Серый"]
        }
    },
    
    # Çaga Otagy
    {
        "id": "chaga-otag", 
        "name_tm": "Çaga Otagy Toplumy", 
        "name_ru": "Детская Комната", 
        "price": 4200, 
        "images": ["/static/images/chaga1.jpg", "/static/images/chaga2.jpg", "/static/images/chaga1.jpg"], 
        "url": "/haryt/chaga-otag", 
        "category": "chaga",
        "features": {
            "tm": ["Düzümi: Şkaf, Stol, Krowat", "Material: Ekologik arassa DSP", "Reňk: Ak / Ýaşyl", "Krowat: 90x200 sm"],
            "ru": ["Состав: Шкаф, Стол, Кровать", "Материал: Экологичный ДСП", "Цвет: Белый / Зеленый", "Кровать: 90x200 см"]
        }
    },
    {
        "id": "chaga-bed", 
        "name_tm": "Çaga Krowaty (Maşynly)", 
        "name_ru": "Детская Кровать (Машинка)", 
        "price": 2000, 
        "images": ["/static/images/chaga2.jpg", "/static/images/chaga1.jpg", "/static/images/chaga2.jpg"], 
        "url": "/haryt/chaga-bed", 
        "category": "chaga",
        "features": {
            "tm": ["Material: Plastik karkas", "Ýagtylandyryş: Fara we tekerlerde", "Ölçeg: 90x190 sm", "Reňk: Gyzyl"],
            "ru": ["Материал: Пластиковый каркас", "Подсветка: Фары и колеса", "Размер: 90x190 см", "Цвет: Красный"]
        }
    },

    # Myhman Otagy (Salon)
    {
        "id": "myhman-divan", 
        "name_tm": "Lüks Diwan Toplumy", 
        "name_ru": "Люкс Диванный Набор", 
        "price": 6000, 
        "images": ["/static/images/myhman1.jpg", "/static/images/myhman2.jpg", "/static/images/myhman1.jpg"], 
        "url": "/haryt/myhman-divan", 
        "category": "myhman",
        "features": {
            "tm": ["Komplekt: 3+2+1", "Material: Türkiýe matasy", "Karkas: Buk agajy", "Reňk: Bež / Altyn"],
            "ru": ["Комплект: 3+2+1", "Материал: Турецкая ткань", "Каркас: Бук", "Цвет: Беж / Золото"]
        }
    },
    {
        "id": "myhman-tv", 
        "name_tm": "TW Tumbasy", 
        "name_ru": "ТВ Тумба", 
        "price": 1800, 
        "images": ["/static/images/myhman2.jpg", "/static/images/myhman1.jpg", "/static/images/myhman2.jpg"], 
        "url": "/haryt/myhman-tv", 
        "category": "myhman",
        "features": {
            "tm": ["Uzynlyk: 220 sm", "Material: Hglos Panel", "Reňk: Gara Mermer", "Aýratynlyk: LED yşykly"],
            "ru": ["Длина: 220 см", "Материал: Хайглосс Панель", "Цвет: Черный Мрамор", "Особенность: LED подсветка"]
        }
    },
]

CATEGORY_NAMES = {
    "ashana": {"tm": "Aşhana Mebelleri", "ru": "Кухня"},
    "yatylyan": {"tm": "Ýatylýan Otag Mebelleri", "ru": "Спальня"},
    "myhman": {"tm": "Myhman Otag Mebelleri", "ru": "Гостиная"},
    "chaga": {"tm": "Çaga Otaglary", "ru": "Детская"},
    "ofis": {"tm": "Ofis Mebelleri", "ru": "Офис"},
    "gapy": {"tm": "Gapy & Penjire", "ru": "Двери и Окна"}
}

# --- YARDIMCI FONKSİYONLAR ---
def get_locale():
    return request.args.get('lang', 'tm')

def get_trans(lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS['tm'])

# --- ROTALAR (SAYFALAR) ---

@app.route('/')
def home():
    lang = get_locale()
    t = get_trans(lang)
    return render_template('index.html', lang=lang, t=t)

@app.route('/satlyk-harytlar')
def satlyk_harytlar():
    lang = get_locale()
    t = get_trans(lang)
    # Prepare products with localized names
    localized_products = []
    for p in PRODUCTS:
        p_copy = p.copy()
        p_copy['name'] = p.get(f'name_{lang}', p['name_tm'])
        # Use first image for list view
        p_copy['image'] = p['images'][0] if p.get('images') else ''
        localized_products.append(p_copy)
        
    return render_template('satlyk-harytlar.html', products=localized_products, lang=lang, t=t)

@app.route('/kategori/<category_key>')
def kategori_detay(category_key):
    lang = get_locale()
    t = get_trans(lang)
    
    # Kategoriye ait ürünleri filtrele
    category_products = []
    for p in PRODUCTS:
        if p['category'] == category_key:
            p_copy = p.copy()
            p_copy['name'] = p.get(f'name_{lang}', p['name_tm'])
             # Use first image for list view
            p_copy['image'] = p['images'][0] if p.get('images') else ''
            category_products.append(p_copy)
            
    cat_names = CATEGORY_NAMES.get(category_key, {"tm": "Kategoriýa", "ru": "Категория"})
    category_name = cat_names.get(lang, cat_names['tm'])
    
    return render_template('kategori_detaly.html', 
                         products=category_products, 
                         category_name=category_name,
                         lang=lang, t=t)

# Dinamiki Haryt Sahypasy
@app.route('/haryt/<product_id>')
def haryt_detaly(product_id):
    lang = get_locale()
    t = get_trans(lang)
    
    # Ürünü bul
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    
    if product:
        # İsim lokalizasyonu
        product_copy = product.copy()
        product_copy['name'] = product.get(f'name_{lang}', product['name_tm'])
        # Features localization
        product_copy['features'] = product['features'].get(lang, product['features']['tm'])
        return render_template('haryt_detaly.html', product=product_copy, lang=lang, t=t)
    else:
        return "Haryt tapylmady", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

