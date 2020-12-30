# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class AccountResultReportWizard(models.TransientModel):
    _name = 'project.project.report.wizard'
    _description = "Wizard Project"

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    #partner = fields.Many2one('hr.partner', string="Partner")
    project = fields.Many2one('project.project', string="Project")

    def get_report(self):
        data = {
            'model':'project.project.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report.project_project_report').with_context(landscape=True).report_action(self, data=data)

