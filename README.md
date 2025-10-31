
# SOČ Archiv API

Tento projekt poskytuje REST API pro vyhledávání a správu vítězných prací ze soutěže Středoškolská odborná činnost (SOČ). Data jsou získávána zeřazením archivu na [archiv.soc.cz](https://archiv.soc.cz) a jsou uložena lokálně ve formátu JSON. API umožňuje fulltextové vyhledávání, filtrování podle oboru, školy a roku, a zajišťuje základní správu záznamů v souladu s požadavky GDPR.

---

## Funkce

- **Vyhledávání prací** podle názvu, autora, oboru nebo anotace.
- **Filtrování** podle oboru, školy a roku.
- **Správa záznamů**: možnost smazání práce (např. kvůli odvolání souhlasu s publikací).
- **Seznam účastníků** s historií jejich účasti v jednotlivých ročnících.
- **Automatická dokumentace API** přes Swagger UI na `/api`.

---

## Požadavky

Pro spuštění aplikace je třeba mít nainstalováno:

- Python 3.8 nebo novější
- `pip` 

Požadované závislosti:

- `fastapi`
- `uvicorn`
- `requests`
- `beautifulsoup4`

---

## Instalace a spuštění

1. **Klonujte repozitář** (nebo stáhněte soubory):

   ```bash
   git clone https://github.com/paronim5/soc_api.git
   cd soc_api
   ```  

2. **Nainstalujte závislosti**:

   ```bash
   pip install fastapi uvicorn requests beautifulsoup4
   ```

3. **Scrapování dat**:

   Pokud chcete aktualizovat nebo vytvořit soubor `data.json`, spusťte:

   ```bash
   python scrape_soc.py
   ```

   Tento krok může trvat několik minut, protože stahuje data z archivu.

4. **Spusťte server**:

   ```bash
   python uvicorn main:app --reload
   ```

   API bude dostupné na:

   - Hlavní stránka: http://localhost:8000
   - Swagger dokumentace: http://localhost:8000/api

---

## Struktura souborů

- `scrape.py` – skript pro scrapování dat z `archiv.soc.cz` do `data.json`.
- `main.py` – hlavní soubor FastAPI aplikace.
- `data.json` – databáze prací ve formátu JSON (vytvořena scrapovacím skriptem).

---

## Endpoints

| Metoda | Cesta                 | Popis |
|--------|-----------------------|-------|
| GET    | `/`                   | Základní informace o API a počet prací. |
| GET    | `/works`              | Vyhledávání a filtrování prací. Parametry: `query`, `field`, `school`, `year`. |
| DELETE | `/admin/works/{id}`   | Smazání práce podle ID (pro účely GDPR). |
| GET    | `/participants`       | Seznam autorů a ročníků, ve kterých se účastnili. |
| GET    | `/api`                | Interaktivní dokumentace API (Swagger UI). |
