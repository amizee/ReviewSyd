from .models import Tutor, UoSComment, LocationReviews, Locations, UoS
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase, RequestFactory, Client
from myapp.models import User, PasswordResetToken
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from myapp.models import UserProfile 
from myapp.forms import EmailForm
from .views import logout_view, send_feedback_email
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from myapp.views import verification_codes
from django.contrib.auth import get_user
from django.contrib import messages
from django.utils import timezone
from unittest.mock import patch
from django.urls import reverse
from django.core import mail
from django import forms
import random
import json
# import mock

class HomePageTest(TestCase):
    def setUp(self):
        # Login user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.loc1 = Locations.objects.create(name="Fisher Library")

    def test_map_redirect(self):
        url = reverse('location list') 
        response = self.client.get(url)

        # Check if the response contains the anchor link
        self.assertContains(response, 'href="{0}"'.format(reverse('locationsMap')))

        # Extract the URL from the anchor link's `href` attribute.
        anchor_url = response.content.decode() 

        # Check if the anchor link redirects to the correct URL.
        self.assertIn(reverse('locationsMap'), anchor_url) 

    def test_location_redirect(self):
        url = reverse('location list')
        response = self.client.get(url)

        # Check that the response does not contain a link to the location page since it is misspelt
        expected_url = reverse('location', args=["Fisher Librar"])
        self.assertNotContains(response, 'href="{0}"'.format(expected_url))

        # Now the spelling is correct
        expected_url = reverse('location', args=["Fisher Library"])
        self.assertContains(response, 'href="{0}"'.format(expected_url))

        # Simulate clicking the link
        response = self.client.get(expected_url)

        # Check if the response status code is 200, indicating a successful redirection
        self.assertEqual(response.status_code, 200)
        

class LocationsMapViewTest(TestCase):
    def test_map_view_renders_map_template(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Issue a GET request using the Django test client
        response = self.client.get(reverse('locationsMap'), {'navbar': 'locationsMap'})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template was used
        self.assertTemplateUsed(response, 'locationsMap.html')

        
class HelpViewTest(TestCase):
    def test_help_view_renders_help_template(self):
        # Issue a GET request using the Django test client
        response = self.client.get(reverse('help'))
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template was used
        self.assertTemplateUsed(response, 'help.html')


class FeedbackViewTest(TestCase):
    def test_feedback_view_renders_feedback_template(self):
        # Issue a GET request using the Django test client
        response = self.client.get(reverse('feedback'))

        # Check that the correct template was used
        self.assertTemplateUsed(response, 'feedback.html')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)


class PrivacyViewTest(TestCase):
    def test_feedback_view_renders_feedback_template(self):
        # Issue a GET request using the Django test client
        response = self.client.get(reverse('privacy'))

        # Check that the correct template was used
        self.assertTemplateUsed(response, 'privacy.html')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)


class TermsAndConditionsTest(TestCase):
    def test_terms_and_conditions_view_renders_ts_template(self):
        # Issue a GET request using the Django test client
        response = self.client.get(reverse('terms and conditions'))

        # Check that the correct template was used
        self.assertTemplateUsed(response, 'ts.html')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):
    def setUp(self):
        # Create an instance of RequestFactory to build request objects
        self.factory = RequestFactory()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_logout_view(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Create a GET request to the logout view
        request = self.factory.get('/logout/')
        # Attach the test user to the request
        request.user = self.user

        # Add session to the request
        request.session = self.client.session

        # Call the logout view
        response = logout_view(request)

        # Check if the user is logged out
        self.assertFalse(request.user.is_authenticated)

        # Check if the response is a successful redirect
        self.assertEqual(response.status_code, 302)
        # Check if the user is redirected to the login page
        self.assertEqual(response.url, '/login/')


class SendFeedbackEmailTest(TestCase):
    def setUp(self):
        # Create an instance of RequestFactory
        self.factory = RequestFactory()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_send_feedback_email(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Create POST data for the feedback form
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        # Create a POST request to the send feedback email view
        request = self.factory.post('/send_feedback_email/', data)
        # Attach the test user to the request
        request.user = self.user

        # Add session and messages to the request
        request.session = self.client.session
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Call the send feedback email view
        response = send_feedback_email(request)

        # Check if an email has been sent
        self.assertEqual(len(mail.outbox), 1)
        # Check the subject of the sent email
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
        # Check the content of the sent email
        self.assertIn('Message from Test User', mail.outbox[0].body)
        self.assertIn('test@example.com', mail.outbox[0].body)
        self.assertIn('Test Message', mail.outbox[0].body)

        # Check if the success message has been added
        messages_list = [str(message) for message in get_messages(request)]
        self.assertIn('Your feedback has been sent!', messages_list)

        # Check if the response is a successful redirect
        self.assertEqual(response.status_code, 302)
        # Check if the user is redirected to the feedback page
        self.assertEqual(response.url, '/feedback/')




class FindTutorTest(TestCase):
    def setUp(self):
        # Creating a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Creating tutors
        self.tutor1 = Tutor.objects.create(user=self.user, name='Test Tutor 1', subject='Math', email='test1@example.com')
        self.tutor2 = Tutor.objects.create(user=self.user, name='Test Tutor 2', subject='Physics', email='test2@example.com')

        # Logging in the user
        self.client.login(username='testuser', password='testpassword')

    def test_find_tutor_with_search(self):
        # Making a GET request to findTutor view with a search query
        response = self.client.get(reverse('findTutor'), {'search': 'Test Tutor 1'})

        # Getting the expected result using values_list method
        expected_result = Tutor.objects.filter(name__icontains='Test Tutor 1').values_list('name', flat=True)

        # Getting the paginator object
        paginator = Paginator(Tutor.objects.filter(name__icontains='Test Tutor 1'), 9)

        # Comparing the results
        self.assertQuerysetEqual(response.context['tutors'], expected_result, transform=lambda x: x.name)
        self.assertEqual(response.context['paginator'].num_pages, paginator.num_pages)
        self.assertEqual(response.context['page'], 1)
        self.assertEqual(response.status_code, 200)


class AddTutorTest(TestCase):
    def setUp(self):
        # Create a client to issue POST requests
        self.client = Client()
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_tutor(self):
        # Issue a POST request to add a tutor
        data = {
            'name': 'Test Tutor',
            'subject': 'Test Subject',
            'email': 'test@example.com',
            'description': 'Test Description'
        }
        response = self.client.post(reverse('add_tutor'), data)
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Check that the tutor was added to the database
        self.assertEqual(Tutor.objects.count(), 1)
        # Check that the tutor's attributes are correct
        tutor = Tutor.objects.first()
        self.assertEqual(tutor.name, 'Test Tutor')
        self.assertEqual(tutor.subject, 'Test Subject')
        self.assertEqual(tutor.email, 'test@example.com')
        self.assertEqual(tutor.description, 'Test Description')


class RemoveTutorTest(TestCase):
    def setUp(self):
        # Create a client to issue POST requests
        self.client = Client()
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        # Create a tutor object for testing
        self.tutor = Tutor.objects.create(user=self.user, name='Test Tutor', subject='Test Subject', email='test@example.com')

    def test_remove_tutor(self):
        # Issue a POST request to remove the tutor
        response = self.client.post(reverse('remove_tutor', args=[self.tutor.id]))
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Check that the tutor was removed from the database
        self.assertEqual(Tutor.objects.count(), 0)


class AccountSettingsViewTest(TestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create instances of Tutor, UoS, UoSComment, Locations, and LocationReviews
        self.tutor = Tutor.objects.create(user=self.user, name='Test Tutor', subject='Math', email='test@example.com')
        
        self.uos = UoS.objects.create(code='MATH101', name='Intro to Math')
        self.uos_comment = UoSComment.objects.create(user=self.user, comment='Great Course!', uos=self.uos)
        
        self.location = Locations.objects.create(name='Library', location='Main St')
        self.location_review = LocationReviews.objects.create(user=self.user, writtenReview='Quiet place', location=self.location)

    def test_account_settings_view(self):
        # Send GET request to the account settings page
        response = self.client.get(reverse('accountSettings'))

        # Check if the status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the view is using the correct template
        self.assertTemplateUsed(response, 'accountSettings.html')

        # Check if the context data is correct
        self.assertEqual(response.context['current_user'], self.user)
        self.assertEqual(list(response.context['user_tutors']), [self.tutor])
        self.assertEqual(list(response.context['user_uos_comments']), [self.uos_comment])
        self.assertEqual(list(response.context['user_location_reviews']), [self.location_review])


class PasswordUpdateTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='old_password')
        # Initialize the Django test client
        self.client = Client()
        # Log the user in
        self.client.login(username='testuser', password='old_password')

    def test_update_password(self):
        # Define the URL for the update_password view
        url = reverse('update_password')
        # Send a POST request to update the password
        response = self.client.post(url, {'new_password': 'new_password'})
        # Check if the password was updated successfully
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"success": True, "message": "Password updated successfully!"})
        # Check if the user is still logged in after changing the password
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_verify_current_password(self):
        # Define the URL for the verify_current_password view
        url = reverse('verify_current_password')
        # Send a POST request with the correct current password
        response = self.client.post(url, {'current_password': 'old_password'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"is_correct": True})
        # Send a POST request with an incorrect current password
        response = self.client.post(url, {'current_password': 'wrong_password'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {"is_correct": False, "message": "Incorrect current password."})


class NameUpdateTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='test_password', first_name='Old', last_name='Name')
        # Initialize the Django test client
        self.client = Client()
        # Log the user in
        self.client.login(username='testuser', password='test_password')

    def test_update_name(self):
        # Define the URL for the update_name view
        url = reverse('updateName')
        # Data to be sent in POST request
        data = {
            'first_name': 'New',
            'last_name': 'Name'
        }
        # Send a POST request to update the name
        response = self.client.post(url, data)
        # Check if the name was updated successfully
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"success": True, "message": "Name updated successfully!"})
        # Fetch the updated user from the database
        updated_user = User.objects.get(username='testuser')
        # Check if the first name and last name have been updated correctly
        self.assertEqual(updated_user.first_name, 'New')
        self.assertEqual(updated_user.last_name, 'Name')

    def test_invalid_request(self):
        # Define the URL for the update_name view
        url = reverse('updateName')
        # Send a GET request (which is invalid for this view)
        response = self.client.get(url)
        # Check if the response indicates an invalid request
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {"success": False, "message": "Invalid request"})




class LoginViewTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test@example.com', email='test@example.com', password='testpassword')
        self.url = reverse('login_view')  # Make sure 'login' is the correct name for your login URL pattern

    def test_login_success(self):
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

    def test_login_failure(self):
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'Invalid email or password'})
    
    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')



User = get_user_model()

class SignupViewTest(TestCase):

    def setUp(self):
        self.url = reverse('signup')  # Make sure 'signup' is the correct name for your signup URL pattern

    def test_signup_success(self):
        data = {
            'first_name': 'John',
            'surname': 'Doe',
            'email': 'johndoe',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # 302 Found - redirected
        self.assertTrue(User.objects.filter(email='johndoe@uni.sydney.edu.au').exists())
        self.assertTrue(UserProfile.objects.filter(user__email='johndoe@uni.sydney.edu.au').exists())

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')


User = get_user_model()

class VerifyEmailTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/verify_email/'  # Replace with your actual URL

    @patch('myapp.views.random.randint')
    @patch('myapp.views.send_mail')
    def test_verify_email_new_user(self, mock_send_mail, mock_randint):
        mock_randint.return_value = 123456
        response = self.client.post(self.url, {'email': 'newuser@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"success": True})
        mock_send_mail.assert_called_once()

    def test_verify_email_existing_user(self):
        # Create a test user
        User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        response = self.client.post(self.url, {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"success": False, "error": "Current user already exist."})

    @patch('myapp.views.send_mail')
    def test_verify_email_send_mail_error(self, mock_send_mail):
        mock_send_mail.side_effect = Exception("Some error")
        response = self.client.post(self.url, {'email': 'newuser@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"success": False, "error": "Email sending failed."})




class CheckVerificationCodeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/check_verification_code/'  # Replace with your actual URL
        verification_codes.clear()  # Ensure it's empty at the start of tests

    def test_check_verification_code_correct(self):
        verification_codes['testuser@example.com'] = '123456'
        response = self.client.post(self.url, {'email': 'testuser@example.com', 'code': '123456'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"success": True})

    def test_check_verification_code_incorrect(self):
        verification_codes['testuser@example.com'] = '123456'
        response = self.client.post(self.url, {'email': 'testuser@example.com', 'code': '654321'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"success": False, "error": "Invalid verification code."})

    def test_check_verification_code_no_email_in_dict(self):
        response = self.client.post(self.url, {'email': 'nonexistent@example.com', 'code': '123456'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"success": False, "error": "Invalid verification code."})

    def test_check_verification_code_invalid_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"success": False, "error": "Invalid request."})



class PasswordResetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('request_password_reset')  # replace with your actual URL name
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_valid_email(self):
        response = self.client.post(self.url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Reset link successfully sent", response.content.decode())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('test@example.com', mail.outbox[0].to)
        self.assertTrue(PasswordResetToken.objects.filter(user=self.user).exists())

    def test_invalid_email(self):
        response = self.client.post(self.url, {'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("This is not a valid email address", response.content.decode())
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(PasswordResetToken.objects.filter(user=self.user).exists())

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'request_password_reset.html')



class PasswordResetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'old_password')
        self.token = 'valid_token'
        self.expired_token = 'expired_token'
        PasswordResetToken.objects.create(user=self.user, token=self.token, expiration_date=timezone.now() + timezone.timedelta(hours=1))
        PasswordResetToken.objects.create(user=self.user, token=self.expired_token, expiration_date=timezone.now() - timezone.timedelta(hours=1))
        self.url = reverse('reset_password')

    def test_no_token_provided(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('request_password_reset'))

    def test_invalid_or_expired_token(self):
        response = self.client.get(self.url, {'token': 'invalid_token'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reset_password.html')

    def test_post_valid_data(self):
        data = {'new_password': 'new_password123', 'confirm_password': 'new_password123'}
        response = self.client.post(self.url + '?token=' + self.token, data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Password reset successfully.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password123'))

    def test_post_invalid_data(self):
        data = {'new_password': 'new_password123'}
        response = self.client.post(self.url + '?token=' + self.token, data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Form errors.')
        self.assertIn('confirm_password', response_data['errors'])

    def test_get_request(self):
        response = self.client.get(self.url, {'token': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reset_password.html')
        self.assertIsInstance(response.context['form'], forms.Form)


class UoSListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    def test_uos_list_view_renders_uos_list_template(self):
        # Issue a GET request using the Django test client
        response = self.client.get(reverse('UoSList'))

        # Check that the correct template was used
        self.assertTemplateUsed(response, 'UoSList.html')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)


class UoSTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        testuos = UoS.objects.create(code="1232", name="testunit")
        testuosC = UoSComment.objects.create(user=self.user, comment="test com", uos=testuos)
    def test_uos_values(self):
        uos=UoS.objects.get(name="testunit")
        self.assertEqual(uos.code, "1232")
    def test_uos_site(self):
        expected_url=reverse('UoS', args=["testunit"])
        print(expected_url)
        response = self.client.get('/UoS/testunit/')
        print(response)
        self.assertContains(response, 'href="{0}"'.format(expected_url))
        self.assertTemplateUsed(response, 'UoS.html')
        # Check if the response status code is 200, indicating a successful redirection
        self.assertEqual(response.status_code, 200)
    def test_uos_comment(self):
        uosC=UoSComment.objects.get(user=self.user)
        self.assertEqual(uosC.comment, "test com")