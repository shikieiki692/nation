import requests
import json
import os
import urllib.parse

# Use the Wikimedia API search to find actual filenames
searches = {
    'mo_diagram': 'molecular orbital diagram diatomic',
    'sigma_pi': 'sigma pi bond orbital',
    'h2_energy': 'hydrogen molecule dissociation energy',
    'cft_splitting': 'crystal field splitting octahedral',
    'vsepr': 'VSEPR geometries',
    'spectrochemical': 'spectrochemical series',
}

print("=== Searching Wikimedia Commons with proper encoding ===\n")
found_urls = {}

for key, query in searches.items():
    print(f"--- {key} ---")
    encoded_query = urllib.parse.quote(query)
    api_url = f'https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&srnamespace=6&srlimit=5&format=json'
    try:
        r = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        data = r.json()
        results = data.get('query', {}).get('search', [])
        for i, result in enumerate(results):
            title = result.get('title', '')
            # Get the actual file info
            file_api = f'https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url|size|mime&format=json'
            r2 = requests.get(file_api, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            data2 = r2.json()
            pages2 = data2.get('query', {}).get('pages', {})
            for pid, pdata in pages2.items():
                if 'imageinfo' in pdata:
                    info = pdata['imageinfo'][0]
                    mime = info.get('mime', '')
                    if mime.startswith('image/') and key not in found_urls:
                        found_urls[key] = {
                            'url': info['url'],
                            'size': info.get('size', 0),
                            'mime': mime,
                            'title': title,
                        }
                        print(f"  {i+1}. {title}")
                        print(f"     URL: {info['url']}")
                        print(f"     Size: {info.get('size', 'unknown')} bytes, MIME: {mime}")
    except Exception as e:
        print(f"  ERROR: {e}")
    if key not in found_urls:
        print(f"  No image found")
    print()

# Save results
with open(os.path.join(r'C:\Obsidion\妙妙屋\media', 'found_urls.json'), 'w', encoding='utf-8') as f:
    json.dump(found_urls, f, indent=2, ensure_ascii=False)

print(f"\nFound {len(found_urls)}/{len(searches)} images")
for key in found_urls:
    print(f"  [OK] {key}")
for key in searches:
    if key not in found_urls:
        print(f"  [MISS] {key}")
