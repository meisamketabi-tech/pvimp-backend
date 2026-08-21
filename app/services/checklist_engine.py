class ChecklistEngine:


    def evaluate(
        self,
        answers
    ):

        failed=[]


        for item in answers:

            if item.get("answer")=="NO":

                failed.append(item)



        return {
            "passed":
            len(failed)==0,

            "failed_items":failed
        }



engine=ChecklistEngine()
