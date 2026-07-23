class LIMSService:


    def send_sample(
        self,
        sample
    ):

        return {
            "sent":True,
            "sample":sample
        }



    def receive_result(
        self,
        sample_id
    ):

        return {
            "sample_id":sample_id,
            "status":"pending"
        }



service=LIMSService()
