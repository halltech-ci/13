# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = "project.task"
    
    stock_request_ids = fields.One2many("stock.request", "task_id", string="Stock Request")
    request_order_ids = fields.One2many('stock.request.order', "project_task_id", string="Request Order")