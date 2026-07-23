class OutbreakService:


    def register(
        self,
        data
    ):

        return {

            "registered":True,

            "outbreak":data

        }



    def monitor(self):

        return []



service=OutbreakService()
