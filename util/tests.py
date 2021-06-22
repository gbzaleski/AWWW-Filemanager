from django.test import TestCase
from django.test.client import Client
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from http import HTTPStatus
from django.utils.crypto import get_random_string
import random
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from .views import *

class TestBasic(TestCase):

    def setUp(self):
        self.mainuser = User.objects.create()

        self.dir1 = Directory.objects.create(
            name = 'Dir 1',
            owner = self.mainuser,
            description = 'Opis folderu'
        )

        self.filecontenttest = SimpleUploadedFile(
            "best_file_eva.txt",
            b"these are the file contents!" # for convertion to bytes
        )

        self.fil1 = File.objects.create(
            name = 'Fil 1',
            owner = self.mainuser,
            description = 'Opis pliku',
            directory = self.dir1,
            content = self.filecontenttest
        )

        self.sec1 = FileSection.objects.create(
            name = 'Sec 1',
            description = 'Opis sekcji',
            category = 'important',
            status = 'created '
        )
       

    def test(self):
        self.assertEqual(1, 2 - 1)
        self.assertFalse(1 == 2)
        self.assertTrue(True)

        self.assertEqual(self.dir1.name, 'Dir 1')
        self.assertFalse(self.dir1.name == 'dir 2')
        self.assertFalse(self.dir1.deleted)
        self.assertTrue(self.dir1.creation_date)
        self.assertTrue(self.dir1.creation_date <= timezone.now())
        self.assertEqual(self.dir1.owner, self.mainuser)

        self.assertEqual(self.fil1.name, 'Fil 1')
        self.assertFalse(self.fil1.name == 'fil 1')
        self.assertFalse(self.fil1.deleted)
        self.assertTrue(self.fil1.creation_date)
        self.assertTrue(self.fil1.creation_date <= timezone.now())
        self.assertEqual(self.fil1.owner, self.mainuser)
        self.assertEqual(self.fil1.directory, self.dir1)
        self.assertTrue(self.fil1.content)

        self.assertEqual(self.sec1.name, 'Sec 1')
        self.assertNotEqual(self.sec1.name, 'sec 1')
        self.assertTrue(self.sec1.creation_date)
        self.assertTrue(self.sec1.creation_date <= timezone.now())
        self.assertTrue(self.sec1.status_date)
        self.assertTrue(self.sec1.status_date <= timezone.now())

        self.assertTrue(self.dir1.__str__())
        self.assertTrue(self.fil1.__str__())
        self.assertTrue(self.sec1.__str__())

        self.assertTrue(self.fil1.get_absolute_url() == '/')
        self.assertTrue(self.dir1.get_absolute_url() == '/')
        self.assertTrue(self.sec1.get_absolute_url() == '/')
        
    def testError(self):
        try:
            self.dir2 = Directory.objects.create(
                name = 'None owner',
                description = 'Opis folderu'
            )
            self.assertTrue(False)
        except IntegrityError:
            self.assertTrue(True)

    def testError2(self):
        try:
            self.fil2 = File.objects.create(
            name = 'No parent directory',
            owner = self.mainuser,
            description = 'Opis pliku',
            content = self.filecontenttest
        )
            self.assertTrue(False)
        except IntegrityError:
            self.assertTrue(True)

    def testForm(self):

        response = self.client.post(
            "/add-dir/", data = {"name": "nazwa"}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def testView(self):
        self.client.login(username='username', password='test')
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'util/form.html')

    def testContext(self):
        context = {
            'files': File.objects.all(),
            'directories': Directory.objects.all(),
        }
        
        self.assertTrue(context);
        self.assertEquals(len(context), 2)
        self.assertEquals(len(context['files']), 1)
        self.assertEquals(len(context['directories']), 1)
        self.assertEquals(context['files'][0], self.fil1)
        self.assertEquals(context['directories'][0], self.dir1)

class AdvancedTestBase(TestCase):
    url = reverse("util-home")
    client: Client = None

    example_user: str = None
    example_user_password: str = None
    example_admin: str = None
    example_admin_password: str = None

    def login_as_user(self):
        self.assertTrue(self.client.login(
            username=self.example_user,
            password=self.example_user_password
        ))

    def login_as_admin(self):
        self.assertTrue(self.client.login(
            username=self.example_admin,
            password=self.example_admin_password
        ))

    def logout(self):
        self.client.logout()

    def setUp(self):
        self.example_user = get_random_string(10)
        self.example_user_password = get_random_string(10)
        self.example_admin = get_random_string(10)
        self.example_admin_password = get_random_string(10)

        user = User.objects.create(
            username=self.example_user
        )
        user.set_password(self.example_user_password)
        user.save()

        admin = User.objects.create_superuser(
            username=self.example_admin
        )
        admin.set_password(self.example_admin_password)
        admin.save()

        self.client = Client()

    def assert_menu(self, response):
        self.assertContains(response, "Add File")
        self.assertContains(response, "Add Directory")
        self.assertContains(response, "Frama-C")
        self.assertContains(response, "Focus")
        self.assertContains(response, "Frama compilation mode")

    def assert_logout(self, response):
        self.assertContains(response, "Login")
        self.assertContains(response, "Register")

    def assert_user(self, response):
        self.assertContains(response, self.example_user)
        self.assertContains(response, "Logout")
        self.assert_menu(response)



    def assert_admin(self, response):
        self.assertContains(response, self.example_admin)
        self.assertContains(response, "Logout")
        self.assert_menu(response)


class BaseViewTest(AdvancedTestBase):
    def test_logout_navbar(self):
        response = self.client.get(self.url)
        self.assert_logout(response)

    def test_user_navbar(self):
        self.login_as_user()

        with self.assertRaises(Exception) as context:
            response = self.client.post(
                reverse('util-update'),
                data={'fileid': 'test_id'},
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )

        with self.assertRaises(Exception) as context:
            response = self.client.post(
                reverse('util-edit-code'),
                data={'fileid': 'test_id'},
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )

        response = self.client.get(self.url)
        self.assert_user(response)

    def test_admin_navbar(self):
        self.login_as_admin()
        response = self.client.get(self.url)
        self.assert_admin(response)

    def test_cookies(self):
        self.test_logout_navbar()

        for i in range(20):
            if random.randint(0, 1) == 0:
                self.test_admin_navbar()
            else:
                self.test_user_navbar()
            self.logout()
            self.test_logout_navbar()

class FileFormAddTest(TestCase):
    def setUp(self):
        self.example_user = get_random_string(10)
        self.example_user_password = get_random_string(10)

        self.user = User.objects.create(
            username = self.example_user
        )
        self.user.set_password(self.example_user_password)
        self.user.save()
        self.client = Client()

        self.dir = Directory.objects.create(
            name = 'Dir 1',
            owner = self.user,
            description = 'Opis folderu'
        )

class AjaxTest(TestCase):
     def test(self):
        response = self.client.get(reverse("util-update"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get("add-file/")
        self.assertEqual(response.status_code, 404)

        response = self.client.post("util-update", {'csrfmiddlewaretoken': "wrong-token", 'fileid':"wrong-id"})
        self.assertEqual(response.status_code, 404)

        response = self.client.post("delete/", {'dirs': 'test', 'files': 'test'})
        self.assertEqual(response.status_code, 404)

class DirectoryFormAddTest(FileFormAddTest):
    def test_form_dir(self):
        name = get_random_string(10)
        description = get_random_string(10)

        form = DirectoryCreateView(
            data={
                "name": name,
                "description": description
            }
        )
        
        self.assertTrue(form)

class TestMenuButtons(AdvancedTestBase):
    url = reverse("util-add-file")
    
    def test_add_file(self):
        self.login_as_user()
        response = self.client.get(self.url)
        self.assertContains(response, "Add File")
        self.assertContains(response, "Name")
        self.assertContains(response, "Owner")
        self.assertContains(response, "Directory")
        self.assertContains(response, "Content")
        self.assertContains(response, "Description")
        self.assertContains(response, "Upload new file")

    def test_add_directory(self):
        self.login_as_user()
        response = self.client.get(reverse("util-add-directory"))
        self.assertContains(response, "Add Directory")
        self.assertContains(response, "Name")
        self.assertContains(response, "Description")
        self.assertContains(response, "Create new Directory")

    def test_delete(self):
        self.login_as_user()
        response = self.client.get(reverse("util-delete"))
        self.assertContains(response, "Delete Directory")
        self.assertContains(response, "Delete File")