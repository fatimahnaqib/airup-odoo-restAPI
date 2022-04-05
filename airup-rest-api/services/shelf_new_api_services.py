
from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi

class ShelfNewApiService(Component):
    _inherit = "base.rest.service"
    _name = "shelf.new_api.service"
    _usage = "shelf"
    _collection = "base.rest.public.airup.services"
    _description = """
        Shelf New API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/"], "GET")],
        output_param=restapi.Datamodel("shelf.info", is_list=True),
        auth="public",
    )
    def get_shelfs(self):
        """
        List all shelfs in the warehouse

        """
        domain = []
        domain.append(("shelf_location", "=", True))

        res = []
        ShelfInfo = self.env.datamodels["shelf.info"]
        for shelf in self.env["stock.location"].search(domain):
            res.append(ShelfInfo(id=shelf.id,row=shelf.row, bay=shelf.bay))

        return res

    @restapi.method(
        [(["/<string:row>/<string:bay>"], "GET")],
        output_param=restapi.Datamodel("shelf.info", is_list=True),
        auth="public",
    )
    def get_by_row_and_bay(self, _row, _bay):
        """
        Shelf with all properties
        """
        domain = []
        domain.append(("shelf_location", "=", True))
        if _row:
            domain.append(("row", "=", _row))
        if _bay:
            domain.append(("bay", "=", _bay))
        res = []
        ShelfSizeInfo = self.env.datamodels["shelf.info"]
        for shelf in self.env["stock.location"].search(domain):
            res.append(ShelfSizeInfo(id=shelf.id, width=shelf.width, height=shelf.height,
                                     depth=shelf.depth))
        return res

    @restapi.method(
        [(["/<string:row>"], "GET")],
        output_param=restapi.Datamodel("shelf.info", is_list=True),
        auth="public",
    )
    def get_by_row(self, _row):
        """
        List all shelfs in one row of the warehouse
        """

        domain = []
        domain.append(("shelf_location", "=", True))
        if _row:
            domain.append(("row", "like", _row))
        res = []
        ShelfInfo = self.env.datamodels["shelf.info"]
        for shelf in self.env["stock.location"].search(domain):
            res.append(ShelfInfo(id=shelf.id,bay=shelf.bay))
        return res

    @restapi.method(
        [(["/"], "POST")],
        input_param=restapi.Datamodel("shelf.create.param"),
        auth="public",
    )
    def create(self, shelf_create_param):
        """
        Create Shelf
        """
        params = {}
        params['shelf_location'] = True
        if shelf_create_param.bay:
            params['name'] = shelf_create_param.bay
        if shelf_create_param.row:
            #This will be the parent location
            row_location_id = self.env['stock.location'].search([('name','=',shelf_create_param.row)])[0].id
            params['location_id'] = row_location_id
        if shelf_create_param.width:
            params['width'] = shelf_create_param.width
        if shelf_create_param.height:
            params['height'] = shelf_create_param.height
        if shelf_create_param.depth:
            params['depth'] = shelf_create_param.depth


        shelf = self.env["stock.location"].create(params)
        return {"response": "Shelf has been created"}

    @restapi.method(
        [(["/<string:row>/<string:bay>"], "PATCH")],
        input_param=restapi.Datamodel("shelf.depth.info"),
        auth="public",
    )
    def update_shelf(self, row, bay,params):
        """
        Update on Shelf
        """
        shelf_location = self.env["stock.location"].search([("row","=",row),("bay","=",bay)])[0]
        shelf_location.write({'depth': params.depth})

        return {"response": "Shelf with requested row and bay is updated"}

    @restapi.method(
        [(["/<string:row>/<string:bay>"], "DELETE")],
        auth="public",
    )
    def delete_shelf(self, row, bay):
        """
        Delete on Shelf
        """
        self.env["stock.location"].search([("row", "=", row), ("bay", "=", bay)]).unlink()
        return {"response": "Shelf has been deleted"}
