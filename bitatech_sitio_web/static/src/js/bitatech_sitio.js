/** @odoo-module **/

/**
 * BITATECH - Sitio Web JavaScript
 * Sistemas Empresariales Inteligentes
 *
 * Funcionalidades:
 * - Animaciones de scroll (IntersectionObserver)
 * - Validacion de formularios
 * - Scroll suave para anclas
 * - Proteccion contra doble envio
 * - Menu movil toggle
 */

document.addEventListener('DOMContentLoaded', function () {

    // ================================================================
    // 1. ANIMACIONES DE SCROLL CON INTERSECTION OBSERVER
    // ================================================================
    const elementosAnimar = document.querySelectorAll('.bitatech-animar');

    if (elementosAnimar.length > 0 && 'IntersectionObserver' in window) {
        const observadorOpciones = {
            root: null,
            rootMargin: '0px 0px -60px 0px',
            threshold: 0.1,
        };

        const observadorCallback = function (entradas, observador) {
            entradas.forEach(function (entrada) {
                if (entrada.isIntersecting) {
                    const elemento = entrada.target;
                    const retraso = parseInt(elemento.getAttribute('data-delay') || '0', 10);

                    setTimeout(function () {
                        elemento.classList.add('bitatech-visible');
                    }, retraso);

                    observador.unobserve(elemento);
                }
            });
        };

        const observador = new IntersectionObserver(observadorCallback, observadorOpciones);

        elementosAnimar.forEach(function (elemento) {
            observador.observe(elemento);
        });
    } else {
        // Fallback: mostrar todo si no hay IntersectionObserver
        elementosAnimar.forEach(function (elemento) {
            elemento.classList.add('bitatech-visible');
        });
    }

    // ================================================================
    // 2. VALIDACION DE FORMULARIOS
    // ================================================================
    const formularios = document.querySelectorAll('.bitatech-formulario');

    formularios.forEach(function (formulario) {
        formulario.addEventListener('submit', function (evento) {
            let esValido = true;

            // Limpiar errores previos
            formulario.querySelectorAll('.bitatech-campo-error').forEach(function (campo) {
                campo.classList.remove('bitatech-campo-error');
            });
            formulario.querySelectorAll('.bitatech-campo-error-mensaje').forEach(function (msg) {
                msg.remove();
            });

            // Validar campos requeridos
            const camposRequeridos = formulario.querySelectorAll('[required]');
            camposRequeridos.forEach(function (campo) {
                if (!campo.value || !campo.value.trim()) {
                    esValido = false;
                    marcarError(campo, 'Este campo es requerido');
                }
            });

            // Validar formato de correo
            const campoCorreo = formulario.querySelector('input[type="email"], input[name="correo"]');
            if (campoCorreo && campoCorreo.value && campoCorreo.value.trim()) {
                const patronCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!patronCorreo.test(campoCorreo.value.trim())) {
                    esValido = false;
                    marcarError(campoCorreo, 'Ingresa un correo electronico valido');
                }
            }

            if (!esValido) {
                evento.preventDefault();
                // Scroll al primer error
                const primerError = formulario.querySelector('.bitatech-campo-error');
                if (primerError) {
                    primerError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    primerError.focus();
                }
                return false;
            }

            // Proteccion contra doble envio
            const botonSubmit = formulario.querySelector('button[type="submit"]');
            if (botonSubmit) {
                if (botonSubmit.dataset.enviando === 'true') {
                    evento.preventDefault();
                    return false;
                }
                botonSubmit.dataset.enviando = 'true';
                botonSubmit.disabled = true;
                botonSubmit.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Enviando...';

                // Restaurar despues de 10 segundos por si hay error
                setTimeout(function () {
                    botonSubmit.dataset.enviando = 'false';
                    botonSubmit.disabled = false;
                    botonSubmit.innerHTML = 'Enviar Solicitud';
                }, 10000);
            }
        });
    });

    /**
     * Marca un campo con error visual y mensaje.
     * @param {HTMLElement} campo - El campo de formulario.
     * @param {string} mensaje - Mensaje de error a mostrar.
     */
    function marcarError(campo, mensaje) {
        campo.classList.add('bitatech-campo-error');
        const elementoMensaje = document.createElement('span');
        elementoMensaje.className = 'bitatech-campo-error-mensaje';
        elementoMensaje.textContent = mensaje;
        campo.parentNode.appendChild(elementoMensaje);
    }

    // Limpiar error al escribir
    document.querySelectorAll('.bitatech-campo-input, .bitatech-campo-select, .bitatech-campo-textarea')
        .forEach(function (campo) {
            campo.addEventListener('input', function () {
                this.classList.remove('bitatech-campo-error');
                const msgError = this.parentNode.querySelector('.bitatech-campo-error-mensaje');
                if (msgError) {
                    msgError.remove();
                }
            });
        });

    // ================================================================
    // 3. SCROLL SUAVE PARA ENLACES ANCLA
    // ================================================================
    document.querySelectorAll('.bitatech-envoltorio a[href*="#"]').forEach(function (enlace) {
        enlace.addEventListener('click', function (evento) {
            const href = this.getAttribute('href');
            if (!href || href === '#') return;

            // Extraer el hash (puede ser #seccion o /pagina#seccion)
            const hashIndex = href.indexOf('#');
            if (hashIndex === -1) return;

            const hash = href.substring(hashIndex);
            const destino = document.querySelector(hash);

            if (destino) {
                evento.preventDefault();
                const offsetTop = destino.getBoundingClientRect().top + window.pageYOffset - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth',
                });
            }
        });
    });

    // ================================================================
    // 4. MENU MOVIL TOGGLE
    // ================================================================
    const botonMenu = document.querySelector('.bitatech-menu-movil');
    const navMenu = document.querySelector('.bitatech-nav');

    if (botonMenu && navMenu) {
        botonMenu.addEventListener('click', function () {
            this.classList.toggle('activo');
            navMenu.classList.toggle('bitatech-nav-abierto');
        });

        // Cerrar menu al hacer clic en un enlace
        navMenu.querySelectorAll('.bitatech-nav-enlace').forEach(function (enlace) {
            enlace.addEventListener('click', function () {
                botonMenu.classList.remove('activo');
                navMenu.classList.remove('bitatech-nav-abierto');
            });
        });
    }

    // ================================================================
    // 5. HEADER CON EFECTO AL HACER SCROLL
    // ================================================================
    const header = document.querySelector('.bitatech-header');
    if (header) {
        let ultimoScroll = 0;
        window.addEventListener('scroll', function () {
            const scrollActual = window.pageYOffset;
            if (scrollActual > 100) {
                header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.5)';
            } else {
                header.style.boxShadow = 'none';
            }
            ultimoScroll = scrollActual;
        }, { passive: true });
    }

});
