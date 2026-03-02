# Bitatech - Sitio Web

Modulo del sitio web corporativo de Bitatech para Odoo 19.

## Requisitos

- Odoo 19.0 (odoo.sh o servidor propio)
- Modulos base: `website`, `crm`, `mail`

## Instalacion

### En odoo.sh

1. Subir la carpeta `bitatech_sitio_web` al repositorio vinculado.
2. Ir a Aplicaciones > Actualizar lista de aplicaciones.
3. Buscar "Bitatech" e instalar "Bitatech - Sitio Web".

### En servidor propio

1. Copiar la carpeta `bitatech_sitio_web` al directorio de addons.
2. Agregar la ruta al parametro `--addons-path` en la configuracion de Odoo.
3. Reiniciar el servicio de Odoo.
4. Ir a Aplicaciones > Actualizar lista de aplicaciones.
5. Buscar "Bitatech" e instalar.

## Estructura

```
bitatech_sitio_web/
    __init__.py
    __manifest__.py
    controllers/
        __init__.py
        controlador_contacto.py
    models/
        __init__.py
        solicitud_contacto.py
    security/
        ir.model.access.csv
    data/
        correo_contacto_plantilla.xml
        menus_sitio_web.xml
    views/
        disposicion_bitatech.xml
        pagina_inicio.xml
        pagina_servicios.xml
        pagina_nosotros.xml
        pagina_contacto.xml
        pagina_landing_campana.xml
        pagina_gracias.xml
        solicitud_contacto_vistas.xml
        menu_backend.xml
    static/
        src/
            css/
                bitatech_estilos.css
            js/
                bitatech_sitio.js
```

## Paginas

| URL | Descripcion |
|-----|-------------|
| `/bitatech` | Pagina de inicio |
| `/bitatech/servicios` | Detalle de los 5 servicios |
| `/bitatech/nosotros` | Mision, vision, valores, comparativa |
| `/bitatech/contacto` | Formulario de contacto completo |
| `/bitatech/diagnostico` | Landing de campana (Google Ads) |
| `/bitatech/gracias` | Pagina post-envio |

## Backend

- Menu: Bitatech > Solicitudes de Contacto
- Vistas: Kanban (agrupado por estado), Lista, Formulario
- Integracion automatica con CRM (crea oportunidad)
- Notificacion por correo al recibir solicitud

## Version

19.0.1.0.0
