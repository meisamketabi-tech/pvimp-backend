class AnimalService:


    def register(
        self,
        data
    ):

        return {

            "registered":True,

            "animal":data

        }



    def get(
        self,
        animal_id
    ):

        return {

            "id":animal_id

        }



service=AnimalService()
