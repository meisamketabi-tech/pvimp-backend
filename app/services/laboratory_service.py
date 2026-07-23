class LaboratoryService:


    def send_sample(
        self,
        data
    ):

        return {

            "sent":True,

            "request":data

        }



    def receive_result(
        self,
        data
    ):

        return {

            "received":True,

            "result":data

        }



service=LaboratoryService()
