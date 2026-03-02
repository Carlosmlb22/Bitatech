{
    'name': 'Bitatech - Sitio Web',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Landing profesional y formulario de diagnostico BSI para Bitatech',
    'description': """
        Modulo web completo para Bitatech - Sistemas Empresariales Inteligentes.
        Incluye landing page, formulario de diagnostico BSI, snippets reutilizables
        y gestion de solicitudes.
    """,
    'author': 'Bitatech',
    'website': 'https://bitatech.ai',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/correo_diagnostico_plantilla.xml',
        'views/solicitud_diagnostico_vistas.xml',
        'views/menu_bitatech.xml',
        'views/pagina_landing.xml',
        'snippets/sello_bitatech.xml',
        'snippets/llamado_diagnostico.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'bitatech_sitio_web/static/src/css/bitatech_estilos.css',
            'bitatech_sitio_web/static/src/js/bitatech_formulario.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
