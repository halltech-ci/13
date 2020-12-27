# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"
    
    project_task = fields.Many2one('project.task')
    timesheet_ids = fields.One2many(related="project_task.timesheet_ids")
    
    @api.onchange('project_task')
    def _onchange_project_task(self):
        for rec in self:
            if rec.project_task:
                request = self.env['stock.request'].search([('task_id', '=', self.project_task.id)])
                lines = [(5, 0, 0)]
                for line in request:
                    vals = {
                        #'id': line.id,
                        "product_id": line.product_id.id,
                        "product_uom_id": line.product_uom_id.id,
                        "product_uom_qty": line.product_uom_qty,
                        "company_id": self.company_id.id,
                        "warehouse_id": self.warehouse_id.id,
                        "location_id": self.location_id.id,
                        "expected_date": self.expected_date,
                    }
                    lines.append((0, 0, vals))
                rec.stock_request_ids = lines