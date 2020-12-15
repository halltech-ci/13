# -*- coding: utf-8 -*-

from odoo import models, fields, api
    
class ProjectTaskProduct(models.Model):
    _name = "project.task.product"
    _description ="Task consume material"
    
    task_id = fields.Many2one('project.task')
    analytic_line_id = fields.Many2one('account.analytic.line', string='Analytic Line')
    product_id = fields.Many2one('product.product', string='Product', domain=[('type', 'in', ('product', 'consu'))])
    product_uom = fields.Many2one('uom.uom', string='Product Unit')
    product_qty = fields.Float(string="Initial Quantity")
    product_code = fields.Char(related='product_id.default_code', string="Code")
    
    @api.constrains("product_qty")
    def _check_quantity(self):
        for material in self:
            if not material.product_qty > 0.0:
                raise ValidationError(
                    _("Quantity of material consumed must be greater than 0.")
                )
