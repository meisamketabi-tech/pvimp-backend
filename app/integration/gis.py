class GISConnector:


    def get_location(self,entity_id):

        return {
            "entity_id":entity_id,
            "latitude":0,
            "longitude":0
        }


connector=GISConnector()
