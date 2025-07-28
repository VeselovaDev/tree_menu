import pytest
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from tree_menu.models import Menu, MenuItem


@pytest.mark.django_db
def test_menu_creation() -> None:
    # Test basic creation of Menu and MenuItem
    menu = Menu.objects.create(name="main menu")
    item = MenuItem.objects.create(menu=menu, title="Home", url="/")
    assert menu.items.count() == 1
    assert item.get_absolute_url() == "/"


@pytest.mark.django_db
def test_menu_item_named_url(client: Client) -> None:
    # Test that MenuItem with named_url resolves correctly
    menu = Menu.objects.create(name="main menu")
    item = MenuItem.objects.create(menu=menu, title="Go Home", named_url="home")
    assert item.get_absolute_url() == reverse("home")

    response = client.get(item.get_absolute_url())
    assert response.status_code == 200


@pytest.mark.django_db
def test_menu_rendered_in_response(client: Client) -> None:
    # Test that the menu renders on the page and contains correct links
    menu = Menu.objects.create(name="main menu")
    MenuItem.objects.create(menu=menu, title="Home", named_url="home")

    response = client.get(reverse("home"))

    assert response.status_code == 200
    # Check that the menu item title appears in the HTML content
    assert b"Home" in response.content
    # Check that the URL is rendered correctly in href
    assert b'href="' + reverse("home").encode() + b'"' in response.content


@pytest.mark.django_db
def test_active_menu_item_highlighted(client: Client) -> None:
    # Test that the active menu item gets the 'active' CSS class based on current URL
    menu = Menu.objects.create(name="main menu")
    MenuItem.objects.create(menu=menu, title="Home", named_url="home")
    MenuItem.objects.create(menu=menu, title="About", named_url="about")

    response = client.get(reverse("home"))
    assert response.status_code == 200

    # The active class should appear for the "Home" menu item
    assert b'class="active"' in response.content
    assert b'Home' in response.content

    # The "About" menu item should not have the active class
    about_pos = response.content.find(b'About')
    active_pos = response.content.find(b'class="active"')
    assert active_pos < about_pos  # active class appears before About, so not for About


@pytest.mark.django_db
def test_menu_expansion_logic(client: Client) -> None:
    # Test that the menu expands properly: parent and first-level children are visible
    menu = Menu.objects.create(name="main menu")
    parent = MenuItem.objects.create(menu=menu, title="Parent", url="/parent/")
    MenuItem.objects.create(menu=menu, title="Child", url="/parent/child/", parent=parent)

    response = client.get("/parent/child/")
    assert response.status_code == 200

    # Both parent and child should be visible in the menu
    assert b'Parent' in response.content
    assert b'Child' in response.content
    # The child menu item should be marked active
    assert b'class="active"' in response.content


@pytest.mark.django_db
def test_menu_query_count(client: Client) -> None:
    # Test that rendering the menu triggers only one query to the MenuItem table
    menu = Menu.objects.create(name="main menu")
    for i in range(5):
        MenuItem.objects.create(menu=menu, title=f"Item {i}", url=f"/item{i}/")

    with CaptureQueriesContext(connection) as ctx:
        response = client.get(reverse("home"))
        assert response.status_code == 200

    # Count queries related to MenuItem table
    menu_queries = [q for q in ctx.captured_queries if 'tree_menu_menuitem' in q['sql']]
    assert len(menu_queries) <= 1
