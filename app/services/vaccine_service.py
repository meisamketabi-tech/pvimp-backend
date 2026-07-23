class VaccineService:


    def register(
        self,
        data
    ):

        return {

            "registered":True,

            "vaccine":data

        }



    def inventory(self):

        return []



service=VaccineService()
