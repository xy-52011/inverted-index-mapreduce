import os
import re
from collections import defaultdict

INPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
STOPWORDS_FILE = os.path.join(INPUT_DIR, 'stopwords.txt')

def load_stopwords(path):
    stopwords = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if word:
                stopwords.add(word)
    return stopwords

def mapper(filepath, stopwords):
    intermediate = []
    filename = os.path.basename(filepath)
    if filename == 'stopwords.txt':
        return intermediate
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    tokens = re.split(r'[^a-zA-Z]+', text)
    for token in tokens:
        if not token or len(token) < 2:
            continue
        if token in stopwords:
            continue
        intermediate.append((token + '#' + filename, 1))
    return intermediate

def combiner(mapped_data):
    combined = defaultdict(int)
    for key, value in mapped_data:
        combined[key] += value
    return combined

def reducer(combined_data):
    word_postings = defaultdict(list)
    for key, count in combined_data.items():
        word, filename = key.split('#', 1)
        word_postings[word].append((filename, count))
    result = {}
    for word in sorted(word_postings.keys()):
        postings = sorted(word_postings[word], key=lambda x: x[0])
        total = sum(c for _, c in postings)
        parts = ['<{},{}>'.format(fn, c) for fn, c in postings]
        parts.append('<total,{}>'.format(total))
        result[word] = ';'.join(parts) + '.'
    return result

def main():
    stopwords = load_stopwords(STOPWORDS_FILE)
    all_mapped = []
    txt_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.txt') and f != 'stopwords.txt'])
    print('Documents to process:')
    for fn in txt_files:
        print('  ' + fn)
        filepath = os.path.join(INPUT_DIR, fn)
        all_mapped.extend(mapper(filepath, stopwords))
    print('\nTotal mapped records: {}'.format(len(all_mapped)))
    combined = combiner(all_mapped)
    print('Unique word-document pairs: {}'.format(len(combined)))
    result = reducer(combined)
    print('Unique indexed words: {}'.format(len(result)))
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, 'part-r-00000')
    with open(output_path, 'w', encoding='utf-8') as f:
        for word, postings in result.items():
            f.write('{}\t{}\n'.format(word, postings))
    print('\nOutput written to: ' + output_path)
    print('\nSample results (first 20 words):')
    for i, (word, postings) in enumerate(result.items()):
        if i >= 20:
            break
        print('{}  {}'.format(word, postings))

if __name__ == '__main__':
    main()
