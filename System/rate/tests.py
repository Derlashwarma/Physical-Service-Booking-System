from django.test import TestCase, Client
from django.urls import reverse
from register.models import CustomUser   
from job.models import Job, JobApplication
from rate.models import Rating

class RateUserTestCase(TestCase):
    def setUp(self):
        # Create users
        self.worker = CustomUser .objects.create(username="worker", is_worker=True)
        self.worker.set_password("password")
        self.worker.save()

        self.employer = CustomUser .objects.create(username="employer", is_worker=False)
        self.employer.set_password("password")
        self.employer.save()

        # Create a job and job application
        self.job = Job.objects.create(
            employer=self.employer, 
            rated=False,
            title="Sample Job",
            description="Description of the job.",
            budget=100.00,
            location="Location",
            date="2024-12-01",
            payment_method="cash",
            category="repair",
            schedule="fulltime"
        )
        
        # Create job application
        self.application = JobApplication.objects.create(
            job=self.job, 
            worker=self.worker, 
            rated=False, 
            status='completed'
        )

        self.job.is_done = True
        self.job.save()

        # Client setup
        self.client = Client()

    #blank ratings
    def test_rate_employer_invalid_submission(self):
        self.client.login(username="worker", password="password")
        url = reverse('rate:rate_user', args=[self.employer.username, self.job.id])
        
        response = self.client.post(url, data={})
  
        self.assertTemplateUsed(response, "rate_employer.html") 
        self.assertContains(response, "All fields are required")

    def test_rate_user_invalid_submission(self):
        self.client.login(username="employer", password="password")
        url = reverse('rate:rate_user', args=[self.worker.username, self.job.id])
        
        response = self.client.post(url, data={})
  
        self.assertTemplateUsed(response, "rate_user.html") 
        self.assertContains(response, "All fields are required")

    def test_rate_worker_valid(self):
        self.client.login(username="employer", password="password")
        url = reverse('rate:rate_user', args=[self.worker.username, self.job.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "rate_user.html")

        rating_data = {
            'timeliness_rating': 5,
            'professionalism_rating': 5,
            'communication_rating': 5,
            'review': 'Great worker!'
        }
        response = self.client.post(url,rating_data)

        self.assertRedirects(response, reverse('job:my_jobs', args=[self.job.id]))

    def test_rate_employer_valid(self):
        self.client.login(username="worker", password="password")
        url = reverse('rate:rate_user', args=[self.employer.username, self.job.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "rate_employer.html")

        rating_data = {
            'communication_rating': 5,
            'fairness_respect_rating': 5,
            'timeliness_payment_rating': 5,
            'review': 'Great employer!'
        }
        response = self.client.post(url, data=rating_data)

        self.assertRedirects(response, reverse('job:apply_job', args=[self.job.id]))


    def test_rate_employer_already_rated(self):
        self.client.login(username="worker", password="password")
        url = reverse('rate:rate_user', args=[self.employer.username, self.job.id])

        rating_data = {
            'communication_rating': 5,
            'fairness_respect_rating': 5,
            'timeliness_payment_rating': 5,
            'review': 'Great employer!'
        }
        response = self.client.post(url, data=rating_data)
        
        self.assertRedirects(response, reverse('job:apply_job', args=[self.job.id]))
        
        #submit it again
        response = self.client.post(url, data=rating_data)
        self.assertEqual(response.status_code, 405)

    def test_rate_worker_already_rated(self):
        self.client.login(username="employer", password="password")
        url = reverse('rate:rate_user', args=[self.worker.username, self.job.id])
        
        # First rating submission
        rating_data = {
            'timeliness_rating': 5,
            'professionalism_rating': 5,
            'communication_rating': 5,
            'review': 'Great worker!'
        }
        response = self.client.post(url, data=rating_data)
        self.assertRedirects(response, reverse('job:my_jobs', args=[self.job.id]))

        response = self.client.post(url, data=rating_data)
        self.assertEqual(response.status_code, 405)

    def test_no_job_found(self):
        self.client.login(username="employer", password="password")
        url = reverse('rate:rate_user', args=[self.worker.username, 10000])

        rating_data = {
            'timeliness_rating': 5,
            'professionalism_rating': 5,
            'communication_rating': 5,
            'review': 'Great worker!'
        }
        response = self.client.post(url, data=rating_data)
        self.assertEqual(response.status_code, 404)

    def test_no_user_found(self):
        self.client.login(username="employer", password="password")
        url = reverse('rate:rate_user', args=['user that does not exist', self.job.id])
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 404)