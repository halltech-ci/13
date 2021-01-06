# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class EtatTvaReportWizard(models.TransientModel):
    _name = 'etat.tva.report.wizard'
    _description = "Wizard Etat TVA"

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    partner = fields.Many2one('res.partner', string="Partner")
    #project = fields.Many2one('project.project', string="Project")

    def get_report(self):
        data = {
            'model':'etat.tva.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report.etat_tva_report').with_context(landscape=True).report_action(self, data=data)

