from django.test import TestCase

from server.apps.api.management.commands.update_ip_data import blocked_domains, update_ip_data
from server.apps.api.models import Domain, Case


class CheckBlockedTest(TestCase):

    @classmethod
    def setUp(self):
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
            Case.objects.create(
                domain=domains[0],
                client_ip=ip_addresses[0],
                client_provider=providers[0],
                client_region=regions[0]
            )

        # reports from multiple users
        for i in range(2):
            Case.objects.create(
                domain=domains[1],
                client_ip=ip_addresses[i],
                client_provider=providers[i],
                client_region=regions[i]
            )

        # hash cases
        update_ip_data()

    def tearDown(self):
        # clean db
        Domain.objects.all().delete()

    def test_multiple_from_single_client(self):
        domains = blocked_domains()
        self.assertFalse('example_0.com' in domains)

    def test_single_domain_from_multiple_clients(self):
        domains = blocked_domains()
        self.assertTrue('example_1.com' in domains)
