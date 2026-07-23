class ChecklistService:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "checklist":data

        }



    def get(
        self,
        checklist_id
    ):

        return {

            "id":checklist_id,

            "items":[]

        }



service=ChecklistService()
