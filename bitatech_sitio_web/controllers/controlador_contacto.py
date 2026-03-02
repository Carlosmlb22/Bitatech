# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ControladorContactoBitatech(http.Controller):
    """Controlador para el formulario de contacto del sitio web de Bitatech."""

    @http.route(
        '/bitatech/contacto/enviar',
        type='http',
        auth='public',
        website=True,
        csrf=True,
        methods=['POST'],
    )
    def enviar_formulario_contacto(self, **kwargs):
        """Recibe datos del formulario de contacto y crea la solicitud."""
        valores = {
            'nombre_completo': kwargs.get('nombre_completo', '').strip(),
            'correo': kwargs.get('correo', '').strip(),
            'telefono': kwargs.get('telefono', '').strip(),
            'nombre_empresa': kwargs.get('nombre_empresa', '').strip(),
            'servicio_interes': kwargs.get('servicio_interes', 'otro'),
            'mensaje': kwargs.get('mensaje', '').strip(),
            'cantidad_empleados': kwargs.get('cantidad_empleados', ''),
            'origen': 'sitio_web',
        }

        try:
            modelo_solicitud = request.env['bitatech.solicitud.contacto'].sudo()
            modelo_solicitud.crear_desde_formulario(valores)
            _logger.info(
                'Solicitud de contacto creada desde sitio web: %s (%s)',
                valores.get('nombre_completo'),
                valores.get('correo'),
            )
        except Exception:
            _logger.exception('Error al crear solicitud de contacto desde formulario web')

        return request.redirect('/bitatech/gracias')
