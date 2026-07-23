class DiseaseService:


    def register(
        self,
        data
    ):

        return {

            "registered":True,

            "disease":data

        }



    def list(self):

        return []



service=DiseaseService()
