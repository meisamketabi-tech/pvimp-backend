class ViolationService:


    def register(
        self,
        data
    ):

        return {

            "registered":True,

            "violation":data

        }



    def resolve(
        self,
        violation_id
    ):

        return {

            "resolved":True,

            "id":violation_id

        }



service=ViolationService()
