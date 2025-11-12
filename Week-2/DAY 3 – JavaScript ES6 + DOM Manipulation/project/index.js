document.addEventListener("DOMContentLoaded", function() {
    const questions = document.querySelectorAll('.question');
    questions.forEach(function(question) {
        question.addEventListener('click', function() {
            const answer = this.nextElementSibling; 
            const icon = this.querySelector('i'); 
            answer.classList.toggle('show');
            icon.classList.toggle('rotate');
        });
    });
});
