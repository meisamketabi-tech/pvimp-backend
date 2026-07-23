class BackupService:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "backup":data

        }



    def restore(
        self,
        backup_id
    ):

        return {

            "restored":True,

            "id":backup_id

        }



    def history(self):

        return []



service=BackupService()
