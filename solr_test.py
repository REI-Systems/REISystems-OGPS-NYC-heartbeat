import pysolr
import unittest


# http://sdw5.reisys.com:18983/solr/checkbook_nycha_dev.public.solr_nycha/select/?q=*:*&facet=true&facet.mincount=1&facet.sort=count&facet.limit=30&facet.field=domain&start=0&rows=0&sort=domain_ordering+asc%2Cdate_ordering+desc&wt=xml


class TestNychaSolr(unittest.TestCase):

    def setUp(self) -> None:
        solr_server = 'http://sdw5.reisys.com:18983/solr/'
        self._solr_nycha = pysolr.Solr(solr_server+'checkbook_nycha_dev.public.solr_nycha/')

    def tearDown(self) -> None:
        self._solr_nycha.get_session().close()

    def test_nycha_domains(self):
        results = self._solr_nycha.search('*:*', **{
            'facet': 'true',
            'facet.mincount': 1,
            'facet.field': 'domain',
            'rows': 0
        })

        self.assertTrue('contracts' in results.facets['facet_fields']['domain'], 'Contracts records not found in NYCHA')
        self.assertTrue('payroll' in results.facets['facet_fields']['domain'], 'Payroll records not found in NYCHA')


if __name__ == '__main__':
    unittest.main()
