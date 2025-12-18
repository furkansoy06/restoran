from flask import Flask, render_template

app = Flask(__name__)

menu_verileri = [
    {"id": "corba", "kategori": "🥣 Çorbalar", "urunler": [
        {"isim": "Süzme Mercimek", "detay": "Kıtır ekmek ve tereyağlı sos ile", "fiyat": "120 TL", "resim": "https://images.unsplash.com/photo-1547592166-23ac45744acd?q=80&w=200"},
        {"isim": "Kelle Paça", "detay": "Bol sarımsak ve sirke soslu", "fiyat": "180 TL", "resim": "https://cdn.kisikatesakademi.com.tr/image-cache/cache/recipe_main_image_large/https---cdn.kisikatesakademi.com.tr/recipe-media/d39c4bc4a5bd53f5f680d589ac7a796cae0e6321.jpeg.webp"}
    ]},
    {"id": "durum", "kategori": "🌟 Dürümler", "urunler": [
        {"isim": "Et Döner Dürüm", "detay": "Soslu, Soğanlı, Kaşarlı", "fiyat": "420 TL", "resim": "https://saraylidoner.com/wp-content/uploads/2021/09/durum-doner.jpg"},
        {"isim": "Tavuk Döner Dürüm", "detay": "Soslu, Soğanlı, Kaşarlı", "fiyat": "220 TL", "resim": "https://bestofdurum.com/images/product/3195433439686-638-Bestoftavukdoner.jpg"},
    
    ]},
    {"id": "pide", "kategori": "🍕 Pide & Lahmacun", "urunler": [
        {"isim": "Lahmacun", "detay": "Çıtır hamur", "fiyat": "150 TL", "resim": "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?q=80&w=200"},
        {"isim": "Kuşbaşılı", "detay": "Çıtır hamur", "fiyat": "170 TL", "resim": "https://www.evin.com.tr/wp-content/uploads/2023/08/kusbasilipide.jpg"},
        {"isim": "Kaşarlı", "detay": "Çıtır hamur", "fiyat": "110 TL", "resim": "https://dedemkebap.net/uploads/kasarli-pide%20dedemkeb.jpg"},
    ]},
    {"id": "izgara", "kategori": "🔥 Izgara Çeşitleri", "urunler": [
        {"isim": "Adana Kebap", "detay": "Zırh kıyması", "fiyat": "400 TL", "resim": "https://iasbh.tmgrup.com.tr/92c180/752/395/0/71/1152/675?u=https://isbh.tmgrup.com.tr/sbh/2020/03/05/en-harika-adana-kebap-tarifi-adana-kebap-nasil-yapilir-1583404717106.jpg"},
        {"isim": "Beyti", "detay": "Zırh kıyması", "fiyat": "400 TL", "resim": "https://media.istockphoto.com/id/1412738954/tr/foto%C4%9Fraf/turkish-beyti-kebap-or-kebab-with-grilled-vegetables.jpg?s=612x612&w=0&k=20&c=eqL-iu-RNOzYhTlXUfE9EUfZPXwHp3R0LpYNiL68Rng="},
        {"isim": "Kuzu Şiş", "detay": "Zırh kıyması", "fiyat": "400 TL", "resim": "https://ia.tmgrup.com.tr/482a24/483/272/0/0/2048/1151?u=https://i.tmgrup.com.tr/sfr/2025/07/28/kuzu-sis-1753691728279.jpg"},
        {"isim": "Tavuk Şiş", "detay": "Zırh kıyması", "fiyat": "400 TL", "resim": "https://saraylidoner.com/wp-content/uploads/2021/09/tavuk-sis.jpg"},
    ]},
    {"id": "tatli", "kategori": "🍰 Tatlılar", "urunler": [
        {"isim": "Dondurmalı İrmik", "detay": "Sıcak servis", "fiyat": "120 TL", "resim": "https://upload.wikimedia.org/wikipedia/commons/0/03/K%C3%BCnefe_and_dondurma.jpg"},
        {"isim": "Dondurmalı Künefe", "detay": "Sıcak servis", "fiyat": "120 TL", "resim": "https://www.bycitir.com.tr/upload/resimler/DondurmalY_Kunefe.jpg"},
        {"isim": "Dondurmalı Kadayıf ", "detay": "Sıcak servis", "fiyat": "120 TL", "resim": "https://sagalassosyorukcadiri.com/wp-content/uploads/2023/06/Dondurmali-Kadayif-768x768.jpg"},
    ]},
    {"id": "icecek", "kategori": "🍸 İçecek", "urunler": [
        {"isim": "Ayran", "detay": "Soğuk servis", "fiyat": "50 TL", "resim": "https://www.elbetsteakhouse.com.tr/wp-content/uploads/2021/09/ayran-piknik-bu%CC%88fe.jpg"},
        {"isim": "Kola", "detay": "Soğuk servis", "fiyat": "50 TL", "resim": "https://misas.com.tr/wp-content/uploads/2025/09/317531-600x600.webp"},
        {"isim": "Fanta", "detay": "Soğuk servis", "fiyat": "50 TL", "resim": "https://images.migrosone.com/sanalmarket/product/08011004/8011004_yan-7d2460-1650x1650.png"},
        {"isim": "İce-Tea", "detay": "Soğuk servis", "fiyat": "50 TL", "resim": "http://images.migrosone.com/sanalmarket/product/08059549/8059549_1-b020ec-1650x1650.jpg"},
        {"isim": "Su", "detay": "Soğuk-Sıcak servis", "fiyat": "25 TL", "resim": "https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/48857/uploads/urunresimleri/buyuk/1003838--4d90-.jpg"},
        {"isim": "Çay", "detay": "Sıcak servis", "fiyat": "25 TL", "resim": "https://odulbufe.com/wp-content/uploads/2021/08/C%CC%A7ay.jpg"},
        {"isim": "Kahve", "detay": "Sıcak servis", "fiyat": "50 TL", "resim": "https://www.deryauluduz.com/wp-content/uploads/2021/10/kahve-ne-ise-yariyor.jpg"},
    ]}
]

@app.route('/')
def menu_goster():
    return render_template('menu.html', menu=menu_verileri)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)