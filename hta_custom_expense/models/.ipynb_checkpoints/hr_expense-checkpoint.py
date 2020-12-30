# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    payment_mode = fields.Selection(selection_add=[('employee', 'To justify')], default='employee')