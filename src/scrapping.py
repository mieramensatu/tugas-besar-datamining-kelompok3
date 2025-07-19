from playwright.sync_api import sync_playwright
import csv
import time


def human_scroll(page, delay=1.5, max_scrolls=20):
    last_height = 0
    for _ in range(max_scrolls):
        page.mouse.wheel(0, 3000)
        time.sleep(delay)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scrape_shop_info(page):
    page.goto("https://www.tokopedia.com/erigo", timeout=120000)
    page.wait_for_load_state("load")  # atau bisa juga hanya time.sleep
    time.sleep(2)

    try:
        nama_toko = page.locator('[data-testid="shopNameHeader"]').text_content().strip()
    except:
        nama_toko = "-"

    try:
        rating_toko = page.locator('p.css-49tczq-unf-heading').text_content().strip()
    except:
        rating_toko = "-"

    # kategori = "Fashion Pria"

    return {
        "Nama Toko": nama_toko,
        "Rating Toko": rating_toko,
        # "Kategori": kategori
    }


def get_all_product_links(page):
    print("🔄 Mengambil semua link produk...")
    page.goto("https://www.tokopedia.com/erigo/product", timeout=120000)
    page.wait_for_load_state("load")  # atau bisa juga hanya time.sleep
    human_scroll(page)
    links = page.locator('div.css-79elbk a').all()
    product_urls = []
    for link in links:
        href = link.get_attribute("href")
        if href and "/erigo/" in href:
            if href.startswith("/"):
                href = "https://www.tokopedia.com" + href
            product_urls.append(href)
    return list(set(product_urls))  # remove duplicates


def scrape_product_detail(page, url):
    page.goto(url, timeout=120000)
    page.wait_for_load_state("load")  # atau bisa juga hanya time.sleep
    time.sleep(2)

    try:
        nama_produk = page.locator('h1').first.text_content().strip()
    except:
        nama_produk = "-"
    try:
        harga = page.locator('[data-testid="lblPDPDetailProductPrice"]').first.text_content().strip()
    except:
        harga = "-"
    try:
        terjual = page.locator('[data-testid="lblPDPDetailProductSoldCounter"]').first.text_content().strip()
        terjual = terjual.replace("Terjual", "").strip()  # hasil akhir: "250+"
    except:
        terjual = "-"
    # Ambil Rating Produk (khusus PDP page)
    try:
        rating_produk = page.locator('[data-testid="lblPDPDetailProductRatingNumber"]').first.text_content().strip()
    except:
        rating_produk = "-"
    try:
        review_info = page.locator('p.css-scw5ei-unf-heading').first.text_content().strip()
        jumlah_ulasan = review_info.split("•")[1].strip().split(" ")[0]
    # hasilnya "52 ulasan"
    except:
        jumlah_ulasan = "-"

    try:
        kategori_items = page.locator("nav a").all()
        kategori = " > ".join([item.text_content().strip() for item in kategori_items])
    except:
        kategori = "-"


    # Ambil 1-3 ulasan sebagai sampel
# Ambil semua ulasan yang muncul di halaman
    reviews = []
    try:
        # Lazy load scroll dulu
        for _ in range(10):
            page.mouse.wheel(0, 1000)
            time.sleep(1)

        review_cards = page.locator('div.css-1k41fl7')
        count = review_cards.count()

        for i in range(count):
            card = review_cards.nth(i)
            try:
                username = card.locator('span.name').text_content().strip()
            except:
                username = "-"
            try:
                bintang = str(card.locator('[data-testid="icnStarRating"] svg').count())
            except:
                bintang = "-"
            try:
                tanggal = card.locator('p.css-1rpz5os-unf-heading').text_content().strip()
            except:
                tanggal = "-"
            try:
                isi = card.locator('[data-testid="lblItemUlasan"]').text_content().strip()
            except:
                isi = "-"
            
            reviews.append({
                "Username": username,
                "Rating": bintang,
                "Tanggal Komentar": tanggal,
                "Teks Ulasan": isi
            })
    except Exception as e:
        print("❌ Gagal mengambil review:", e)


    return {
        "Nama Produk": nama_produk,
        "Harga Produk": harga,
        "Rating Produk": rating_produk,
        "Jumlah Ulasan": jumlah_ulasan,
        "Jumlah Terjual": terjual,
        "Ulasan": reviews,
        "Kategori": kategori
    }


def main():
    all_data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        shop_info = scrape_shop_info(page)
        product_links = get_all_product_links(page)
        print(f"🔗 Total produk ditemukan: {len(product_links)}")

        for idx, url in enumerate(product_links[:100]): 
            print(f"🔍 Memproses produk ke-{idx+1}: {url}")
            try:
                product = scrape_product_detail(page, url)
            except Exception as e:
                print(f"❌ Gagal memproses produk ke-{idx+1}: {e}")
                continue

            if product["Ulasan"]:
                for review in product["Ulasan"]:
                    row = {
                        **shop_info,
                        **{k: v for k, v in product.items() if k != "Ulasan"},
                        **review
                    }
                    all_data.append(row)
            else:
                row = {
                    **shop_info,
                    **{k: v for k, v in product.items() if k != "Ulasan"},
                    "Username": "-",
                    "Rating": "-",
                    "Tanggal Komentar": "-",
                    "Teks Ulasan": "-"
                }
                all_data.append(row)

        browser.close()

    # Simpan ke CSV
    if all_data:
        # Cari semua key unik dari semua row agar CSV rapi
        all_keys = set()
        for row in all_data:
            all_keys.update(row.keys())
        all_keys = list(sorted(all_keys))  # Urutkan agar konsisten

        # Simpan ke CSV
        with open("Erigo_full_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            writer.writerows(all_data)
        print("✅ Data berhasil disimpan ke Erigo_full_data.csv")
    else:
        print("⚠ Tidak ada data ulasan ditemukan.")


if __name__ == "__main__":
    main()

