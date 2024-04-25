

const postArea = document.getElementById('textpostarea');
const postCharCount = document.getElementById('char-count');

postArea.addEventListener('input', function() {
    const remaining = 255 - postArea.value.length;
    postCharCount.textContent = remaining + ' characters remaining';
});


const commentArea = document.getElementById('textcommentarea');
const commentCharCount = document.getElementById('char-count');

commentArea.addEventListener('input', function() {
    const remaining = 255 - commentArea.value.length;
    postCharCount.textContent = remaining + ' characters remaining';
});
