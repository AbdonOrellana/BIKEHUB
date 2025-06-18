    // Manejo del menú de categorías
    const categoriasBtn = document.getElementById('categorias-btn');
    const categoriasMenu = document.getElementById('categorias-menu');
    let isMenuOpen = false;

    //Variables menu usuario
    var userName = document.getElementById('user-name');
    var userMenu = document.getElementById('user-menu');

    var timeout;



    document.addEventListener('DOMContentLoaded', function() {
        var categoriasBtn = document.getElementById('categorias-btn');
        var categoriasMenu = document.getElementById('categorias-menu');
        var isMenuOpen = false;
        var timeout;

        categoriasBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            isMenuOpen = !isMenuOpen;
            categoriasMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', function(e) {
            if (isMenuOpen && !categoriasMenu.contains(e.target) && e.target !== categoriasBtn) {
                isMenuOpen = false;
                categoriasMenu.classList.add('hidden');
            }
        });

        categoriasBtn.addEventListener('mouseenter', function() {
            clearTimeout(timeout);
            isMenuOpen = true;
            categoriasMenu.classList.remove('hidden');
        });

        categoriasBtn.addEventListener('mouseleave', function() {
            timeout = setTimeout(function() {
                isMenuOpen = false;
                categoriasMenu.classList.add('hidden');
            }, 1500); // 1.5 segundos
        });

        categoriasMenu.addEventListener('mouseenter', function() {
            clearTimeout(timeout);
            isMenuOpen = true;
            categoriasMenu.classList.remove('hidden');
        });

        categoriasMenu.addEventListener('mouseleave', function() {
            timeout = setTimeout(function() {
                isMenuOpen = false;
                categoriasMenu.classList.add('hidden');
            }, 1500); // 1.5 segundos
        });
    });

    //Funcion menu usuario
    document.addEventListener('DOMContentLoaded', function() {
    userName.addEventListener('mouseenter', function() {
        clearTimeout(timeout);
        userMenu.classList.remove('hidden');
    });

    userName.addEventListener('mouseleave', function() {
        timeout = setTimeout(function() {
            userMenu.classList.add('hidden');
        }, 1500); // 2 segundos
    });

    userMenu.addEventListener('mouseenter', function() {
        clearTimeout(timeout);
        userMenu.classList.remove('hidden');
    });

    userMenu.addEventListener('mouseleave', function() {
        timeout = setTimeout(function() {
            userMenu.classList.add('hidden');
        }, 1500); // 2 segundos
    });
});