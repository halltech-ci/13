# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    expense_cost = fields.Monetary("Expense Cost", compute='_compute_expense_cost', store=True,)
    
    def _compute_expense_cost(self):
        for record in self:
            expenses = self.env['hr.expense'].search([('employee_id', '=', record.id), ('payment_mode', '=', 'employee')])
            cost = 0
            if expenses:
                for expense in expenses:
                    cost += expense.total_amount
            record.expense_cost = cost
            
class EmployeePublic(models.Model):
    _inherit = 'hr.employee.public'
    
    expense_cost = fields.Monetary("Expense Cost", store=True)