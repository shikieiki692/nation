import json, re

with open('replaced_pics.json', 'r', encoding='utf-8') as f:
    replaced = json.load(f)
with open('missing_placeholders.json', 'r', encoding='utf-8') as f:
    missing = json.load(f)
with open('ocr_images.json', 'r', encoding='utf-8') as f:
    ocr_images = json.load(f)

# Build a list of all targets
targets = []
for r in replaced:
    targets.append({
        'id': r['file'] + '::' + r['caption'],
        'type': 'revert',
        'file': r['file'],
        'path': r['path'],
        'bad_hash': r['hash'],
        'desc': r['caption'] + ' ' + r['desc'],
        'full_match': r['full']
    })

for m in missing:
    targets.append({
        'id': m['file'] + '::' + m['desc'],
        'type': 'missing',
        'file': m['basename'],
        'path': m['file'],
        'desc': m['desc'],
        'full_match': m['full_match']
    })

def get_keywords(text):
    # Extract english words and numbers/formulas
    en_words = re.findall(r'[a-zA-Z0-9_\-\.\+]+', text)
    
    # Extract Chinese consecutive character pairs (bigrams)
    ch_chars = re.findall(r'[\u4e00-\u9fa5]', text)
    ch_bigrams = []
    if len(ch_chars) >= 2:
        ch_bigrams = [ch_chars[i]+ch_chars[i+1] for i in range(len(ch_chars)-1)]
        
    return set([w.lower() for w in en_words if len(w)>1] + ch_bigrams)

results = {}
for t in targets:
    kws = get_keywords(t['desc'])
    
    # specific manual boosts for known terms
    if 'Weller' in t['desc']: kws.add('weller')
    if 'Atkins' in t['desc']: kws.add('atkins')
    if 'Zchem' in t['desc']: kws.add('zchem')
    
    # specific figure numbers like '14E.2' or '图 16.1'
    fig_match = re.search(r'图\s*(\d+[A-Z\.]*\d*)', t['desc'])
    fig_num = fig_match.group(1).lower() if fig_match else None
    
    best_score = 0
    best_img = None
    
    for img in ocr_images:
        context = img['context'].lower()
        score = 0
        for kw in kws:
            if kw in context:
                score += 1
                if kw in ['born-haber', 'pourbaix', 'sackur-tetrode', 'dlvo', 'langmuir', 'zintl', 'keggin', 'born']:
                    score += 10 # massive boost
                    
        if fig_num and '图' + fig_num in context.replace(' ', ''):
            score += 20
            
        if score > best_score:
            best_score = score
            best_img = img
            
    if best_score >= 4:
        results[t['id']] = {
            'target': t,
            'match': best_img,
            'score': best_score,
            'kws': list(kws)
        }

with open('match_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"Matched {len(results)} out of {len(targets)}")
