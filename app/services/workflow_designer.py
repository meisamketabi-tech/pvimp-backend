class WorkflowDesigner:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "workflow":data

        }



    def validate(
        self,
        definition
    ):

        return {

            "valid":True,

            "definition":definition

        }



designer=WorkflowDesigner()
