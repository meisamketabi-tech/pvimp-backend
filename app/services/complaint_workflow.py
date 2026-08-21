class ComplaintWorkflow:


    def process(
        self,
        complaint
    ):

        status="REGISTERED"


        if complaint.get("priority")=="HIGH":

            status="URGENT_REVIEW"


        return {

            "complaint":complaint,

            "status":status

        }



engine=ComplaintWorkflow()
