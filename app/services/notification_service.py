class NotificationService:


    notifications=[]


    def send(
        self,
        data
    ):

        self.notifications.append(data)


        return {

            "sent":True

        }



    def unread(
        self,
        user_id
    ):

        return [

        ]



service=NotificationService()
