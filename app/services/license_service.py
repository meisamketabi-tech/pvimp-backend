class LicenseService:


    def issue(
        self,
        data
    ):

        return {

            "issued":True,

            "license":data

        }



    def verify(
        self,
        number
    ):

        return {

            "license":number,

            "valid":True

        }



service=LicenseService()
