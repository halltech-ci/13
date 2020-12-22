# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"
    
    project_task_id = fields.Many2one('project.task', string="Task")
    
    stock_request_ids = fields.One2many(
        "stock.request", inverse_name="order_id", copy=True,
        compute="_compute_stock_request_ids"
    )
    
    @api.depends('project_task_id')
    def _compute_stock_request_ids(self):
        res_obj = self.env['stock.request'].search([('task_id', '=', self.project_task_id.id),
                                                   ])
        self.stock_request_ids = res_obj
    
    @api.onchange('project_task_id')
    def _onchange_stock_request_ids(self):
        res_obj = self.env['stock.request'].search([('task_id', '=', self.project_task_id.id)])
        self.stock_request_ids = res_obj