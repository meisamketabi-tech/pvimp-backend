class LabService:


    def register_result(
        self,
        data
    ):

        return {

            "registered":True,

            "result":data

        }



    def get_result(
        self,
        sample_id
    ):

        return {

            "sample_id":sample_id,

            "results":[]

        }



service=LabService()
