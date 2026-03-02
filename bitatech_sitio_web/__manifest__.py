# -*- coding: utf-8 -*-
{
    'name': 'Bitatech - Sitio Web',
    'version': '19.0.1.0.0',
    'summary': 'Sitio web corporativo de Bitatech - Sistemas Empresariales Inteligentes',
    'description': """
        Modulo completo del sitio web de Bitatech.
        Incluye landing pages, formulario de contacto, integracion con CRM
        y panel de administracion de solicitudes.
    """,
    'category': 'Website',
    'author': 'Bitatech',
    'website': 'https://www.bitatech.co',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'crm',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/correo_contacto_plantilla.xml',
        'data/menus_sitio_web.xml',
        'views/disposicion_bitatech.xml',
        'views/pagina_inicio.xml',
        'views/pagina_servicios.xml',
        'views/pagina_planes.xml',
        'views/pagina_nosotros.xml',
        'views/pagina_contacto.xml',
        'views/pagina_landing_campana.xml',
        'views/pagina_gracias.xml',
        'views/solicitud_contacto_vistas.xml',
        'views/menu_backend.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'bitatech_sitio_web/static/src/css/bitatech_estilos.css',
            'bitatech_sitio_web/static/src/js/bitatech_sitio.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
