from app.workflow.transitions import TRANSITIONS



class WorkflowRuntime:


    def can_move(
        self,
        current,
        target
    ):

        return (
            current,
            target
        ) in TRANSITIONS



    def move(
        self,
        current,
        target
    ):

        if self.can_move(
            current,
            target
        ):

            return {
                "success":True,
                "state":target
            }


        return {
            "success":False,
            "state":current
        }



runtime=WorkflowRuntime()
