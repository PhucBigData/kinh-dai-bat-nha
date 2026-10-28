#!/usr/bin/env python3
"""
Prajñā Full-Text Inverted Index Builder
Extracts all vocabulary and Buddhist compound terms across all 600 Quyển.
Outputs a high-performance, compact inverted index JSON for zero-latency browser search.
"""

import glob
import re
import json
import os
import sys

def build_index():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tap_files = sorted(glob.glob(os.path.join(repo_root, 'Tap_*', '*.md')))
    
    if len(tap_files) != 600:
        print(f"Warning: expected 600 files, found {len(tap_files)}")
        
    index = {} # term -> list of [quyen, count]
    
    print(f"Indexing {len(tap_files)} scripture files...")
    
    for idx, fpath in enumerate(tap_files):
        q_num = idx + 1
        with open(fpath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Extract only scripture text (skip audit table and headers)
        scripture_lines = []
        skipping_table = False
        
        for line in lines:
            trimmed = line.strip()
            if trimmed.startswith('### BẢNG ĐỐI CHIẾU TRANG NGUYÊN BẢN'):
                skipping_table = True
                continue
            if skipping_table:
                if trimmed.startswith('### NỘI DUNG KINH VĂN'):
                    skipping_table = False
                continue
            if trimmed.startswith('|') and trimmed.endswith('|'):
                continue
            if trimmed.startswith('#') or trimmed.startswith('* ') or trimmed.startswith('- '):
                continue
            if trimmed:
                scripture_lines.append(trimmed)
                
        text = " ".join(scripture_lines).lower()
        
        # 1. Single words (len >= 2)
        words = re.findall(r'[a-zà-ỹđ]+', text)
        word_counts = {}
        for w in words:
            if len(w) >= 2:
                word_counts[w] = word_counts.get(w, 0) + 1
                
        # 2. Hyphenated compound terms (e.g. bồ-tát, bát-nhã, ba-la-mật, ma-ha-tát, tát-bà-nhã)
        compounds = re.findall(r'[a-zà-ỹđ]+(?:-[a-zà-ỹđ]+){1,3}', text)
        compound_counts = {}
        for c in compounds:
            compound_counts[c] = compound_counts.get(c, 0) + 1
            # Also count space version
            space_ver = c.replace('-', ' ')
            compound_counts[space_ver] = compound_counts.get(space_ver, 0) + 1
            
        # Merge counts for this quyen
        all_terms = {**word_counts, **compound_counts}
        for term, cnt in all_terms.items():
            if term not in index:
                index[term] = []
            index[term].append([q_num, cnt])
            
    print(f"Total unique terms indexed: {len(index)}")
    
    # Save output
    out_path = os.path.join(repo_root, 'reader', 'data', 'search_index.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    with open(out_path, 'w', encoding='utf-8') as out_f:
        json.dump(index, out_f, ensure_ascii=False, separators=(',', ':'))
        
    size_kb = os.path.getsize(out_path) / 1024
    print(f"Generated {out_path} ({size_kb:.2f} KB)")

if __name__ == '__main__':
    build_index()
