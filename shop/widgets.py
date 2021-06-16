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

class MaterializeTextArea(widgets.Textarea):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'materialize-textarea'
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

class MoneyInput(widgets.TextInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['data-mask-money'] = 'on'
        return context

    def value_from_datadict(self, data, files, name):
        value = str(super().value_from_datadict(data, files, name))
        return value.replace(' ', '')

    class Media:
        js = (
            'https://unpkg.com/vanilla-masker@1.1.1/build/vanilla-masker.min.js',
            'widgets/common.js',
        )
