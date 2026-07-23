class PlanningService:


    def create_plan(
        self,
        data
    ):

        return {

            "created":True,

            "plan":data

        }



    def generate_schedule(
        self,
        plan_id
    ):

        return {

            "plan_id":plan_id,

            "schedule":[]

        }



service=PlanningService()
