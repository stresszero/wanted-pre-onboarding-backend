import json

from django.test import TestCase, Client

from .models import Country, Area, JobPosting


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
        Country.objects.create(name='한국')
        Area.objects.create(name='서울')
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
        Area.objects.all().delete()
        Country.objects.all().delete()