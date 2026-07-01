import requests
import json
import os
import urllib.parse

media_dir = r'C:\Obsidion\妙妙屋\media'
os.makedirs(media_dir, exist_ok=True)

def search_and_get_url(query, namespace=6, limit=3):
    """Search Wikimedia and return first image URL"""
    encoded_query = urllib.parse.quote(query)
    api_url = f'https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&srnamespace={namespace}&srlimit={limit}&format=json'
    r = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
    data = r.json()
    results = data.get('query', {}).get('search', [])
    for result in results:
        title = result.get('title', '')
        # Get file info - need to URL-encode the title properly
        # The title starts with "File:" - we need to encode the whole thing
        encoded_title = urllib.parse.quote(title, safe='/:')
        file_api = f'https://commons.wikimedia.org/w/api.php?action=query&titles={encoded_title}&prop=imageinfo&iiprop=url|size|mime&format=json'
        r2 = requests.get(file_api, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        data2 = r2.json()
        pages2 = data2.get('query', {}).get('pages', {})
        for pid, pdata in pages2.items():
            if 'imageinfo' in pdata:
                info = pdata['imageinfo'][0]
                mime = info.get('mime', '')
                if mime.startswith('image/'):
                    return {
                        'url': info['url'],
                        'size': info.get('size', 0),
                        'mime': mime,
                        'title': title,
                    }
    return None

def get_file_url(filename):
    """Get URL for a specific file"""
    encoded_title = urllib.parse.quote(f'File:{filename}', safe='/:')
    api_url = f'https://commons.wikimedia.org/w/api.php?action=query&titles={encoded_title}&prop=imageinfo&iiprop=url|size|mime&format=json'
    r = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    data = r.json()
    pages = data.get('query', {}).get('pages', {})
    for pid, pdata in pages.items():
        if 'imageinfo' in pdata:
            info = pdata['imageinfo'][0]
            return {
                'url': info['url'],
                'size': info.get('size', 0),
                'mime': info.get('mime', ''),
                'title': f'File:{filename}',
            }
    return None

def download_image(url, filepath):
    """Download image from URL"""
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    if r.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(r.content)
        return len(r.content)
    return None

# Define what we need with multiple search strategies
image_specs = [
    {
        'key': 'mo_diagram',
        'output': 'mo_diagram_textbook.png',
        'searches': ['molecular orbital diagram diatomic'],
        'try_files': ['2nd_row_diatomic_MOs.png', 'MO_diagram_O2_F2.png'],
    },
    {
        'key': 'sigma_pi',
        'output': 'sigma_pi_bond_textbook.png',
        'searches': ['sigma pi bond', 'orbital overlap bond'],
        'try_files': ['Sigma-and-pi-bonds.png', 'Pi_bond.svg'],
    },
    {
        'key': 'h2_energy',
        'output': 'h2_energy_curve_textbook.png',
        'searches': ['hydrogen molecule dissociation energy curve', 'molecular dissociation energy'],
        'try_files': ['Dissociation_energy_diagram_of_H2_molecule.png'],
    },
    {
        'key': 'cft_splitting',
        'output': 'cft_splitting_textbook.png',
        'searches': ['crystal field splitting octahedral', 'octahedral splitting diagram'],
        'try_files': ['Octahedral_splitting_diagram.svg', 'CFT_OF_OH.png'],
    },
    {
        'key': 'vsepr',
        'output': 'vsepr_geometries_textbook.png',
        'searches': ['VSEPR geometries', 'VSEPR molecular geometry'],
        'try_files': ['VSEPR_geometries.PNG', 'Geometrie_VSEPR.png'],
    },
    {
        'key': 'spectrochemical',
        'output': 'spectrochemical_series_textbook.png',
        'searches': ['spectrochemical series ligand field'],
        'try_files': ['Spectrochemical_series.png'],
    },
]

results = {}
for spec in image_specs:
    key = spec['key']
    print(f"\n=== {key} ===")
    found = None

    # Try specific files first
    for filename in spec.get('try_files', []):
        result = get_file_url(filename)
        if result:
            print(f"  Found file: {filename}")
            found = result
            break

    # If not found, search
    if not found:
        for query in spec['searches']:
            print(f"  Searching: {query}")
            result = search_and_get_url(query)
            if result:
                print(f"  Found: {result['title']}")
                found = result
                break

    if found:
        filepath = os.path.join(media_dir, spec['output'])
        size = download_image(found['url'], filepath)
        if size:
            print(f"  DOWNLOADED: {spec['output']} ({size:,} bytes)")
            results[key] = {'status': 'OK', 'size': size, 'file': spec['output']}
        else:
            print(f"  DOWNLOAD FAILED")
            results[key] = {'status': 'DOWNLOAD_FAILED'}
    else:
        print(f"  NOT FOUND")
        results[key] = {'status': 'NOT_FOUND'}

# Summary
print("\n\n=== FINAL SUMMARY ===")
for key, result in results.items():
    if result['status'] == 'OK':
        print(f"  [OK]   {result['file']} - {result['size']:,} bytes")
    else:
        print(f"  [FAIL] {key} - {result['status']}")
