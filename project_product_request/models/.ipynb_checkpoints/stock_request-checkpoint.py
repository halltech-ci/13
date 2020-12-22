# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockRequest(models.Model):
    _inherit = "stock.request"
    
    task_id = fields.Many2one('project.task', string="Task")
    initial_qty = fields.Float(string='Initial Qty', states={"draft": [("readonly", False)]}, readonly=True)
    product_uom_qty = fields.Float(
        states={"draft": [("readonly", False)]}, readonly=True
    )