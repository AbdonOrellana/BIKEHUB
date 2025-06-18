    // Manejo del menú de categorías
    const categoriasBtn = document.getElementById('categorias-btn');
    const categoriasMenu = document.getElementById('categorias-menu');
    let isMenuOpen = false;

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