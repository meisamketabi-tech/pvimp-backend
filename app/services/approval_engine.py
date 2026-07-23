class ApprovalEngine:


    def approve(
        self,
        data
    ):

        return {

            "approved":True,

            "entity":data

        }



    def reject(
        self,
        data
    ):

        return {

            "approved":False,

            "entity":data

        }



engine=ApprovalEngine()
