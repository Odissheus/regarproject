import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
from chat_manager import ChatManager

def scrape_aifa_news():
    """Esegue lo scraping delle ultime news dal sito AIFA"""
    url = "https://www.aifa.gov.it/news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.aifa.gov.it/'
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            print("Non è stato possibile accedere al sito AIFA")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []
        
        # Trova tutti gli articoli di news
        articles = soup.find_all('article', class_='news-item')
        print(f"Numero di articoli trovati: {len(articles)}")
        
        if not articles:
            # Prova una ricerca più generica
            print("Tentativo con selettore alternativo")
            articles = soup.find_all(['article', 'div'], class_=['news-item', 'news', 'article'])
            print(f"Articoli trovati con selettore alternativo: {len(articles)}")
        
        # Inizializza ChatManager per riassunti
        chat_manager = None
        try:
            chat_manager = ChatManager()
        except Exception as e:
            print(f"Impossibile inizializzare ChatManager: {e}")
        
        for idx, article in enumerate(articles[:10]):
            try:
                # Estrai data
                date_elem = article.find('time')
                date_str = date_elem.text.strip() if date_elem else ""
                try:
                    # Converte la data dal formato italiano a ISO
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                    date_iso = date_obj.isoformat()
                except:
                    date_iso = datetime.now().isoformat()
                
                # Estrai titolo
                title_elem = article.find('h2')
                title = title_elem.text.strip() if title_elem else "Titolo non disponibile"
                
                # Estrai link
                link_elem = title_elem.find('a') if title_elem else None
                link = "https://www.aifa.gov.it" + link_elem['href'] if link_elem and 'href' in link_elem.attrs else ""
                
                # Ottieni il contenuto completo dell'articolo
                content = get_article_content(link) if link else "Contenuto non disponibile"
                
                # Estrai summary
                summary_elem = article.find('div', class_='field-summary')
                summary = summary_elem.text.strip() if summary_elem else ""
                
                # Se abbiamo il ChatManager e non c'è un riassunto, generalo
                if not summary and chat_manager and content != "Contenuto non disponibile":
                    summary = generate_summary(title, content, link, chat_manager)
                elif not summary:
                    summary = content[:150] + "..." if len(content) > 150 else content
                
                # Aggiungi alla lista
                news_items.append({
                    "id": idx + 1,
                    "date": date_iso,
                    "title": title,
                    "summary": summary,
                    "link": link
                })
                print(f"Articolo elaborato: {title}")
            except Exception as e:
                print(f"Errore nell'elaborazione di un articolo: {e}")
        
        return news_items
    except Exception as e:
        print(f"Errore generale nello scraping: {e}")
        return []

def get_article_content(article_url):
    """Ottiene il contenuto completo di un articolo"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(article_url, headers=headers)
        
        if response.status_code != 200:
            return "Contenuto non disponibile"
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Cerca il contenuto dell'articolo
        article_content = soup.find('div', class_='field-body')
        
        if not article_content:
            # Prova selettori alternativi
            article_content = soup.find(['div', 'article'], class_=['content', 'body', 'article-content'])
        
        if article_content:
            # Estrai solo testo senza HTML
            return article_content.get_text(separator='\n', strip=True)
        else:
            return "Contenuto non disponibile"
    except Exception as e:
        print(f"Errore nell'estrazione del contenuto dell'articolo: {e}")
        return "Errore nell'estrazione del contenuto"

def generate_summary(title, content, url, chat_manager):
    """Genera un riassunto intelligente usando un LLM"""
    try:
        prompt = f"Riassumi questa notizia AIFA in circa 2-3 frasi, mantenendo le informazioni essenziali:\n\nTitolo: {title}\n\nContenuto: {content}\n\nURL: {url}"
        summary = chat_manager.get_response(prompt)
        return summary
    except Exception as e:
        print(f"Errore nella generazione del riassunto: {e}")
        return content[:150] + "..." if len(content) > 150 else content

def scrape_aifa_site_structure():
    """Mappa la struttura del sito AIFA per aiutare la navigazione"""
    base_url = "https://www.aifa.gov.it"
    main_sections = [
        {"url": f"{base_url}/farmaci-e-dispositivi/farmaci", "name": "Farmaci", "description": "Informazioni sui farmaci, autorizzazioni e monitoraggio"},
        {"url": f"{base_url}/farmaci-equivalenti", "name": "Farmaci Equivalenti", "description": "Liste di trasparenza e farmaci equivalenti"},
        {"url": f"{base_url}/farmacovigilanza", "name": "Farmacovigilanza", "description": "Segnalazione e monitoraggio delle reazioni avverse"},
        {"url": f"{base_url}/carenze-di-medicinali", "name": "Carenze di Medicinali", "description": "Informazioni sulle carenze di farmaci e indisponibilità"},
        {"url": f"{base_url}/prezzi-e-rimborso", "name": "Prezzi e Rimborso", "description": "Informazioni su prezzi, fasce di rimborsabilità e negoziazioni"},
        {"url": f"{base_url}/normativa", "name": "Normativa", "description": "Leggi, determine, note e circolari relative ai farmaci"},
        {"url": f"{base_url}/modulistica", "name": "Modulistica", "description": "Moduli e documentazione necessaria per varie procedure"}
    ]
    
    sections = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Per ogni sezione principale, raccoglie informazioni di base
    for section in main_sections:
        try:
            response = requests.get(section["url"], headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Trova eventuali sottosezioni
                subsections = []
                menu_items = soup.find_all('a', class_='nav-link')
                for item in menu_items[:5]:  # Limita a 5 sottosezioni
                    href = item.get('href', '')
                    if href and href.startswith('/'):
                        subsections.append({
                            "name": item.text.strip(),
                            "url": f"{base_url}{href}"
                        })
                
                sections.append({
                    "name": section["name"],
                    "description": section["description"],
                    "url": section["url"],
                    "subsections": subsections
                })
        except Exception as e:
            print(f"Errore nello scraping della sezione {section['name']}: {e}")
            # Aggiungi comunque la sezione senza sottosezioni
            sections.append({
                "name": section["name"],
                "description": section["description"],
                "url": section["url"],
                "subsections": []
            })
    
    return sections

def update_database_with_site_structure(db_path='database.db'):
    """Aggiorna il database con la struttura del sito AIFA"""
    sections = scrape_aifa_site_structure()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crea tabella se non esiste
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aifa_sections (
        id INTEGER PRIMARY KEY,
        section_name TEXT,
        description TEXT,
        url TEXT,
        parent_id INTEGER NULL,
        FOREIGN KEY (parent_id) REFERENCES aifa_sections (id)
    )
    ''')
    
    # Pulisci la tabella
    cursor.execute("DELETE FROM aifa_sections")
    
    # Inserisci le sezioni principali
    for section in sections:
        cursor.execute('''
        INSERT INTO aifa_sections (section_name, description, url)
        VALUES (?, ?, ?)
        ''', (section["name"], section["description"], section["url"]))
        
        parent_id = cursor.lastrowid
        
        # Inserisci le sottosezioni
        for subsection in section.get("subsections", []):
            cursor.execute('''
            INSERT INTO aifa_sections (section_name, description, url, parent_id)
            VALUES (?, ?, ?, ?)
            ''', (subsection["name"], "", subsection["url"], parent_id))
    
    conn.commit()
    conn.close()
    
    return len(sections)

if __name__ == "__main__":
    print("Esecuzione dello scraper AIFA...")
    news = scrape_aifa_news()
    print(f"Trovate {len(news)} notizie")
    for item in news:
        print(f"- {item['title']}")