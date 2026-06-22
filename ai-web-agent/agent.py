from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def browse(url, page):
    print(f"🌐 Browsing: {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    
    # Scroll biar konten lazy-load muncul
    page.mouse.wheel(0, 3000)
    page.wait_for_timeout(2000)
    
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return text[:2000]

def tanya_ai(goal, content, visited_urls):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Kamu adalah AI web agent. Jawab hanya dengan format DONE: atau BROWSE: tanpa penjelasan tambahan."
            },
            {
                "role": "user",
                "content": f"""Goal: {goal}

URL yang sudah dikunjungi: {visited_urls}

Konten halaman:
{content}

Apakah goal sudah tercapai?
- Kalau sudah: DONE: [ringkasan singkat hasil]
- Kalau belum dan perlu URL baru (bukan yang sudah dikunjungi): BROWSE: [URL]
- Kalau tidak ada URL lain: DONE: Tidak ditemukan informasi yang relevan"""
            }
        ]
    )
    return response.choices[0].message.content

def run_agent(goal, start_url):
    print(f"\n🤖 AI Web Agent")
    print(f"📋 Goal: {goal}")
    print(f"🚀 Starting at: {start_url}\n")
    
    visited_urls = []
    max_steps = 5
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        current_url = start_url
        
        for step in range(max_steps):
            print(f"--- Step {step + 1} ---")
            
            if current_url in visited_urls:
                print("❌ URL sudah dikunjungi, stop.")
                break
                
            visited_urls.append(current_url)
            content = browse(current_url, page)
            decision = tanya_ai(goal, content, visited_urls)
            print(f"AI: {decision}\n")
            
            if decision.startswith("DONE:"):
                print(f"✅ Selesai!")
                print(decision.replace("DONE:", "").strip())
                break
            elif decision.startswith("BROWSE:"):
                next_url = decision.replace("BROWSE:", "").strip()
                if next_url.startswith("http") and next_url not in visited_urls:
                    current_url = next_url
                else:
                    print("❌ URL ga valid atau sudah dikunjungi, stop.")
                    break
        
        browser.close()

if __name__ == "__main__":
    goal = input("Masukkan goal: ")
    start_url = input("Masukkan URL awal: ")
    run_agent(goal, start_url)