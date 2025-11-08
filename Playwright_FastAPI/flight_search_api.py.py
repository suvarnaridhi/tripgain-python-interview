from fastapi import FastAPI, Query
from playwright.sync_api import sync_playwright
from typing import List
import json 
import time

app = FastAPI(title="Flight Search API", description="Scrapes flight data from BudgetTicket", version="1.0")

@app.get("/flight-search")
def flight_search(
    origin: str = Query(..., description="Origin city name"),
    destination: str = Query(..., description="Destination city name")
):
    """
    Scrape flight details for given origin, destination, and journey_date.
    Returns JSON with list of flights.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.budgetticket.in/", timeout=60000)

        # --- ORIGIN ---
        origin_input = page.get_by_role("textbox", name="Select Origin City").nth(0)
        origin_input.click()
        origin_input.fill(origin)
        page.wait_for_selector(".angucomplete-row", timeout=5000)
        page.locator(".angucomplete-row", has_text=origin).first.click()

        # --- DESTINATION ---
        dest_input = page.get_by_role("textbox", name="Select Destination City").nth(0)
        dest_input.click()
        dest_input.fill(destination)
        page.wait_for_selector(".angucomplete-row", timeout=5000)
        page.locator(".angucomplete-row", has_text=destination).first.click()

        # (Journey date picker skipped as site defaults to nearest available date)

        # --- SEARCH FLIGHTS ---
        page.locator("input[value='Search']").first.click()
        print(f"🔍 Searching flights {origin} → {destination}")

        # --- WAIT FOR RESULTS ---
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("div.search-card.card", timeout=90000)

        # --- SCRAPE USING JS (faster method) ---
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

        browser.close()

        print(f"✅ Extracted {len(flights)} flights from {origin} → {destination}")
        return {"origin": origin, "destination": destination, "flights_found": len(flights), "flights": flights}
