

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



//For the likes 
// Function to handle like button click
function likePost(button) {
    const postId = button.getAttribute('data-post-id');
    // Fetch CSRF token from a meta tag or another source
    const csrfToken = getCSRFToken();
    
    // Make the fetch request to the server to toggle the like
    fetch('/toggle-like', {
        method: 'POST',
        body: JSON.stringify({ post_id: postId }),
        headers: {
            'Content-Type': 'application/json',
            // Include CSRF token in the request headers
            'X-CSRF-Token': csrfToken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json(); // Assuming the server responds with JSON
    })
    .then(data => {
        if (data.success) {
            // Update the number of likes displayed
            const likeCountSpan = button.nextElementSibling; // Assuming the <span> immediately follows the button
            likeCountSpan.textContent = data.likeCount;
            // Toggle heart icon style
            button.querySelector('i').classList.toggle('bi-heart-fill');
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to retrieve CSRF token
function getCSRFToken() {
    const csrfMetaTag = document.querySelector('meta[name="csrf-token"]');
    return csrfMetaTag ? csrfMetaTag.getAttribute('content') : '';
}