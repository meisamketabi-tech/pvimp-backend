class ProfileService:


    def update(
        self,
        data
    ):

        return {

            "updated":True,

            "profile":data

        }



    def get(
        self,
        user_id
    ):

        return {

            "user_id":user_id,

            "profile":{}

        }



service=ProfileService()
