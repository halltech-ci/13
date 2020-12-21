# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    request_id = fields.Many2one('stock.move.request', string="Transfert")