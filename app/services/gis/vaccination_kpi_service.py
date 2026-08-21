from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

VACCINATION_TABLE = "gis_vaccination_performances"


def _filters(
    province_code: str | None = None,
    county_code: str | None = None,
    vaccine_type: str | None = None,
    unit_code: str | None = None,
) -> tuple[str, dict[str, Any]]:

    clauses: list[str] = []
    params: dict[str, Any] = {}

    if province_code:
        clauses.append("province_code = :province_code")
        params["province_code"] = province_code

    if county_code:
        clauses.append("county_code = :county_code")
        params["county_code"] = county_code

    if vaccine_type:
        clauses.append("vaccine_type = :vaccine_type")
        params["vaccine_type"] = vaccine_type

    if unit_code:
        clauses.append("epidemiology_unit_code = :unit_code")
        params["unit_code"] = unit_code

    if not clauses:
        return "", params

    return (
        " WHERE " + " AND ".join(clauses),
        params,
    )


def _pct(
    numerator: float | None,
    denominator: float | None,
) -> float:

    if not denominator:
        return 0.0

    return round(
        (float(numerator or 0) / float(denominator)) * 100,
        2,
    )


def _adverse_events(
    row: Any,
) -> int:

    return sum(
        int(row[key] or 0)
        for key in (
            "shock_count",
            "death_count",
            "abortion_count",
            "hypersensitivity_count",
            "local_complication_count",
        )
    )


def _master_animals_sql(
    alias: str = "u",
) -> str:

    return f"""
        COALESCE({alias}.sheep_count,0)
        +
        COALESCE({alias}.cattle_count,0)
        +
        COALESCE({alias}.goat_count,0)
        +
        COALESCE({alias}.horse_count,0)
        +
        COALESCE({alias}.dog_count,0)
        +
        COALESCE({alias}.camel_count,0)
        +
        COALESCE({alias}.buffalo_count,0)
    """


def _coverage_denominator(
    eligible_animals: int,
    recorded_total_animals: int,
    master_animals: int = 0,
) -> int:

    if eligible_animals > 0:
        return eligible_animals

    if recorded_total_animals > 0:
        return recorded_total_animals

    return master_animals


def _coverage_status(
    coverage: float,
) -> str:

    if coverage < 50:
        return "CRITICAL"

    if coverage < 75:
        return "WARNING"

    if coverage < 90:
        return "ON_TRACK"

    return "EXCELLENT"


def dashboard(
    db: Session,
    province_code: str | None = None,
    county_code: str | None = None,
    vaccine_type: str | None = None,
) -> dict[str, Any]:

    where, params = _filters(
        province_code,
        county_code,
        vaccine_type,
    )

    query = text(f"""
        SELECT

            COUNT(*) AS records,

            COALESCE(
                SUM(total_animals),
                0
            ) AS total_animals,

            COALESCE(
                SUM(eligible_animals),
                0
            ) AS eligible_animals,

            COALESCE(
                SUM(vaccinated_animals),
                0
            ) AS vaccinated_animals,

            COUNT(
                DISTINCT county_code
            ) AS counties,

            COUNT(
                DISTINCT epidemiology_unit_code
            ) AS units,

            COUNT(
                DISTINCT vaccine_type
            ) AS vaccine_types,

            COALESCE(
                SUM(shock_count),
                0
            )
            +
            COALESCE(
                SUM(death_count),
                0
            )
            +
            COALESCE(
                SUM(abortion_count),
                0
            )
            +
            COALESCE(
                SUM(hypersensitivity_count),
                0
            )
            +
            COALESCE(
                SUM(local_complication_count),
                0
            ) AS adverse_events

        FROM {VACCINATION_TABLE}

        {where}
        """)

    row = (
        db.execute(
            query,
            params,
        )
        .mappings()
        .one()
    )

    total_animals = int(row["total_animals"] or 0)

    eligible_animals = int(row["eligible_animals"] or 0)

    vaccinated_animals = int(row["vaccinated_animals"] or 0)

    denominator = _coverage_denominator(
        eligible_animals,
        total_animals,
    )

    adverse_events = int(row["adverse_events"] or 0)

    return {
        "records": int(row["records"] or 0),
        "total_animals": total_animals,
        "eligible_animals": eligible_animals,
        "coverage_denominator": denominator,
        "vaccinated_animals": vaccinated_animals,
        "remaining_animals": max(
            denominator - vaccinated_animals,
            0,
        ),
        "coverage_percent": _pct(
            vaccinated_animals,
            denominator,
        ),
        "counties": int(row["counties"] or 0),
        "units": int(row["units"] or 0),
        "vaccine_types": int(row["vaccine_types"] or 0),
        "adverse_events": adverse_events,
        "adverse_event_rate_percent": _pct(
            adverse_events,
            vaccinated_animals,
        ),
    }


def counties(
    db: Session,
    province_code: str | None = None,
    vaccine_type: str | None = None,
) -> list[dict[str, Any]]:

    where, params = _filters(
        province_code,
        None,
        vaccine_type,
    )

    query = text(f"""
        SELECT

            county_code,

            MAX(county_name)
                AS county_name,

            COUNT(*) AS records,

            COUNT(
                DISTINCT epidemiology_unit_code
            ) AS units,

            COALESCE(
                SUM(total_animals),
                0
            ) AS total_animals,

            COALESCE(
                SUM(eligible_animals),
                0
            ) AS eligible_animals,

            COALESCE(
                SUM(vaccinated_animals),
                0
            ) AS vaccinated_animals,

            COALESCE(
                SUM(shock_count),
                0
            )
            +
            COALESCE(
                SUM(death_count),
                0
            )
            +
            COALESCE(
                SUM(abortion_count),
                0
            )
            +
            COALESCE(
                SUM(hypersensitivity_count),
                0
            )
            +
            COALESCE(
                SUM(local_complication_count),
                0
            ) AS adverse_events

        FROM {VACCINATION_TABLE}

        {where}

        GROUP BY county_code

        ORDER BY county_name NULLS LAST
        """)

    rows = (
        db.execute(
            query,
            params,
        )
        .mappings()
        .all()
    )

    result: list[dict[str, Any]] = []

    for row in rows:

        total_animals = int(row["total_animals"] or 0)

        eligible_animals = int(row["eligible_animals"] or 0)

        vaccinated_animals = int(row["vaccinated_animals"] or 0)

        denominator = _coverage_denominator(
            eligible_animals,
            total_animals,
        )

        coverage = _pct(
            vaccinated_animals,
            denominator,
        )

        result.append(
            {
                "county_code": row["county_code"],
                "county_name": row["county_name"],
                "records": int(row["records"] or 0),
                "units": int(row["units"] or 0),
                "total_animals": total_animals,
                "eligible_animals": eligible_animals,
                "coverage_denominator": denominator,
                "vaccinated_animals": vaccinated_animals,
                "remaining_animals": max(
                    denominator - vaccinated_animals,
                    0,
                ),
                "coverage_percent": coverage,
                "status": _coverage_status(
                    coverage,
                ),
                "adverse_events": int(row["adverse_events"] or 0),
            }
        )

    return result


def vaccines(
    db: Session,
    province_code: str | None = None,
    county_code: str | None = None,
    vaccine_type: str | None = None,
    unit_code: str | None = None,
) -> list[dict[str, Any]]:

    where, params = _filters(
        province_code,
        county_code,
        vaccine_type,
        unit_code,
    )

    query = text(f"""
        SELECT

            vaccine_type,

            MAX(vaccine_brand)
                AS vaccine_brand,

            COUNT(*) AS records,

            COALESCE(
                SUM(total_animals),
                0
            ) AS total_animals,

            COALESCE(
                SUM(eligible_animals),
                0
            ) AS eligible_animals,

            COALESCE(
                SUM(vaccinated_animals),
                0
            ) AS vaccinated_animals,

            COALESCE(
                SUM(shock_count),
                0
            )
            +
            COALESCE(
                SUM(death_count),
                0
            )
            +
            COALESCE(
                SUM(abortion_count),
                0
            )
            +
            COALESCE(
                SUM(hypersensitivity_count),
                0
            )
            +
            COALESCE(
                SUM(local_complication_count),
                0
            ) AS adverse_events

        FROM {VACCINATION_TABLE}

        {where}

        GROUP BY vaccine_type

        ORDER BY vaccine_type NULLS LAST
        """)

    rows = (
        db.execute(
            query,
            params,
        )
        .mappings()
        .all()
    )

    result: list[dict[str, Any]] = []

    for row in rows:

        total_animals = int(row["total_animals"] or 0)

        eligible_animals = int(row["eligible_animals"] or 0)

        vaccinated_animals = int(row["vaccinated_animals"] or 0)

        denominator = _coverage_denominator(
            eligible_animals,
            total_animals,
        )

        adverse_events = int(row["adverse_events"] or 0)

        result.append(
            {
                "vaccine_type": row["vaccine_type"],
                "vaccine_brand": row["vaccine_brand"],
                "records": int(row["records"] or 0),
                "total_animals": total_animals,
                "eligible_animals": eligible_animals,
                "coverage_denominator": denominator,
                "vaccinated_animals": vaccinated_animals,
                "remaining_animals": max(
                    denominator - vaccinated_animals,
                    0,
                ),
                "coverage_percent": _pct(
                    vaccinated_animals,
                    denominator,
                ),
                "adverse_events": adverse_events,
                "adverse_event_rate_percent": _pct(
                    adverse_events,
                    vaccinated_animals,
                ),
            }
        )

    return result


def units(
    db: Session,
    province_code: str | None = None,
    county_code: str | None = None,
    vaccine_type: str | None = None,
    unit_code: str | None = None,
) -> list[dict[str, Any]]:

    where, params = _filters(
        province_code,
        county_code,
        vaccine_type,
        unit_code,
    )

    query = text(f"""
        SELECT

            epidemiology_unit_code,

            MAX(epidemiology_unit_name)
                AS epidemiology_unit_name,

            MAX(province_name)
                AS province_name,

            MAX(county_name)
                AS county_name,

            MAX(epidemiology_unit_type)
                AS epidemiology_unit_type,

            COUNT(*) AS records,

            COALESCE(
                SUM(total_animals),
                0
            ) AS total_animals,

            COALESCE(
                SUM(eligible_animals),
                0
            ) AS eligible_animals,

            COALESCE(
                SUM(vaccinated_animals),
                0
            ) AS vaccinated_animals,

            COALESCE(
                SUM(shock_count),
                0
            )
            +
            COALESCE(
                SUM(death_count),
                0
            )
            +
            COALESCE(
                SUM(abortion_count),
                0
            )
            +
            COALESCE(
                SUM(hypersensitivity_count),
                0
            )
            +
            COALESCE(
                SUM(local_complication_count),
                0
            ) AS adverse_events

        FROM {VACCINATION_TABLE}

        {where}

        GROUP BY epidemiology_unit_code

        ORDER BY
            county_name NULLS LAST,
            epidemiology_unit_name NULLS LAST
        """)

    rows = (
        db.execute(
            query,
            params,
        )
        .mappings()
        .all()
    )

    result: list[dict[str, Any]] = []

    for row in rows:

        total_animals = int(row["total_animals"] or 0)

        eligible_animals = int(row["eligible_animals"] or 0)

        vaccinated_animals = int(row["vaccinated_animals"] or 0)

        denominator = _coverage_denominator(
            eligible_animals,
            total_animals,
        )

        adverse_events = int(row["adverse_events"] or 0)

        coverage = _pct(
            vaccinated_animals,
            denominator,
        )

        result.append(
            {
                "unit_code": row["epidemiology_unit_code"],
                "unit_name": row["epidemiology_unit_name"],
                "province_name": row["province_name"],
                "county_name": row["county_name"],
                "unit_type": row["epidemiology_unit_type"],
                "records": int(row["records"] or 0),
                "total_animals": total_animals,
                "eligible_animals": eligible_animals,
                "coverage_denominator": denominator,
                "vaccinated_animals": vaccinated_animals,
                "remaining_animals": max(
                    denominator - vaccinated_animals,
                    0,
                ),
                "coverage_percent": coverage,
                "status": _coverage_status(
                    coverage,
                ),
                "adverse_events": adverse_events,
                "adverse_event_rate_percent": _pct(
                    adverse_events,
                    vaccinated_animals,
                ),
            }
        )

    return result


def vaccine_unit_report(
    db: Session,
    vaccine_type: str,
    province_code: str | None = None,
    county_code: str | None = None,
) -> list[dict[str, Any]]:

    return [
        item
        for item in units(
            db,
            province_code=province_code,
            county_code=county_code,
            vaccine_type=vaccine_type,
        )
    ]


def county_units_report(
    db: Session,
    county_id: int,
) -> dict[str, Any]:

    query = text(f"""
        SELECT

            u.id,

            u.unit_code,

            u.unit_name,

            u.county_id,

            p.province_code,

            p.province_name,

            c.county_code,

            c.county_name,

            {_master_animals_sql("u")}
                AS master_animals,

            ut.title
                AS unit_type,

            COALESCE(
                v.records,
                0
            ) AS records,

            COALESCE(
                v.total_animals,
                0
            ) AS recorded_total_animals,

            COALESCE(
                v.eligible_animals,
                0
            ) AS eligible_animals,

            COALESCE(
                v.vaccinated_animals,
                0
            ) AS vaccinated_animals,

            COALESCE(
                v.adverse_events,
                0
            ) AS adverse_events


        FROM gis_epidemiology_units u


        JOIN gis_provinces p

            ON p.id = u.province_id


        JOIN gis_counties c

            ON c.id = u.county_id


        LEFT JOIN gis_epidemiology_unit_types ut

            ON ut.id = u.unit_type_id


        LEFT JOIN (

            SELECT

                epidemiology_unit_code,

                COUNT(*) AS records,

                COALESCE(
                    SUM(total_animals),
                    0
                ) AS total_animals,

                COALESCE(
                    SUM(eligible_animals),
                    0
                ) AS eligible_animals,

                COALESCE(
                    SUM(vaccinated_animals),
                    0
                ) AS vaccinated_animals,

                COALESCE(
                    SUM(shock_count),
                    0
                )
                +
                COALESCE(
                    SUM(death_count),
                    0
                )
                +
                COALESCE(
                    SUM(abortion_count),
                    0
                )
                +
                COALESCE(
                    SUM(hypersensitivity_count),
                    0
                )
                +
                COALESCE(
                    SUM(local_complication_count),
                    0
                ) AS adverse_events


            FROM {VACCINATION_TABLE}


            GROUP BY epidemiology_unit_code

        ) v


        ON v.epidemiology_unit_code =
           u.unit_code


        WHERE
            u.is_active = TRUE

        AND
            u.county_id = :county_id


        ORDER BY
            u.unit_name NULLS LAST
        """)

    rows = (
        db.execute(
            query,
            {
                "county_id": county_id,
            },
        )
        .mappings()
        .all()
    )

    result: list[dict[str, Any]] = []

    county_name = None
    county_code = None

    province_name = None
    province_code = None

    for row in rows:

        county_name = row["county_name"]
        county_code = row["county_code"]

        province_name = row["province_name"]
        province_code = row["province_code"]

        master_animals = int(row["master_animals"] or 0)

        recorded_total_animals = int(row["recorded_total_animals"] or 0)

        eligible_animals = int(row["eligible_animals"] or 0)

        vaccinated_animals = int(row["vaccinated_animals"] or 0)

        denominator = _coverage_denominator(
            eligible_animals,
            recorded_total_animals,
            master_animals,
        )

        coverage = _pct(
            vaccinated_animals,
            denominator,
        )

        result.append(
            {
                "unit_id": row["id"],
                "unit_code": row["unit_code"],
                "unit_name": row["unit_name"],
                "province_code": province_code,
                "province_name": province_name,
                "county_id": county_id,
                "county_code": county_code,
                "county_name": county_name,
                "unit_type": row["unit_type"],
                "records": int(row["records"] or 0),
                "master_animals": master_animals,
                "total_animals": recorded_total_animals,
                "eligible_animals": eligible_animals,
                "coverage_denominator": denominator,
                "vaccinated_animals": vaccinated_animals,
                "remaining_animals": max(
                    denominator - vaccinated_animals,
                    0,
                ),
                "coverage_percent": coverage,
                "status": _coverage_status(
                    coverage,
                ),
                "adverse_events": int(row["adverse_events"] or 0),
                "adverse_event_rate_percent": _pct(
                    int(row["adverse_events"] or 0),
                    vaccinated_animals,
                ),
            }
        )

    return {
        "county_id": county_id,
        "county_code": county_code,
        "county_name": county_name,
        "province_code": province_code,
        "province_name": province_name,
        "units_count": len(result),
        "units": result,
    }


def alerts(
    db: Session,
    province_code: str | None = None,
    vaccine_type: str | None = None,
) -> list[dict[str, Any]]:

    result: list[dict[str, Any]] = []

    for row in counties(
        db,
        province_code=province_code,
        vaccine_type=vaccine_type,
    ):

        coverage = float(row["coverage_percent"] or 0)

        adverse_rate = float(
            row.get(
                "adverse_event_rate_percent",
                0,
            )
            or 0
        )

        if coverage < 50:

            result.append(
                {
                    "severity": "CRITICAL",
                    "type": "LOW_COVERAGE",
                    "county_code": row["county_code"],
                    "county_name": row["county_name"],
                    "message": ("پوشش واکسیناسیون شهرستان " "کمتر از ۵۰ درصد است."),
                    "details": row,
                }
            )

        elif coverage < 75:

            result.append(
                {
                    "severity": "WARNING",
                    "type": "LOW_COVERAGE",
                    "county_code": row["county_code"],
                    "county_name": row["county_name"],
                    "message": ("پوشش واکسیناسیون شهرستان " "نیازمند پیگیری است."),
                    "details": row,
                }
            )

        if adverse_rate >= 1:

            result.append(
                {
                    "severity": "HIGH",
                    "type": "ADVERSE_EVENT_RATE",
                    "county_code": row["county_code"],
                    "county_name": row["county_name"],
                    "message": ("نرخ عوارض واکسیناسیون " "نیازمند بررسی است."),
                    "details": row,
                }
            )

    return result


def effectiveness(
    db: Session,
    province_code: str | None = None,
    county_code: str | None = None,
    vaccine_type: str | None = None,
    unit_code: str | None = None,
) -> dict[str, Any]:

    where, params = _filters(
        province_code,
        county_code,
        vaccine_type,
        unit_code,
    )

    vaccination = (
        db.execute(
            text(f"""
                SELECT

                    COUNT(
                        DISTINCT epidemiology_unit_code
                    ) AS vaccinated_units,

                    COALESCE(
                        SUM(vaccinated_animals),
                        0
                    ) AS vaccinated_animals,

                    COALESCE(
                        SUM(shock_count),
                        0
                    )
                    +
                    COALESCE(
                        SUM(death_count),
                        0
                    )
                    +
                    COALESCE(
                        SUM(abortion_count),
                        0
                    )
                    +
                    COALESCE(
                        SUM(hypersensitivity_count),
                        0
                    )
                    +
                    COALESCE(
                        SUM(local_complication_count),
                        0
                    ) AS adverse_events


                FROM {VACCINATION_TABLE}

                {where}
                """),
            params,
        )
        .mappings()
        .one()
    )

    disease_params: dict[str, Any] = {}

    disease_where: list[str] = []

    if province_code:

        disease_where.append("""
            p.province_code = :province_code
            """)

        disease_params["province_code"] = province_code

    if county_code:

        disease_where.append("""
            c.county_code = :county_code
            """)

        disease_params["county_code"] = county_code

    if unit_code:

        disease_where.append("""
            u.unit_code = :unit_code
            """)

        disease_params["unit_code"] = unit_code

    disease_filter = ""

    if disease_where:

        disease_filter = " WHERE " + " AND ".join(disease_where)

    disease = (
        db.execute(
            text(f"""
                SELECT

                    COUNT(*) AS disease_records,

                    COUNT(
                        DISTINCT
                        d.epidemiology_unit_id
                    ) AS affected_units,

                    COALESCE(
                        SUM(d.infected_count),
                        0
                    ) AS infected_count,

                    COALESCE(
                        SUM(d.dead_count),
                        0
                    ) AS dead_count


                FROM gis_disease_occurrences d


                LEFT JOIN gis_epidemiology_units u

                    ON u.id =
                       d.epidemiology_unit_id


                LEFT JOIN gis_counties c

                    ON c.id =
                       u.county_id


                LEFT JOIN gis_provinces p

                    ON p.id =
                       u.province_id


                {disease_filter}
                """),
            disease_params,
        )
        .mappings()
        .one()
    )

    vaccinated_animals = int(vaccination["vaccinated_animals"] or 0)

    adverse_events = int(vaccination["adverse_events"] or 0)

    return {
        "vaccinated_units": int(vaccination["vaccinated_units"] or 0),
        "vaccinated_animals": vaccinated_animals,
        "adverse_events": adverse_events,
        "adverse_event_rate_percent": _pct(
            adverse_events,
            vaccinated_animals,
        ),
        "disease_records": int(disease["disease_records"] or 0),
        "affected_units": int(disease["affected_units"] or 0),
        "infected_count": int(disease["infected_count"] or 0),
        "dead_count": int(disease["dead_count"] or 0),
        "interpretation": (
            "رخداد بیماری پس از واکسیناسیون "
            "تنها یک سیگنال بررسی است و "
            "به‌تنهایی اثبات‌کننده عدم "
            "اثربخشی واکسن نیست."
        ),
    }


def unit_detail(
    db: Session,
    unit_code: str,
) -> dict[str, Any]:

    return {
        "unit_code": unit_code,
        "vaccination": units(
            db,
            unit_code=unit_code,
        ),
        "vaccines": vaccines(
            db,
            unit_code=unit_code,
        ),
        "effectiveness": effectiveness(
            db,
            unit_code=unit_code,
        ),
    }


def vaccine_county_report(
    db: Session,
    vaccine_type: str,
    province_code: str | None = None,
    county_code: str | None = None,
) -> list[dict[str, Any]]:

    return counties(
        db,
        province_code=province_code,
        vaccine_type=vaccine_type,
    )


def vaccine_management_report(
    db: Session,
    province_code: str | None = None,
    county_code: str | None = None,
    vaccine_type: str | None = None,
) -> dict[str, Any]:

    return {
        "dashboard": dashboard(
            db,
            province_code=province_code,
            county_code=county_code,
            vaccine_type=vaccine_type,
        ),
        "counties": counties(
            db,
            province_code=province_code,
            vaccine_type=vaccine_type,
        ),
        "vaccines": vaccines(
            db,
            province_code=province_code,
            county_code=county_code,
            vaccine_type=vaccine_type,
        ),
        "units": units(
            db,
            province_code=province_code,
            county_code=county_code,
            vaccine_type=vaccine_type,
        ),
        "alerts": alerts(
            db,
            province_code=province_code,
            vaccine_type=vaccine_type,
        ),
    }


def vaccine_unit_report_paginated(
    db: Session,
    vaccine_type: str,
    province_code: str | None = None,
    county_code: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> dict[str, Any]:

    data = vaccine_unit_report(
        db,
        vaccine_type=vaccine_type,
        province_code=province_code,
        county_code=county_code,
    )

    total = len(data)

    start = (page - 1) * page_size

    end = start + page_size

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": ((total + page_size - 1) // page_size if page_size else 1),
        "items": data[start:end],
    }
