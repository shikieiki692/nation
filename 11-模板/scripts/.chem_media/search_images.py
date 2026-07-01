import requests
import json

# Search Wikimedia Commons for each image using the search API
searches = {
    'mo_diagram': 'molecular orbital diagram homonuclear diatomic second period',
    'sigma_pi': 'sigma pi bond orbital overlap',
    'h2_energy': 'hydrogen molecule potential energy dissociation curve',
    'cft_splitting': 'crystal field splitting octahedral d orbital',
    'vsepr': 'VSEPR molecular geometry shapes',
    'spectrochemical': 'spectrochemical series ligand',
}

print("=== Searching Wikimedia Commons ===\n")
for key, query in searches.items():
    print(f"--- {key} ---")
    api_url = f'https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={query}&srnamespace=6&srlimit=5&format=json'
    try:
        r = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        data = r.json()
        results = data.get('query', {}).get('search', [])
        for i, result in enumerate(results):
            title = result.get('title', '')
            print(f"  {i+1}. {title}")
    except Exception as e:
        print(f"  ERROR: {e}")
    print()
