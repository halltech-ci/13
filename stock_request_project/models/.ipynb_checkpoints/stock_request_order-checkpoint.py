# Copyright 2020 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"

    task_ids = fields.One2many(
        "project.task",
        compute="_compute_task_ids",
        string="Project Task",
        readonly=True,
    )
    task_count = fields.Integer(
        string="Task Orders count",
        compute="_compute_task_ids",
        readonly=True,
    )

    @api.depends("stock_request_ids")
    def _compute_task_ids(self):
        for req in self:
            req.task_ids = req.stock_request_ids.mapped("task_ids")
            req.task_count = len(req.task_ids)
            
    """
    def action_view_project_task(self):#action_view_mrp_production
        action = self.env.ref("mrp.mrp_production_action").read()[0]
        productions = self.mapped("production_ids")
        if len(productions) > 1:
            action["domain"] = [("id", "in", productions.ids)]
            action["views"] = [
                (self.env.ref("mrp.mrp_production_tree_view").id, "tree"),
                (self.env.ref("mrp.mrp_production_form_view").id, "form"),
            ]
        elif productions:
            action["views"] = [
                (self.env.ref("mrp.mrp_production_form_view").id, "form")
            ]
            action["res_id"] = productions.id
        return action
        """
