# Copyright 2020 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockRequest(models.Model):
    _inherit = "stock.request"

    task_ids = fields.Many2many(
        "project.task",
        "project_task_stock_request_rel",
        "stock_request_id",
        "project_task_id",
        string="Project Task",
        readonly=True,
    )
    task_count = fields.Integer(
        string="Task Orders count",
        compute="_compute_task_ids",
        readonly=True,
    )

    @api.depends("task_ids")
    def _compute_task_ids(self):
        for request in self:
            request.task_count = len(request.task_ids)

    @api.constrains("task_ids", "company_id")
    def _check_task_company_constrains(self):
        if any(
            any(
                task.company_id != req.company_id
                for task in req.task_ids
            )
            for req in self
        ):
            raise ValidationError(
                _(
                    "You have linked to a task Order "
                    "that belongs to another company."
                )
            )

    """
    def action_view_mrp_production(self):
        action = self.env.ref("mrp.mrp_production_action").read()[0]
        productions = self.mapped("production_ids")
        if len(productions) > 1:
            action["domain"] = [("id", "in", productions.ids)]
        elif productions:
            action["views"] = [
                (self.env.ref("mrp.mrp_production_form_view").id, "form")
            ]
            action["res_id"] = productions.id
        return action
    """
