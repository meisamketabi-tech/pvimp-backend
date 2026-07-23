class OrganizationService:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "unit":data

        }



    def tree(self):

        return []



service=OrganizationService()
