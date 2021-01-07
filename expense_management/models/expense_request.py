# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExepnseRequest(models.Model):
    _name = 'expense.request'
    _description = 'Custom expense request'
    
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id
    
    name = fields.Char('Description', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, states={'draft': [('readonly', False)]}, default=_default_employee_id, check_company=True)
    line_ids = fields.One2many('expense.line', 'request_id', string='Expense Line')
    intermediary = fields.Many2one('hr.employee', string="Intermediaire")