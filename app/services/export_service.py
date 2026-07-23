class ExportService:


    def excel(
        self,
        data
    ):

        return {
            "format":"xlsx",
            "data":data
        }



    def pdf(
        self,
        data
    ):

        return {
            "format":"pdf",
            "data":data
        }



service=ExportService()
