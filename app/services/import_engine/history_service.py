from sqlalchemy import text
from datetime import datetime



class HistoryService:
    """
    Store import changes history.
    """



    def create_history(
        self,
        db,
        table_name,
        operation,
        old_data,
        new_data
    ):

        sql = """
        INSERT INTO gis_import_history
        (
            table_name,
            operation,
            old_data,
            new_data,
            created_at
        )

        VALUES
        (
            :table_name,
            :operation,
            :old_data,
            :new_data,
            :created_at
        )
        """

        db.execute(
            text(sql),
            {
                "table_name": table_name,
                "operation": operation,
                "old_data": str(old_data),
                "new_data": str(new_data),
                "created_at": datetime.utcnow()
            }
        )



    def record_insert(
        self,
        db,
        table_name,
        new_data
    ):

        self.create_history(
            db,
            table_name,
            "INSERT",
            None,
            new_data
        )



    def record_update(
        self,
        db,
        table_name,
        old_data,
        new_data
    ):

        self.create_history(
            db,
            table_name,
            "UPDATE",
            old_data,
            new_data
        )



    def record_delete(
        self,
        db,
        table_name,
        old_data
    ):

        self.create_history(
            db,
            table_name,
            "DELETE",
            old_data,
            None
        )