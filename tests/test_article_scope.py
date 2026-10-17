from pathlib import Path
import os
import re,json,html,subprocess,unittest
ROOT = Path(__file__).resolve().parents[1]
BASE_REF = os.environ.get('GRIDLAS_BASE_REF', 'origin/main')
FILES=['grid-bottleneck/index.html','powering-around-the-queue/index.html','glossary/index.html']
PRIMARY='https://eta-publications.lbl.gov/sites/default/files/2026-06/queued_up_2026_edition.pdf'
def read(n):return (ROOT/n).read_text(encoding='utf-8')
def schemas(s):return [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)]
def plain(s):return html.unescape(re.sub('<[^>]+>','',s)).strip()
class Articles(unittest.TestCase):
 def test_scope_note_and_source_on_each_page(self):
  for n in FILES:
   with self.subTest(page=n):
    s=read(n);self.assertIn('id="queue-scope"',s);self.assertIn(PRIMARY,s);self.assertIn('excludes large-load queues',s)
 def test_grid_metadata_names_generation_not_load_wait(self):
  s=read(FILES[0]); metas=re.findall(r'<meta [^>]*description[^>]*content="([^"]*)"',s)
  self.assertEqual(len(metas),3)
  for x in metas:self.assertIn('generation and storage',x)
 def test_no_unqualified_bypass_or_five_year_load_claims(self):
  forbidden=['is a five-year line','The five-year wait created','A new grid interconnection now takes','skip the queue entirely','skip the interconnection queue entirely','opts out of the queue','around the five-year grid queue','routing around the queue entirely']
  for n in FILES:
   for phrase in forbidden:self.assertNotIn(phrase,read(n),n)
 def test_workaround_chart_discloses_incompatible_clocks(self):
  s=read(FILES[1]);self.assertIn('not directly comparable',s);self.assertIn('Generation cohort',s);self.assertNotIn('New grid interconnection: ~5-year median wait',s)
 def test_article_faqs_exactly_match_visible_text(self):
  for n in FILES[:2]:
   s=read(n);visible=[(plain(q),plain(a)) for q,a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>',s,re.S)]
   schema=next(x for x in schemas(s) if x.get('@type')=='FAQPage')
   structured=[(x['name'],x['acceptedAnswer']['text']) for x in schema['mainEntity']]
   self.assertTrue(visible);self.assertEqual(visible,structured,n)
 def test_glossary_terms_exactly_match_visible_text(self):
  s=read(FILES[2]); terms=next(x for x in schemas(s) if x.get('@type')=='DefinedTermSet')['hasDefinedTerm']
  visible={i:(plain(n),plain(p)) for i,n,p in re.findall(r'<div class="gterm" id="([^"]+)">\s*<h2>(.*?)</h2>\s*<p>(.*?)</p>',s,re.S)}
  self.assertEqual(len(terms),len(visible))
  for t in terms:self.assertEqual((t['name'],t['description']),visible[t['@id'].split('#')[-1]])
 def test_smr_definition_does_not_guarantee_grid_bypass(self):
  s=read(FILES[2]);self.assertNotIn('without waiting on the grid',s)
  terms=next(x for x in schemas(s) if x.get('@type')=='DefinedTermSet')['hasDefinedTerm']
  definition=next(t['description'] for t in terms if t['@id'].endswith('#smr'))
  self.assertIn('licensing',definition)
  self.assertIn('utility coordination',definition)
 def test_forms_styles_and_executable_scripts_preserved(self):
  for n in FILES:
   before=subprocess.check_output(['git','-C',str(ROOT),'show',BASE_REF+':'+n],text=True, encoding='utf-8');after=read(n)
   for pattern in [r'<form\b.*?</form>',r'<style>.*?</style>',r'<script(?! type="application/ld\+json")[^>]*>.*?</script>']:
    self.assertEqual(re.findall(pattern,before,re.S),re.findall(pattern,after,re.S),n)
if __name__=='__main__':unittest.main(verbosity=2)
