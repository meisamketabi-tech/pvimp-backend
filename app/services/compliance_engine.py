class ComplianceEngine:


    def evaluate(self,data):

        result={
            "compliant":True,
            "issues":[]
        }


        if data.get("expired_permit"):

            result["compliant"]=False

            result["issues"].append(
                "Expired permit"
            )


        return result


engine=ComplianceEngine()
