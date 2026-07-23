class SyncService:


    def execute(
        self,
        system
    ):

        return {

            "system":system,

            "status":"completed"

        }



    def history(self):

        return []



service=SyncService()
