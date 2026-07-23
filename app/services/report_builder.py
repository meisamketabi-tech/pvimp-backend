class ReportBuilder:


    def create(
        self,
        template,
        data
    ):

        return {

            "template":template,

            "data":data,

            "format":"PDF",

            "status":"ready"

        }



builder=ReportBuilder()
