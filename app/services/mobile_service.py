class MobileService:


    def sync(
        self,
        user,
        data
    ):

        return {

            "synced":True,

            "user":user,

            "data":data

        }



    def offline_package(
        self,
        user
    ):

        return {

            "user":user,

            "package":[]

        }



service=MobileService()
