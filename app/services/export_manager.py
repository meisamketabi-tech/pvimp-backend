class ExportManager:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "export":data

        }



    def status(
        self,
        export_id
    ):

        return {

            "id":export_id,

            "status":"ready"

        }



manager=ExportManager()
