$(document).ready(function() {
    try {
        document.querySelectorAll(".upvote-active, .downvote-active").forEach( (up_button) => {
            up_button.style.animation = "like 0.8s forwards";
        });
    } catch (error) {
        
    }
});