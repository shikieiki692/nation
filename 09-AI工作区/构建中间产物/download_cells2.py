import urllib.request
import urllib.parse
import json
import hashlib
import os
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

MEDIA_DIR = r"c:\Obsidion\妙妙屋\媒体仓库"
os.makedirs(MEDIA_DIR, exist_ok=True)

files_to_download = [
    "File:Cadmium-iodide-3D-balls.png",
    "File:Copper(I)-oxide-unit-cell-A-3D-balls.png"
]

results = {}

def get_image(filename):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            pages = data['query']['pages']
            for page_id in pages:
                if 'imageinfo' in pages[page_id]:
                    img_url = pages[page_id]['imageinfo'][0]['url']
                    print(f"Found URL for {filename}: {img_url}")
                    
                    time.sleep(2) # avoid ratelimit
                    img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0'})
                    with urllib.request.urlopen(img_req) as img_resp:
                        img_data = img_resp.read()
                        
                        h = hashlib.sha256(img_data).hexdigest()
                        ext = 'png'
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
    time.sleep(2)

with open(r"c:\Obsidion\妙妙屋\download_results2.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Done!")
