# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"
    
    project_task = fields.Many2one('project.task')