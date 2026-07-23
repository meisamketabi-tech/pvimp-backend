class DocumentService:


    def upload(
        self,
        data
    ):

        return {

            "uploaded":True,

            "document":data

        }



    def list(
        self
    ):

        return []



    def delete(
        self,
        document_id
    ):

        return {

            "deleted":True,

            "id":document_id

        }



service=DocumentService()
