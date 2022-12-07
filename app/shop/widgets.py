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

class MaterializeSelectMultiple(MaterializeSelect):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)

    def value_omitted_from_data(self, data, files, name):
        # An unselected <select multiple> doesn't appear in POST data, so it's
        # never known if the value is actually omitted.
        return False
