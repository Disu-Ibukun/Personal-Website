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
        self.assertIn('mailto:disuibukun00@gmail.com',html)
        self.assertIn('tel:+2347061027312',html)
        self.assertNotIn('Download CV',html)
        self.assertIn('class="project-open"',html)
        self.assertNotIn('Thrift by Parrots',html)
        self.assertIn('Rhodium Solicitors and Advocates',html)

    def test_about_education_and_new_portrait(self):
        html=(ROOT/'dist'/'index.html').read_text(encoding='utf-8')
        self.assertIn('src="/assets/portrait.webp"', html)
        self.assertTrue((ROOT/'dist'/'assets'/'portrait.webp').exists())
        self.assertIn("Hello, I'm Disu Ibukunoluwa.", self.data['about']['heading'])
        self.assertIn('Technology has always fascinated me', html)
        self.assertIn('reliable data pipelines', html)

    def test_no_unpublished_project_page(self):
        for p in self.data['projects']:
            if not p['published']:
                self.assertFalse((ROOT/'dist'/'projects'/p['slug']).exists())

    def test_project_publishing_guard(self):
        data=deepcopy(self.data)
        data['projects'][0].update(published=True, outcomes='')
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

    def test_marketing_platform_case_study(self):
        path = ROOT / 'dist' / 'projects' / 'marketing-data-platform-databricks-dbt' / 'index.html'
        self.assertTrue(path.exists())
        page = path.read_text(encoding='utf-8')
        for phrase in ('Databricks', 'Snapchat Ads', 'Elementary', 'Unity Catalog',
                       'The unified data product', 'Data quality and observability',
                       'Environments, security and delivery', 'Service Principal',
                       'Outcomes', 'Metrics and business definitions'):
            self.assertIn(phrase, page)
        self.assertIn('href="/projects/marketing-data-platform-databricks-dbt/"',
                      (ROOT / 'dist' / 'index.html').read_text(encoding='utf-8'))

    def test_requested_content_updates(self):
        html = (ROOT/'dist'/'index.html').read_text(encoding='utf-8')
        self.assertIn('>Core toolkit<small>Python', html)
        self.assertNotIn('Experience at Quidax', html)
        self.assertIn('Computer Systems Engineering', html)
        self.assertIn('Rhodium Solicitors and Advocates', html)
        self.assertIn('Docker', html)
        self.assertIn('Airbyte', html)
        self.assertIn('BigQuery', html)
        self.assertIn('4.65/5.0', html)
        self.assertIn('pipeline-visual', html)
        self.assertLess(html.index('id="projects"'), html.index('id="beyond"'))
        self.assertLess(html.index('id="skills"'), html.index('id="entrepreneurship"'))
        detail = (ROOT/'dist'/'projects'/'cryptocurrency-price-data-pipeline'/'index.html').read_text(encoding='utf-8')
        for term in ('CoinMarketCap', 'PostgreSQL', 'GitHub Actions', '0 0 1 * *',
                     'CSV', 'crypto_dag'):
            self.assertIn(term, detail)

    def test_portfolio_refresh(self):
        html=(ROOT/'dist'/'index.html').read_text(encoding='utf-8')
        self.assertNotIn('Selected work &amp; experience', html)
        self.assertIn('id="certifications"', html)
        self.assertIn('Agentic AI and AI Agents', html)
        self.assertIn('Prompt Engineering Course', html)
        self.assertIn('ClickHouse Certified Developer', html)
        self.assertIn('AML detection for cryptocurrency transactions', html)
        self.assertIn('96.65%', html)
        self.assertIn('0.9315', html)
        self.assertIn('href="/projects/aml-cryptocurrency-transaction-detection/"', html)
        detail=(ROOT/'dist'/'projects'/'aml-cryptocurrency-transaction-detection'/'index.html').read_text(encoding='utf-8')
        for term in ('Elliptic++', 'Random Forest', 'XGBoost', 'Logistic Regression', 'Render', 'T4 GPU'):
            self.assertIn(term, detail)

    def test_business_instagram_links_and_personal_note(self):
        html=(ROOT/'dist'/'index.html').read_text(encoding='utf-8')
        self.assertIn('https://www.instagram.com/thriftbycaret/', html)
        self.assertIn('https://www.instagram.com/bookcart.ng/', html)
        self.assertEqual(html.count('class="business business-link"'), 2)
        self.assertEqual(html.count('View on Instagram'), 2)
        self.assertIn('reading fiction, public speaking and debate, and exploring Lagos', html)
        self.assertIn('rel="noopener noreferrer" aria-label="Visit thriftbycaret on Instagram"', html)

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
