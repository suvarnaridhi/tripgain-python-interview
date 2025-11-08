from playwright.sync_api import sync_playwright
import time
import json

def safe_text(locator):
    try:
        return locator.inner_text().strip()
    except:
        return ""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto("https://www.budgetticket.in/", timeout=60000)

    # --- ORIGIN ---
    origin = page.get_by_role("textbox", name="Select Origin City").nth(0)
    origin.click()
    origin.fill("Bangalore")
    page.wait_for_selector(".angucomplete-row", timeout=5000)
    page.locator(".angucomplete-row", has_text="Bangalore").first.click()

    # --- DESTINATION ---
    dest = page.get_by_role("textbox", name="Select Destination City").nth(0)
    dest.click()
    dest.fill("Delhi")
    page.wait_for_selector(".angucomplete-row", timeout=5000)
    page.locator(".angucomplete-row", has_text="Delhi").first.click()

    # --- SEARCH FLIGHTS ---
    page.locator("input[value='Search']").first.click()

    print("⏳ Waiting for flight results to load...")
    page.wait_for_load_state("networkidle")
    page.locator("div.search-card").first.wait_for(state="visible", timeout=60000)

    # --- EXTRACT FLIGHTS ---
    flight_cards = page.locator("div.search-card.card")
    flight_count = flight_cards.count()
    print(f"Found {flight_count} flights")

    # Extract all flight details via JS evaluation (fast)
    flights = page.evaluate("""
    () => {
        const cards = Array.from(document.querySelectorAll('div.search-card.card'));
        return cards.map(card => ({
            airline: card.querySelector('p.h6.responsive-bold, p.text-mild-dark')?.innerText.trim() || '',
            flight_number: Array.from(card.querySelectorAll('p')).find(p => p.innerText.includes('-'))?.innerText.trim() || '',
            dep_time: card.querySelector('span.text-mild-dark')?.innerText.trim() || '',
            arr_time: card.querySelectorAll('span.text-mild-dark')[1]?.innerText.trim() || '',
            duration: Array.from(card.querySelectorAll('span')).find(s => s.innerText.includes('h'))?.innerText.trim() || '',
            price: Array.from(card.querySelectorAll('p, span')).find(e => e.innerText.includes('₹'))?.innerText.trim() || ''
        }));
    }
    """)

    # Save results to JSON file
    with open("flight_results.json", "w", encoding="utf-8") as f:
        json.dump(flights, f, indent=4, ensure_ascii=False)

    print(f"✅ Extracted {len(flights)} flights and saved to flight_results.json")

    browser.close()
