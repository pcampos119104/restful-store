from extensions import ma
from models.item import ItemModel
from models.store import StoreModel

class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = ("store",)
        dump_only = ("id",)
        # to link with Store id
        include_fk = True
