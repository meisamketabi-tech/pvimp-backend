import json


class InspectionFormEngine:


    def build(
        self,
        schema
    ):

        return json.loads(schema)



    def validate(
        self,
        schema,
        data
    ):

        errors=[]


        for field in schema:

            if field.get("required"):

                if field.get("name") not in data:

                    errors.append(
                        field.get("name")
                    )


        return {
            "valid":
            len(errors)==0,
            "errors":errors
        }



engine=InspectionFormEngine()
