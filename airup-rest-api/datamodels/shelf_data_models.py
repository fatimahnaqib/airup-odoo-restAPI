from odoo.addons.datamodel.core import Datamodel
from marshmallow import fields

class ShelfDepthInfo(Datamodel):
    _name = 'shelf.depth.info'

    depth = fields.Float(required=False, allow_none=True)

class ShelfInfo(Datamodel):
    _name = "shelf.info"

    id = fields.Integer(required=False, allow_none=False)
    shelf_location = fields.Boolean(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=True)
    row = fields.String(required=False, allow_none=True)
    bay = fields.String(required=False, allow_none=True)
    width = fields.Float(required=False, allow_none=False)
    height = fields.Float(required=False, allow_none=False)
    depth = fields.Float(required=False, allow_none=False)

class ShelfCreateParam(Datamodel):
    _name = 'shelf.create.param'

    shelf_location = fields.Boolean(required=True, allow_none=False)
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