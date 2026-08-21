class AutomationService:


    def schedule_report(
        self,
        data
    ):

        return {

            "scheduled":True,

            "report":data

        }



    def execute(
        self,
        job
    ):

        return {

            "executed":True,

            "job":job

        }



service=AutomationService()
