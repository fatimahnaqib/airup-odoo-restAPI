from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
from odoo import models


class WarehouseApiService(Component):
    _inherit = "base.rest.service"
    _name = "warehouse.new_api.service"
    _usage = "warehouse"
    _collection = "base.rest.public.airup.services"
    _description = """
        Warehouse New API Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/", "/"], "GET")],
        output_param=restapi.Datamodel("warehouse.info", is_list=True),
        auth="public",
    )
    def get_warehouse_info(self):
        """
        List a summary of all stored articles
        """

        res = []
        WarehouseInfo = self.env.datamodels["warehouse.info"]
        for product in self.env["product.product"].search([]):
            res.append(WarehouseInfo(id=product.id, name=product.name,amount=product.qty_available))

        return res

    @restapi.method(
        [(["/search"], "GET")],
        input_param=restapi.Datamodel("warehouse.search.param"),
        output_param=restapi.Datamodel("warehouse.article.shelfs", is_list=True),
        auth="public",
    )
    def search(self, warehouse_search_param):
        """
        Search stored articles with the help of the URL parameters row, bay and id in
        each combination.
        """

        #domain to search the stock.location
        loc_domain = []
        if warehouse_search_param.row:
            loc_domain.append(("row", "=", warehouse_search_param.row))
        if warehouse_search_param.bay:
            loc_domain.append(("bay", "=", warehouse_search_param.bay))


        #id of the articles
        articles = []
        if warehouse_search_param.id:
            articles.append(warehouse_search_param.id)

        if loc_domain:
            for location in self.env["stock.location"].search(loc_domain):
                for quant in self.env["stock.quant"].search([('location_id','=',location.id)]):
                    #get the articles id if is not already in the list of articles
                    if quant.product_id.id not in articles:
                        articles.append(quant.product_id.id)


        res= []
        WarehouseArticleShelfs = self.env.datamodels["warehouse.article.shelfs"]
        ShelfDetailWarehouse= self.env.datamodels['shelf.detail.warehouse']

        for article in self.env["product.product"].browse(articles):
            shelf_detail = []
            for quant in self.env['stock.quant'].search([('product_id','=',article.id)]):
                if quant.location_id.usage == 'internal':
                    shelf_detail.append(ShelfDetailWarehouse(amount=quant.quantity,bay=quant.location_id.bay if quant.location_id.bay else "bay to be assigned", row=quant.location_id.row if quant.location_id.row else "row to be assigned" ))
            res.append(WarehouseArticleShelfs(id=article.id,shelfs=shelf_detail,name=article.name))

        return res

    @restapi.method(
        [(["/"], "POST")],
        input_param=restapi.Datamodel("warehouse.article.shelf.transfer"),
        auth="public",
    )
    def receipt_transfer_of_articles(self,request_body):
        """
        Load a number of article in a shelf
        """

        source_location_id = self.env["stock.location"].search(
            [("name", "=", "Vendors"),('usage','=','supplier')])[0].id

        operation_type_id = self.env['stock.picking.type'].search(
            [('name', '=', "Receipts"), ('code', '=', 'incoming')]).id

        location_dest_id = self.env['stock.location'].search(
            [('shelf_location','=',True),('row','=',request_body.row),('bay','=',request_body.bay)],limit=1)

        if not location_dest_id:
            return {"response": "The Shelf does not exist in the system. Please create it."}

        article = self.env['product.product'].search([('id','=',request_body.id)])

        amount = request_body.amount

        move_name = "Receipt Transfer for" + article.name

        # carry out receipt transfer for article
        self.env['warehouse.helper.model'].create_transfer(operation_type_id,source_location_id,location_dest_id.id,article,move_name,amount)

        return {"response": "Receipt Transfer has been carried out."}

    @restapi.method(
        [(["/"], "PUT")],
        input_param=restapi.Datamodel("warehouse.search.param"),
        auth="public",
    )
    def delivery_order_of_articles(self, request_body):
        """
        Pick one specific article from one shelf
        """

        location_dest_id = self.env["stock.location"].search(
            [("name", "=", "Customers"), ('usage', '=', 'customer')])[0].id
        operation_type_id = self.env['stock.picking.type'].search(
            [('name', '=', "Delivery Orders"), ('code', '=', 'outgoing')]).id
        source_location_id = self.env['stock.location'].search(
            [('shelf_location', '=', True), ('row', '=', request_body.row), ('bay', '=', request_body.bay)], limit=1)

        if not source_location_id:
            return {"response": "The Shelf does not exist in the system."}

        article = self.env['product.product'].search([('id','=',request_body.id)])

        move_name = "Delivery Order for" + article.name
        amount = 1

        #carry out delivery order transfer for article
        self.env['warehouse.helper.model'].create_transfer(operation_type_id,source_location_id.id,location_dest_id,article,move_name,amount)

        return {"response": "Delivery Order has been carried out."}


class WarehouseHelperClass(models.Model):
    _name = 'warehouse.helper.model'

    """Helper Function"""

    def create_transfer(self, operation_type_id, source_location_id, location_dest_id, article,move_name,amount):
        article_uom = self.env['uom.uom'].search(
            [('name', '=', 'Units'), ('category_id.name', '=', 'Unit')], limit=1).id

        article_to_move = {
            "name": move_name,
            'product_id': article.id,
            'product_uom_qty': amount,
            'quantity_done': amount,
            'product_uom': article_uom,
        }

        vals = {
            'picking_type_id': operation_type_id,
            'location_id': source_location_id,
            "location_dest_id": location_dest_id,
            'move_ids_without_package': [(0, 0, article_to_move)]
        }

        res = self.env["stock.picking"].create(vals)
        res.action_confirm()
        res.button_validate()































