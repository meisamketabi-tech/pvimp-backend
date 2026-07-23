class TaskEngine:


    def create(
        self,
        data
    ):

        return {
            "created":True,
            "task":data
        }



    def close(
        self,
        task_id
    ):

        return {
            "closed":True,
            "task_id":task_id
        }



engine=TaskEngine()
