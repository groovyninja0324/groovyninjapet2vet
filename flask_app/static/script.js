let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-slide');

function showSlide(index) {
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = 'none';
    }

    currentSlide = (index + slides.length) % slides.length;
    slides[currentSlide].style.display = 'block';
}

function nextSlide() {
    showSlide(currentSlide + 1);
}

function prevSlide() {
    showSlide(currentSlide - 1);
}

// Automatic slide change (optional)
setInterval(nextSlide, 3000);

showSlide(currentSlide);