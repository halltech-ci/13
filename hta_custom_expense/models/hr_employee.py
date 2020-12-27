# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    expense_cost = fields.Monetary("Expense Cost", compute='_compute_expense_cost', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, default=lambda self: self.env.company.currency_id) 
    
    def _compute_expense_cost(self):
        for record in self:
            expenses = self.env['hr.expense'].search([('employee_id', '=', record.id), ('payment_mode', '=', 'employee')])
            cost = 0
            if expenses:
                for expense in expenses:
                    cost += expense.total_amount
            record.expense_cost = cost
            
