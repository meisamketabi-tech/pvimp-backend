from app.services.import_engine.template19_sample_send import (
    Template19SampleSendImporter,
)

from app.services.import_engine.template20_disease_outbreak import (
    Template20DiseaseOutbreakImporter,
)


class ImporterFactory:

    @staticmethod
    def get_importer(template_id):

        if int(template_id) == 19:

            return Template19SampleSendImporter()

        if int(template_id) == 20:

            return Template20DiseaseOutbreakImporter()

        return None
