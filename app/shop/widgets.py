from django.forms import widgets

class MarkdownTextArea(widgets.Textarea):
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

class MaterializeCheckBox(widgets.CheckboxInput):
    template_name = 'django/forms/widgets/material-checkbox.html'
    label = ''

    def __init__(self, label, attrs = None):
        self.label = label
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label'] = self.label
        return context

class MaterializeSelect(widgets.Select):
    template_name = 'django/forms/widgets/material-select.html'
    label = ''

    def __init__(self, label, attrs = None):
        self.label = label
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label'] = self.label
        return context

class MaterializeFileInput(widgets.ClearableFileInput):
    template_name = 'django/forms/widgets/material-file.html'
    label = ''

    def __init__(self, label, attrs = None):
        self.label = label
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label'] = self.label
        return context

