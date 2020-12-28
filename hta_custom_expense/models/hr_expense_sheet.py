# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'
    
    amount_advance = fields.Monetary(string="Advanced Amount", 
                                     #compute="_compute_advance_amount"
                                    )
    justify_amount = fields.Monetary(string="Justified Amount")
    amount_residual = fields.Monetary(string="Residual Amount", 
                                      #compute="_compute_residual_amount", 
                                      readonly=True
                                     )
    assigned_to = fields.Many2one('hr.employee', string="Beneficiaire")
    employee_id = fields.Many2one("hr.employee", string="Destinataire")