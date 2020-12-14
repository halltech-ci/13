# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    task_material_id = fields.One2many(
        'project.task.product',
        'analytic_line_id',
        string='Project Task Material',
    )

    def _timesheet_postprocess_values(self, values):
        res = super(AccountAnalyticLine, self)._timesheet_postprocess_values(
            values)
        # Delete the changes in amount if the analytic lines
        # come from task material.
        for key in (self.filtered(lambda x: x.task_material_id).ids):
            res[key].pop('amount', None)
        return res
