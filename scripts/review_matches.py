import json

with open('match_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

high = []
low = []
zero = []

for fname, items in results.items():
    for item in items:
        if item['score'] >= 5:
            high.append(item)
        elif item['score'] > 0:
            low.append(item)
        else:
            zero.append(item)

print(f'High confidence (>=5): {len(high)}')
print(f'Low confidence (1-4): {len(low)}')
print(f'No match (0): {len(zero)}')

with open('match_review.txt', 'w', encoding='utf-8') as f:
    f.write('--- High Matches ---\n')
    for item in high:
        f.write(f"P: {item['placeholder']['desc']}\n")
        f.write(f"M: {item['best_match']['desc']} (Score: {item['score']})\n\n")
        
    f.write('--- Low Matches ---\n')
    for item in low:
        f.write(f"P: {item['placeholder']['desc']}\n")
        f.write(f"M: {item['best_match']['desc']} (Score: {item['score']})\n\n")

