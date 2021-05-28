from django.forms.widgets import Textarea

class MarkdownTextArea(Textarea):
    class Media:
        css = {
            'all': [
                'https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css',
                'admin/css/mde.custom.css',
            ],
        }
        js = [
            'https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js',
            'admin/js/simplemde.init.js'
        ]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'markdown-editor'
        return context