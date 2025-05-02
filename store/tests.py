from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product, Order

class StoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.staff_user = User.objects.create_user(username='staffuser', password='staffpass', is_staff=True)
        self.category = Category.objects.create(name="2009")
        self.product = Product.objects.create(
            name="Avatar",
            description="Experience the magic of Avatar!",
            price=760.50,
            category=self.category,
            location="Hollywood"
        )

    # Model Tests (already added above)
    def test_category_creation(self):
        self.assertEqual(self.category.name, "2009")
        self.assertEqual(str(self.category), "2009")

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Avatar")
        self.assertEqual(self.product.price, 760.50)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(str(self.product), "Avatar")

    def test_order_creation(self):
        order = Order.objects.create(user=self.user, product=self.product, quantity=2)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(str(order), "testuser - Avatar")

    # View Tests
    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Screenplay Superstore")
        self.assertContains(response, "Avatar")

    def test_product_list_search(self):
        response = self.client.get(reverse('product_list'), {'q': 'Avatar'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Avatar")
        response = self.client.get(reverse('product_list'), {'q': 'Nonexistent'})
        self.assertContains(response, "No movies found.")

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Avatar")
        self.assertContains(response, "Experience the magic of Avatar!")

    def test_order_create_view_unauthenticated(self):
        response = self.client.get(reverse('order_create', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)  # Redirects to login
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_order_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('order_create', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        # Test placing an order
        response = self.client.post(reverse('order_create', args=[self.product.pk]), {'quantity': 3})
        self.assertEqual(response.status_code, 302)  # Redirects to product list
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.quantity, 3)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)

    def test_admin_dashboard_view_unauthenticated(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_admin_dashboard_view_non_staff(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)  # Forbidden for non-staff

    def test_admin_dashboard_view_staff(self):
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Dashboard")