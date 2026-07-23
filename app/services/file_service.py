class FileService:


    def upload(
        self,
        data
    ):

        return {

            "uploaded":True,

            "file":data

        }



    def list_files(
        self,
        entity,
        entity_id
    ):

        return []



service=FileService()
