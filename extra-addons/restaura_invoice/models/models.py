# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError

import json
import requests

import logging
import sys
import traceback
# from datetime import datetime
import datetime

_logger = logging.getLogger(__name__)

# Importar los módulos necesarios
from odoo import api, SUPERUSER_ID


class mail_notification(models.Model):
	_name = 'restaurar_invoices'
	_description = 'restaurar invoices'


	# Definir una función para regenerar el PDF de la factura
	def regenerate_invoice_pdf(self,invoice_id):
	    # Obtener el entorno de Odoo
		env = api.Environment(env.cr, SUPERUSER_ID, {})
	    # Obtener la factura
		invoice = self.env['account.move'].browse(invoice_id)
		if invoice.exists():
	        # Generar el PDF	
			pdf_content, _ = self.env.ref('account.account_invoices')._render_qweb_pdf([invoice_id])
	        # Nombre del archivo PDF
			pdf_name = 'Factura-%s.pdf' % invoice.name
        
	        # Guardar el PDF como adjunto
			attachment = self.env['ir.attachment'].create({
        	    'name': pdf_name,
	            'type': 'binary',
	            'datas': base64.b64encode(pdf_content),
	            'res_model': 'account.move',
	            'res_id': invoice_id,
	            'mimetype': 'application/pdf'
	        })
        
			return attachment
		else:
			return None
	
	# ID de la factura que deseas regenerar
	def restore_invoice(self,invoice_id=False):
		if not invoice_id:
			invoice_id = 29376  # Reemplaza con el ID de la factura
	    # Llamar a la función para regenerar el PDF
		attachment = self.regenerate_invoice_pdf(invoice_id)
		if attachment:
			print("PDF regenerado y adjuntado con éxito.")
		else:
			print("Factura no encontrada.")


