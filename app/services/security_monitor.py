class SecurityMonitor:


    def check_access(
        self,
        data
    ):

        return {

            "allowed":True,

            "user":data.get("user_id")

        }



    def events(self):

        return []



monitor=SecurityMonitor()
