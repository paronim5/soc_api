import requests
from bs4 import BeautifulSoup
import json
import time
import re

BASE_URL = "https://archiv.soc.cz"

def get_soup(url):
    print(f"Načítám: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def scrape_soc_archiv():
    works = []
    work_id = 1

    for year_num in range(30, 48):
        rocnik_url = f"{BASE_URL}/archiv/rocnik{year_num}"
        try:
            rocnik_soup = get_soup(rocnik_url)
        except Exception as e:
            print(f"  ⚠️ Ročník {year_num} nenalezen: {e}")
            continue

        obor_links = rocnik_soup.find_all("a", href=re.compile(rf"/archiv/rocnik{year_num}/obor/\d+$"))
        print(f"  Ročník {year_num}: nalezeno {len(obor_links)} oborů")

        for link in obor_links:
            obor_url = BASE_URL + link["href"]
            try:
                obor_soup = get_soup(obor_url)
            except Exception as e:
                print(f"    ⚠️ Chyba při načítání oboru: {e}")
                continue

            obor_name = link.get_text(strip=True)
            ol = obor_soup.find("ol")
            if not ol:
                continue

            for li in ol.find_all("li", recursive=False):
                try:

                    strong = li.find("strong")
                    if not strong:
                        continue
                    title = strong.get_text(strip=True)
                    title_strong = str(strong)
                    rest = str(li).split(title_strong, 1)[-1]

                    clean_rest = BeautifulSoup(rest, "html.parser").get_text()
                    lines = [line.strip() for line in clean_rest.splitlines() if line.strip()]
                    author = "Neuveden"
                    school = "Neuvedena"

                    if lines:
                        author_line = lines[0]
                        if author_line.startswith("Autor/ři:"):
                            author = author_line[len("Autor/ři:"):].strip()
                        else:
                            author = author_line
                    annotation_div = li.find("div", style=re.compile(r"background:\s*#ddd", re.I))
                    annotation = annotation_div.get_text(strip=True) if annotation_div else ""

                    pdf_link = li.find("a", string=re.compile(r"Text práce ve formátu PDF", re.I))
                    pdf_url = ""
                    if pdf_link and pdf_link.get("href"):
                        href = pdf_link["href"]
                        pdf_url = href if href.startswith("http") else "http:" + href if href.startswith("//") else BASE_URL + "/" + href.lstrip("/")

                    actual_year = 1969 + year_num

                    works.append({
                        "id": work_id,
                        "title": title,
                        "author": author,
                        "school": school, 
                        "field": obor_name,
                        "year": actual_year,
                        "keywords": [],
                        "content_url": pdf_url,
                        "annotation": annotation
                    })
                    work_id += 1

                except Exception as e:
                    print(f"zpracování práce: {e}")
                    continue

        time.sleep(0.5)

    return works

if __name__ == "__main__":
    try:
        data = scrape_soc_archiv()
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nÚspěšně scrapováno {len(data)} prací. Uloženo do data.json")
    except Exception as e:
        print(f"Chyba: {e}")
        import traceback
        traceback.print_exc()