from odoo import fields, models, api

class Shelf(models.Model):
    """ Adds additional fields to the native stock.location model """

    _inherit = "stock.location"

    shelf_location = fields.Boolean(string="Is a Shelf Location?")
    row = fields.Char(string='Row',related='location_id.name')
    bay = fields.Char(string='Bay',related='name')
    height = fields.Float(string="Height")
    width = fields.Float(string="Width")
    depth = fields.Float(string="Depth")
