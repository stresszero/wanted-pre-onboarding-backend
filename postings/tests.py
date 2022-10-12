import json

from django.test import TestCase, Client

from .models import Country, Area, JobPosting
from companies.models import Company
from users.models import User, UserJobApplication


class JobPostingViewTest(TestCase):
    def setUp(self):
        Company.objects.create(name="원티드")
        Country.objects.create(name='한국')
        Area.objects.create(name='서울', country_id=1)
        JobPosting.objects.create(
            company_id=1,
            country_id=1,
            area_id=1,
            position='프론트엔드 개발자',
            reward=100000,
            tech="React",
            content="test content"
        )
        JobPosting.objects.create(
            company_id=1,
            country_id=1,
            area_id=1,
            position='백엔드 개발자',
            reward=1000000,
            tech="Django",
            content="test content"
        )
    
    def tearDown(self):
        Company.objects.all().delete()
        Country.objects.all().delete()
        Area.objects.all().delete()
        JobPosting.objects.all().delete()

    def test_success_get_job_posting(self):
        client = Client()
        response = client.get('/postings/1')
        result = {
            'posting_id'  : 1,
            'company_name': "원티드",
            'country_name': "한국",
            'area_name'   : "서울",
            'position'    : "프론트엔드 개발자",
            'reward'      : 100000,
            'tech'        : "React",
            'content'     : "test content",
            'posting_id_list_by_company': [1, 2]
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), result)
    
    def test_fail_get_job_posting(self):
        client = Client()
        response = client.get('/postings/3')
        self.assertEqual(response.status_code, 404)

    def test_fail_405_get_job_posting(self):
        client = Client()
        response = client.post('/postings/1')
        self.assertEqual(response.status_code, 405)

    def test_success_delete_job_posting(self):
        client = Client()
        response = client.delete('/postings/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Posting deleted'})
    
    def test_fail_delete_job_posting(self):
        client = Client()
        response = client.delete('/postings/3')
        self.assertEqual(response.status_code, 404)

    def test_success_patch_job_posting(self):
        client = Client()
        data = {
            'position': '프론트엔드 개발자',
            'reward': 500000,
            'tech': 'React',
            'content': 'test content'
        }
        response = client.patch('/postings/1', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Posting updated'})
    
    def test_fail_patch_job_posting(self):
        client = Client()
        data = {
            'position': '프론트엔드 개발자',
            'reward': 500000,
            'tech': 'React',
            'conten': 'test content'
        }
        response = client.patch('/postings/1', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Invalid input'})


class CreateJobPostingTest(TestCase):
    def setUp(self):
        JobPosting.objects.create(
            company_id=1,
            country_id=1,
            area_id=1,
            position='프론트엔드 개발자',
            reward=100000,
            tech="React",
            content="test content"
        )

    def tearDown(self):
        JobPosting.objects.all().delete()

    def test_success_create_job_posting(self):
        client = Client()
        data = {
            'company_id': 1,
            'country_id': 1,
            'area_id': 1,
            'position': '프론트엔드 개발자',
            'reward': 100000,
            'tech': "React",
            'content': "test content"
        }
        response = client.post('/postings', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'success'})

    def test_fail_405_create_job_posting(self):
        client = Client()
        data = {
            'company_id': 1,
            'country_id': 1,
            'area_id': 1,
            'position': '프론트엔드 개발자',
            'reward': 100000,
            'tech': "React",
            'content': "test content"
        }
        response = client.put('/postings', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'message': 'Method not allowed'})


class GetJobPostingsTest(TestCase):
    def setUp(self):
        Company.objects.create(name="원티드")
        Country.objects.create(name='한국')
        Area.objects.create(name='서울', country_id=1)
        JobPosting.objects.create(
            company_id=1,
            country_id=1,
            area_id=1,
            position='프론트엔드 개발자',
            reward=100000,
            tech="React",
            content="test content"
        )
        JobPosting.objects.create(
            company_id=1,
            country_id=1,
            area_id=1,
            position='백엔드 개발자',
            reward=1000000,
            tech="Django",
            content="test content"
        )
    
    def tearDown(self):
        Company.objects.all().delete()
        JobPosting.objects.all().delete()
        Area.objects.all().delete()
        Country.objects.all().delete()

    def test_success_get_job_postings(self):
        client = Client()
        response = client.get('/postings/list')
        results = [
            {
                'posting_id'  : 1,
                'company_name': "원티드",
                'country_name': "한국",
                'area_name'   : "서울",
                'position'    : "프론트엔드 개발자",
                'reward'      : 100000,
                'tech'        : "React",
            },
            {
                'posting_id'  : 2,
                'company_name': "원티드",
                'country_name': "한국",
                'area_name'   : "서울",
                'position'    : "백엔드 개발자",
                'reward'      : 1000000,
                'tech'        : "Django",
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), results)

    def test_success_get_job_postings_with_search(self):
        client = Client()
        response = client.get('/postings/list?search=django')
        results = [
            {
                'posting_id'  : 2,
                'company_name': "원티드",
                'country_name': "한국",
                'area_name'   : "서울",
                'position'    : "백엔드 개발자",
                'reward'      : 1000000,
                'tech'        : "Django",
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), results)

    def test_fail_405_get_job_postings(self):
        client = Client()
        response = client.post('/postings/list')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'message': 'Method not allowed'})


class UserJobApplyTest(TestCase):
    def setUp(self):
        Company.objects.create(name="원티드")
        Country.objects.create(name='한국')
        Area.objects.create(name='서울', country_id=1)
        JobPosting.objects.create(
            company_id=1,
            country_id=1,
            area_id=1,
            position='프론트엔드 개발자',
            reward=100000,
            tech="React",
            content="test content"
        )
        JobPosting.objects.create(
            company_id=1,
            country_id=1,
            area_id=1,
            position='백엔드 개발자',
            reward=1000000,
            tech="Django",
            content="test content"
        )
        User.objects.create(name="세영")
        UserJobApplication.objects.create(user_id=1, job_posting_id=1)
    
    def tearDown(self):
        Company.objects.all().delete()
        JobPosting.objects.all().delete()
        Area.objects.all().delete()
        Country.objects.all().delete()
        User.objects.all().delete()
        UserJobApplication.objects.all().delete()

    def test_success_user_job_apply(self):
        client = Client()
        data = {
            'user_id': 1,
            'posting_id': 2
        }
        response = client.post('/postings/2/apply', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'success'})

    def test_fail_405_user_job_apply(self):
        client = Client()
        data = {
            'user_id': 1,
            'posting_id': 2
        }
        response = client.put('/postings/2/apply', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'message': 'Method not allowed'})

    def test_fail_400_user_job_apply(self):
        client = Client()
        data = {
            'user_id': 1,
            'posting_id': 1
        }
        response = client.post('/postings/1/apply', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'You have already applied for this job'})

