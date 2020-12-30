# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class StockRequest(models.Model):
    _inherit = "stock.request"
    
    task_id = fields.Many2one('project.task', string='Task')
    initial_qty = fields.Float('Initial Qty', digits="Product Unit of Measure")
    product_uom_qty = fields.Float(required=False)
    
    @api.constrains('initial_qty', 'product_uom_qty')
    def compare_product_qty(self):
        if self.task_id:
            if self.initial_qty < self.product_uom_qty:
                raise ValidationError(_("{0} quantity can not be greater than {1}".format(self.product_id.name, self.initial_qty)))
            
    @api.model
    def create(self, vals):
        upd_vals = vals.copy()
        if upd_vals.get("name", "/") == "/":
            upd_vals["name"] = self.env["ir.sequence"].next_by_code("product.request")
        return super().create(upd_vals)
            
class StockMove(models.AbstractModel):
    _inherit = 'stock.request.abstract'
    
    @api.constrains("product_qty")
    def _check_qty(self):
        for rec in self:
            if rec.product_qty < 0:
                raise ValidationError(
                    _("Stock Request product quantity has to be strictly positive.")
                )