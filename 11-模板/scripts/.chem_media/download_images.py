"""
Download chemistry textbook images from Wikimedia Commons.
Uses the Wikimedia Commons API to search for and download images.
"""
import requests
import json
import os
import sys
import time

MEDIA_DIR = r"C:\Obsidion\妙妙屋\media"

# Image search queries and target filenames
IMAGES = [
    {
        "filename": "pi_bond_textbook.png",
        "search_terms": ["Pi-bond", "Sigma-and-pi-bonds", "Orbital overlap pi bond", "Ethylene pi bond orbital"],
    },
    {
        "filename": "mo_diagram_o2_textbook.jpg",
        "search_terms": ["MO diagram of O2", "Molecular orbital diagram oxygen", "MO_diagram_of_O2"],
    },
    {
        "filename": "intermolecular_forces_textbook.jpg",
        "search_terms": ["Intermolecular forces", "Hydrogen bond water diagram", "Water hydrogen bonding diagram"],
    },
    {
        "filename": "dd_transition_textbook.jpg",
        "search_terms": ["Crystal field splitting diagram", "d-d transition", "Color of transition metal ions"],
    },
    {
        "filename": "spectrochemical_series_textbook.jpg",
        "search_terms": ["Spectrochemical series", "D-orbital splitting diagram", "Spectrochemical_series"],
    },
    {
        "filename": "hs_ls_comparison_textbook.jpg",
        "search_terms": ["Crystal field splitting diagram for octahedral complex", "High spin low spin d orbital"],
    },
    {
        "filename": "cft_tetrahedral_textbook.jpg",
        "search_terms": ["Tetrahedral Crystal Field Splitting", "Tetrahedral crystal field"],
    },
    {
        "filename": "isomerism_textbook.jpg",
        "search_terms": ["Cisplatin", "Cis-trans isomerism coordination", "Geometric isomerism"],
    },
]


def search_commons(search_term, limit=5):
    """Search Wikimedia Commons for files matching a search term."""
    api_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "srnamespace": "6",  # File namespace
        "srlimit": str(limit),
        "format": "json",
    }
    try:
        r = requests.get(api_url, params=params, headers={"User-Agent": "ChemistryHandoutBot/1.0"}, timeout=15)
        data = r.json()
        results = data.get("query", {}).get("search", [])
        return [r["title"].replace("File:", "") for r in results]
    except Exception as e:
        print(f"    Search error: {e}")
        return []


def get_file_url(filename):
    """Get the direct download URL for a Wikimedia Commons file (prefers PNG thumbnail)."""
    api_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "iiurlwidth": 1200,
        "format": "json",
    }
    try:
        r = requests.get(api_url, params=params, headers={"User-Agent": "ChemistryHandoutBot/1.0"}, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if "imageinfo" in page_data:
                info = page_data["imageinfo"][0]
                # Use thumbnail if available (max 1200px wide)
                if "thumburl" in info:
                    return info["thumburl"], info.get("mime", "")
                return info["url"], info.get("mime", "")
    except Exception as e:
        print(f"    API error: {e}")
    return None, None


def download_file(url, filepath):
    """Download a file from URL to filepath."""
    r = requests.get(url, headers={"User-Agent": "ChemistryHandoutBot/1.0"}, timeout=60)
    if r.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(r.content)
        return len(r.content)
    else:
        raise Exception(f"HTTP {r.status_code}")


def process_image(image_info):
    """Search for and download a single image."""
    target_filename = image_info["filename"]
    print(f"\n{'='*60}")
    print(f"Target: {target_filename}")

    all_results = []
    for term in image_info["search_terms"]:
        print(f"  Searching: '{term}'")
        results = search_commons(term, limit=3)
        if results:
            print(f"    Found: {results[:3]}")
            all_results.extend(results)
        time.sleep(0.5)

    # Deduplicate while preserving order
    seen = set()
    unique_results = []
    for r in all_results:
        if r not in seen:
            seen.add(r)
            unique_results.append(r)

    if not unique_results:
        print(f"  FAILED: No results found for any search term.")
        return False

    # Try each result until we get a successful download
    for result_file in unique_results:
        try:
            url, mime = get_file_url(result_file)
            if url is None:
                print(f"    {result_file}: no URL, skipping")
                continue

            # Determine target path
            target_path = os.path.join(MEDIA_DIR, target_filename)

            print(f"    Downloading: {result_file}")
            print(f"    URL: {url[:100]}...")
            size = download_file(url, target_path)
            print(f"    SUCCESS: {target_filename} ({size:,} bytes)")
            return True

        except Exception as e:
            print(f"    Error downloading {result_file}: {e}")
            continue

    print(f"  FAILED: Could not download any image.")
    return False


def main():
    os.makedirs(MEDIA_DIR, exist_ok=True)

    print("=" * 60)
    print("Chemistry Textbook Image Downloader")
    print("Source: Wikimedia Commons")
    print("=" * 60)

    results = {}
    for img in IMAGES:
        success = process_image(img)
        results[img["filename"]] = success
        time.sleep(1)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for filename, success in results.items():
        status = "OK" if success else "FAILED"
        print(f"  [{status}] {filename}")

    success_count = sum(1 for v in results.values() if v)
    print(f"\nTotal: {success_count}/{len(results)} downloaded successfully.")

    return success_count


if __name__ == "__main__":
    sys.exit(0 if main() > 0 else 1)
