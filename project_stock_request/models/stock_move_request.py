# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To be approved"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("done", "Done"),
]

class ProjectTask(models.Model):
    _inherit = "project.task"
    
    stock_request_ids = fields.One2many('stock.move.request', 'task_id')

class StockMoveRequest(models.Model):
    _name = 'stock.move.request'
    _description = "Custom module for stock move request"
    
    @api.model
    def _company_get(self):
        return self.env["res.company"].browse(self.env.company.id)

    
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
    
    @api.model
    def _default_picking_type(self):
        type_obj = self.env["stock.picking.type"]
        company_id = self.env.context.get("company_id") or self.env.company.id
        types = type_obj.search(
            [("code", "=", "outgoing"), ("warehouse_id.company_id", "=", company_id)]
        )
        if not types:
            types = type_obj.search(
                [("code", "=", "outgoing"), ("warehouse_id", "=", False)]
            )
        return types[:1]
    
    name = fields.Char(
        string="Request Reference",
        required=True,
        default=_get_default_name,
        track_visibility="onchange",
    )    
    task_id = fields.Many2one('project.task',)
    move_lines = fields.One2many('stock.request.move.line', 'move_request_id' ,
                                 #related="task_id.task_product_ids",
                                 readonly=False,
                                 copy=True,
                                 track_visibility="onchange",
    )
    company_id = fields.Many2one(comodel_name="res.company",
        string="Company",
        required=True,
        default=_company_get,
        track_visibility="onchange",
    )
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
    date_start = fields.Datetime('Creation Date',
        default=fields.Datetime.now, index=True, tracking=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Creation Date, usually the time of the request")
    
    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account",
        string="Analytic Account",
        track_visibility="onchange",
    )
    
    assigned_to = fields.Many2one(comodel_name="res.users",
        string="Approver",
        track_visibility="onchange",
        domain=lambda self: [
            ("groups_id", "in", self.env.ref("project.group_project_manager").id,)
        ],
        index=True,
    )
    
    to_approve_allowed = fields.Boolean(compute="_compute_to_approve_allowed")
    
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')
    
    picking_ids = fields.One2many('stock.picking', 'request_id', string='Transfers')
    
    @api.depends('picking_ids')
    def _compute_picking_ids(self):
        for request in self:
            request.delivery_count = len(request.picking_ids)
    
    @api.onchange('task_id')
    def onchange_task_id(self):
        if self.task_id.task_product_ids:
            lines = [line for line in self.task_id.task_product_ids]
            res = {}
            for line in lines:
                res.update({
                    'product_id': line.product_id.id,
                    'product_qty': line.product_qty,
                    'task_id': self.task_id.id,
                    'move_request_id': self.id,
                })
                self.env['stock.request.move.line'].create(res)
        
    @api.depends("state", "move_lines")
    def _compute_to_approve_allowed(self):
        for rec in self:
            if rec.move_lines:
                rec.to_approve_allowed = rec.state == "draft" 
            
    @api.model
    def create(self, vals):
        request = super(StockMoveRequest, self).create(vals)
        return request
    
    def write(self, vals):
        res = super(StockMoveRequest, self).write(vals)
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
                
class StockRequestMoveLine(models.Model):
    #_inherit = "project.task.product"
    _name = 'stock.request.move.line'
    _description = 'Stock request move line'
    
    product_id = fields.Many2one('product.product')
    product_code = fields.Char(related="product_id.default_code", string = 'Code')
    product_qty = fields.Float()
    product_uom_id = fields.Many2one(comodel_name="uom.uom",
        string="Product Unit of Measure",
        track_visibility="onchange",
    )
    qty_in_progress = fields.Float(string="Qty in progress", track_visibility="onchange", digits="Product Unit of Measure")
    qty_done = fields.Float(string="Received Qty")
    move_request_id = fields.Many2one('stock.move.request', string='Stock Request', 
        ondelete="cascade",
        readonly=True,
        index=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        related="move_request_id.company_id",
        string="Company",
        store=True,
    )
    state = fields.Selection(
        selection=_STATES,
        string="Status",
        index=True,
        track_visibility="onchange",
        required=True,
        copy=False,
        compute="_compute_state",
    )
    requested_by = fields.Many2one(comodel_name="res.users",
        related="move_request_id.requested_by",
        string="Requested by",
        store=True,
    )
    assigned_to = fields.Many2one(comodel_name="res.users",
        related="move_request_id.assigned_to",
        string="Assigned to",
        store=True,
    )
    task_id = fields.Many2one('project.task')
    
    @api.constrains('product_qty', 'qty_in_progress')
    def compare_product_qty(self):
        if self.qty_in_progress and self.product_qty:
            if self.qty_in_progress > self.product_qty:
                raise ValidationError("%s quantity cannot be greater than %s" % (self.product_id.name, self.product_qty))
    
    @api.depends('move_request_id')
    def _compute_state(self):
        self.state = 'draft'
        if self.move_request_id:
            self.state = self.move_request_id.state
    
    