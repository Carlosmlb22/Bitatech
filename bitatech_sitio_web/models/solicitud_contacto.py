# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

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
        group_expand='_group_expand_estados',
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
    # Metodo de grupo expand para kanban
    # ------------------------------------------------------------------
    @api.model
    def _group_expand_estados(self, states, domain):
        return [clave for clave, _etiqueta in OPCIONES_ESTADO]

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
            plantilla = self.env.ref(
                'bitatech_sitio_web.correo_nueva_solicitud_contacto',
                raise_if_not_found=False,
            )
            if plantilla:
                plantilla.sudo().send_mail(solicitud.id, force_send=True)
        except Exception:
            _logger.exception(
                'No se pudo enviar correo de notificacion para solicitud %s',
                solicitud.id,
            )

        return solicitud
