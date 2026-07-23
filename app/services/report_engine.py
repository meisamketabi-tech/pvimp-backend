class ReportEngine:


    def generate(self,template,data):

        return {
            "template":template,
            "data":data,
            "format":"PDF"
        }


engine=ReportEngine()
