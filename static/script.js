
const textAreaPost = document.getElementById('textpostarea');
if (textAreaPost) {
    const postCharCount = document.getElementById('char-count-post');

    textAreaPost.addEventListener('input', function(e) {
        const remaining = 255 - e.currentTarget.value.length;
        postCharCount.textContent = remaining + ' characters remaining';
    });
}

const textAreaComment = document.getElementById('textcommentarea');
if (textAreaComment) {
    const commentCharCount = document.getElementById('char-count-comment');

    textAreaComment.addEventListener('input', function(e) {
        const remaining = 255 - e.currentTarget.value.length;
        commentCharCount.textContent = remaining + ' characters remaining';
    });
}




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


// For profile replies button

document.addEventListener('DOMContentLoaded', function() {
    openBtn(evt, 'MyPosts');
});

function openBtn(evt, TabName){
    var i, btnContent, profileBtns;

    btnContent = document.getElementsByClassName("btnContent");
    for(i = 0; i < btnContent.length; i++){
        btnContent[i].style.display = "none";
    }

    profileBtns = document.getElementsByClassName("profile-btns");
    for(i = 0; i < profileBtns.length; i++){
        profileBtns[i].className = profileBtns[i].className.replace(" active", "");
    }

    document.getElementById(TabName).style.display = "block";
    evt.currentTarget.className += " active";
}
