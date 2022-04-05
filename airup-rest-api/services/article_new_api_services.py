from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi

class ArticleApiService(Component):
    _inherit = "base.rest.service"
    _name = "article.new_api.service"
    _usage = "article"
    _collection = "base.rest.public.airup.services"
    _description = """
        Article New API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/", "/"], "GET")],
        output_param=restapi.Datamodel("article.short.info", is_list=True),
        auth="public",
    )
    def get_articles(self):
        """
        List all articles

        """

        res = []
        ArticleInfo = self.env.datamodels["article.short.info"]
        for product in self.env["product.product"].search([('type','=','product')]):
            res.append(ArticleInfo(id=product.id, name=product.name))

        return res

    @restapi.method(
        [(["/<string:id>"], "GET")],
        output_param=restapi.Datamodel("article.info",is_list=True),
        auth="public",
    )
    def get_by_id(self, id):
        """
        Article with all properties
        """

        domain = []
        if id:
            domain.append(("id", "=", id))
        res = []
        ArticleInfo = self.env.datamodels["article.info"]
        for article in self.env["product.product"].search(domain):
            res.append(ArticleInfo(id=article.id, name=article.name,description=article.description))
        return res

    @restapi.method(
        [(["/"], "POST")],
        input_param=restapi.Datamodel("article.create.param"),
        auth="public",
    )
    def create(self, article_create_param):
        """
        Create Article
        """
        params = {}
        params['type'] = 'product'
        if article_create_param.name:
            params['name'] = article_create_param.name
        if article_create_param.description:
            params['description'] = article_create_param.description

        shelf = self.env["product.product"].create(params)
        return {"response": "Article has been created"}

    @restapi.method(
        [(["/<string:id>"], "PATCH")],
        input_param=restapi.Datamodel("article.update.param"),
        auth="public",
    )
    def update_shelf(self, id, params):
        """
        Update on Article
        """
        self.env["product.product"].search([("id", "=", id)])[0].write({'description': params.description})

        return {"response": "Article with requested id is updated"}

    @restapi.method(
        [(["/<int:id>"], "DELETE")],
        auth="public",
    )
    def delete_article(self, id):
        """
        Delete on Article
        """
        self.env["product.product"].search([("id", "=", id)]).unlink()
        return {"response": "Record has been deleted"}

