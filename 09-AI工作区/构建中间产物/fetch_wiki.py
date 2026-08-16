import urllib.request, json
def get_wiki_image(title):
    url = f'https://en.wikipedia.org/w/api.php?action=query&titles={title}&prop=pageimages|images&format=json&pithumbsize=1000'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            pages = data['query']['pages']
            for page_id in pages:
                if 'thumbnail' in pages[page_id]:
                    print(f'{title}: {pages[page_id]["thumbnail"]["source"]}')
                else:
                    print(f'{title}: No thumbnail found')
    except Exception as e:
        print(f'Error fetching {title}: {e}')

get_wiki_image('Rutile')
get_wiki_image('Wurtzite_crystal_structure')
get_wiki_image('Nickel_arsenide')
get_wiki_image('Cuprite')
get_wiki_image('Cadmium_iodide')
get_wiki_image('Corundum')
