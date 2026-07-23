class MessageService:


    messages=[]


    def send(
        self,
        data
    ):

        self.messages.append(data)

        return {

            "sent":True,

            "message":data

        }



    def inbox(
        self,
        user_id
    ):

        return []



service=MessageService()
