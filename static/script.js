const textarea = document.getElementById('textpostarea');
    const charCount = document.getElementById('char-count');

    textarea.addEventListener('input', function() {
        const remaining = 255 - textarea.value.length;
        charCount.textContent = remaining + ' characters remaining';
    });
