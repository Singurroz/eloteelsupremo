#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el documento Word con el plan de fases Elote El Supremo."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

OUTPUT = Path(__file__).resolve().parent.parent / 'Elote_El_Supremo_Plan_de_Fases.docx'


def set_cell_shading(cell, hex_color):
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), hex_color)
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)


def add_table(doc, headers, rows, header_color='2E4057'):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        set_cell_shading(hdr[i], header_color)
        for p in hdr[i].paragraphs:
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(10)
    for ri, row in enumerate(rows):
        cells = table.rows[ri + 1].cells
        for ci, val in enumerate(row):
            cells[ci].text = str(val)
            for p in cells[ci].paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
    doc.add_paragraph()


def status_icon(st):
    return {'✅': 'Completa', '🔶': 'Parcial', '⏳': 'Pendiente'}.get(st, st)


def build_document():
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

    title = doc.add_heading('Elote El Supremo — Banco Supremo', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sub = doc.add_paragraph('Plan de fases y estado del proyecto')
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.runs[0].font.size = Pt(14)
    sub.runs[0].font.italic = True

    meta = doc.add_paragraph(
        'Odoo 19 Community · Repositorio: extra-addons/eloteelsupremo · '
        'Versión módulo: 19.0.2.0.0'
    )
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.runs[0].font.size = Pt(10)
    meta.runs[0].font.color.rgb = RGBColor(100, 100, 100)

    doc.add_paragraph()
    doc.add_heading('Leyenda de estados', level=2)
    add_table(doc, ['Símbolo', 'Significado'], [
        ['✅', 'Completa'],
        ['🔶', 'Parcial (base lista, falta pulir o validar)'],
        ['⏳', 'Pendiente'],
    ], '555555')

    doc.add_heading('Vista general', level=1)
    add_table(doc, ['Fase', 'Nombre', 'Estado'], [
        ['1', 'Core Banco Supremo', '✅ Completa'],
        ['2', 'QR gráfico, POS avanzado, PWA básica', '✅ Completa'],
        ['3', 'Pruebas en instancia real', '⏳ Pendiente (actual)'],
        ['4', 'Sitio web comercial', '⏳ Pendiente'],
        ['5', 'Operación en sucursales (refinamiento)', '🔶 Parcial'],
        ['6', 'Fiscal México (CFDI)', '⏳ Pendiente'],
        ['7', 'App móvil / PWA avanzada', '🔶 Parcial'],
    ])

    # --- FASE 1 ---
    doc.add_page_break()
    doc.add_heading('FASE 1 — Core Banco Supremo ✅', level=1)
    doc.add_paragraph(
        'Base del ecosistema Moned Supreme + Puntos Supremos. Incluye módulos, '
        'programas de fidelidad, reglas de negocio, pagos sin pasarela, portal, POS y configuración admin.'
    )

    doc.add_heading('1.1 Módulos creados', level=2)
    add_table(doc, ['Subfase', 'Módulo', 'Estado'], [
        ['1.1.1', 'eloteelsupremo_base', '✅'],
        ['1.1.2', 'eloteelsupremo_wallet', '✅'],
        ['1.1.3', 'eloteelsupremo_loyalty', '✅'],
        ['1.1.4', 'eloteelsupremo_payment', '✅'],
        ['1.1.5', 'eloteelsupremo_website', '✅'],
        ['1.1.6', 'eloteelsupremo_pos', '✅'],
        ['1.1.7', 'eloteelsupremo (meta-app)', '✅'],
    ])

    doc.add_heading('1.2 Programas de fidelidad', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['1.2.1', 'Programa Moned Supreme (eWallet)', '✅'],
        ['1.2.2', 'Programa Puntos Supremos (loyalty)', '✅'],
        ['1.2.3', 'Producto Recarga Moned Supreme', '✅'],
        ['1.2.4', 'Campo supreme_program_kind en programas', '✅'],
    ])

    doc.add_heading('1.3 Reglas de negocio (backend)', level=2)
    add_table(doc, ['Subfase', 'Regla', 'Estado'], [
        ['1.3.1', 'Bono +10% al recargar (POS y web)', '✅'],
        ['1.3.2', '+5% Puntos Supremos al pagar con Moned (web + POS)', '✅'],
        ['1.3.3', '-5% descuento al pagar con Moned (web)', '✅'],
        ['1.3.4', 'Número de miembro Supremo (secuencia #350…)', '✅'],
        ['1.3.5', 'Tarjetas loyalty automáticas por cliente', '✅'],
    ])

    doc.add_heading('1.4 Pagos sin pasarela', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['1.4.1', 'Proveedor Recarga / Pago en sucursal', '✅'],
        ['1.4.2', 'Método de pago store_payment', '✅'],
        ['1.4.3', 'Pedido web pendiente hasta pagar en tienda', '✅'],
    ])

    doc.add_heading('1.5 Portal web básico', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['1.5.1', 'Ruta /my/banco-supremo', '✅'],
        ['1.5.2', 'Saldo Moned Supreme y Puntos Supremos', '✅'],
        ['1.5.3', 'Enlace en Mi cuenta', '✅'],
        ['1.5.4', 'QR identificación', '✅ (mejorado en Fase 2)'],
        ['1.5.5', 'Generar QR de pago desde portal', '✅'],
    ])

    doc.add_heading('1.6 POS básico', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['1.6.1', 'Escaneo de códigos SUPREMO:…', '✅'],
        ['1.6.2', 'QR identificación → bienvenida + saldo', '✅'],
        ['1.6.3', 'QR pago → débito Moned Supreme', '✅'],
        ['1.6.4', 'Opción QR Banco Supremo en config POS', '✅'],
    ])

    doc.add_heading('1.7 Configuración admin', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['1.7.1', 'Ventas → Configuración → Banco Supremo', '✅'],
        ['1.7.2', 'Menú Banco Supremo (programas, tokens QR)', '✅'],
        ['1.7.3', 'Seguridad Odoo 19 (user_ids, privilege)', '✅'],
    ])

    doc.add_heading('1.8 Instalación', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['1.8.1', 'Instalable en BD eloteelsupremo', '✅'],
        ['1.8.2', 'Fixes Odoo 19 (security, payment, XML, portal)', '✅'],
        ['1.8.3', 'README del repositorio', '✅'],
    ])

    # --- FASE 2 ---
    doc.add_page_break()
    doc.add_heading('FASE 2 — Mejoras operativas ✅', level=1)

    doc.add_heading('2.1 QR gráfico en portal', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['2.1.1', 'Imagen QR escaneable (/report/barcode/QR/…)', '✅'],
        ['2.1.2', 'QR identificación como imagen', '✅'],
        ['2.1.3', 'QR de pago como imagen', '✅'],
    ])

    doc.add_heading('2.2 Descuento 5% en POS', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['2.2.1', 'Carga de % desde config al POS', '✅'],
        ['2.2.2', 'Campo supreme_program_kind en datos POS', '✅'],
        ['2.2.3', 'Parche JS al aplicar eWallet Moned Supreme', '✅'],
        ['2.2.4', 'Validado en pruebas reales', '⏳ Fase 3'],
    ])

    doc.add_heading('2.3 QR de pago vinculado a orden POS', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['2.3.1', 'Token QR estado reserved', '✅'],
        ['2.3.2', 'Escaneo con orden abierta → reserva + eWallet', '✅'],
        ['2.3.3', 'Campo supreme_qr_token_id en orden POS', '✅'],
        ['2.3.4', 'Cierre token al confirmar venta', '✅'],
        ['2.3.5', 'Pago standalone sin orden', '✅'],
        ['2.3.6', 'Cron expiración tokens (5 min)', '✅'],
        ['2.3.7', 'Validado en pruebas reales', '⏳ Fase 3'],
    ])

    doc.add_heading('2.4 PWA básica', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['2.4.1', 'Manifest /eloteelsupremo/manifest.webmanifest', '✅'],
        ['2.4.2', 'Meta tags Agregar a inicio', '✅'],
        ['2.4.3', 'Iconos propios de marca', '⏳'],
        ['2.4.4', 'Service worker / offline', '⏳'],
    ])

    doc.add_heading('2.5 Calidad de código', level=2)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['2.5.1', 'author / license en todos los manifests', '⏳'],
        ['2.5.2', 'Tests automatizados Odoo', '⏳'],
        ['2.5.3', 'Repositorio git inicializado', '⏳'],
    ])

    # --- FASE 3 ---
    doc.add_page_break()
    doc.add_heading('FASE 3 — Pruebas en instancia ⏳ (ACTUAL)', level=1)
    doc.add_paragraph(
        'Validar que todo funciona en la instancia real (BD eloteelsupremo, '
        'http://127.0.0.1:10019).'
    )

    doc.add_heading('3.1 Preparación del entorno', level=2)
    add_table(doc, ['#', 'Check', 'Estado'], [
        ['3.1.1', 'BD correcta (eloteelsupremo)', '⏳'],
        ['3.1.2', 'Módulo instalado/actualizado', '✅'],
        ['3.1.3', 'Programas loyalty visibles', '⏳'],
        ['3.1.4', 'Recarga en POS activa', '⏳'],
        ['3.1.5', 'Programas en config POS', '⏳'],
        ['3.1.6', 'Proveedor Pago en sucursal activo', '⏳'],
        ['3.1.7', 'Cliente de prueba con portal', '⏳'],
    ])

    doc.add_heading('3.2 Prueba recarga + bono 10%', level=2)
    add_table(doc, ['#', 'Escenario', 'Estado'], [
        ['3.2.1', 'POS: $300 efectivo → 330 MS', '⏳'],
        ['3.2.2', 'Historial loyalty correcto', '⏳'],
        ['3.2.3', 'Recarga vía web + pago en sucursal', '⏳'],
    ])

    doc.add_heading('3.3 Prueba portal', level=2)
    add_table(doc, ['#', 'Escenario', 'Estado'], [
        ['3.3.1', '/my/banco-supremo muestra saldos', '⏳'],
        ['3.3.2', 'QR identificación (imagen)', '⏳'],
        ['3.3.3', 'QR pago $100 generado', '⏳'],
    ])

    doc.add_heading('3.4 Prueba POS + Moned Supreme', level=2)
    add_table(doc, ['#', 'Escenario', 'Estado'], [
        ['3.4.1', 'Venta $200 pagada con eWallet', '⏳'],
        ['3.4.2', 'Descuento ~5% (~$190 cobrados)', '⏳'],
        ['3.4.3', '+10 Puntos Supremos (5% de $200)', '⏳'],
    ])

    doc.add_heading('3.5 Prueba QR en caja', level=2)
    add_table(doc, ['#', 'Escenario', 'Estado'], [
        ['3.5.1', 'QR identificación', '⏳'],
        ['3.5.2', 'QR pago con orden abierta', '⏳'],
        ['3.5.3', 'QR expirado / token usado', '⏳'],
    ])

    doc.add_heading('3.6 Prueba eCommerce', level=2)
    add_table(doc, ['#', 'Escenario', 'Estado'], [
        ['3.6.1', 'Checkout sin PayPal (pago en sucursal)', '⏳'],
        ['3.6.2', 'Checkout pagando con Moned Supreme', '⏳'],
        ['3.6.3', 'Promociones web', '⏳'],
    ])

    doc.add_heading('3.7 Corrección de bugs', level=2)
    add_table(doc, ['#', 'Actividad', 'Estado'], [
        ['3.7.1', 'Documentar incidencias', '⏳'],
        ['3.7.2', 'Fixes según resultados', '⏳'],
    ])

    # --- FASE 4-7 ---
    doc.add_page_break()
    doc.add_heading('FASE 4 — Sitio web comercial ⏳', level=1)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['4.1.1', 'Página principal / branding', '⏳'],
        ['4.1.2', 'Catálogo productos completo', '⏳'],
        ['4.1.3', 'Promociones destacadas (snippets)', '⏳'],
        ['4.1.4', 'Videos embebidos', '⏳'],
        ['4.2.1', 'Página Descargar app', '⏳'],
        ['4.2.2', 'Links Android / iOS', '⏳'],
        ['4.3.1', 'Confirmar si web es Odoo o externa', '⏳'],
        ['4.3.2', 'Unificar diseño / dominio', '⏳'],
    ])

    doc.add_heading('FASE 5 — Operación en sucursales 🔶', level=1)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['5.1.1', 'Popup grande al escanear QR', '⏳'],
        ['5.1.2', 'Flujo recarga tiempo aire optimizado', '⏳'],
        ['5.1.3', 'Cancelar token reservado si abortan venta', '🔶'],
        ['5.2.1', 'Diseño tarjeta virtual', '⏳'],
        ['5.2.2', 'Impresión / PDF tarjeta', '⏳'],
        ['5.3.1', 'Varios POS con mismas reglas', '⏳'],
        ['5.3.2', 'Reportes por sucursal', '⏳'],
        ['5.4.1', 'Reporte recargas del día', '⏳'],
        ['5.4.2', 'Reporte movimientos Moned / Puntos', '⏳'],
        ['5.4.3', 'Tokens QR usados/expirados', '🔶'],
    ])

    doc.add_heading('FASE 6 — Fiscal México (CFDI) ⏳', level=1)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['6.1', 'Factura por recarga Moned Supreme', '⏳'],
        ['6.2', 'Factura por venta pagada con Moned', '⏳'],
        ['6.3', 'Integración con modulo_sat / CFDI', '⏳'],
        ['6.4', 'Asesoría legal monedero electrónico', '⏳'],
    ])

    doc.add_heading('FASE 7 — App móvil / PWA avanzada 🔶', level=1)
    add_table(doc, ['Subfase', 'Entregable', 'Estado'], [
        ['7.1', 'PWA con iconos de marca', '🔶'],
        ['7.2', 'Notificaciones push', '⏳'],
        ['7.3', 'App nativa (React / Flutter)', '⏳'],
        ['7.4', 'API REST documentada', '⏳'],
    ])

    # Resumen
    doc.add_page_break()
    doc.add_heading('Resumen numérico', level=1)
    add_table(doc, ['Estado', 'Cantidad aprox.'], [
        ['✅ Completas (Fase 1 + 2 core)', '~45 subfases'],
        ['🔶 Parciales', '~8 subfases'],
        ['⏳ Pendientes (Fase 3–7)', '~35 subfases'],
    ])

    doc.add_heading('Próximo paso', level=1)
    doc.add_paragraph(
        'Fase 3.1 — Checklist de preparación: confirmar BD eloteelsupremo, programas '
        'Moned Supreme y Puntos Supremos, producto Recarga en POS, cliente de prueba con portal.'
    )
    doc.add_paragraph(
        'Orden recomendado post-pruebas: Fase 3 → Fase 4 (web comercial) → '
        'Fase 5 (UX sucursal) → Fase 6 (CFDI).'
    )

    doc.add_heading('Guía rápida de pruebas (Fase 3)', level=1)
    tests = [
        ('3.2', 'Recarga POS', 'Paga $300 en efectivo → debe quedar 330 MS (+10%)'),
        ('3.3', 'Portal', 'Entrar a /my/banco-supremo → ver saldo y QR imagen'),
        ('3.4', 'POS eWallet', 'Venta $200 → paga ~$190 MS + 10 puntos'),
        ('3.5', 'QR caja', 'Escanear QR identificación y QR pago'),
        ('3.6', 'Web', 'Checkout con Pago en sucursal o Moned Supreme'),
    ]
    add_table(doc, ['Prueba', 'Nombre', 'Resultado esperado'], tests)

    doc.add_heading('Comando de actualización', level=2)
    cmd = doc.add_paragraph()
    cmd.add_run(
        '/opt/odoo19/odoo19v/bin/python3 /opt/odoo19/odoo/odoo-bin '
        '-c /opt/odoo19/config/odoo19.conf -d eloteelsupremo '
        '-u eloteelsupremo --stop-after-init'
    ).font.name = 'Courier New'
    cmd.runs[0].font.size = Pt(9)

    doc.save(OUTPUT)
    return OUTPUT


if __name__ == '__main__':
    path = build_document()
    print(f'Documento generado: {path}')
