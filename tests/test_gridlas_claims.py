import json
from pathlib import Path
import os
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE_REF = os.environ.get('GRIDLAS_BASE_REF', 'origin/main')
PRIMARY = 'https://eta-publications.lbl.gov/sites/default/files/2026-06/queued_up_2026_edition.pdf'

def text(name):
    return (ROOT / name).read_text(encoding='utf-8')

def original(name):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', BASE_REF + ':' + name], text=True, encoding='utf-8')

def schemas(name):
    return [json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text(name), re.S)]

class Claims(unittest.TestCase):
    def test_home_schema_names_generation_cohort(self):
        obs = next(o for s in schemas('index.html') if s.get('@type') == 'ItemList' for o in s['itemListElement'] if o.get('unitText') == 'years')
        self.assertIn('generation', obs['name'].lower())
        self.assertIn('not a data-center connection-time estimate', obs['description'])

    def test_home_headline_is_generation_not_typical_load_wait(self):
        home = text('index.html')
        self.assertNotIn('typical interconnection wait</div>', home)
        self.assertIn('generation projects completed in 2025', home)

    def test_home_share_metadata_scopes_wait_statistic(self):
        self.assertNotIn('~5-year grid interconnection wait', text('index.html'))

    def test_home_faq_rejects_national_load_wait_inference(self):
        faq = next(s for s in schemas('index.html') if s.get('@type') == 'FAQPage')
        answer = next(q['acceptedAnswer']['text'] for q in faq['mainEntity'] if 'interconnection' in q['name'])
        self.assertIn('not a national data-center connection wait', answer)

    def test_findings_faq_schema_matches_visible_corrected_answer(self):
        faq = next(s for s in schemas('findings.html') if s.get('@type') == 'FAQPage')
        answer = next(q['acceptedAnswer']['text'] for q in faq['mainEntity'] if 'connect a data center' in q['name'])
        self.assertIn('not data-center connection times', answer)
        self.assertIn('<p>' + answer + '</p>', text('findings.html'))

    def test_unsupported_secondary_market_ratio_removed(self):
        self.assertNotIn('3.5× every secondary U.S. market combined', text('findings.html'))

    def test_home_plant_count_has_threshold_each_time(self):
        occurrences = re.findall(r'2,459[^<]*', text('index.html'))
        self.assertEqual(len(occurrences), 2)
        for occurrence in occurrences:
            self.assertIn('≥100 MW', occurrence)

    def test_direct_report_link_and_data_vintage_note(self):
        for name in ('index.html', 'findings.html'):
            self.assertIn('href="' + PRIMARY + '"', text(name))
        self.assertIn('id="data-scope"', text('findings.html'))
        self.assertIn('Individual charts retain their stated observation dates', text('findings.html'))

    def test_alternatives_card_does_not_imply_five_year_load_wait(self):
        home = text('index.html')
        self.assertNotIn('routes around the 5-year wait', home)
        self.assertIn('alternatives to grid-connection constraints', home)

    def test_generation_queue_composition_is_explicitly_separate(self):
        home = text('index.html')
        self.assertNotIn("The queue's composition is shifting to match", home)
        self.assertIn("Separately, the generation and storage queue's composition is shifting", home)

    def test_forms_scripts_purchase_links_preserved(self):
        for name in ('index.html', 'findings.html'):
            before = re.sub(r'<!--.*?-->', '', original(name), flags=re.S)
            after = re.sub(r'<!--.*?-->', '', text(name), flags=re.S)
            for pattern in (r'<form\b.*?</form>', r'<script(?! type="application/ld\+json").*?</script>', r'<a\b[^>]*href="[^"]*(?:shopify|cart)[^"]*"[^>]*>.*?</a>'):
                self.assertEqual(re.findall(pattern, before, re.S), re.findall(pattern, after, re.S))

if __name__ == '__main__':
    unittest.main(verbosity=2)
