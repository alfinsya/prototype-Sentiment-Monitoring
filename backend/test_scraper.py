"""Test Google Scraper"""
import sys
sys.path.insert(0, r'c:\KULIAH\MAGANG\Magang di Perhutani\Project perhutani\monitoring-web\backend')

from services.google_scraper import search_google_news_scrape

# Test scraping
print("Testing Google News Scraper...")
print("-" * 50)

result = search_google_news_scrape("laptop samsung", max_results=5)

print(f"Success: {result.get('success')}")
print(f"Total results: {result.get('total')}")
print(f"Method: {result.get('method')}")
print()

if result.get('success'):
    for i, article in enumerate(result.get('results', []), 1):
        print(f"\n{i}. {article.get('title')}")
        print(f"   Source: {article.get('source')}")
        print(f"   URL: {article.get('url')[:80]}...")
else:
    print(f"Error: {result.get('error')}")
