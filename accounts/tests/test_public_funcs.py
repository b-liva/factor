from django.contrib.auth import get_user_model
from customer.models import Type
User = get_user_model()


def sample_user(username='testuser', password='testpass123'):
    """Create a sample user"""
    return User.objects.create_user(username, password)


def sample_customer_type(name='پتروشیمی'):
    """Create a sample customer type"""
    return Type.objects.create(name=name)
