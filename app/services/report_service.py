class ReportService:


    def generate(
        self,
        data
    ):

        return {

            "generated":True,

            "report":data

        }



    def list_reports(self):

        return []



service=ReportService()
