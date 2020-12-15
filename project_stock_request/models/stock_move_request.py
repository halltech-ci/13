# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMoveRequest(models.Model):
    _name = 'stock.move.request'
    _description = "Custom module for stock move request"
    
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)
    
    """@api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("purchase.request")
    """
    
    name = fields.Char(string="Name")
    
    task_id = fields.Many2one('project.task')
    move_lines = fields.One2many(related="task_id.task_product_ids")
    requested_by = fields.Many2one(
        "res.users",
        "Requested by",
        required=True,
        track_visibility="onchange",
        default=lambda s: s._get_default_requested_by(),
        readonly=True
    )
    expected_date = fields.Datetime(
        "Expected Date",
        default=lambda s: s._get_default_expected_date(),
        index=True,
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Date when you expect to receive the goods.",
    )

    
class ProjectTaskProduct(models.Model):
    _inherit = "project.task.product"
    
    qty_in_progress = fields.Float(string="Qty in progress", )
    qty_done = fields.Float(string="Rceived Qty")
    
    