class LocationService:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "location":data

        }



    def list(
        self
    ):

        return []



service=LocationService()
