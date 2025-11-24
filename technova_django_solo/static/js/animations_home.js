// ========================================
// TECHNOVA - technova-animations.js
// Archivo principal de animaciones 3D
// ========================================

// Esperar a que el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // 3D BACKGROUND SCENE (Hero Banner)
    // ========================================
    const canvas3d = document.getElementById('canvas3d');
    
    if (canvas3d) {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 600, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ 
            canvas: canvas3d,
            antialias: true,
            alpha: true 
        });

        renderer.setSize(window.innerWidth, 600);
        renderer.setClearColor(0x000000, 0);

        // Crear múltiples geometrías abstractas
        const geometries = [];
        
        // Torus principal
        const torusGeo = new THREE.TorusGeometry(10, 2, 16, 100);
        const torusMat = new THREE.MeshPhongMaterial({ 
            color: 0x3b82f6,
            transparent: true,
            opacity: 0.15,
            wireframe: true
        });
        const torus = new THREE.Mesh(torusGeo, torusMat);
        scene.add(torus);
        geometries.push(torus);

        // Esfera con wireframe
        const sphereGeo = new THREE.SphereGeometry(8, 32, 32);
        const sphereMat = new THREE.MeshPhongMaterial({ 
            color: 0x60a5fa,
            transparent: true,
            opacity: 0.1,
            wireframe: true
        });
        const sphere = new THREE.Mesh(sphereGeo, sphereMat);
        sphere.position.set(-15, 0, -10);
        scene.add(sphere);
        geometries.push(sphere);

        // Icosahedron
        const icoGeo = new THREE.IcosahedronGeometry(6, 0);
        const icoMat = new THREE.MeshPhongMaterial({ 
            color: 0x93c5fd,
            transparent: true,
            opacity: 0.12,
            wireframe: true
        });
        const ico = new THREE.Mesh(icoGeo, icoMat);
        ico.position.set(15, 5, -5);
        scene.add(ico);
        geometries.push(ico);

        // Octahedron
        const octaGeo = new THREE.OctahedronGeometry(5, 0);
        const octaMat = new THREE.MeshPhongMaterial({ 
            color: 0xbfdbfe,
            transparent: true,
            opacity: 0.1,
            wireframe: true
        });
        const octa = new THREE.Mesh(octaGeo, octaMat);
        octa.position.set(0, -10, -15);
        scene.add(octa);
        geometries.push(octa);

        // Luces
        const pointLight1 = new THREE.PointLight(0xffffff, 1);
        pointLight1.position.set(10, 10, 10);
        scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0x3b82f6, 0.8);
        pointLight2.position.set(-10, -10, 5);
        scene.add(pointLight2);

        const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
        scene.add(ambientLight);

        camera.position.z = 30;

        // Variables de animación
        let time = 0;

        // Animación del fondo
        function animateBackground() {
            requestAnimationFrame(animateBackground);
            time += 0.01;

            // Animar cada geometría de forma diferente
            torus.rotation.x = time * 0.3;
            torus.rotation.y = time * 0.5;

            sphere.rotation.x = time * 0.2;
            sphere.rotation.y = time * 0.3;
            sphere.position.y = Math.sin(time) * 2;

            ico.rotation.x = time * 0.4;
            ico.rotation.z = time * 0.2;

            octa.rotation.y = time * 0.5;
            octa.rotation.z = time * 0.3;

            // Movimiento de cámara sutil
            camera.position.x = Math.sin(time * 0.1) * 2;
            camera.position.y = Math.cos(time * 0.15) * 1;
            camera.lookAt(0, 0, 0);

            renderer.render(scene, camera);
        }

        animateBackground();

        // Responsive
        window.addEventListener('resize', () => {
            const width = window.innerWidth;
            const height = 600;
            renderer.setSize(width, height);
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
        });
    }

    // ========================================
    // PARTICLES (Partículas flotantes)
    // ========================================
    function createParticles() {
        const particlesContainer = document.getElementById('particles');
        
        if (particlesContainer) {
            for (let i = 0; i < 40; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.width = Math.random() * 6 + 2 + 'px';
                particle.style.height = particle.style.width;
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDuration = Math.random() * 8 + 12 + 's';
                particle.style.animationDelay = Math.random() * 8 + 's';
                particlesContainer.appendChild(particle);
            }
        }
    }

    createParticles();

    // ========================================
    // WISHLIST FUNCTIONALITY
    // ========================================
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const icon = this.querySelector('i');
            const productId = this.getAttribute('data-product-id');
            
            if (icon.classList.contains('far')) {
                // Agregar a wishlist
                icon.classList.remove('far');
                icon.classList.add('fas');
                this.style.background = '#1d4ed8';
                this.style.borderColor = '#1d4ed8';
                icon.style.color = 'white';
                
                // Aquí puedes hacer una petición AJAX a Django
                console.log('Producto agregado a wishlist:', productId);
                
                // Opcional: Mostrar notificación
                showNotification('Agregado a favoritos ❤️');
                
            } else {
                // Quitar de wishlist
                icon.classList.remove('fas');
                icon.classList.add('far');
                this.style.background = 'white';
                this.style.borderColor = '#e5e7eb';
                icon.style.color = '#6b7280';
                
                console.log('Producto eliminado de wishlist:', productId);
                showNotification('Eliminado de favoritos');
            }
        });
    });

    // ========================================
    // SCROLL ANIMATIONS (Intersection Observer)
    // ========================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observar elementos que necesitan animación al hacer scroll
    document.querySelectorAll('.product-card, .category-card, .trust-badge').forEach(card => {
        observer.observe(card);
    });

    // ========================================
    // SMOOTH SCROLL
    // ========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ========================================
    // NOTIFICATION HELPER
    // ========================================
    function showNotification(message) {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = 'notification-toast';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #1d4ed8;
            color: white;
            padding: 15px 25px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(29, 78, 216, 0.3);
            z-index: 9999;
            animation: slideInRight 0.3s ease;
            font-weight: 600;
        `;
        
        document.body.appendChild(notification);
        
        // Remover después de 3 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // ========================================
    // CATEGORY CARDS HOVER EFFECT
    // ========================================
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // ========================================
    // PRODUCT IMAGE LAZY LOADING
    // ========================================
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ========================================
    // PRICE ANIMATION ON HOVER
    // ========================================
    document.querySelectorAll('.product-price').forEach(price => {
        const card = price.closest('.product-card');
        if (card) {
            card.addEventListener('mouseenter', () => {
                price.style.transform = 'scale(1.1)';
            });
            card.addEventListener('mouseleave', () => {
                price.style.transform = 'scale(1)';
            });
        }
    });

});

// ========================================
// ANIMATIONS CSS (agregar al <head>)
// ========================================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);