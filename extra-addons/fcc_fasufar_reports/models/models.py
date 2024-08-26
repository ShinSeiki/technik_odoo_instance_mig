# -*- coding: utf-8 -*-
import json
from datetime import datetime
from odoo import models, fields, api
import uuid

class AccountMove(models.Model):
    _inherit = 'account.move'
    condicionpago = fields.Char("Condición Pago", default="LETRA 60 DIAS")
    client_order_ref = fields.Char("Referencia del Cliente", )
    guiaremision = fields.Char("Guía Remision")
    observacion = fields.Text("Observación", default="""* Si el presente documento no es cancelado en su vencimiento se cobrarán intereses moratorios y compensatorios bancarios de acuerdo a ley.
* IMPORTANTE es nulo todo pago hecho a personas no autorizadas por la compañía.
* Después de 48 horas de recibido la mercadería se dará como aceptada/conforme.
    """)
    gravada = fields.Char(compute="_gravada")
    def _gravada(self):
        self.gravada=""
        for x in self.amount_by_group:
            if x[0]=='IGV':
                self.gravada= x[4]

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    motivo=fields.Char(compute="_motivo")
    def _motivo(self):
        self.motivo=""
        if self.pe_transfer_code:
            for a in self.env['pe.datas'].get_selection("PE.CPE.CATALOG20"):
                if self.pe_transfer_code==a[0]:
                    self.motivo = a[1]
                    return


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    def name_get(self):
        result = []
        for lote in self:
            if lote.life_date:
                formatted_date = lote.life_date.strftime('%Y-%m-%d')
                name = "%s [%s] (%s)" % (lote.name, formatted_date, lote.product_qty)
            else:
                name = "%s (%s)" % (lote.name,lote.product_qty)
            result.append((lote.id, name))
        return result




class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    life_date = fields.Datetime(related="lot_id.life_date")


class StockMove(models.Model):
    _inherit = 'stock.move'

    lote = fields.Char("Lote")
    fechavencimiento = fields.Date("Fecha de Vencimiento")


class StockMove(models.Model):
    _inherit = 'account.journal'
    letradecambio = fields.Boolean("Diario para letras de cambio", default=False)


class StockMove(models.Model):
    _inherit = 'account.payment'

    numero = fields.Char("Número de Letra de Cambio")
    referencia = fields.Char("Referencia de Girador")
    fechagiro = fields.Date("Fecha de Giro")
    fechavencimiento = fields.Date("Fecha de Vencimiento")
    lugargiro = fields.Char("Lugar de Giro")
    aval_partner_id = fields.Many2one("res.partner", "Aval")
    journal_id_letradecambio = fields.Boolean("Diario para letras de cambio", related="journal_id.letradecambio")


class SaleORderLine(models.Model):
    _inherit = 'sale.order.line'


    lote = fields.Char("Lote")
    fechavencimiento = fields.Date("Fecha de Vencimiento")
    unico=fields.Char("unico",default= uuid.uuid1().hex)

    def _prepare_invoice_line(self):
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id if not self.display_type else False,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
            'lote':self.lot_id.name,
            'fechavencimiento': self.lot_id.life_date,

        }
        if self.display_type:
            res['account_id'] = False
        return res


class SaleORder(models.Model):
    _inherit = 'purchase.order'

    fecha_formateada = fields.Char(string='Fecha Formateada', compute='_compute_fecha_formateada')
    grupodecompra = fields.Char("Grupo de Compra", default="LIMA")
    moneda = fields.Char("Moneda", default="PEN - SOL")
    condicionpago = fields.Char("Condición Pago", default="EFECTIVO")
    firma1 = fields.Char("Firma 1 ", default="V°.B AREA DE COMPRAS ")
    firma2 = fields.Char("Firma 2", default="V°.B ADMINISTRACION Y FINANZAS ")
    ordengravada = fields.Char("Orden Gravada",
                               default=" * Si la Orden Esta Gravada Con El IGV, Los Precios Estan Incluidos Con el IGV")

    @api.depends('date_order')
    def _compute_fecha_formateada(self):
        for record in self:
            if record.date_order:
                fecha_str = record.date_order.strftime("%Y-%m-%d")
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
                fecha_formateada = fecha_obj.strftime("%A %d de %B del %Y")
                record.fecha_formateada = fecha_formateada

    amount_to_text = fields.Char(
        compute="_amount_in_words", string="In Words", help="The amount in words"
    )

    @api.depends("amount_total", "partner_id", "partner_id.lang")
    def _amount_in_words(self):
        self.amount_to_text = self.numero_a_cheque(self.amount_total)

    MONEDA_SINGULAR = 'dolar'
    MONEDA_PLURAL = 'dolares'

    CENTIMOS_SINGULAR = 'centavo'
    CENTIMOS_PLURAL = 'centavos'

    MAX_NUMERO = 999999999999

    UNIDADES = (
        'cero',
        'uno',
        'dos',
        'tres',
        'cuatro',
        'cinco',
        'seis',
        'siete',
        'ocho',
        'nueve'
    )

    DECENAS = (
        'diez',
        'once',
        'doce',
        'trece',
        'catorce',
        'quince',
        'dieciseis',
        'diecisiete',
        'dieciocho',
        'diecinueve'
    )

    DIEZ_DIEZ = (
        'cero',
        'diez',
        'veinte',
        'treinta',
        'cuarenta',
        'cincuenta',
        'sesenta',
        'setenta',
        'ochenta',
        'noventa'
    )

    CIENTOS = (
        '_',
        'ciento',
        'doscientos',
        'trescientos',
        'cuatroscientos',
        'quinientos',
        'seiscientos',
        'setecientos',
        'ochocientos',
        'novecientos'
    )

    def numero_a_letras(self, numero):
        numero_entero = int(numero)
        if numero_entero > self.MAX_NUMERO:
            raise OverflowError('Número demasiado alto')
        if numero_entero < 0:
            return 'menos %s' % self.numero_a_letras(abs(numero))
        letras_decimal = ''
        parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
        if parte_decimal > 9:
            letras_decimal = 'punto %s' % self.numero_a_letras(parte_decimal)
        elif parte_decimal > 0:
            letras_decimal = 'punto cero %s' % self.numero_a_letras(parte_decimal)
        if (numero_entero <= 99):
            resultado = self.leer_decenas(numero_entero)
        elif (numero_entero <= 999):
            resultado = self.leer_centenas(numero_entero)
        elif (numero_entero <= 999999):
            resultado = self.leer_miles(numero_entero)
        elif (numero_entero <= 999999999):
            resultado = self.leer_millones(numero_entero)
        else:
            resultado = self.leer_millardos(numero_entero)
        resultado = resultado.replace('uno mil', 'un mil')
        resultado = resultado.strip()
        resultado = resultado.replace(' _ ', ' ')
        resultado = resultado.replace('  ', ' ')
        if parte_decimal > 0:
            resultado = '%s %s' % (resultado, letras_decimal)
        return resultado

    def numero_a_cheque(self, numero):
        numero_entero = int(numero)
        parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
        centimos = ''
        if parte_decimal == 1:
            centimos = self.CENTIMOS_SINGULAR
        else:
            centimos = self.CENTIMOS_PLURAL
        moneda = ''
        if numero_entero == 1:
            moneda = self.MONEDA_SINGULAR
        else:
            moneda = self.MONEDA_PLURAL
        letras = self.numero_a_letras(numero_entero)
        letras = letras.replace('uno', 'un')
        letras_decimal = '%02d/100' % (parte_decimal)
        letras = '%s con %s' % (letras, letras_decimal)
        return letras

    def numero_a_moneda(self, numero):
        numero_entero = int(numero)
        parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
        centimos = ''
        if parte_decimal == 1:
            centimos = self.CENTIMOS_SINGULAR
        else:
            centimos = self.CENTIMOS_PLURAL
        moneda = ''
        if numero_entero == 1:
            moneda = self.MONEDA_SINGULAR
        else:
            moneda = self.MONEDA_PLURAL
        letras = self.numero_a_letras(numero_entero)
        letras = letras.replace('uno', 'un')
        letras_decimal = 'con %s %s' % (self.numero_a_letras(parte_decimal).replace('uno', 'un'), centimos)
        letras = '%s %s %s' % (letras, moneda, letras_decimal)
        return letras

    def leer_decenas(self, numero):
        if numero < 10:
            return self.UNIDADES[numero]
        decena, unidad = divmod(numero, 10)
        if numero <= 19:
            resultado = self.DECENAS[unidad]
        elif 21 <= numero <= 29:
            resultado = 'veinti%s' % self.UNIDADES[unidad]
        else:
            resultado = self.DIEZ_DIEZ[decena]
            if unidad > 0:
                resultado = '%s y %s' % (resultado, self.UNIDADES[unidad])
        return resultado

    def leer_centenas(self, numero):
        centena, decena = divmod(numero, 100)
        if numero == 0:
            resultado = 'cien'
        else:
            resultado = self.CIENTOS[centena]
            if decena > 0:
                resultado = '%s %s' % (resultado, self.leer_decenas(decena))
        return resultado

    def leer_miles(self, numero):
        millar, centena = divmod(numero, 1000)
        resultado = ''
        if (millar == 1):
            resultado = ''
        if (millar >= 2) and (millar <= 9):
            resultado = self.UNIDADES[millar]
        elif (millar >= 10) and (millar <= 99):
            resultado = self.leer_decenas(millar)
        elif (millar >= 100) and (millar <= 999):
            resultado = self.leer_centenas(millar)
        resultado = '%s mil' % resultado
        if centena > 0:
            resultado = '%s %s' % (resultado, self.leer_centenas(centena))
        return resultado

    def leer_millones(self, numero):
        millon, millar = divmod(numero, 1000000)
        resultado = ''
        if (millon == 1):
            resultado = ' un millon '
        if (millon >= 2) and (millon <= 9):
            resultado = self.UNIDADES[millon]
        elif (millon >= 10) and (millon <= 99):
            resultado = self.leer_decenas(millon)
        elif (millon >= 100) and (millon <= 999):
            resultado = self.leer_centenas(millon)
        if millon > 1:
            resultado = '%s millones' % resultado
        if (millar > 0) and (millar <= 999):
            resultado = '%s %s' % (resultado, self.leer_centenas(millar))
        elif (millar >= 1000) and (millar <= 999999):
            resultado = '%s %s' % (resultado, self.leer_miles(millar))
        return resultado

    def leer_millardos(self, numero):
        millardo, millon = divmod(numero, 1000000)
        return '%s millones %s' % (self.leer_miles(millardo), self.leer_millones(millon))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    fecha_formateada = fields.Char(string='Fecha Formateada', compute='_compute_fecha_formateada')
    motivo = fields.Char("Motivo")
    precios = fields.Char("Precios", default="INCLUYE IGV (18%)")
    formadepago = fields.Char("Forma de Pago", default="CREDITO COMERCIAL")
    validezcotizacion = fields.Char("Validez de la cotización en días", default="5")
    moneda = fields.Char("Moneda", default="SOL")
    garantia = fields.Char("Garantía en meses", default="6")
    plazodeentrega = fields.Char("Plazo de Entrega en días", default="6")
    representantelegal = fields.Char("Representante Legal", default="Juan David Tipte Sulca")

    @api.depends('date_order')
    def _compute_fecha_formateada(self):
        for record in self:
            if record.date_order:
                fecha_str = record.date_order.strftime("%Y-%m-%d")
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
                fecha_formateada = fecha_obj.strftime("%A %d de %B del %Y")
                record.fecha_formateada = fecha_formateada

    amount_to_text = fields.Char(
        compute="_amount_in_words", string="In Words", help="The amount in words"
    )

    @api.depends("amount_total", "partner_id", "partner_id.lang")
    def _amount_in_words(self):
        self.amount_to_text = self.numero_a_cheque(self.amount_total)

    MONEDA_SINGULAR = 'dolar'
    MONEDA_PLURAL = 'dolares'

    CENTIMOS_SINGULAR = 'centavo'
    CENTIMOS_PLURAL = 'centavos'

    MAX_NUMERO = 999999999999

    UNIDADES = (
        'cero',
        'uno',
        'dos',
        'tres',
        'cuatro',
        'cinco',
        'seis',
        'siete',
        'ocho',
        'nueve'
    )

    DECENAS = (
        'diez',
        'once',
        'doce',
        'trece',
        'catorce',
        'quince',
        'dieciseis',
        'diecisiete',
        'dieciocho',
        'diecinueve'
    )

    DIEZ_DIEZ = (
        'cero',
        'diez',
        'veinte',
        'treinta',
        'cuarenta',
        'cincuenta',
        'sesenta',
        'setenta',
        'ochenta',
        'noventa'
    )

    CIENTOS = (
        '_',
        'ciento',
        'doscientos',
        'trescientos',
        'cuatroscientos',
        'quinientos',
        'seiscientos',
        'setecientos',
        'ochocientos',
        'novecientos'
    )

    def numero_a_letras(self, numero):
        numero_entero = int(numero)
        if numero_entero > self.MAX_NUMERO:
            raise OverflowError('Número demasiado alto')
        if numero_entero < 0:
            return 'menos %s' % self.numero_a_letras(abs(numero))
        letras_decimal = ''
        parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
        if parte_decimal > 9:
            letras_decimal = 'punto %s' % self.numero_a_letras(parte_decimal)
        elif parte_decimal > 0:
            letras_decimal = 'punto cero %s' % self.numero_a_letras(parte_decimal)
        if (numero_entero <= 99):
            resultado = self.leer_decenas(numero_entero)
        elif (numero_entero <= 999):
            resultado = self.leer_centenas(numero_entero)
        elif (numero_entero <= 999999):
            resultado = self.leer_miles(numero_entero)
        elif (numero_entero <= 999999999):
            resultado = self.leer_millones(numero_entero)
        else:
            resultado = self.leer_millardos(numero_entero)
        resultado = resultado.replace('uno mil', 'un mil')
        resultado = resultado.strip()
        resultado = resultado.replace(' _ ', ' ')
        resultado = resultado.replace('  ', ' ')
        if parte_decimal > 0:
            resultado = '%s %s' % (resultado, letras_decimal)
        return resultado

    def numero_a_cheque(self, numero):
        numero_entero = int(numero)
        parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
        centimos = ''
        if parte_decimal == 1:
            centimos = self.CENTIMOS_SINGULAR
        else:
            centimos = self.CENTIMOS_PLURAL
        moneda = ''
        if numero_entero == 1:
            moneda = self.MONEDA_SINGULAR
        else:
            moneda = self.MONEDA_PLURAL
        letras = self.numero_a_letras(numero_entero)
        letras = letras.replace('uno', 'un')
        letras_decimal = '%02d/100' % (parte_decimal)
        letras = '%s con %s' % (letras, letras_decimal)
        return letras

    def numero_a_moneda(self, numero):
        numero_entero = int(numero)
        parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
        centimos = ''
        if parte_decimal == 1:
            centimos = self.CENTIMOS_SINGULAR
        else:
            centimos = self.CENTIMOS_PLURAL
        moneda = ''
        if numero_entero == 1:
            moneda = self.MONEDA_SINGULAR
        else:
            moneda = self.MONEDA_PLURAL
        letras = self.numero_a_letras(numero_entero)
        letras = letras.replace('uno', 'un')
        letras_decimal = 'con %s %s' % (self.numero_a_letras(parte_decimal).replace('uno', 'un'), centimos)
        letras = '%s %s %s' % (letras, moneda, letras_decimal)
        return letras

    def leer_decenas(self, numero):
        if numero < 10:
            return self.UNIDADES[numero]
        decena, unidad = divmod(numero, 10)
        if numero <= 19:
            resultado = self.DECENAS[unidad]
        elif 21 <= numero <= 29:
            resultado = 'veinti%s' % self.UNIDADES[unidad]
        else:
            resultado = self.DIEZ_DIEZ[decena]
            if unidad > 0:
                resultado = '%s y %s' % (resultado, self.UNIDADES[unidad])
        return resultado

    def leer_centenas(self, numero):
        centena, decena = divmod(numero, 100)
        if numero == 0:
            resultado = 'cien'
        else:
            resultado = self.CIENTOS[centena]
            if decena > 0:
                resultado = '%s %s' % (resultado, self.leer_decenas(decena))
        return resultado

    def leer_miles(self, numero):
        millar, centena = divmod(numero, 1000)
        resultado = ''
        if (millar == 1):
            resultado = ''
        if (millar >= 2) and (millar <= 9):
            resultado = self.UNIDADES[millar]
        elif (millar >= 10) and (millar <= 99):
            resultado = self.leer_decenas(millar)
        elif (millar >= 100) and (millar <= 999):
            resultado = self.leer_centenas(millar)
        resultado = '%s mil' % resultado
        if centena > 0:
            resultado = '%s %s' % (resultado, self.leer_centenas(centena))
        return resultado

    def leer_millones(self, numero):
        millon, millar = divmod(numero, 1000000)
        resultado = ''
        if (millon == 1):
            resultado = ' un millon '
        if (millon >= 2) and (millon <= 9):
            resultado = self.UNIDADES[millon]
        elif (millon >= 10) and (millon <= 99):
            resultado = self.leer_decenas(millon)
        elif (millon >= 100) and (millon <= 999):
            resultado = self.leer_centenas(millon)
        if millon > 1:
            resultado = '%s millones' % resultado
        if (millar > 0) and (millar <= 999):
            resultado = '%s %s' % (resultado, self.leer_centenas(millar))
        elif (millar >= 1000) and (millar <= 999999):
            resultado = '%s %s' % (resultado, self.leer_miles(millar))
        return resultado

    def leer_millardos(self, numero):
        millardo, millon = divmod(numero, 1000000)
        return '%s millones %s' % (self.leer_miles(millardo), self.leer_millones(millon))


class ResCompany(models.Model):
    _inherit = "res.company"
    mobile = fields.Char("Mobile")
    textocotizacion = fields.Text("Texto Cotización", default="""Mediante el presente es grato dirigirme UD. para saludarle cordialmente  y hacerle llegar nuestra propuesta económica.
Después de haber revisado en forma detallada la documentación remitida declaro que las características técnicas de los bienes cotizados por mi representada si cumple con las Especificaciones Técnicas.
En tal sentido, indico que el costo total por requerido es la que detallo a continuación: En tal sentido, indico que el costo total por requerido es la que detallo a continuación:""")

    # qrlink = fields.Binary("Qr Link")
    # qrlink_invoice = fields.Binary("Qr consultar Factura")
    textopaguese = fields.Text("Texto Paguese a la orden",
                               default="""BANCO // BCP - PEN SOL 191 - 2571783 - 0 - 04 CCI 002 - 191 - 002571783004 - 53 // BCP - PEN SOL191 - 2637783 - 1 - 81 // BBVA PEN SOL 0011 - 0152 - 0100091981 CCI XXXXXX """)
    observacion_ordencompra = fields.Text("Observación",
                                          default="""* Se aceptará mercadería con un vencimiento mínimo de 3 años.
* adjuntar a la factura los siguientes documentos; registro sanitario, certificado de análisis, guía de remisión y orden de compra.
* la vigencia de los registro sanitario debe ser mayor a un (1) año  
* cada orden de compra tendrá validez solo para los productos que se consigna en la factura correspondiente  (para atenciones parciales coordinar con área de compras).
En caso incumpla con lo señalado  se devolverá la mercadería.
""")


class ResPartner(models.Model):
    _inherit = "res.partner"
    numerocuentabancaria = fields.Char("Numero Cuenta Bancaria")

class ProductTemplate(models.Model):
    _inherit = "product.product"

    @api.depends("product_tmpl_id.name")
    def _nombre(self):
        for x in self:
            x.name = x.product_tmpl_id.name
            # name += " " + x.default_code
            # name += " " + x.pharmaceutical_composition
            # name += " " + x.batch
            # x.product_id_domain = name

    name=fields.Char("Nombre",compute="_nombre",store=True)

    product_id_domain = fields.Char(
        compute="_compute_product_id_domain",
        readonly=True,
        store=True,
    )



    @api.depends('name')
    def _compute_product_id_domain(self):
        for rec in self:
            rec.product_id_domain = json.dumps(
                [('type', '=', 'product'), ('product_tmpl_id.name', 'like', rec.name)]
            )
            print(rec.product_id_domain)


    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        search_terms = name.split()
        domain = []
        for term in search_terms:
            domain += [
                '|', '|', '|', '|',
                ('product_tmpl_id.name', operator, term),
                ('default_code', operator, term),
                ('product_tmpl_id.pharmaceutical_composition', operator, term),
                ('product_tmpl_id.batch', operator, term),
                ('product_tmpl_id.barcode', operator, term),
            ]
        records = self.search(domain + args, limit=limit)
        return records.name_get()


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):

        if not args:
            args = []
        search_terms = name.split()
        domain = []
        for term in search_terms:
            domain += ['|', '|', '|', ('name', operator, term), ('default_code', operator, term),
                       ('pharmaceutical_composition', operator, term), ('batch', operator, term)]

        records = self.search(domain + args, limit=limit)
        return records.name_get()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    Health_register = fields.Char(
        string="Health register", related="product_id.Health_register")

    pharmaceutical_composition = fields.Char(
        string="Pharmaceutical composition", related="product_id.pharmaceutical_composition")

    pharmaceutical_form = fields.Many2one("tk.pharmaceutical_form",
                                          string="Pharmaceutical form"
                                          , related="product_id.pharmaceutical_form")

    route = fields.Many2one("tk.route",
                            string="Route", related="product_id.route")

    dosage = fields.Many2one("tk.dosage",
                             string='Dosage', related="product_id.dosage")

    quantity_per_presentation = fields.Integer(
        string="Quantity per presentation", related="product_id.quantity_per_presentation")

    origin = fields.Many2one("res.country",
                             string="Origin", related="product_id.origin")

    batch = fields.Char(
        string="Batch", related="product_id.batch")

    due_date = fields.Date(
        string="Due date", related="product_id.due_date")



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    Health_register = fields.Char(
        string="Health register", related="product_id.Health_register")

    pharmaceutical_composition = fields.Char(
        string="Pharmaceutical composition", related="product_id.pharmaceutical_composition")

    pharmaceutical_form = fields.Many2one("tk.pharmaceutical_form",
                                          string="Pharmaceutical form"
                                          , related="product_id.pharmaceutical_form")

    route = fields.Many2one("tk.route",
                            string="Route", related="product_id.route")

    dosage = fields.Many2one("tk.dosage",
                             string='Dosage', related="product_id.dosage")

    quantity_per_presentation = fields.Integer(
        string="Quantity per presentation", related="product_id.quantity_per_presentation")

    origin = fields.Many2one("res.country",
                             string="Origin", related="product_id.origin")

    batch = fields.Char(
        string="Batch", related="product_id.batch")

    due_date = fields.Date(string="Due date", related="product_id.due_date")

    lote = fields.Char("Lote")
    fechavencimiento = fields.Date("Fecha de Vencimiento")
