class SystemService:


    def health(self):

        return {

            "status":"healthy",

            "service":"PVIMP"

        }



    def settings(self):

        return []



service=SystemService()
