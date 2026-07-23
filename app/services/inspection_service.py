class InspectionService:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "inspection":data

        }



    def list(self):

        return []



service=InspectionService()
