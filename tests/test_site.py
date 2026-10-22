"""Built-in content/rendering tests; run python -m unittest discover -s tests -v"""
import json
import sys
import unittest
import tempfile
from unittest.mock import patch
from copy import deepcopy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((ROOT/'content'/'site.json').read_text(encoding='utf-8'))
        build.build()

    def test_generated_pages_and_assets_exist(self):
        for f in ['index.html','404.html','assets/style.css','assets/main.js','assets/favicon.svg','assets/og-cover.png']:
            self.assertTrue((ROOT/'dist'/f).exists(),f)

    def test_all_menu_targets_exist(self):
        html=(ROOT/'dist'/'index.html').read_text(encoding='utf-8')
        for fragment in ['about','experience','projects','beyond','contact']:
            self.assertIn('id="'+fragment+'"',html)

    def test_no_fake_links_or_unprovided_cv(self):
        html=(ROOT/'dist'/'index.html').read_text(encoding='utf-8')
        self.assertNotIn('href=""',html)
        self.assertNotIn('mailto:',html)
        self.assertNotIn('Download CV',html)
        self.assertNotIn('<a class="project-open"',html)
        self.assertIn('Contact details will be added',html)

    def test_no_unpublished_project_page(self):
        for p in self.data['projects']:
            if not p['published']:
                self.assertFalse((ROOT/'dist'/'projects'/p['slug']).exists())

    def test_project_publishing_guard(self):
        data=deepcopy(self.data)
        data['projects'][0]['published']=True
        with self.assertRaisesRegex(ValueError,'Cannot publish'):
            build.validate(data)

    def test_published_case_study_is_generated(self):
        data=deepcopy(self.data)
        p=data['projects'][0]
        p.update(published=True, challenge='A real challenge', approach=['Real approach'],
                 decisions=[{'title': 'Choice', 'body': 'Trade-off'}],
                 outcomes='What happened', lessons='What I learned')
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'site.json'
            source.write_text(json.dumps(data), encoding='utf-8')
            output=Path(temp)/'dist'
            with patch.object(build, 'SOURCE', source), patch.object(build, 'DIST', output):
                build.build()
                project_page=output/'projects'/p['slug']/'index.html'
                self.assertTrue(project_page.exists())
                self.assertIn('Trade-off', project_page.read_text(encoding='utf-8'))
                self.assertIn('/projects/'+p['slug']+'/',(output/'index.html').read_text(encoding='utf-8'))

    def test_escaped_user_content(self):
        data=deepcopy(self.data)
        data['hero']['lead']='</p><script>alert(1)</script>'
        page=build.render_home(data)
        self.assertNotIn('<script>alert(1)</script>',page)
        self.assertIn('&lt;script&gt;',page)

    def test_complete_case_study_routes(self):
        data=deepcopy(self.data)
        p=data['projects'][0]
        p.update(published=True,challenge='A genuine issue',approach=['What I did'],decisions=[{'title':'Choice','body':'Trade-off'}],outcomes='Outcome',lessons='Lesson',stack=['SQL'])
        build.validate(data)
        html=build.render_case(data,p)
        self.assertIn('The challenge',html)
        self.assertIn('Decisions &amp; trade-offs',html)
        self.assertIn('SQL',html)

if __name__=='__main__':
    unittest.main()
