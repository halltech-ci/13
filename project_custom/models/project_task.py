# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    consume_product = fields.Boolean(
        help="If you mark this check, when a task goes to this state, "
             "it will consume the associated materials",
    )

class Task(models.Model):
    _inherit = "project.task"
    
    task_product_ids = fields.One2many('project.task.product', 'task_id', string='Product Use') 
    