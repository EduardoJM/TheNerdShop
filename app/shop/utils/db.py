from ..models import Category, Product

def has_products(category):
    return len(category.product_set.all()) > 0

def get_toplevel_menu_children(id):
    menu_items = Category.objects.filter(parent=id)
    output = []
    for i in menu_items:
        if not has_products(i):
            continue
        childs = get_toplevel_menu_children(i.id)
        output += [
            dict(
                id = i.id,
                text = i.text,
                icon = i.icon.name,
                children = childs,
            )
        ]
    return output

def get_toplevel_menu():
    menu_items = Category.objects.filter(top_menu=1)
    output = []
    for i in menu_items:
        if not has_products(i):
            continue
        childs = get_toplevel_menu_children(i.id)
        output += [
            dict(
                id = i.id,
                text = i.text,
                icon = i.icon.name,
                children = childs,
            )
        ]
    return output