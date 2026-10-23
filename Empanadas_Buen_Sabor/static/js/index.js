document.addEventListener("DOMContentLoaded", () => {
    
    // 1. MANEJO DEL LOADER
    const loader = document.getElementById('loader');
    if (loader) {
        setTimeout(() => {
            loader.classList.add('loader-hidden');
        }, 2300);
    }

    // 2. RED DE SEGURIDAD PARA IMÁGENES QUE NO CARGUEN
    const loaderImg = document.getElementById('loader-logo-img');
    const loaderEmoji = document.getElementById('loader-emoji');

    if (loaderImg) {
        loaderImg.addEventListener('error', () => {
            loaderImg.style.display = 'none';
            if (loaderEmoji) {
                loaderEmoji.style.display = 'block';
            }
        });
    }

    const headerLogoImg = document.getElementById('nav-header-logo-img');
    if (headerLogoImg) {
        headerLogoImg.addEventListener('error', () => {
            headerLogoImg.style.display = 'none';
        });
    }

    // 3. MENÚ RESPONSIVE EN MÓVILES
    const navToggle = document.getElementById("nav-toggle");
    const navLinks = document.getElementById("nav-links");

    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            navLinks.classList.toggle("shower");
        });
    }

    const navItems = document.querySelectorAll(".nav-link-item");
    navItems.forEach(item => {
        item.addEventListener("click", () => {
            if (navLinks) {
                navLinks.classList.remove("shower");
            }
        });
    });

    // 4. CAMBIO DE SOMBRA EN NAVBAR AL HACER SCROLL
    window.addEventListener("scroll", () => {
        const navbar = document.getElementById("navbar");
        if (navbar) {
            if (window.scrollY > 30) {
                navbar.classList.add("scrolled");
            } else {
                navbar.classList.remove("scrolled");
            }
        }
    });

});