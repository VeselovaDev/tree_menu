from typing import Any, Dict, List, Optional, Union

from django import template
from django.http import HttpRequest

from tree_menu.models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context: Dict[str, Any], menu_name: str) -> Dict[str, List[Dict[str, Union[MenuItem, List[Any], bool]]]]:
    request: HttpRequest = context['request']
    current_path: str = request.path

    try:
        menu: Menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_items': []}

    # Load all items of this menu in one query
    all_items = list(menu.items.select_related('parent').order_by('id'))

    # Find active item by URL
    active_item: Optional[MenuItem] = None
    for item in all_items:
        if item.get_absolute_url() == current_path:
            active_item = item
            break

    # Helper: check if item is in the active path (ancestors)
    def is_in_active_path(item: MenuItem, active: Optional[MenuItem]) -> bool:
        while active:
            if active == item:
                return True
            active = active.parent
        return False

    # Build tree purely from flat list — no queries here
    def build_tree(parent_id: Optional[int] = None) -> List[Dict[str, Union[MenuItem, List[Any], bool]]]:
        branch = []
        for item in all_items:
            pid = item.parent.id if item.parent else None
            if pid == parent_id:
                children = build_tree(item.id)
                branch.append({
                    'item': item,
                    'children': children,
                    'is_active': active_item == item,
                    'in_path': is_in_active_path(item, active_item),
                })
        return branch

    return {'menu_items': build_tree()}
