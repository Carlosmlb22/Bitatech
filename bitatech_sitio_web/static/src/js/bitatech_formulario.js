/** @odoo-module **/

document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // -------------------------------------------------------
    // Validacion del formulario de diagnostico
    // -------------------------------------------------------
    const formulario = document.getElementById('formulario_diagnostico');
    if (formulario) {
        formulario.addEventListener('submit', function (e) {
            const nombre = document.getElementById('campo_nombre');
            const empresa = document.getElementById('campo_empresa');
            const correo = document.getElementById('campo_correo');
            let valido = true;

            // Limpiar errores previos
            document.querySelectorAll('.bitatech-campo--error').forEach(function (el) {
                el.classList.remove('bitatech-campo--error');
            });

            if (!nombre.value.trim()) {
                nombre.closest('.bitatech-campo').classList.add('bitatech-campo--error');
                valido = false;
            }
            if (!empresa.value.trim()) {
                empresa.closest('.bitatech-campo').classList.add('bitatech-campo--error');
                valido = false;
            }
            if (!correo.value.trim() || !correo.value.includes('@')) {
                correo.closest('.bitatech-campo').classList.add('bitatech-campo--error');
                valido = false;
            }

            if (!valido) {
                e.preventDefault();
                // Scroll al primer campo con error
                const primerError = document.querySelector('.bitatech-campo--error');
                if (primerError) {
                    primerError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return false;
            }

            // Deshabilitar boton para evitar doble envio
            const boton = formulario.querySelector('button[type="submit"]');
            if (boton) {
                boton.disabled = true;
                boton.textContent = 'Enviando...';
            }
        });
    }

    // -------------------------------------------------------
    // Scroll suave para anclas internas
    // -------------------------------------------------------
    document.querySelectorAll('.bitatech-landing a[href^="#"]').forEach(function (enlace) {
        enlace.addEventListener('click', function (e) {
            e.preventDefault();
            const destino = document.querySelector(this.getAttribute('href'));
            if (destino) {
                destino.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // -------------------------------------------------------
    // Animaciones al hacer scroll
    // -------------------------------------------------------
    const elementosAnimar = document.querySelectorAll(
        '.bitatech-tarjeta-problema, .bitatech-metodo-paso, .bitatech-tarjeta-plan, .bitatech-filtro-tarjeta'
    );

    if (elementosAnimar.length > 0 && 'IntersectionObserver' in window) {
        elementosAnimar.forEach(function (el) {
            el.classList.add('bitatech-animar');
        });

        const observador = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('bitatech-animar--visible');
                    observador.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.15,
            rootMargin: '0px 0px -40px 0px'
        });

        elementosAnimar.forEach(function (el) {
            observador.observe(el);
        });
    }
});
