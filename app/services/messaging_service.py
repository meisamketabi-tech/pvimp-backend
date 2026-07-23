class MessagingService:


    def send(
        self,
        data
    ):

        return {

            "sent":True,

            "message":data

        }



    def inbox(
        self,
        user_id
    ):

        return []



service=MessagingService()
