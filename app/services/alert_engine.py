class AlertEngine:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "alert":data

        }



    def active(self):

        return []



engine=AlertEngine()
