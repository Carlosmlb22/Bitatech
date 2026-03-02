import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class SolicitudDiagnostico(models.Model):
    _name = 'bitatech.solicitud.diagnostico'
    _description = 'Solicitud de Diagnostico BSI'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # ------------------------------------------------------------------
    # Campos del formulario
    # ------------------------------------------------------------------
    nombre = fields.Char(
        string='Nombre completo',
        required=True,
        tracking=True,
    )
    empresa = fields.Char(
        string='Empresa',
        required=True,
        tracking=True,
    )
    correo = fields.Char(
        string='Correo electronico',
        required=True,
        tracking=True,
    )
    telefono = fields.Char(
        string='Telefono',
        tracking=True,
    )
    tamano_equipo = fields.Selection(
        selection=[
            ('1-5', '1 a 5 personas'),
            ('6-15', '6 a 15 personas'),
            ('16-30', '16 a 30 personas'),
            ('31-50', '31 a 50 personas'),
            ('50+', 'Mas de 50 personas'),
        ],
        string='Tamano del equipo',
        tracking=True,
    )
    facturacion_aproximada = fields.Selection(
        selection=[
            ('menos_50k', 'Menos de USD 50,000/mes'),
            ('50k_150k', 'USD 50,000 - 150,000/mes'),
            ('150k_500k', 'USD 150,000 - 500,000/mes'),
            ('500k_1m', 'USD 500,000 - 1,000,000/mes'),
            ('mas_1m', 'Mas de USD 1,000,000/mes'),
        ],
        string='Facturacion aproximada',
        tracking=True,
    )
    principal_dolor = fields.Selection(
        selection=[
            ('dependencia_dueno', 'Todo depende de mi como dueno'),
            ('caos_operativo', 'Caos operativo y procesos manuales'),
            ('sin_metricas', 'No tengo metricas claras de mi negocio'),
            ('herramientas_desconectadas', 'Uso muchas herramientas sin integracion'),
            ('escalar', 'Quiero escalar pero la operacion no lo permite'),
            ('otro', 'Otro'),
        ],
        string='Principal dolor operativo',
        tracking=True,
    )
    mensaje = fields.Text(
        string='Mensaje adicional',
    )
    estado = fields.Selection(
        selection=[
            ('nuevo', 'Nuevo'),
            ('contactado', 'Contactado'),
            ('diagnostico', 'En Diagnostico'),
            ('propuesta', 'Propuesta Enviada'),
            ('cerrado_ganado', 'Cerrado - Ganado'),
            ('cerrado_perdido', 'Cerrado - Perdido'),
        ],
        string='Estado',
        default='nuevo',
        tracking=True,
    )
    lead_id = fields.Many2one(
        'crm.lead',
        string='Oportunidad CRM',
        readonly=True,
    )
    notas_internas = fields.Html(
        string='Notas internas',
    )

    # ------------------------------------------------------------------
    # Metodos
    # ------------------------------------------------------------------
    def name_get(self):
        resultado = []
        for registro in self:
            nombre = f"[{registro.empresa}] {registro.nombre}"
            resultado.append((registro.id, nombre))
        return resultado

    @api.model_create_multi
    def create(self, vals_list):
        registros = super().create(vals_list)
        for registro in registros:
            registro._crear_lead_si_crm()
            registro._enviar_notificacion()
        return registros

    def _crear_lead_si_crm(self):
        """Crea un lead en CRM si el modulo esta instalado."""
        self.ensure_one()
        try:
            modulo_crm = self.env['ir.module.module'].sudo().search([
                ('name', '=', 'crm'),
                ('state', '=', 'installed'),
            ], limit=1)
            if modulo_crm:
                dolor_texto = dict(
                    self._fields['principal_dolor'].selection
                ).get(self.principal_dolor, '')
                lead = self.env['crm.lead'].sudo().create({
                    'name': f"BSI - {self.empresa}",
                    'partner_name': self.empresa,
                    'contact_name': self.nombre,
                    'email_from': self.correo,
                    'phone': self.telefono,
                    'description': (
                        f"Dolor principal: {dolor_texto}\n"
                        f"Tamano equipo: {self.tamano_equipo}\n"
                        f"Facturacion: {self.facturacion_aproximada}\n\n"
                        f"Mensaje: {self.mensaje or 'Sin mensaje adicional'}"
                    ),
                    'type': 'opportunity',
                })
                self.lead_id = lead.id
                _logger.info(
                    "Lead CRM creado para solicitud BSI: %s", self.empresa
                )
        except Exception as e:
            _logger.warning("No se pudo crear lead CRM: %s", str(e))

    def _enviar_notificacion(self):
        """Envia correo de notificacion interna."""
        self.ensure_one()
        try:
            plantilla = self.env.ref(
                'bitatech_sitio_web.correo_diagnostico_plantilla',
                raise_if_not_found=False,
            )
            if plantilla:
                plantilla.sudo().send_mail(self.id, force_send=True)
                _logger.info(
                    "Notificacion enviada para solicitud BSI: %s",
                    self.empresa,
                )
        except Exception as e:
            _logger.warning("Error enviando notificacion: %s", str(e))

    def accion_marcar_contactado(self):
        self.write({'estado': 'contactado'})

    def accion_marcar_diagnostico(self):
        self.write({'estado': 'diagnostico'})

    def accion_enviar_propuesta(self):
        self.write({'estado': 'propuesta'})

    def accion_cerrar_ganado(self):
        self.write({'estado': 'cerrado_ganado'})

    def accion_cerrar_perdido(self):
        self.write({'estado': 'cerrado_perdido'})
