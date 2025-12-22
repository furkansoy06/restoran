from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'menu_verileri.json'

# SENİN TAM LİSTEN - SİSTEMİ İLK ÇALIŞTIRDIĞINDA BU LİSTE YÜKLENİR
varsayilan_liste = [
    {"id": "corba", "kategori": "🥣 Çorbalar", "urunler": [
        {"isim": "Süzme Mercimek", "detay": "Kıtır ekmek ve tereyağlı sos ile", "fiyat": "120 TL", "stok": True, "oneri": "Lahmacun", "resim": "https://images.unsplash.com/photo-1547592166-23ac45744acd?q=80&w=200"},
        {"isim": "Kelle Paça", "detay": "Bol sarımsak ve sirke soslu", "fiyat": "180 TL", "stok": True, "oneri": "Kahve", "resim": "https://cdn.kisikatesakademi.com.tr/image-cache/cache/recipe_main_image_large/https---cdn.kisikatesakademi.com.tr/recipe-media/d39c4bc4a5bd53f5f680d589ac7a796cae0e6321.jpeg.webp"}
    ]},
    {"id": "durum", "kategori": "🌟 Dürümler", "urunler": [
        {"isim": "Et Döner Dürüm", "detay": "Soslu, Soğanlı, Kaşarlı", "fiyat": "420 TL", "stok": True, "oneri": "Ayran", "resim": "https://saraylidoner.com/wp-content/uploads/2021/09/durum-doner.jpg"},
        {"isim": "Tavuk Döner Dürüm", "detay": "Soslu, Soğanlı, Kaşarlı", "fiyat": "220 TL", "stok": True, "oneri": "Kola", "resim": "https://bestofdurum.com/images/product/3195433439686-638-Bestoftavukdoner.jpg"}
    ]},
    {"id": "pide", "kategori": "🍕 Pide & Lahmacun", "urunler": [
        {"isim": "Lahmacun", "detay": "Çıtır hamur", "fiyat": "150 TL", "stok": True, "oneri": "Ayran", "resim": "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?q=80&w=200"},
        {"isim": "Kuşbaşılı", "detay": "Çıtır hamur", "fiyat": "170 TL", "stok": True, "oneri": "Fanta", "resim": "https://www.evin.com.tr/wp-content/uploads/2023/08/kusbasilipide.jpg"},
        {"isim": "Kaşarlı", "detay": "Çıtır hamur", "fiyat": "110 TL", "stok": True, "oneri": "Çay", "resim": "https://dedemkebap.net/uploads/kasarli-pide%20dedemkeb.jpg"}
    ]},
    {"id": "izgara", "kategori": "🔥 Izgara Çeşitleri", "urunler": [
        {"isim": "Adana Kebap", "detay": "Zırh kıyması", "fiyat": "400 TL", "stok": True, "oneri": "Şalgam", "resim": "https://iasbh.tmgrup.com.tr/92c180/752/395/0/71/1152/675?u=https://isbh.tmgrup.com.tr/sbh/2020/03/05/en-harika-adana-kebap-tarifi-adana-kebap-nasil-yapilir-1583404717106.jpg"},
        {"isim": "Beyti", "detay": "Zırh kıyması", "fiyat": "400 TL", "stok": True, "oneri": "Ayran", "resim": "https://media.istockphoto.com/id/1412738954/tr/foto%C4%9Fraf/turkish-beyti-kebap-or-kebab-with-grilled-vegetables.jpg?s=612x612&w=0&k=20&c=eqL-iu-RNOzYhTlXUfE9EUfZPXwHp3R0LpYNiL68Rng="},
        {"isim": "Kuzu Şiş", "detay": "Süt kuzu", "fiyat": "400 TL", "stok": True, "oneri": "Ayran", "resim": "https://ia.tmgrup.com.tr/482a24/483/272/0/0/2048/1151?u=https://i.tmgrup.com.tr/sfr/2025/07/28/kuzu-sis-1753691728279.jpg"},
        {"isim": "Tavuk Şiş", "detay": "Özel soslu", "fiyat": "400 TL", "stok": True, "oneri": "Kola", "resim": "https://saraylidoner.com/wp-content/uploads/2021/09/tavuk-sis.jpg"}
    ]},
    {"id": "tatli", "kategori": "🍰 Tatlılar", "urunler": [
        {"isim": "Dondurmalı İrmik", "detay": "Sıcak servis", "fiyat": "120 TL", "stok": True, "oneri": "Çay", "resim": "https://upload.wikimedia.org/wikipedia/commons/0/03/K%C3%BCnefe_and_dondurma.jpg"},
        {"isim": "Dondurmalı Künefe", "detay": "Sıcak servis", "fiyat": "120 TL", "stok": True, "oneri": "Kahve", "resim": "https://www.bycitir.com.tr/upload/resimler/DondurmalY_Kunefe.jpg"},
        {"isim": "Dondurmalı Kadayıf", "detay": "Sıcak servis", "fiyat": "120 TL", "stok": True, "oneri": "Çay", "resim": "https://sagalassosyorukcadiri.com/wp-content/uploads/2023/06/Dondurmali-Kadayif-768x768.jpg"}
    ]},
    {"id": "icecek", "kategori": "🍸 İçecekler", "urunler": [
        {"isim": "Ayran", "detay": "Yayık ayranı", "fiyat": "50 TL", "stok": True, "resim": "https://www.elbetsteakhouse.com.tr/wp-content/uploads/2021/09/ayran-piknik-bu%CC%88fe.jpg"},
        {"isim": "Kola", "detay": "Buz gibi", "fiyat": "50 TL", "stok": True, "resim": "https://misas.com.tr/wp-content/uploads/2025/09/317531-600x600.webp"},
        {"isim": "Fanta", "detay": "Meyveli", "fiyat": "50 TL", "stok": True, "resim": "https://images.migrosone.com/sanalmarket/product/08011004/8011004_yan-7d2460-1650x1650.png"},
        {"isim": "Çay", "detay": "Taze demlenmiş", "fiyat": "25 TL", "stok": True, "resim": "https://odulbufe.com/wp-content/uploads/2021/08/C%CC%A7ay.jpg"},
        {"isim": "Kahve", "detay": "Türk kahvesi", "fiyat": "50 TL", "stok": True, "resim": "https://www.deryauluduz.com/wp-content/uploads/2021/10/kahve-ne-ise-yariyor.jpg"}
    ]}
]

# --- FONKSİYONLAR ---
def verileri_yukle():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(varsayilan_liste, f, ensure_ascii=False, indent=4)
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def verileri_kaydet(veri):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

# --- ROTALAR ---
@app.route('/')
def ana_sayfa():
    menu = verileri_yukle()
    return render_template('menu.html', menu=menu)

@app.route('/admin')
def admin_paneli():
    menu = verileri_yukle()
    return render_template('admin.html', menu=menu)

@app.route('/admin/stok/<k_id>/<int:u_idx>')
def stok_degistir(k_id, u_idx):
    menu = verileri_yukle()
    for g in menu:
        if g['id'] == k_id:
            g['urunler'][u_idx]['stok'] = not g['urunler'][u_idx].get('stok', True)
            break
    verileri_kaydet(menu)
    return redirect(url_for('admin_paneli'))

@app.route('/admin/ekle', methods=['POST'])
def urun_ekle():
    menu = verileri_yukle()
    k_id = request.form.get('kategori_id')
    k_ad = request.form.get('kategori_ad')
    yeni = {
        "isim": request.form.get('isim'),
        "detay": request.form.get('detay'),
        "fiyat": request.form.get('fiyat') + " TL",
        "resim": request.form.get('resim'),
        "stok": True,
        "oneri": request.form.get('oneri')
    }
    bulundu = False
    for g in menu:
        if g['id'] == k_id:
            g['urunler'].append(yeni)
            bulundu = True
            break
    if not bulundu:
        menu.append({"id": k_id, "kategori": k_ad, "urunler": [yeni]})
    verileri_kaydet(menu)
    return redirect(url_for('admin_paneli'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)