class WorkflowBuilder:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "workflow":data

        }



    def execute(
        self,
        workflow,
        action
    ):

        return {

            "workflow":workflow,

            "action":action,

            "status":"executed"

        }



builder=WorkflowBuilder()
