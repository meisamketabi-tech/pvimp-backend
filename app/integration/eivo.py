class EIVOConnector:


    def sync(self,data):

        return {
            "status":"synchronized",
            "data":data
        }


connector=EIVOConnector()
