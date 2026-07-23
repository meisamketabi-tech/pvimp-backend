class SmartInspectionPlanner:


    def generate(self,units):

        result=[]


        for unit in units:

            result.append(
                {
                    "unit_id":unit,
                    "priority":"NORMAL"
                }
            )


        return result


engine=SmartInspectionPlanner()
