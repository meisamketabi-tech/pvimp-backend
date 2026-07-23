class ComplaintService:


    def submit(
        self,
        data
    ):

        return {

            "submitted":True,

            "complaint":data

        }



    def track(
        self,
        complaint_id
    ):

        return {

            "id":complaint_id,

            "status":"received"

        }



service=ComplaintService()
