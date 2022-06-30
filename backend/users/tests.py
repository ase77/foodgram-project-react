# from django.test import TestCase
# from django.contrib.auth import get_user_model


# class UsersManagersTests(TestCase):

#     def test_create_user(self):
#         User = get_user_model()
#         user = User.objects.create_user(
#             username='user',
#             email='normal@user.com',
#             password='foo'
#         )
#         self.assertEqual(user.username, 'user')
#         self.assertEqual(user.email, 'normal@user.com')
#         self.assertFalse(user.is_superuser)

#     def test_create_superuser(self):
#         User = get_user_model()
#         admin_user = User.objects.create_superuser(
#             username='superuser',
#             email='super@user.com',
#             password='foo'
#         )
#         self.assertEqual(admin_user.username, 'superuser')
#         self.assertEqual(admin_user.email, 'super@user.com')
#         self.assertTrue(admin_user.is_superuser)
