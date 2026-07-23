class CalendarService:


    def create_event(
        self,
        data
    ):

        return {

            "created":True,

            "event":data

        }



    def plan_inspection(
        self,
        data
    ):

        return {

            "planned":True,

            "inspection":data

        }



service=CalendarService()
