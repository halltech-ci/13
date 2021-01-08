# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExepnseRequest(models.Model):
    _name = 'expense.request'
    _description = 'Custom expense request'
    
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id
    
    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)
    
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
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange',
                    default=_get_default_requested_by)
    date = fields.Date(readonly=True, default=fields.Date.context_today, string="Date")
    
    
    
    @api.model
    def create(self, vals):
        request = super(ExpenseRequest, self).create(vals)
        return request
    
    def write(self, vals):
        res = super(ExpenseRequest, self).write(vals)
        return res