class KPIService:


    def calculate(
        self,
        data
    ):

        return {

            "calculated":True,

            "kpi":data

        }



    def dashboard(self):

        return []



service=KPIService()
