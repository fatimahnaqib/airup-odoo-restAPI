from odoo.addons.datamodel.core import Datamodel
from marshmallow import fields

class ShelfShorterInfo(Datamodel):
    _name = 'shelf.shorter.info'

    id = fields.Integer(required=False, allow_none=False)
    bay = fields.String(required=False, allow_none=True)

class ShelfShortInfo(Datamodel):
    _name = 'shelf.short.info'
    _inherit = 'shelf.shorter.info'

    row = fields.String(required=False, allow_none=True)

class ShelfDepthInfo(Datamodel):
    _name = 'shelf.depth.info'

    depth = fields.Float(required=False, allow_none=True)

class ShelfSizeInfo(Datamodel):
    _name = 'shelf.size.info'
    _inherit = 'shelf.depth.info'

    width = fields.Float(required=False, allow_none=False)
    height = fields.Float(required=False, allow_none=False)

class ShelfFullInfo(Datamodel):
    _name = 'shelf.full.info'
    _inherit = 'shelf.short.info'

    width = fields.Float(required=False, allow_none=False)
    height = fields.Float(required=False, allow_none=False)
    depth = fields.Float(required=False, allow_none=False)

class ShelfCreateParam(Datamodel):
    _name = 'shelf.create.param'

    row = fields.String(required=False, allow_none=True)
    bay = fields.String(required=False, allow_none=True)
    width = fields.Float(required=False, allow_none=False)
    height = fields.Float(required=False, allow_none=False)
    depth = fields.Float(required=False, allow_none=False)

class ShelfDetailWarehouse(Datamodel):
    _name = "shelf.detail.warehouse"

    amount = fields.Integer(required=False, allow_none=False)
    row = fields.String(required=False, allow_none=False)
    bay = fields.String(required=False, allow_none=False)