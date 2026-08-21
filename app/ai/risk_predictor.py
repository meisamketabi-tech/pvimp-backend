class RiskPredictor:


    def predict(self,data):

        score=0


        if data.get("past_violations",0)>3:
            score +=40


        if data.get("complaints",0)>5:
            score +=30


        if data.get("sampling_failures",0)>0:
            score +=30



        level="LOW"


        if score>=70:
            level="HIGH"

        elif score>=40:
            level="MEDIUM"


        return {
            "risk_score":score,
            "risk_level":level
        }


engine=RiskPredictor()
