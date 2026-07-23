class UnitService:


    def register(
        self,
        data
    ):

        return {
            "registered":True,
            "unit":data
        }



    def search(
        self,
        keyword
    ):

        return []



service=UnitService()
