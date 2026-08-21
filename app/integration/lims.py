class LIMSConnector:


    def send_sample(self,data):

        return {
            "status":"sent",
            "sample":data
        }


    def get_result(self,sample_id):

        return {
            "sample_id":sample_id,
            "result":"pending"
        }


connector=LIMSConnector()
