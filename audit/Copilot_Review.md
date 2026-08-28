Críticos

• Aislamiento multiempresa roto: varias vistas consultan objetos solo por  id , permitiendo acceder o modificar datos de otra empresa ( inventory/views.py ,  products/views.py ,  purchases/views/purchase.py ,  fiscal/views/fiscal_invoice.py ).
• Selector de empresas expone todos los tenants:  company/views/select.py:14  usa  Company.objects.all()  y acepta cualquier ID en  set_active_company .
• Permisos insuficientes:  RolePermissionMiddleware  solo verifica permisos  can_view_* ; las operaciones de escritura no validan permisos de edición.
• Eliminación pública por GET:  fiscal/views/electronic_voucher_book.py:27-33  no exige autenticación y elimina registros mediante GET.
• Configuración insegura comprometida:  config/settings.py  contiene  SECRET_KEY , credenciales MySQL,  DEBUG=True  y  ALLOWED_HOSTS=[] .
• Cookies de sesión registradas en logs:  core/views/auth.py:14-26  puede permitir secuestro de sesiones.
• Datos de clientes expuestos sin autenticación:  customers/views.py  permite listar y crear clientes sin filtrar por empresa.

Errores funcionales y de integridad

•  JournalEntry.clean()  usa campos inexistentes  Period.is_closed  e  is_locked .
•  JournalEntryLine.clean()  usa  Account.type , pero el campo es  account_type .
• Los reportes de balance llaman métodos inexistentes o con firmas incorrectas.
• Integraciones de ventas, compras e inventario usan campos y relaciones que no existen.
• La creación de proveedores asigna un modelo de perfil fiscal incompatible.
• Hay dos implementaciones incompatibles de  CompanyProfile ; además se asignan campos inexistentes.
• Los movimientos de inventario aceptan cantidades negativas.
• Los formularios permiten seleccionar cuentas, productos y ubicaciones de otras empresas.
• La numeración de facturas fiscales es vulnerable a condiciones de carrera.
• El subsistema  reports  no tiene rutas y contiene imports/campos inválidos.
• Varias plantillas usan nombres de URL sin namespace y producen  NoReverseMatch .
• El admin de contabilidad referencia  obj.level , que no existe, y usa incorrectamente  format_html .
•  accounting/scripts/load_chart_of_accounts.py:157  contiene un error de sintaxis.
• El handler 403 apunta a  core/errors/403.html , pero la plantilla está en otra ruta.
• Las eliminaciones y cambios de períodos contables usan GET y no exigen permisos de escritura.

 manage.py check  y los tests existentes pasan: 14 tests, pero  check --deploy  reporta 7 advertencias de seguridad. No modifiqué archivos.
