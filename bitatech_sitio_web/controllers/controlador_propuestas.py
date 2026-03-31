# -*- coding: utf-8 -*-
import os
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ControladorPropuestas(http.Controller):
    """Controlador para servir propuestas comerciales como paginas dedicadas."""

    @http.route(
        '/propuesta/sip',
        type='http',
        auth='public',
        website=False,
        csrf=False,
        sitemap=False,
    )
    def propuesta_sip(self, **kwargs):
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(
            module_path, 'static', 'src', 'propuestas', 'sip.html'
        )
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return request.make_response(
                html_content,
                headers=[('Content-Type', 'text/html; charset=utf-8')],
            )
        except FileNotFoundError:
            _logger.error('Propuesta SIP no encontrada: %s', file_path)
            return request.not_found()

    @http.route(
        '/propuesta/sistecomp',
        type='http',
        auth='public',
        website=False,
        csrf=False,
        sitemap=False,
    )
    def propuesta_sistecomp(self, **kwargs):
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(
            module_path, 'static', 'src', 'propuestas', 'sistecomp.html'
        )
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return request.make_response(
                html_content,
                headers=[('Content-Type', 'text/html; charset=utf-8')],
            )
        except FileNotFoundError:
            _logger.error('Propuesta Sistecomp no encontrada: %s', file_path)
            return request.not_found()
