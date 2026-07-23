class AssignmentService:


    def assign(
        self,
        data
    ):

        return {

            "assigned":True,

            "assignment":data

        }



    def accept(
        self,
        assignment_id
    ):

        return {

            "accepted":True,

            "id":assignment_id

        }



service=AssignmentService()
