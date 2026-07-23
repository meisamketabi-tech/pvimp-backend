class InventoryService:


    def add(
        self,
        data
    ):

        return {

            "added":True,

            "item":data

        }



    def stock(
        self
    ):

        return []



service=InventoryService()
