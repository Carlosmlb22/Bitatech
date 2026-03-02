import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ControladorBitatech(http.Controller):

    @http.route(
        ['/bitatech', '/bitatech/'],
        type='http',
        auth='public',
        website=True,
        sitemap=True,
    )
    def pagina_landing(self, **kwargs):
        """Renderiza la landing page principal de Bitatech."""
        return request.render('bitatech_sitio_web.pagina_landing_bitatech')

    @http.route(
        '/bitatech/diagnostico/enviar',
        type='http',
        auth='public',
        website=True,
        methods=['POST'],
        csrf=True,
    )
    def enviar_diagnostico(self, **post):
        """Recibe el formulario de diagnostico BSI y crea la solicitud."""
        valores = {
            'nombre': post.get('nombre', '').strip(),
            'empresa': post.get('empresa', '').strip(),
            'correo': post.get('correo', '').strip(),
            'telefono': post.get('telefono', '').strip(),
            'tamano_equipo': post.get('tamano_equipo', ''),
            'facturacion_aproximada': post.get('facturacion_aproximada', ''),
            'principal_dolor': post.get('principal_dolor', ''),
            'mensaje': post.get('mensaje', '').strip(),
        }

        # Validacion basica
        if not valores['nombre'] or not valores['empresa'] or not valores['correo']:
            return request.render(
                'bitatech_sitio_web.pagina_landing_bitatech',
                {'error': 'Por favor completa los campos obligatorios.'},
            )

        try:
            request.env['bitatech.solicitud.diagnostico'].sudo().create(valores)
            _logger.info(
                "Solicitud BSI recibida de: %s - %s",
                valores['nombre'],
                valores['empresa'],
            )
        except Exception as e:
            _logger.error("Error creando solicitud BSI: %s", str(e))
            return request.render(
                'bitatech_sitio_web.pagina_landing_bitatech',
                {'error': 'Ocurrio un error. Intenta nuevamente.'},
            )

        return request.render(
            'bitatech_sitio_web.pagina_diagnostico_exito',
        )
