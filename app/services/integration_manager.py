class IntegrationManager:


    systems={

        "GIS":"active",

        "LIMS":"active",

        "EIVO":"active"

    }



    def status(self):

        return self.systems



    def sync(
        self,
        system,
        data
    ):

        return {

            "system":system,

            "synced":True,

            "data":data

        }



manager=IntegrationManager()
