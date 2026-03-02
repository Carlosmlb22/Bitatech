# -*- coding: utf-8 -*-
import logging
from markupsafe import Markup
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

CORREO_NOTIFICACION = 'info@bitatech.ai'

OPCIONES_SERVICIO = [
    ('erp', 'Implementacion ERP'),
    ('automatizacion', 'Automatizacion Avanzada'),
    ('chat', 'Sistemas de Chat y Conversion'),
    ('optimizacion', 'Optimizacion Operativa'),
    ('desarrollo', 'Desarrollo a Medida'),
    ('otro', 'Otro'),
]

OPCIONES_EMPLEADOS = [
    ('1-5', '1 a 5 empleados'),
    ('6-15', '6 a 15 empleados'),
    ('16-50', '16 a 50 empleados'),
    ('51-200', '51 a 200 empleados'),
    ('200+', 'Mas de 200 empleados'),
]

OPCIONES_ORIGEN = [
    ('sitio_web', 'Sitio Web'),
    ('referido', 'Referido'),
    ('redes', 'Redes Sociales'),
    ('google', 'Google'),
    ('otro', 'Otro'),
]

OPCIONES_ESTADO = [
    ('nuevo', 'Nuevo'),
    ('contactado', 'Contactado'),
    ('diagnostico', 'Diagnostico'),
    ('propuesta', 'Propuesta'),
    ('ganado', 'Ganado'),
    ('cerrado', 'Cerrado'),
]


class SolicitudContactoBitatech(models.Model):
    _name = 'bitatech.solicitud.contacto'
    _description = 'Solicitud de Contacto Bitatech'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # --- Datos del formulario ---
    nombre_completo = fields.Char(
        string='Nombre Completo',
        required=True,
        tracking=True,
    )
    correo = fields.Char(
        string='Correo Electronico',
        required=True,
        tracking=True,
    )
    telefono = fields.Char(
        string='Telefono',
        tracking=True,
    )
    nombre_empresa = fields.Char(
        string='Empresa',
        tracking=True,
    )
    servicio_interes = fields.Selection(
        selection=OPCIONES_SERVICIO,
        string='Servicio de Interes',
        default='otro',
        tracking=True,
    )
    mensaje = fields.Text(
        string='Mensaje',
    )
    cantidad_empleados = fields.Selection(
        selection=OPCIONES_EMPLEADOS,
        string='Cantidad de Empleados',
        tracking=True,
    )

    # --- Campos internos ---
    origen = fields.Selection(
        selection=OPCIONES_ORIGEN,
        string='Origen',
        default='sitio_web',
        tracking=True,
    )
    estado = fields.Selection(
        selection=OPCIONES_ESTADO,
        string='Estado',
        default='nuevo',
        tracking=True,
    )
    oportunidad_crm_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Oportunidad CRM',
        tracking=True,
    )
    notas_internas = fields.Text(
        string='Notas Internas',
    )

    # ------------------------------------------------------------------
    # Compute
    # ------------------------------------------------------------------
    @api.depends('nombre_completo', 'nombre_empresa')
    def _compute_display_name(self):
        for registro in self:
            partes = [registro.nombre_completo or '']
            if registro.nombre_empresa:
                partes.append('(%s)' % registro.nombre_empresa)
            registro.display_name = ' '.join(partes) or 'Nueva Solicitud'

    # ------------------------------------------------------------------
    # Metodo publico de creacion desde formulario
    # ------------------------------------------------------------------
    @api.model
    def crear_desde_formulario(self, valores):
        """Crea la solicitud, genera un lead en CRM y envia notificacion."""
        solicitud = self.create(valores)

        # Crear oportunidad CRM vinculada
        etiqueta_servicio = dict(OPCIONES_SERVICIO).get(
            solicitud.servicio_interes, 'Otro'
        )
        lead_vals = {
            'name': 'Bitatech Web - %s - %s' % (
                solicitud.nombre_completo,
                etiqueta_servicio,
            ),
            'contact_name': solicitud.nombre_completo,
            'email_from': solicitud.correo,
            'phone': solicitud.telefono,
            'partner_name': solicitud.nombre_empresa,
            'description': solicitud.mensaje or '',
            'type': 'opportunity',
        }
        try:
            lead = self.env['crm.lead'].sudo().create(lead_vals)
            solicitud.write({'oportunidad_crm_id': lead.id})
        except Exception:
            _logger.exception(
                'No se pudo crear oportunidad CRM para solicitud %s',
                solicitud.id,
            )

        # Enviar correo de notificacion interna
        try:
            solicitud._enviar_correo_notificacion()
        except Exception:
            _logger.exception(
                'No se pudo enviar correo de notificacion para solicitud %s',
                solicitud.id,
            )

        return solicitud

    def _enviar_correo_notificacion(self):
        """Construye y envia el correo de notificacion directamente."""
        self.ensure_one()
        etiqueta_servicio = dict(OPCIONES_SERVICIO).get(
            self.servicio_interes, 'Otro'
        )
        etiqueta_empleados = dict(OPCIONES_EMPLEADOS).get(
            self.cantidad_empleados, ''
        )

        filas = ''
        datos = [
            ('Nombre', self.nombre_completo or ''),
            ('Correo', self.correo or ''),
            ('Telefono', self.telefono or ''),
            ('Empresa', self.nombre_empresa or ''),
            ('Servicio', etiqueta_servicio),
            ('Empleados', etiqueta_empleados),
            ('Mensaje', self.mensaje or ''),
        ]
        for label, valor in datos:
            if valor:
                filas += (
                    '<tr>'
                    '<td style="color:#999;width:160px;vertical-align:top;padding:8px;">%s:</td>'
                    '<td style="color:#fff;padding:8px;">%s</td>'
                    '</tr>'
                ) % (label, valor)

        body_html = (
            '<div style="margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;">'
            '<table width="600" cellpadding="0" cellspacing="0" style="margin:20px auto;border:1px solid #e0e0e0;border-radius:8px;overflow:hidden;">'
            '<tr><td style="background-color:#0a0a0a;padding:24px 32px;text-align:center;">'
            '<h1 style="color:#d4a843;margin:0;font-size:22px;letter-spacing:1px;">BITATECH</h1>'
            '<p style="color:#ccc;margin:4px 0 0;font-size:12px;">Sistemas Empresariales Inteligentes</p>'
            '</td></tr>'
            '<tr><td style="background-color:#1a1a1a;padding:32px;">'
            '<h2 style="color:#d4a843;margin:0 0 20px;font-size:18px;">Nueva Solicitud de Contacto</h2>'
            '<table width="100%%" cellpadding="0" cellspacing="0" style="color:#e0e0e0;font-size:14px;">'
            '%s'
            '</table>'
            '</td></tr>'
            '<tr><td style="background-color:#111;padding:16px 32px;text-align:center;">'
            '<p style="color:#666;margin:0;font-size:11px;">Bitatech - Sistemas Empresariales Inteligentes</p>'
            '</td></tr>'
            '</table></div>'
        ) % filas

        mail_values = {
            'subject': 'Nueva solicitud de contacto: %s' % self.nombre_completo,
            'email_from': CORREO_NOTIFICACION,
            'email_to': CORREO_NOTIFICACION,
            'body_html': Markup(body_html),
            'auto_delete': False,
        }
        correo = self.env['mail.mail'].sudo().create(mail_values)
        correo.send()
        _logger.info(
            'Correo de notificacion enviado para solicitud %s', self.id,
        )
