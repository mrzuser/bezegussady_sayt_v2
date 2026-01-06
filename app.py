from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import webbrowser
from threading import Timer

app = Flask(__name__)
app.secret_key = 'supersecretkey' # Flash mesajlary we Session üçin

# --- VERİ YAPILARI ---
# Genişletilmiş Ürün Veritabanı
PRODUCTS = [
    # Gapy (Kapı)
    {"id": "mdf-gapy", "name": "MDF Gapy (Eksklýuziw)", "price": 1200, "image": "/static/images/MDF_Gapy1_esasy.jpg", "url": "/mdf-gapy", "category": "gapy"},
    {"id": "gapy-classic", "name": "Klassiki Agaç Gapy", "price": 1800, "image": "/static/images/gapy2.jpg", "url": "#", "category": "gapy"},
    {"id": "gapy-modern", "name": "Modern Ak Gapy", "price": 1400, "image": "/static/images/gapy3.jpg", "url": "#", "category": "gapy"},
    
    # Ofis
    {"id": "ofis-stol", "name": "Ofis Stoly (Modern)", "price": 1500, "image": "/static/images/Ofis_Stol1_esasy.jpg", "url": "/ofis-stol", "category": "ofis"},
    {"id": "ofis-kreslo", "name": "Ergonomik Kreslo", "price": 2500, "image": "/static/images/ofis_mebel1_2.jpg", "url": "#", "category": "ofis"},
    {"id": "ofis-shkaf", "name": "Ofis Şkafy", "price": 3000, "image": "/static/images/ofis_mebel1_3.jpg", "url": "#", "category": "ofis"},

    # Aşhana
    {"id": "ashana-lux", "name": "Aşhana Mebeli (Lux)", "price": 5000, "image": "/static/images/ashana1.jpg", "url": "#", "category": "ashana"},
    {"id": "ashana-modern", "name": "Modern Aşhana", "price": 4500, "image": "/static/images/ashana2.jpg", "url": "#", "category": "ashana"},
    {"id": "ashana-compact", "name": "Kiçi Aşhana Toplumy", "price": 3500, "image": "/static/images/ashana3.jpg", "url": "#", "category": "ashana"},

    # Ýatylýan Otag (Yatak Odası)
    {"id": "yatylyan-classic", "name": "Ýatylýan Otag (Classic)", "price": 8500, "image": "/static/images/yatylyan1_1.jpg", "url": "#", "category": "yatylyan"},
    {"id": "yatylyan-modern", "name": "Modern Döwrebap Ýatak", "price": 7000, "image": "/static/images/yatylyan1_2.jpg", "url": "#", "category": "yatylyan"},
    
    # Çaga Otagy
    {"id": "chaga-otag", "name": "Çaga Otagy Toplumy", "price": 4200, "image": "/static/images/chaga1.jpg", "url": "#", "category": "chaga"},
    {"id": "chaga-bed", "name": "Çaga Krowaty (Maşynly)", "price": 2000, "image": "/static/images/chaga2.jpg", "url": "#", "category": "chaga"},

    # Myhman Otagy (Salon)
    {"id": "myhman-divan", "name": "Lüks Diwan Toplumy", "price": 6000, "image": "/static/images/myhman1.jpg", "url": "#", "category": "myhman"},
    {"id": "myhman-tv", "name": "TW Tumbasy", "price": 1800, "image": "/static/images/myhman2.jpg", "url": "#", "category": "myhman"},
]

CATEGORY_NAMES = {
    "ashana": "Aşhana Mebelleri",
    "yatylyan": "Ýatylýan Otag Mebelleri",
    "myhman": "Myhman Otag Mebelleri",
    "chaga": "Çaga Otaglary",
    "ofis": "Ofis Mebelleri",
    "gapy": "Gapy & Penjire"
}

ORDER_FILE = 'orders.json'
USER_FILE = 'users.json'

# --- YARDIMCI FONKSİYONLAR ---

def load_json(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- ROTALAR (SAYFALAR) ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/satlyk-harytlar')
def satlyk_harytlar():
    return render_template('satlyk-harytlar.html', products=PRODUCTS)

@app.route('/kategori/<category_key>')
def kategori_detay(category_key):
    # Kategoriye ait ürünleri filtrele
    category_products = [p for p in PRODUCTS if p['category'] == category_key]
    category_name = CATEGORY_NAMES.get(category_key, "Kategoriýa")
    
    return render_template('kategori_detay.html', 
                         products=category_products, 
                         category_name=category_name)

@app.route('/halanlarym')
def halanlarym():
    return render_template('halanlarym.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

# Özel Ürün Sayfaları
@app.route('/mdf-gapy')
def mdf_gapy():
    return render_template('MDF-Gapy.html')

@app.route('/ofis-stol')
def ofis_stol():
    return render_template('Ofis-Stol.html')

# --- SİPARİŞ İŞLEMLERİ ---

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        try:
            cart_data_raw = request.form.get('cart_data', '[]')
            cart_data = json.loads(cart_data_raw)
            
            if not cart_data:
                return "Sebet boş!", 400

            order = {
                'id': f"ORD-{int(datetime.now().timestamp())}",
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'Täze',
                'customer': {
                    'name': request.form.get('name'),
                    'phone': request.form.get('phone'),
                    'address': request.form.get('address'),
                    'notes': request.form.get('notes')
                },
                'items': cart_data,
                'total': sum(item['price'] * item['quantity'] for item in cart_data)
            }
            
            orders = load_json(ORDER_FILE)
            orders.append(order)
            save_json(ORDER_FILE, orders)
            
            return redirect(url_for('order_success'))
        except Exception as e:
            return f"Sipariş ýalňyşlygy: {str(e)}", 400
            
    return render_template('checkout.html')

@app.route('/order-success')
def order_success():
    return render_template('order_success.html')

# --- ADMIN VE GÜVENLİK ---

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    orders = load_json(ORDER_FILE)
    orders.reverse() 
    return render_template('admin.html', orders=orders)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_json(USER_FILE)
        user = next((u for u in users if u['username'] == username), None)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['username']
            return redirect(url_for('admin'))
        else:
            flash('Ýalňyş ulanyjy ady ýa-da açar sözü!', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Güvenlik notu: Gerçek hayatta kayıt sayfası herkese açık olmaz, admin panelinden eklenir.
    # Ancak burada demo amaçlı açık bırakıyoruz.
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_json(USER_FILE)
        
        if any(u['username'] == username for u in users):
            flash('Bu ulanyjy ady eýýäm alynan.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            users.append({'username': username, 'password': hashed_password})
            save_json(USER_FILE, users)
            flash('Hasap üstünlikli döredildi! Indi ulgama girip bilersiňiz.', 'success')
            return redirect(url_for('login'))
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

def open_browser():
    webbrowser.open_new('http://localhost:5000')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(host='0.0.0.0', port=5000, debug=True)
