document.addEventListener('DOMContentLoaded', function () {
        let swiper = new Swiper('.swiper', {
            loop: true,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
        });
    
        let loginModal = document.getElementById('loginModal');
        let closeModalButton = document.getElementById('closeModal');
    
        // Abre el modal y pausa el carrusel si el enlace es hacia #loginModal
        document.querySelectorAll('.service-link').forEach(element => {
            element.addEventListener('click', function(event) {
                if (element.getAttribute('href') === '#loginModal') {
                    event.preventDefault();
                    loginModal.classList.remove('hidden');
                    swiper.autoplay.stop();
                }
            });
        });
    
        // Cierra el modal si se hace clic fuera del cuadro de diálogo del modal
        loginModal.addEventListener('click', function(event) {
            if (event.target === loginModal) {
                loginModal.classList.add('hidden');
                swiper.autoplay.start();
            }
        });
    });