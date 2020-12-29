# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class AccountResultReportWizard(models.TransientModel):
    _name = 'account.result.report.wizard'
    _description = "Wizard Account Result"

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    #partner = fields.Many2one('hr.partner', string="Partner")
    project = fields.Many2one('project.project', string="Project")

    def get_report(self):
        data = {
            'model':'account.result.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report.account_result_report').with_context(landscape=True).report_action(self, data=data)

