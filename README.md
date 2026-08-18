# Elote El Supremo — Banco Supremo (Odoo 19 Community)

Módulos para el ecosistema **Moned Supreme** / **Puntos Supremos** de Elote El Supremo.

## Instalación

1. Asegúrate de que la ruta `extra-addons/eloteelsupremo` esté en `addons_path`.
2. Actualiza la lista de aplicaciones en Odoo.
3. Instala **Elote El Supremo** (`eloteelsupremo`).
4. Actualiza los módulos tras cada fase: `-u eloteelsupremo`.

## Módulos

| Módulo | Función |
|--------|---------|
| `eloteelsupremo_base` | Programas loyalty, producto recarga, configuración |
| `eloteelsupremo_wallet` | Moned Supreme, tokens QR, bono 10% recarga |
| `eloteelsupremo_loyalty` | Puntos Supremos, reglas 5%+5%, descuento POS |
| `eloteelsupremo_payment` | Proveedor "Pago en sucursal" (sin pasarela) |
| `eloteelsupremo_website` | Portal `/my/banco-supremo`, QR gráfico, PWA |
| `eloteelsupremo_pos` | Escaneo QR en caja + pago vinculado a orden |
| `eloteelsupremo` | Meta-módulo (instala todo) |

## Fase 2 (implementada)

- **QR gráfico** en portal (`/report/barcode/QR/…`)
- **Descuento 5%** automático en POS al pagar con Moned Supreme
- **QR de pago vinculado** a la orden POS activa (token reservado → eWallet → confirmación)
- **PWA básica**: manifest en `/eloteelsupremo/manifest.webmanifest`

## Configuración inicial

1. **Ventas → Configuración → Banco Supremo**: porcentajes de bono, descuento y puntos.
2. **Contabilidad → Proveedores de pago**: desactiva PayPal; deja activo **Recarga / Pago en sucursal**.
3. **Punto de venta**: agrega *Recarga Moned Supreme* y programas Moned Supreme / Puntos Supremos.
4. **Website**: clientes en `/my/banco-supremo` ven saldo y QR escaneables.

## Flujos

### Recarga en sucursal (efectivo)
POS → producto *Recarga Moned Supreme* → acreditación 1:1 + **10% bono**.

### Compra con Moned Supreme (web o POS)
Pago con wallet → **5% descuento** + **5% Puntos Supremos** (automático).

### QR en tienda
| QR | Acción en caja |
|----|----------------|
| Identificación | Asigna cliente y muestra saldo |
| Pago (con orden) | Reserva token, aplica eWallet con descuento 5% |
| Pago (sin orden) | Débito directo del saldo |

## Próximos pasos (Fase 3 — pruebas)

- Instalar y probar flujo completo en instancia de staging
- CFDI México para recargas
- Iconos PWA personalizados
- App móvil nativa (opcional)
