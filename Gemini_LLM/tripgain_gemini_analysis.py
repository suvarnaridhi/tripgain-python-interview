import os, re, json, sys, requests
from bs4 import BeautifulSoup, Comment
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ----------------
URL = "https://en.wikipedia.org/wiki/Artificial_intelligence"
# URL = "https://www.bbc.com/news/technology"
# URL = "https://edition.cnn.com/business"

print(f"🌐 Fetching webpage: {URL}")
try:
    html = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
except Exception as e:
    print("❌ Error fetching webpage:", e)
    sys.exit(1)

soup = BeautifulSoup(html, "html.parser")

print(soup)


# prompt = f"""
# You are an expert analyst. Analyze the webpage content below and produce:
# 1. A concise summary in 3–5 bullet points.
# 2. One single-line analytical insight about the overall theme or impact.

# Return the result EXACTLY in this format:

# Summary:
# • point 1
# • point 2
# • point 3
# • point 4
# • point 5
# Insight:
# single-line insight

# === BEGIN CONTENT (source: {URL}) ===
# {text[:350000]}
# === END CONTENT ===
# """.strip()

# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     print("❌ ERROR: Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable.")
#     sys.exit(1)

# client = genai.Client(api_key=api_key)
# print("🤖 Sending content to Gemini 2.5 Flash...")

# try:
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#         config=types.GenerateContentConfig(
#             max_output_tokens=800,
#             temperature=0.2
#         )
#     )
#     output = response.text.strip()
# except Exception as e:
#     print("❌ Error calling Gemini API:", e)
#     sys.exit(1)
# finally:
#     try:
#         client.close()
#     except Exception:
#         pass

# # ---------------- OUTPUT ----------------
# print("\n" + output + "\n")

# # with open("summary_output.txt", "w", encoding="utf-8") as f:
# #     f.write(output)

# # print("✅ Output saved to summary_output.txt")
