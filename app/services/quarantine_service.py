class QuarantineService:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "quarantine":data

        }



    def release(
        self,
        quarantine_id
    ):

        return {

            "released":True,

            "id":quarantine_id

        }



service=QuarantineService()
