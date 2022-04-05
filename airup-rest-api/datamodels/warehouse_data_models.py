
from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class WarehouseInfo(Datamodel):
    _name = "warehouse.info"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    amount = fields.Integer(required=False, allow_none=False)

class WarehouseInfo(Datamodel):
    _name = "warehouse.search.param"

    id = fields.Integer(required=False, allow_none=False)
    row = fields.String(required=False, allow_none=False)
    bay = fields.String(required=False, allow_none=False)

class WarehouseInfo(Datamodel):
    _name = "warehouse.article.shelfs"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    shelfs = fields.List(NestedModel("shelf.detail.warehouse"), required=False)

class WarehouseInfo(Datamodel):
    _name = "warehouse.article.shelf.transfer"

    id = fields.Integer(required=True, allow_none=False)
    row = fields.String(required=True, allow_none=False)
    bay = fields.String(required=True, allow_none=False)
    amount = fields.Float(required=True, allow_none=False)
