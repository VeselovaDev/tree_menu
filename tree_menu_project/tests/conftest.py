import os
import sys

import django
import pytest
from django.test import Client

# Define the project root directory (where manage.py and tree_menu_project folder are)
project_root = os.path.abspath(os.path.dirname(__file__))

# Add project root to sys.path if not already present
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set the DJANGO_SETTINGS_MODULE environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tree_menu.settings')

# Initialize Django
django.setup()




@pytest.fixture
def client() -> Client:
    # Provide Django test client as a fixture for tests
    return Client()
