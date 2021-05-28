document.addEventListener('DOMContentLoaded', function(){
    var elements = document.querySelectorAll('.markdown-editor');
    for (var i = 0; i < elements.length; i += 1) {
        var textArea = elements[i];
        var parent = textArea.parentElement;
        parent.removeChild(textArea);
        var div = document.createElement('div');
        div.append(textArea);
        div.className = 'markdown-editor-container'
        parent.append(div);

        var label = parent.querySelector('label');
        if (label !== undefined) {
            parent.removeChild(label);
            var labelDiv = document.createElement('div');
            labelDiv.append(label);
            parent.prepend(labelDiv);
            var clearDiv = document.createElement('div');
            clearDiv.style.clear = 'both';
            labelDiv.append(clearDiv);
        }

        new SimpleMDE({
            element: textArea,
            spellChecker: false,
        });
    }
});