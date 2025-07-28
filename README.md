# Tree Menu Project

Tree Menu is a Django app for creating and managing hierarchical menus stored in the database. Menus are easily editable through Django’s standard admin interface, rendered on any page via a custom template tag, and support nested items that automatically expand based on the current URL.

## Key Features

- Menus and menu items are stored in the database.

- Menu management via standard Django admin interface.

- Display menus on any page using a template tag by menu name.

- Active menu item is determined by the current page URL.

- Parent items and the first-level children under the active item are expanded.

- Support multiple menus on the same page.

- Only one database query needed per menu rendering.

- Menu item URLs can be set either explicitly or via Django named URLs.


## Technologies Used

- Python 3.12

- Django 5.2

- Pytest and pytest-django for testing

- Poetry for dependency and environment management

## Quick Start
1. Clone the repository via SSH

```
git clone git@github.com:VeselovaDev/tree_menu.git
cd tree_menu

```

2. Install dependencies with Poetry
```
poetry install
```

3. Apply database migrations
```
make migrate

```
4. Run tests
```
make test
```

How to Use

## Create menus and menu items in Django admin; set hierarchy and URLs.

Render menus in templates with the tag:
```
{% load draw_menu %}
{% draw_menu 'main menu' %}
```
The active menu item and its first-level children will be automatically highlighted and expanded.