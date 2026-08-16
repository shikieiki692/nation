import urllib.request
import urllib.parse
import json
import hashlib
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

MEDIA_DIR = r"c:\Obsidion\妙妙屋\媒体仓库"
os.makedirs(MEDIA_DIR, exist_ok=True)

files_to_download = [
    "File:Rutile-unit-cell-3D-balls.png",
    "File:Wurtzite-unit-cell-3D-balls.png",
    "File:Nickel-arsenide-3D-unit-cell.png",
    "File:Corundum-unit-cell-3D-balls.png",
    "File:Cadmium-iodide-3D-balls.png"
]

results = {}

def get_image(filename):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            pages = data['query']['pages']
            for page_id in pages:
                if 'imageinfo' in pages[page_id]:
                    img_url = pages[page_id]['imageinfo'][0]['url']
                    print(f"Found URL for {filename}: {img_url}")
                    
                    img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(img_req) as img_resp:
                        img_data = img_resp.read()
                        
                        h = hashlib.sha256(img_data).hexdigest()
                        ext = img_url.split('.')[-1].lower()
                        new_name = f"{h}.{ext}"
                        new_path = os.path.join(MEDIA_DIR, new_name)
                        
                        with open(new_path, "wb") as f:
                            f.write(img_data)
                        
                        results[filename] = new_name
                        print(f"Saved {filename} as {new_name}")
                        return
                else:
                    print(f"No imageinfo for {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

for f in files_to_download:
    get_image(f)

# Cuprite often goes by a different name, let's search it
def get_cuprite():
    url = "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=Cuprite+unit+cell+balls&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            if data['query']['search']:
                best = data['query']['search'][0]['title']
                print(f"Best match for Cuprite: {best}")
                get_image(best)
            else:
                print("No Cuprite match found")
    except Exception as e:
         print(f"Error searching Cuprite: {e}")

get_cuprite()

with open(r"c:\Obsidion\妙妙屋\download_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Done!")
