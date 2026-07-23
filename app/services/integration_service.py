class IntegrationService:


    def register(
        self,
        data
    ):

        return {

            "registered":True,

            "integration":data

        }



    def sync(
        self,
        system
    ):

        return {

            "system":system,

            "synced":True

        }



service=IntegrationService()
