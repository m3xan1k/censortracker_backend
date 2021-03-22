from django.test import TestCase

from server.apps.api.management.commands.update_ip_data import blocked_domains, hash_case_data
from server.apps.api.models import Domain, Case


class CheckBlockedTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create domains
        domains = Domain.objects.bulk_create(
            [Domain(domain=f'example_{n}.com') for n in range(3)]
        )

        # create cases
        providers = ['mts', 'megafon', 'beeline', 'tele2']
        regions = ['msk', 'spb', 'ekt', 'krd']
        ip_addresses = ['1.1.1.1', '2.2.2.2', '3.3.3.3']

        # multiple reports for single domain from one client
        for i in range(3):
            case = Case.objects.create(
                domain=domains[0],
                client_ip=ip_addresses[0],
                client_provider=providers[0],
                client_region=regions[0]
            )
            hash_case_data(case)

    def test_multiple(self):
        domains = blocked_domains()
        self.assertFalse('example_0.com' not in domains)
