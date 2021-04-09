from ..models import Category

def get_toplevel_menu():
    menu_items = Category.objects.filter(top_menu=1)
    output = []
    for i in menu_items:
        output += [
            dict(
                id = i.id,
                text = i.text,
                icon = i.icon.name,
            )
        ]
        # TODO: add subitems here in the future.
    return output