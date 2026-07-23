class DashboardService:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "dashboard":data

        }



    def load(
        self,
        role
    ):

        return {

            "role":role,

            "widgets":[]

        }



service=DashboardService()
