# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To be approved"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("done", "Done"),
]

class StockMoveRequest(models.Model):
    _name = 'stock.move.request'
    _description = "Custom module for stock move request"
    
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)
    
    @api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("move.request")
    
    @api.depends("state")
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ("to_approve", "approved", "rejected", "done"):
                rec.is_editable = False
            else:
                rec.is_editable = True
    
    name = fields.Char(
        string="Request Reference",
        required=True,
        default=_get_default_name,
        track_visibility="onchange",
    )    
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
        #default=lambda s: s._get_default_expected_date(),
        index=True,
        #required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Date when you expect to receive the goods.",
    )
    state = fields.Selection(
        selection=_STATES,
        string="Status",
        index=True,
        track_visibility="onchange",
        required=True,
        copy=False,
        default="draft",
    )
    is_editable = fields.Boolean(
        string="Is editable", compute="_compute_is_editable", readonly=True
    )
    date_start = fields.Date(
        string="Request date",
        help="Date when the user initiated the request.",
        default=fields.Date.context_today,
        track_visibility="onchange",
    )
    to_approve_allowed = fields.Boolean(compute="_compute_to_approve_allowed")
    
    @api.depends("state", "move_lines")
    def _compute_to_approve_allowed(self):
        for rec in self:
            if rec.move_lines:
                rec.to_approve_allowed = rec.state == "draft" 
            
    @api.model
    def create(self, vals):
        request = super(StockMoveRequest, self).create(vals)
        #if vals.get("assigned_to"):
        #    partner_id = self._get_partner_id(request)
        #    request.message_subscribe(partner_ids=[partner_id])
        return request
    
    def write(self, vals):
        res = super(StockMoveRequest, self).write(vals)
        #for request in self:
        #    if vals.get("assigned_to"):
        #        partner_id = self._get_partner_id(request)
        #        request.message_subscribe(partner_ids=[partner_id])
        return res
    
    def copy(self, default=None):
        default = dict(default or {})
        self.ensure_one()
        default.update({"state": "draft", "name": self._get_default_name()})
        return super(StockMoveRequest, self).copy(default)
    
    def _can_be_deleted(self):
        self.ensure_one()
        return self.state == "draft"
    
    def unlink(self):
        for request in self:
            if not request._can_be_deleted():
                raise UserError(
                    _("You cannot delete a move request which is not draft.")
                )
        return super(StockMoveRequest, self).unlink()

    def button_draft(self):
        self.mapped("move_lines").do_uncancel()
        return self.write({"state": "draft"})

    def button_to_approve(self):
        self.to_approve_allowed_check()
        return self.write({"state": "to_approve"})

    def button_approved(self):
        return self.write({"state": "approved"})

    def button_rejected(self):
        self.mapped("move_lines").do_cancel()
        return self.write({"state": "rejected"})

    def button_done(self):
        return self.write({"state": "done"})
    
    def to_approve_allowed_check(self):
        for rec in self:
            if not rec.to_approve_allowed:
                raise UserError(
                    _(
                        "You can't request an approval for a move request "
                        "which is empty. (%s)"
                    )
                    % rec.name
                )
    
class ProjectTaskProduct(models.Model):
    _inherit = "project.task.product"
    
    qty_in_progress = fields.Float(string="Qty in progress", )
    qty_done = fields.Float(string="Rceived Qty")
    
    