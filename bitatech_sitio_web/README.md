# Bitatech - Sitio Web

Modulo Odoo 18 para la landing page oficial de Bitatech.

## Requisitos

- Odoo 18 Community o Enterprise
- Modulo `website` instalado
- Modulo `mail` instalado
- (Opcional) Modulo `crm` para creacion automatica de leads

## Instalacion

1. Copiar la carpeta `bitatech_sitio_web` al directorio de addons de Odoo
2. Reiniciar el servicio de Odoo
3. Ir a Aplicaciones > Actualizar lista de aplicaciones
4. Buscar "Bitatech" e instalar

## Configuracion

- La landing esta disponible en `/bitatech`
- Las solicitudes se gestionan desde el menu Bitatech > Solicitudes BSI
- Si CRM esta instalado, cada solicitud crea un lead automaticamente
- La plantilla de correo se puede editar desde Ajustes > Tecnico > Plantillas de correo

## Estructura

```
bitatech_sitio_web/
  __manifest__.py
  __init__.py
  controllers/
    __init__.py
    controlador_principal.py
  models/
    __init__.py
    solicitud_diagnostico.py
  views/
    pagina_landing.xml
    solicitud_diagnostico_vistas.xml
    menu_bitatech.xml
  snippets/
    sello_bitatech.xml
    llamado_diagnostico.xml
  data/
    correo_diagnostico_plantilla.xml
  security/
    ir.model.access.csv
  static/
    src/
      css/bitatech_estilos.css
      js/bitatech_formulario.js
      img/
    description/
      icon.png
```

## Notas

- El texto visible NO menciona Odoo en ningun lugar
- El naming tecnico esta en espanol
- Los snippets son reutilizables desde el editor web
- El formulario incluye proteccion CSRF y validacion client-side
