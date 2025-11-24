"""Simple tests to verify GPSS API schemas work correctly."""

from mcp_tools.schemas import (
    DateRange,
    GPSSAPIRequest,
    GPSSAPIResponse,
    OutputFormat,
    OutputSettings,
    PatAG,
    PatDB,
    PatTY,
    PatentRecord,
    SearchCondition,
    SearchLogicOperator,
    SearchQuery,
    SearchSettings,
)


def test_enums():
    """Enumerations expose expected values."""

    assert PatDB.TWA.value == "TWA"
    assert PatDB.USA.value == "USA"
    assert len(list(PatDB)) == 23

    assert PatAG.A.value == "A"
    assert PatAG.B.value == "B"

    assert PatTY.I.value == "I"
    assert PatTY.M.value == "M"
    assert PatTY.D.value == "D"

    assert OutputFormat.XML.value == "xml"
    assert OutputFormat.JSON.value == "json"


def test_search_condition():
    """SearchCondition should map aliases and data correctly."""

    search = SearchCondition(TI="無線裝置")
    assert search.title == "無線裝置"

    search = SearchCondition(TI="無線裝置", AB="降低功耗", IY="US")
    assert search.title == "無線裝置"
    assert search.abstract == "降低功耗"
    assert search.inventor_country == "US"

    data = search.model_dump(by_alias=True, exclude_none=True)
    assert data["TI"] == "無線裝置"
    assert data["AB"] == "降低功耗"
    assert data["IY"] == "US"


def test_search_settings():
    """SearchSettings should serialize using GPSS aliases."""

    settings = SearchSettings(
        patDB=[PatDB.TWA, PatDB.USA], patAG=[PatAG.A], patTY=[PatTY.I]
    )

    assert settings.databases == [PatDB.TWA, PatDB.USA]
    assert settings.application_type == [PatAG.A]
    assert settings.patent_type == [PatTY.I]

    data = settings.model_dump(by_alias=True, exclude_none=True)
    assert data["patDB"] == [PatDB.TWA, PatDB.USA]


def test_output_settings():
    """OutputSettings should expose numeric and enum fields."""

    output = OutputSettings(expQty=50, expSkip=100, expFmt=OutputFormat.JSON)

    assert output.quantity == 50
    assert output.skip == 100
    assert output.format == OutputFormat.JSON


def test_api_request():
    """GPSSAPIRequest should serialize search criteria without auth info."""

    search = SearchCondition(TI="AI")
    request = GPSSAPIRequest(search_condition=search)

    assert request.search_condition.title == "AI"

    params = request.model_dump(by_alias=True, exclude_none=True)
    assert "userCode" not in params


def test_patent_record_accepts_multiple_aliases():
    """PatentRecord should parse inventor/applicant aliases."""

    data = {
        "PN": "TW201644272A",
        "ID": "20170816",
        "TI": "無線充電裝置",
        "AB": "一種無線充電裝置...",
        "IN": "林意美",
        "PA": "測試公司",
    }

    record = PatentRecord(**data)
    assert record.patent_number == "TW201644272A"
    assert record.publication_date == "20170816"
    assert record.title == "無線充電裝置"
    assert record.inventor_name == "林意美"
    assert record.applicant_name == "測試公司"

    legacy_data = {
        "PN": "US10234567B2",
        "ID": "20200512",
        "TI": "Wireless Charging Device",
        "IV": "Inventor Name",
        "AX": "Legacy Applicant",
    }

    legacy_record = PatentRecord(**legacy_data)
    assert legacy_record.inventor_name == "Inventor Name"
    assert legacy_record.applicant_name == "Legacy Applicant"


def test_api_response():
    """GPSSAPIResponse aggregates PatentRecord items."""

    response_data = {
        "total_count": 2,
        "returned_count": 2,
        "records": [
            {"PN": "TW201644272A", "TI": "無線充電裝置"},
            {"PN": "US10234567B2", "TI": "Wireless Charging"},
        ],
    }

    response = GPSSAPIResponse(**response_data)
    assert response.total_count == 2
    assert len(response.records) == 2
    assert response.records[0].patent_number == "TW201644272A"


def test_date_range():
    """DateRange helper returns colon-formatted string."""

    dr = DateRange(start_date="20200101", end_date="20231231")
    assert dr.to_string() == "20200101:20231231"

    dr_start_only = DateRange(start_date="20200101")
    assert dr_start_only.to_string() == "20200101:"

    dr_end_only = DateRange(end_date="20231231")
    assert dr_end_only.to_string() == ":20231231"


def test_search_query():
    """SearchQuery joins keywords with the selected operator."""

    query_or = SearchQuery(keywords=["無線", "藍牙"], operator=SearchLogicOperator.OR)
    assert query_or.to_string() == "無線 OR 藍牙"

    query_and = SearchQuery(keywords=["充電", "快速"], operator=SearchLogicOperator.AND)
    assert query_and.to_string() == "充電 AND 快速"
