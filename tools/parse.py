"""Parse the cached Wyoming text-only statute PDFs into corpus.json. Reads only .cache; deterministic."""
import hashlib, json, os, re
import pymupdf
HERE = os.path.dirname(os.path.abspath(__file__)); CACHE = os.path.join(HERE, '.cache')
BASE = 'https://wyoleg.gov/statutes/compress/'
FROM = '2026-05-08'  # the PDFs' own modification date (all four are within the same hour)
ACTS = [('constitution', 'Title97', 'Constitution of the State of Wyoming', 'WY Const.'),
        ('title-06-crimes-and-offenses', 'Title06', 'Wyoming Statutes Title 6: Crimes and Offenses', 'WY Stat. tit. 6'),
        ('title-17-corporations', 'Title17', 'Wyoming Statutes Title 17: Corporations, Partnerships and Associations', 'WY Stat. tit. 17'),
        ('title-34-property', 'Title34', 'Wyoming Statutes Title 34: Property, Conveyances and Security Transactions', 'WY Stat. tit. 34')]

def fix(s):
    s = s.replace(' ', ' ').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-')
    s = re.sub(r'(?<=[A-Za-z])�(?=[A-Za-z])', "'", s)
    return s

SEC = re.compile(r'^(\d+-\d+-\d+(?:\.\d+)?)\.\s+(.*)$', re.S)
CSEC = re.compile(r'^Article (\d+), Section (\d+[A-Za-z]?)\s+(.*)$', re.S)
GROUP = re.compile(r'^(TITLE|CHAPTER|ARTICLE|SUBARTICLE|PART|SUBCHAPTER)\s+[0-9A-Z.-]+\s+-\s+', re.I)

def blocks(pdf):
    d = pymupdf.open(pdf)
    text = '\n'.join(p.get_text() for p in d)
    out, cur = [], []
    for l in text.split('\n'):
        l = fix(l)
        if not l.strip():
            if cur: out.append(' '.join(x.strip() for x in cur)); cur = []
        else:
            cur.append(l)
    if cur: out.append(' '.join(x.strip() for x in cur))
    return [re.sub(r'\s+', ' ', b).strip() for b in out]

def key(s):
    return re.sub(r'[^a-z0-9-]+', '-', re.sub(r'\d+', lambda m: m.group().zfill(4), s.lower()))

def main():
    acts = []
    for slug, f, title, short in ACTS:
        pdf = os.path.join(CACHE, f + '.pdf')
        units, cur = {}, None
        for b in blocks(pdf):
            if GROUP.match(b) and slug != 'constitution' and not SEC.match(b): continue
            if slug == 'constitution':
                m = CSEC.match(b)
                if GROUP.match(b) and not m: continue
                if m:
                    a, s, h = m.groups(); k = f'art-{int(a):03d}-sec-{key(s)}'; label = f'Art. {int(a)}, § {s}'
                    units[k] = [label, h, []]; cur = k; continue
            else:
                m = SEC.match(b)
                if m:
                    n, h = m.groups(); k = key(n); label = f'W.S. {n}'
                    if k in units: raise SystemExit('dup ' + k)
                    units[k] = [label, h, []]; cur = k; continue
            if cur: units[cur][2].append(b)
        u = {k: {'label': v[0], 'kind': 'section', 'text': f'# {v[0]}. {v[1]}\n' + ''.join(p + '\n' for p in v[2])} for k, v in sorted(units.items())}
        print(slug, len(u))
        acts.append({'slug': slug, 'short': short, 'title': title, 'url': BASE + f + '.pdf', 'first_law': None, 'earlier_laws': [],
                     'versions': [{'from': FROM, 'source_url': BASE + f + '.pdf', 'sha256': hashlib.sha256(open(pdf, 'rb').read()).hexdigest(), 'units': u}]})
    corpus = {'country': {'code': 'US-WY', 'name': 'United States (Wyoming)', 'slug': 'united-states-wyoming', 'lang': 'en', 'tz': 'America/Denver', 'future_branch': 'future',
                          'publisher': {'name': 'Wyoming Legislative Service Office', 'email': 'lso@wyoleg.invalid'},
                          'default_in_force_rule': {'text': 'The Legislative Service Office publishes only the current text; each PDF carries its own modification date, 2026-05-08, which dates the single version.', 'source': 'https://wyoleg.gov/StateStatutes/StatutesDownload'},
                          'licence_note': 'Text-only statute PDFs from the Wyoming Legislative Service Office (wyoleg.gov). The annotated edition (LexisNexis) is not used.'},
              'sources': [{'name': 'Wyoming Statutes - Text Only (Legislative Service Office)', 'url': 'https://wyoleg.gov/StateStatutes/StatutesDownload', 'retrieved': '2026-10-30',
                           'licence': 'Statute text is not copyrightable (Georgia v. Public.Resource.Org, 2020). Only the LSO\'s text-only files are used; the LexisNexis annotations are not.', 'notes': 'wyoleg.gov has no robots.txt (404).'}],
              'laws': {'wy-lso-current': {'label': 'Legislative Service Office text-only edition, 8 May 2026', 'title': 'Wyoming Statutes (text only) and Constitution as published by the Legislative Service Office', 'kind': 'publisher',
                                          'enacted': FROM, 'published': FROM, 'url': 'https://wyoleg.gov/StateStatutes/StatutesDownload', 'temporary_until': None, 'restores': None, 'note': None}},
              'acts': acts, 'applies': [],
              'decisions': [f'Only the current text is online, so each act has one version, the oldest version available, dated {FROM} from the PDFs\' own modification date.',
                            'Scope: the Constitution and Titles 6 (Crimes and Offenses), 17 (Corporations, Partnerships and Associations) and 34 (Property, Conveyances and Security Transactions). Other titles are not included.',
                            'Chapter, article and title heading lines are dropped; section text is joined from the PDF\'s wrapped lines, one paragraph per blank-line block.'],
              'ai_use': ['none']}
    json.dump(corpus, open(os.path.join(HERE, 'corpus.json'), 'w', encoding='utf-8', newline='\n'), indent=1, ensure_ascii=False)

if __name__ == '__main__':
    main()
