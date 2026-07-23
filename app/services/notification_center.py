class NotificationCenter:


    def dispatch(
        self,
        alert
    ):

        return {
            "sent":True,
            "alert":alert
        }



center=NotificationCenter()
