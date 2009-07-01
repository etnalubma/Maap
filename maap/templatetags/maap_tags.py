from django import template
from maap.models import MaapCategory

register = template.Library()
@register.inclusion_tag('../templates/category_list.html')
def category_list(current_node=None):
    roots = MaapCategory.tree.root_nodes()
    if current_node:
        croot = current_node.get_root()
        roots = roots.exclude(pk=croot.pk)
    else:
        croot = None
    return {'roots': roots,'current':current_node,'current_root':croot}
    
