from ma import ma
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema

class StoreSchema(ma.ModelSchema):
    items = ma.Nested(ItemSchema, many=True)
    class Meta:
        model = StoreModel
        load_only = ("store")
        dump_only = ("id",)
        # to link with Store id
        include_fk = True
