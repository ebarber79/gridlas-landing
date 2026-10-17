from pathlib import Path
import os
import json
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
BASE_REF = os.environ.get('GRIDLAS_BASE_REF', 'origin/main')

class EstimatorScope(unittest.TestCase):
    def test_estimator_markup_and_metadata_do_not_promise_connection_times(self):
        s=(ROOT/'tools/data-center-estimator/index.html').read_text(encoding='utf-8')
        self.assertNotIn('grid wait',s.lower())
        self.assertNotIn('interconnection wait',s.lower())
        self.assertNotIn('Time to power</div>',s)
        self.assertNotIn('whether the grid can deliver it',s)
        self.assertIn('Connection timing is not estimated',s)
        self.assertIn('generation and storage',s)
        self.assertIn('https://eta-publications.lbl.gov/sites/default/files/2026-06/queued_up_2026_edition.pdf',s)
        self.assertNotRegex(s,r"\bwait\s*:|m\.wait")
    def test_inbound_tool_promotions_do_not_promise_grid_waits(self):
        for name in ['404.html','data-centers/index.html']:
            self.assertNotIn('grid wait',(ROOT/name).read_text(encoding='utf-8').lower())
    def test_feed_and_machine_readable_summary_scope_the_statistic(self):
        for name in ['feed.xml','llms.txt']:
            s=(ROOT/name).read_text(encoding='utf-8')
            self.assertNotIn('grid wait',s.lower())
            self.assertIn('generation and storage',s)
            self.assertIn('not a data-center connection',s)
    def test_launch_draft_does_not_reintroduce_ratio_or_load_wait(self):
        s=(ROOT/'LAUNCH-POSTS.md').read_text(encoding='utf-8')
        self.assertNotIn('3.5×',s)
        self.assertNotIn('and a 4.5-year wait',s)
        self.assertIn('generation and storage',s)
        self.assertIn('not ready to publish',s)
    def test_all_repository_jsonld_parses(self):
        count=0
        for p in ROOT.rglob('*.html'):
            if '.git' in p.parts:continue
            for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',p.read_text(encoding='utf-8'),re.S):
                json.loads(s);count+=1
        self.assertGreater(count,0)
        print('JSON-LD blocks parsed:',count)

if __name__=='__main__': unittest.main(verbosity=2)
