class SecurityService:


    def log(
        self,
        data
    ):

        return {

            "logged":True,

            "security_event":data

        }



    def monitor(self):

        return []



service=SecurityService()
