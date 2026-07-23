class LegalService:


    def create_case(
        self,
        data
    ):

        return {

            "created":True,

            "case":data

        }



    def update_status(
        self,
        case_id,
        status
    ):

        return {

            "updated":True,

            "id":case_id,

            "status":status

        }



service=LegalService()
