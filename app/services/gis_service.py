class GISService:


    def register(
        self,
        data
    ):

        return {

            "registered":True,

            "location":data

        }



    def nearby(
        self,
        lat,
        lng
    ):

        return []



service=GISService()
