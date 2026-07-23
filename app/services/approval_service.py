class ApprovalService:


    def request(
        self,
        data
    ):

        return {

            "requested":True,

            "approval":data

        }



    def approve(
        self,
        approval_id,
        data
    ):

        return {

            "approved":True,

            "id":approval_id,

            "data":data

        }



    def reject(
        self,
        approval_id,
        data
    ):

        return {

            "rejected":True,

            "id":approval_id,

            "data":data

        }



service=ApprovalService()
