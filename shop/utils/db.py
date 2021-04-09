from ..models import Category

def get_toplevel_menu_children(id):
    menu_items = Category.objects.filter(parent=id)
    output = []
    for i in menu_items:
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