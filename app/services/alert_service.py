class AlertService:


    alerts=[]


    def create(
        self,
        data
    ):

        self.alerts.append(data)

        return {

            "created":True,

            "alert":data

        }



    def active(self):

        return self.alerts



    def resolve(
        self,
        alert_id
    ):

        return {

            "resolved":True,

            "id":alert_id

        }



service=AlertService()
