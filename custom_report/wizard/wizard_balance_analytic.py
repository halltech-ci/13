# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class BalanceAnalyticReportWizard(models.TransientModel):
    _name = 'balance.analytic.report.wizard'
    _description = "Wizard Balance Analytic"
    

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    #partner = fields.Many2one('hr.partner', string="Partner")
    analytic = fields.Many2one('account.analytic.account', string="Account Analytic")

    def get_report(self):
        data = {
            'model':'balance.analytic.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report.balance_analytic_report').with_context(landscape=True).report_action(self, data=data)

