class DecisionSupport:


    def recommend(self,data):

        recommendations=[]


        if data.get("risk_level")=="HIGH":

            recommendations.append(
                "Increase inspection frequency"
            )

            recommendations.append(
                "Perform targeted sampling"
            )


        if not recommendations:

            recommendations.append(
                "Continue normal monitoring"
            )


        return recommendations


engine=DecisionSupport()
