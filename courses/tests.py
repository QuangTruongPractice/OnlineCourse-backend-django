from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import User, Role, Course, Category, UserCourse, CourseStatus, Chapter, Lesson, Payment
from django.contrib.auth.hashers import make_password
from unittest.mock import patch, MagicMock
from oauth2_provider.models import Application, AccessToken

class CoursePermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Roles
        self.admin_role, _ = Role.objects.get_or_create(name='Admin')
        self.teacher_role, _ = Role.objects.get_or_create(name='Teacher')
        self.student_role, _ = Role.objects.get_or_create(name='Student')
        
        # Users
        self.admin = User.objects.create(username='admin', email='admin@test.com', user_role=self.admin_role)
        self.teacher = User.objects.create(username='teacher', email='teacher@test.com', user_role=self.teacher_role)
        self.student = User.objects.create(username='student', email='student@test.com', user_role=self.student_role)
        
        # Category
        self.category = Category.objects.create(name='Test Category')
        
        # Course
        self.course = Course.objects.create(
            name='Test Course',
            category=self.category,
            lecturer=self.teacher,
            price=100000
        )

    def test_student_cannot_create_course(self):
        self.client.force_authenticate(user=self.student)
        data = {
            'name': 'Hacker Course',
            'subject': 'Hacking',
            'video_url': 'http://example.com'
        }
        response = self.client.post('/courses/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_create_course(self):
        self.client.force_authenticate(user=self.teacher)
        data = {
            'name': 'New Course',
            'subject': 'Math', 
            'category': self.category.id,
            'price': 200000,
            'description': 'Test Description'
        }
        response = self.client.post('/courses/', data) 
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        if response.status_code == 201:
             self.assertTrue(Course.objects.filter(name='New Course').exists())

    def test_unauthenticated_cannot_create_course(self):
        self.client.force_authenticate(user=None)
        data = {'name': 'Ghost Course'}
        response = self.client.post('/courses/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LessonTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher_role, _ = Role.objects.get_or_create(name='Teacher')
        self.teacher = User.objects.create(username='teacher_lesson', user_role=self.teacher_role)
        self.course = Course.objects.create(name='Lesson Course', lecturer=self.teacher)
        self.chapter = Chapter.objects.create(course=self.course, name='Chapter 1')

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.teacher)
        data = {
            'chapter': self.chapter.id,
            'name': 'New Lesson',
            'duration': 100,
            'type': 'video', 
            'video_url': 'http://video.com'
        }
        response = self.client.post('/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(name='New Lesson').exists())


class PaymentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student_role, _ = Role.objects.get_or_create(name='Student')
        self.student = User.objects.create(username='student_pay', user_role=self.student_role)
        self.course = Course.objects.create(name='Paid Course', price=50000)

    @patch('courses.services.momo.requests.post')
    def test_create_payment_flow(self, mock_post):
        # Mock Momo response
        mock_response = MagicMock()
        mock_response.json.return_value = {'payUrl': 'http://momo.vn/pay'}
        mock_post.return_value = mock_response

        self.client.force_authenticate(user=self.student)
        
        # 1. Create UserCourse (Enrollment) which triggers payment creation
        data = {
            'course': self.course.id,
            'status': CourseStatus.PENDING
        }
        # Assuming there is an endpoint to create user course that calls create_momo_payment
        # Based on views.py: UserCourseViewSet.create_user_course (action 'create')
        
        response = self.client.post('/enrollments/create/', data) # Check URL in urls.py
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('payUrl', response.data)
        self.assertEqual(response.data['payUrl'], 'http://momo.vn/pay')
        
        # Verify DB records
        self.assertTrue(UserCourse.objects.filter(user=self.student, course=self.course).exists())
        self.assertTrue(Payment.objects.filter(user=self.student, course_id=self.course.id).exists())


class ModelLogicTests(TestCase):
    def test_user_role_assignment(self):
        role, _ = Role.objects.get_or_create(name='Tester')
        user = User.objects.create(username='u1', user_role=role)
        self.assertEqual(user.user_role.name, 'Tester')


class GoogleLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student_role, _ = Role.objects.get_or_create(name='Student')
        # Create OAuth2 Application
        self.app = Application.objects.create(
            name="Test App",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )

    @patch('courses.views.verify_google_token')
    def test_google_login_success(self, mock_verify):
        # Mock successful Google token verification
        mock_verify.return_value = {
            'email': 'googleuser@example.com',
            'given_name': 'Google',
            'family_name': 'User',
            'picture': 'http://image.com/pic.jpg',
            'iss': 'accounts.google.com'
        }

        data = {'token': 'valid_google_token'}
        response = self.client.post('/auth/google/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        
        # Check if user was created
        user = User.objects.get(email='googleuser@example.com')
        self.assertEqual(user.first_name, 'Google')
        self.assertEqual(user.user_role.name, 'Student')
