class TaskManager:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "task":data

        }



    def update_status(
        self,
        task_id,
        status
    ):

        return {

            "updated":True,

            "id":task_id,

            "status":status

        }



    def my_tasks(
        self,
        user_id
    ):

        return []



manager=TaskManager()
