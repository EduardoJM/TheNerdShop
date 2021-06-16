from django.shortcuts import render

from shop.admin import admin_site

def index(request):
    context = dict(
        **admin_site.each_context(request),
    )
    return render(request, 'admin/chat/index.html', context)
