from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class ArticleShortInfo(Datamodel):
    _name = "article.short.info"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)

class ArticleInfo(Datamodel):
    _name = "article.info"
    _inherit = "article.short.info"

    description = fields.String(required=True, allow_none=True)

class ArticleCreateParam(Datamodel):
    _name = "article.create.param"

    name = fields.String(required=True, allow_none=False)
    description = fields.String(required=True, allow_none=True)

class ArticleUpdateParam(Datamodel):
    _name = "article.update.param"

    description = fields.String(required=True, allow_none=True)