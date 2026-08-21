from app.db.session import SessionLocal

from app.db.models.inspection import InspectionType


def seed():

    db = SessionLocal()

    types = [

        "بازرسی بهداشت و مدیریت بیماری‌های دامی",

        "بازرسی بهداشت و مدیریت بیماری‌های طیور",

        "بازرسی بهداشت عمومی و مواد غذایی",

        "بازرسی قرنطینه و امنیت زیستی",

        "بازرسی آزمایشگاه دامپزشکی",

        "بازرسی مراکز عرضه فرآورده‌های خام دامی",

        "بازرسی کشتارگاه‌ها",

    ]


    try:

        for title in types:

            exists = (
                db.query(InspectionType)
                .filter(
                    InspectionType.title == title
                )
                .first()
            )

            if not exists:

                obj = InspectionType(
                    title=title,
                    description=title,
                    is_active=True,
                )

                db.add(obj)


        db.commit()

        print("Inspection types seeded")


    finally:

        db.close()



if __name__ == "__main__":
    seed()