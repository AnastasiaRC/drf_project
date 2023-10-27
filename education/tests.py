from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from education.models import Course, Lesson, Subscription
from users.models import UserRoles, User
from rest_framework_simplejwt.tokens import RefreshToken
import json


class LessonTestCase(APITestCase):
    def setUp(self):
        """Заполнение первичных данных"""

        self.user = User.objects.create(
            email='test@test.ru',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            role=UserRoles.MEMBER,
        )

        self.user.set_password('test1111')
        self.user.save()

        token = RefreshToken.for_user(self.user)
        self.access_token = str(token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(
            title='Python',
            description='lesson 1',
            author=self.user
        )
        self.lesson = Lesson.objects.create(
            title='lesson 1',
            course=self.course,
            description='lesson 1',
            link='https://www.youtube.com/test',
            author=self.user
        )

    def test_get_list(self):
        """Тест получения списка уроков"""

        response = self.client.get(reverse('education:lesson_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['results'],
                         [
                             {
                                 'id': self.lesson.id,
                                 'title': self.lesson.title,
                                 'description': self.lesson.description,
                                 'preview': self.lesson.preview,
                                 'link': self.lesson.link,
                                 'course': self.lesson.course_id,
                                 'author': self.lesson.author_id
                             }
                         ]
                         )

    def test_lesson_create(self):
        """Тест создания уроков"""

        data = {
            'title': 'test_lesson',
            'course': self.course.pk,
            'description': 'test_lesson',
            'link': 'https://www.youtube.com/test',
        }
        response = self.client.post(reverse('education:lesson_create'), data=data,)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, Lesson.objects.all().count())

    def test_lesson_update(self):
        """ Тест обновления урока """

        data = {
            'title': 'test_lesson_up',
            'course': self.course.pk,
            'description': 'test_lesson_up',
            'link': 'https://www.youtube.com/test',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('education:lesson_update', args=[self.lesson.pk]), data=data,)
        self.assertEqual(response.status_code, status.HTTP_200_OK,)
        self.assertTrue(Lesson.objects.all().exists())

    def test_lesson_delete(self):
        """ Тест удаления урока """

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('education:lesson_delete', args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,)
        self.assertFalse(Lesson.objects.all().exists(),)

    def tearDown(self) -> None:
        self.user.delete()
        self.course.delete()
        self.lesson.delete()


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        """Заполнение первичных данных"""

        self.user = User.objects.create(
            email='test@test.ru',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MEMBER,
        )
        self.user.set_password('test1111')
        self.user.save()

        token = RefreshToken.for_user(self.user)
        self.access_token = str(token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(
            title='Java',
            description='lesson 2',
            author=self.user
        )
        self.lesson = Lesson.objects.create(
            title='lesson 2',
            course=self.course,
            description='lesson 2',
            link='https://www.youtube.com/test',
            author=self.user
        )

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            status=False
        )

    def test_create_subscription(self):
        """ Тестирование создание подписки """
        data = {'course': self.course.id, 'user': self.user.id, 'status': False}
        response = self.client.post(reverse('education:subscription_create'), data=data,)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2,Subscription.objects.all().count())

    def test_subscription_destroy(self):
        """ Тестирование удаления подписки """

        response = self.client.delete(reverse('education:subscription_delete', args={self.subscription.pk}))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Subscription.objects.all().count())

    def tearDown(self):
        self.user.delete()
        self.course.delete()
        self.subscription.delete()
