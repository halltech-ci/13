# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockRequest(models.Model):
    _inherit = "stock.request"
    
    task_id = fields.Many2one('project.task', string='Task')