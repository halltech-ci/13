# -*- coding: utf-8 -*-

from odoo import models, fields, api

PAYMENT_MODE = [('justify', 'Employee (To justify)'),
                ('company', 'Company (Not justify)'),
                ('reimburse', 'Employee (To Reimburse)'),
               ]

PAYMENT_TYPE = [('cash', 'Espece'),
                ('trasfert', 'Mobile'),
                ('check', 'Cheque'),
               ]
class ExepnseLine(models.Model):
    _name = 'expense.line'
    _description = 'Custom expense line'
    
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id
    
    name = fields.Char('Description', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('to_approve', 'To Approve'),
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, states={'draft': [('readonly', False)]}, default=_default_employee_id, check_company=True)
    request_id = fields.Many2one('expense.request', string='Expense Request')
    date = fields.Date(readonly=True, default=fields.Date.context_today, string="Date")
    amount = fields.Float("Unit Price", required=True, digits='Product Price')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, 
                                 default=lambda self: self.env.company
                                )
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange',)
    payment_mode = fields.Selection(selection=PAYMENT_MODE, string="Payment Mode")
    payed_by = fields.Selection(selection=PAYMENT_TYPE, string="Payer Par")
    
    def unlink(self):
        for expense in self:
            if expense.state in ['done', 'approved']:
                raise UserError(_('You cannot delete a posted or approved expense.'))
        return super(ExpenseLine, self).unlink()

    def write(self, vals):
        for expense in self:
            if expense.state in ['done', 'approved']:
                raise UserError(_('You cannot delete a posted or approved expense.'))
        return super(ExpenseLine, self).write(vals)
    
