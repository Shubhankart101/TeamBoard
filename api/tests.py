from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Company, KBEntry, QueryLog


class TeamBoardAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Seed KB entries
        self.kb1 = KBEntry.objects.create(
            question="What is select_related in Django ORM?",
            answer="select_related performs a SQL JOIN and fetches related objects.",
            category=KBEntry.Category.DATABASE
        )
        self.kb2 = KBEntry.objects.create(
            question="How to use transaction.atomic()?",
            answer="transaction.atomic() creates a database transaction block.",
            category=KBEntry.Category.DATABASE
        )

    def test_swagger_and_schema_endpoints(self):
        # Schema endpoint
        response = self.client.get('/api/schema/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Swagger UI endpoint
        response_docs = self.client.get('/api/docs/')
        self.assertEqual(response_docs.status_code, status.HTTP_200_OK)

    def test_model_str_methods(self):
        user = User.objects.create_user(username='struser', password='password123')
        company = user.company
        company.company_name = 'Str Company'
        company.save()
        log = QueryLog.objects.create(company=company, search_term='test', results_count=5)

        self.assertIn('Str Company', str(company))
        self.assertEqual(str(self.kb1), "What is select_related in Django ORM?")
        self.assertIn("searched 'test'", str(log))

    def test_01_register_new_company(self):
        url = '/api/auth/register/'
        payload = {
            'username': 'acmecorp',
            'password': 'securepass123',
            'company_name': 'Acme Corp',
            'email': 'dev@acmecorp.com'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('api_key', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['username'], 'acmecorp')
        self.assertEqual(response.data['company_name'], 'Acme Corp')

        # Check company profile was created via signal and updated
        user = User.objects.get(username='acmecorp')
        self.assertTrue(hasattr(user, 'company'))
        self.assertEqual(user.company.company_name, 'Acme Corp')
        self.assertEqual(user.company.role, Company.Role.CLIENT)
        self.assertTrue(len(user.company.api_key) > 0)

    def test_register_missing_fields(self):
        url = '/api/auth/register/'
        payload = {'username': 'incomplete'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_02_register_duplicate_username(self):
        User.objects.create_user(username='acmecorp', password='password123')
        url = '/api/auth/register/'
        payload = {
            'username': 'acmecorp',
            'password': 'newpassword123',
            'company_name': 'Acme Corp Duplicate',
            'email': 'dev2@acmecorp.com'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_03_login_valid_credentials(self):
        user = User.objects.create_user(username='acmecorp', password='securepass123')
        company = user.company
        company.company_name = 'Acme Corp'
        company.save()

        url = '/api/auth/login/'
        payload = {
            'username': 'acmecorp',
            'password': 'securepass123'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['company_name'], 'Acme Corp')
        self.assertEqual(response.data['api_key'], company.api_key)

    def test_login_missing_fields(self):
        url = '/api/auth/login/'
        payload = {'username': 'onlyusername'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_04_login_wrong_password(self):
        User.objects.create_user(username='acmecorp', password='securepass123')
        url = '/api/auth/login/'
        payload = {
            'username': 'acmecorp',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_05_query_kb_no_token(self):
        url = '/api/kb/query/'
        payload = {'search': 'select_related'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_06_query_kb_valid_token_with_results(self):
        user = User.objects.create_user(username='acmecorp', password='securepass123')
        company = user.company

        # Login to get JWT
        login_res = self.client.post('/api/auth/login/', {'username': 'acmecorp', 'password': 'securepass123'}, format='json')
        token = login_res.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = '/api/kb/query/'
        payload = {'search': 'select_related'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.kb1.id)

        # Verify QueryLog was created
        self.assertEqual(QueryLog.objects.count(), 1)
        log = QueryLog.objects.first()
        self.assertEqual(log.company, company)
        self.assertEqual(log.search_term, 'select_related')
        self.assertEqual(log.results_count, 1)

    def test_07_query_kb_valid_token_no_matching_results(self):
        user = User.objects.create_user(username='acmecorp', password='securepass123')
        login_res = self.client.post('/api/auth/login/', {'username': 'acmecorp', 'password': 'securepass123'}, format='json')
        token = login_res.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = '/api/kb/query/'
        payload = {'search': 'nonexistentterm12345'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

        # Verify QueryLog was still created
        self.assertEqual(QueryLog.objects.count(), 1)
        log = QueryLog.objects.first()
        self.assertEqual(log.results_count, 0)

    def test_08_query_kb_missing_search_field(self):
        user = User.objects.create_user(username='acmecorp', password='securepass123')
        login_res = self.client.post('/api/auth/login/', {'username': 'acmecorp', 'password': 'securepass123'}, format='json')
        token = login_res.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = '/api/kb/query/'
        payload = {}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_query_kb_user_without_company(self):
        user = User.objects.create_user(username='nocompanyuser', password='securepass123')
        Company.objects.filter(user=user).delete()

        login_res = self.client.post('/api/auth/login/', {'username': 'nocompanyuser', 'password': 'securepass123'}, format='json')
        token = login_res.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = '/api/kb/query/'
        payload = {'search': 'test'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_09_usage_summary_client_token(self):
        user = User.objects.create_user(username='clientuser', password='securepass123')
        # Role defaults to CLIENT
        login_res = self.client.post('/api/auth/login/', {'username': 'clientuser', 'password': 'securepass123'}, format='json')
        token = login_res.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = '/api/admin/usage-summary/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_10_usage_summary_admin_token(self):
        user = User.objects.create_user(username='adminuser', password='securepass123')
        company = user.company
        company.role = Company.Role.ADMIN
        company.save()

        # Log some queries
        QueryLog.objects.create(company=company, search_term='select_related', results_count=2)
        QueryLog.objects.create(company=company, search_term='select_related', results_count=2)
        QueryLog.objects.create(company=company, search_term='transaction.atomic', results_count=1)

        login_res = self.client.post('/api/auth/login/', {'username': 'adminuser', 'password': 'securepass123'}, format='json')
        token = login_res.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = '/api/admin/usage-summary/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_queries'], 3)
        self.assertEqual(response.data['active_companies'], 1)
        self.assertEqual(len(response.data['top_search_terms']), 2)
        self.assertEqual(response.data['top_search_terms'][0]['search_term'], 'select_related')
        self.assertEqual(response.data['top_search_terms'][0]['count'], 2)
