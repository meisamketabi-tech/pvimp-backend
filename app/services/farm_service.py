class FarmService:


    def register(
        self,
        data
    ):

        return {

            "registered":True,

            "farm":data

        }



    def search(
        self,
        keyword
    ):

        return []



service=FarmService()
