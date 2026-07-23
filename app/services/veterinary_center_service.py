class VeterinaryCenterService:


    def register(
        self,
        data
    ):

        return {

            "registered":True,

            "center":data

        }



    def search(
        self,
        keyword
    ):

        return []



service=VeterinaryCenterService()
