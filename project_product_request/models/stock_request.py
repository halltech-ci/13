# -*- coding: utf-8 -*-

from odoo import models, fields, api


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockRequest(models.AbstractModel):
    _inherit = "stock.request.abstract"
    
    @api.constrains("product_qty")
    def _check_qty(self):
        for rec in self:
            if rec.product_qty < 0:
                raise ValidationError(
                    _("Stock Request product quantity has to be strictly positive.")
                )

class StockRequest(models.Model):
    _inherit = "stock.request"
    
    task_id = fields.Many2one('project.task', string="Task")
    initial_qty = fields.Float(string='Initial Qty', states={"draft": [("readonly", False)]}, readonly=True)
    product_uom_qty = fields.Float(
        states={"draft": [("readonly", False)]}, readonly=True
    )
    
    @api.constrains('product_uom_qty', 'initial_qty')
    def compare_product_qty(self):
        if self.initial_qty and self.product_uom_qty:
            if self.product_uom_qty > self.initial_qty:
                raise ValidationError("%s quantity cannot be greater than %s" % (self.product_id.name, self.initial_qty))