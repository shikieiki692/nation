import requests
import json
import os

# Known correct filenames from search results + some well-known files
files_to_try = {
    'mo_diagram': [
        'Molecular_orbital_energy_level_diagrams_for_homonuclear_diatomic_molecules_B2_through_N2.png',
        'MO_diagram_for_O2_and_F2.svg',
        'MO_diagram_N2.svg',
        'Simple_Molecular_orbital_diagram_for_N2.svg',
        'Molecular_orbital_diagram_of_dinitrogen.svg',
    ],
    'sigma_pi': [
        'Sigma-and-pi-bonds.svg',
        'Sigma_pi_bonds.svg',
        'Orbital_overlap_in_ethylene.svg',
        'Pi_bond.svg',
        'Overlap.png',
    ],
    'h2_energy': [
        'Dissociation_energy_diagram_of_H2_molecule.png',
        'H2_dissociation.png',
        'Morse_potential.svg',
        'Potential_energy_curve.svg',
    ],
    'cft_splitting': [
        'Octahedral_splitting_diagram.svg',
        'CFT_OF_OH.png',
        'Crystal_field_splitting_energy_diagram.png',
        'Crystal_Field_Splitting_Octahedral.svg',
    ],
    'vsepr': [
        'VSEPR_geometries.PNG',
        'Geometrie_VSEPR.png',
        'VSEPR_A-XE.png',
        'VSEPR_chart.svg',
    ],
    'spectrochemical': [
        'Spectrochemical_series.png',
        'Spectrochemical_series.svg',
        'Crystal_field_splitting_spectrochemical.png',
    ],
}

print("=== Trying specific filenames ===\n")
found_urls = {}

for key, filenames in files_to_try.items():
    print(f"--- {key} ---")
    for filename in filenames:
        api_url = f'https://commons.wikimedia.org/w/api.php?action=query&titles=File:{filename}&prop=imageinfo&iiprop=url|size|mime&format=json'
        try:
            r = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            data = r.json()
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if 'imageinfo' in page_data:
                    info = page_data['imageinfo'][0]
                    found_urls[key] = {
                        'url': info['url'],
                        'size': info.get('size', 0),
                        'mime': info.get('mime', 'unknown'),
                        'filename': filename,
                    }
                    print(f"  FOUND: {filename}")
                    print(f"    URL: {info['url']}")
                    print(f"    Size: {info.get('size', 'unknown')} bytes, MIME: {info.get('mime', 'unknown')}")
                    break
        except Exception as e:
            print(f"  ERROR with {filename}: {e}")
    if key not in found_urls:
        print(f"  NOT FOUND")
    print()

# Save found URLs for the download script
with open(os.path.join(r'C:\Obsidion\妙妙屋\media', 'found_urls.json'), 'w') as f:
    json.dump(found_urls, f, indent=2)

print(f"\nFound {len(found_urls)}/{len(files_to_try)} images")
