"""
GPSS Patent Search MCP Tools

This module provides MCP (Model Context Protocol) tools that allow AI agents
to interact with the GPSS (Global Patent Search System) API for patent search.
"""

from __future__ import annotations

from typing import Any, Literal
import os
import httpx
from fastapi import FastAPI
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError

from mcp_tools.schemas import (
    SearchCondition,
    SearchSettings,
    OutputSettings,
    GPSSAPIRequest,
    GPSSAPIResponse,
    PatDB,
    PatAG,
    PatTY,
    OutputFieldCode,
    OutputFormat,
)


class SearchPatentsRequest(BaseModel):
    """Body payload for the `search_patents` MCP tool.

    Note: The tool automatically reads the GPSS API user code from the
    USER_CODE environment variable. You do NOT need to provide it.
    """

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
        "json_schema_extra": {
            "description": (
                "Provide patent search criteria only. Authentication is handled "
                "internally by reading the USER_CODE environment variable; callers "
                "must not supply userCode in the request."
            ),
            "examples": [
                {
                    "keywords": "雲端 AND 轉型",
                    "search_field": "title_abstract_claims",
                    "publication_date_from": "20220101",
                    "max_results": 50,
                }
            ],
        },
    }

    keywords: str = Field(
        ..., description="Keyword expression understood by GPSS (e.g., '雲端 AND 轉型')"
    )
    search_field: Literal["title", "abstract", "claims", "title_abstract_claims"] = (
        Field("title", description="Which GPSS field group to search")
    )
    databases: list[str] | None = Field(
        default=None,
        description="Optional list of GPSS database codes (patDB)",
    )
    application_types: list[str] | None = Field(
        default=None,
        description="Optional list of GPSS application type codes (patAG)",
    )
    patent_types: list[str] | None = Field(
        default=None,
        description="Optional list of GPSS patent type codes (patTY)",
    )
    publication_date_from: str | None = Field(
        default=None,
        description="Lower bound for publication date (YYYYMMDD)",
    )
    publication_date_to: str | None = Field(
        default=None,
        description="Upper bound for publication date (YYYYMMDD)",
    )
    output_format: Literal["json", "xml"] = Field(
        "json", description="Desired GPSS export format"
    )
    max_results: int = Field(
        30,
        ge=1,
        le=500,
        description="Maximum number of results to request from GPSS",
    )


class SearchPatentsData(BaseModel):
    """Container for the GPSS raw payload and optional parsed response."""

    raw: Any = Field(description="Raw GPSS response (JSON dict or XML text)")
    parsed: GPSSAPIResponse | dict[str, Any] | None = Field(
        default=None,
        description="Parsed GPSS payload when JSON mode succeeds",
    )


class SearchPatentsResult(BaseModel):
    """Standard return model for MCP tool operations."""

    success: bool
    data: SearchPatentsData | None = None
    request_params: dict[str, Any] | None = None
    error: str | None = None


class SearchExample(BaseModel):
    """Example search configuration for quick reference."""

    description: str
    keywords: str
    search_field: str
    databases: list[str] | None = None
    publication_date_from: str | None = None
    publication_date_to: str | None = None


class SearchExamplesResponse(BaseModel):
    success: bool
    examples: dict[str, SearchExample]


class DatabasesResponse(BaseModel):
    success: bool
    databases: dict[str, dict[str, str]]


SearchPatentsRequest.model_rebuild()
SearchPatentsData.model_rebuild()
SearchPatentsResult.model_rebuild()
SearchExamplesResponse.model_rebuild()
DatabasesResponse.model_rebuild()


def _normalize_param_value(value: Any) -> Any:
    """Convert enums and lists into GPSS-compatible query parameter values."""

    if value is None:
        return None

    if hasattr(value, "value"):
        return value.value

    if isinstance(value, list):
        normalized_items = []
        for item in value:
            normalized_items.append(_normalize_param_value(item))
        return ",".join(str(item) for item in normalized_items if item is not None)

    return value


def _build_query_params(request: GPSSAPIRequest, user_code: str) -> dict[str, Any]:
    """Flatten the GPSS request models into query parameters."""

    params: dict[str, Any] = {"userCode": user_code}

    if request.search_condition:
        condition_payload = request.search_condition.model_dump(
            by_alias=True, exclude_none=True
        )
        for key, value in condition_payload.items():
            params[key] = _normalize_param_value(value)

    if request.search_settings:
        settings_payload = request.search_settings.model_dump(
            by_alias=True, exclude_none=True
        )
        for key, value in settings_payload.items():
            params[key] = _normalize_param_value(value)

    if request.output_settings:
        output_payload = request.output_settings.model_dump(
            by_alias=True, exclude_none=True
        )
        for key, value in output_payload.items():
            params[key] = _normalize_param_value(value)

    return params


app = FastAPI(
    title="GPSS Patent Search MCP",
    description="MCP tools for searching patents in the Global Patent Search System",
    version="1.0.0",
)

# GPSS API base URL
GPSS_API_URL = "https://tiponet.tipo.gov.tw/gpss1/gpsskmc/gpss_api"


async def search_patents(
    keywords: str,
    search_field: str = "title",
    databases: list[str] | None = None,
    application_types: list[str] | None = None,
    patent_types: list[str] | None = None,
    publication_date_from: str | None = None,
    publication_date_to: str | None = None,
    output_format: str = "json",
    max_results: int = 30,
) -> dict[str, Any]:
    """
    Search patents in the GPSS system.

    **Authentication**: The GPSS API user code is automatically read from the
    USER_CODE environment variable. You do NOT need to provide it as a parameter.

    Args:
        keywords: Search keywords (e.g., '雲端 AND 轉型', supports AND/OR/NOT operators)
        search_field: Which field to search in (title, abstract, claims, title_abstract_claims)
        databases: List of patent databases to search (default: all available)
        application_types: List of application type codes (A for published, B for granted)
        patent_types: List of patent type codes (I=invention, M=utility model, D=design)
        publication_date_from: Publication date from (YYYYMMDD format)
        publication_date_to: Publication date to (YYYYMMDD format)
        output_format: Output format (xml or json)
        max_results: Maximum number of results to return (1-500)

    Returns:
        Dictionary containing search results or error information
    """
    try:
        # Read GPSS API user code from environment
        user_code = os.environ.get("USER_CODE")
        if not user_code:
            return {
                "success": False,
                "error": "GPSS API authentication error: USER_CODE environment variable not set or empty. "
                "Please ensure USER_CODE is configured in your environment before using this tool. "
                "When using Docker, pass: -e USER_CODE=your_api_code",
            }
        # Build search condition based on field
        search_data = {}

        if search_field == "title":
            search_data["TI"] = keywords
        elif search_field == "abstract":
            search_data["AB"] = keywords
        elif search_field == "claims":
            search_data["CL"] = keywords
        elif search_field == "title_abstract_claims":
            search_data["TI/AB/CL"] = keywords
        else:
            return {
                "success": False,
                "error": f"Invalid search_field: {search_field}. "
                "Use: title, abstract, claims, or title_abstract_claims",
            }

        # Add date range if provided
        if publication_date_from or publication_date_to:
            if publication_date_from and publication_date_to:
                search_data["ID"] = f"{publication_date_from}:{publication_date_to}"
            elif publication_date_from:
                search_data["ID"] = f"{publication_date_from}:"
            else:
                search_data["ID"] = f":{publication_date_to}"

        search_condition = SearchCondition(**search_data)

        # Build search settings
        settings_data = {}
        if databases:
            try:
                settings_data["patDB"] = [PatDB(db) for db in databases]
            except ValueError as e:
                return {"success": False, "error": f"Invalid database: {e}"}

        if application_types:
            try:
                settings_data["patAG"] = [PatAG(code) for code in application_types]
            except ValueError as e:
                return {"success": False, "error": f"Invalid application type: {e}"}

        if patent_types:
            try:
                settings_data["patTY"] = [PatTY(code) for code in patent_types]
            except ValueError as e:
                return {"success": False, "error": f"Invalid patent type: {e}"}

        search_settings = SearchSettings.model_validate(settings_data or {})

        # Build output settings
        output_settings = OutputSettings(
            expFmt=OutputFormat.JSON if output_format == "json" else OutputFormat.XML,
            expQty=max_results,
            expSkip=0,
            expFld=[
                OutputFieldCode.PN,
                OutputFieldCode.ID,
                OutputFieldCode.TI,
                OutputFieldCode.AB,
                OutputFieldCode.IN,
            ],
        )

        # Create API request
        request = GPSSAPIRequest(
            search_condition=search_condition,
            search_settings=search_settings,
            output_settings=output_settings,
        )

        # Convert to URL parameters
        params = _build_query_params(request, user_code)
        # Do not leak authentication info back to callers.
        safe_params = {key: value for key, value in params.items() if key != "userCode"}

        # Make API call
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(GPSS_API_URL, params=params)

            # Check for HTTP errors
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"GPSS API returned status code {response.status_code}: {response.text[:500]}",
                }

            # Check if response is empty
            if not response.text:
                return {
                    "success": False,
                    "error": "GPSS API returned an empty response. The USER_CODE may be invalid or the API may be temporarily unavailable.",
                }

            # Parse response - detect format automatically
            parsed_response: GPSSAPIResponse | None = None
            result = None
            is_xml = response.text.strip().startswith("<")

            try:
                if is_xml:
                    # GPSS API often returns XML regardless of requested format
                    result = response.text
                    # XML parsing is stored as text, no JSON validation needed
                else:
                    # Try to parse as JSON
                    try:
                        result = response.json()
                        if isinstance(result, dict):
                            try:
                                parsed_response = GPSSAPIResponse.model_validate(result)
                            except ValidationError:
                                parsed_response = None
                    except ValueError as e:
                        return {
                            "success": False,
                            "error": f"Failed to parse GPSS API response as JSON: {str(e)}. Raw response: {response.text[:500]}",
                        }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Unexpected error parsing GPSS API response: {str(e)}",
                }

            payload: dict[str, Any] = {"raw": result}
            if parsed_response is not None:
                payload["parsed"] = parsed_response.model_dump(by_alias=True)

            return {
                "success": True,
                "data": payload,
                "request_params": safe_params,
            }

    except httpx.HTTPError as e:
        return {
            "success": False,
            "error": f"API request failed: {str(e)}",
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Invalid parameters: {str(e)}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
        }


async def get_available_databases() -> dict[str, Any]:
    """
    Get list of available patent databases.

    Returns:
        Dictionary with available databases and their descriptions
    """
    databases = {
        "TW": {
            "TWA": "Taiwan Patent - Published/Disclosed",
            "TWB": "Taiwan Patent - Granted",
            "TWD": "Taiwan Design",
        },
        "US": {
            "USA": "United States Patent - Published/Disclosed",
            "USB": "United States Patent - Granted",
            "USD": "United States Design",
        },
        "JP": {
            "JPA": "Japan Patent - Published/Disclosed",
            "JPB": "Japan Patent - Granted",
            "JPD": "Japan Design",
        },
        "EP": {
            "EPA": "European Patent - Published/Disclosed",
            "EPB": "European Patent - Granted",
            "EUIPO": "EU Design",
        },
        "KR": {
            "KPA": "Korea Patent - Published/Disclosed",
            "KPB": "Korea Patent - Granted",
            "KPD": "Korea Design",
        },
        "CN": {
            "CNA": "China Patent - Published/Disclosed",
            "CNB": "China Patent - Granted",
            "CND": "China Design",
        },
        "International": {
            "WO": "WIPO Published",
            "SEAA": "Southeast Asia - Published (No Full Text)",
            "SEAB": "Southeast Asia - Granted (No Full Text)",
            "OTA": "Other Countries - Published (No Full Text)",
            "OTB": "Other Countries - Granted (No Full Text)",
        },
    }
    return {"success": True, "databases": databases}


async def get_search_examples() -> dict[str, Any]:
    """
    Get example search queries for different use cases.

    Returns:
        Dictionary with search examples
    """
    examples = {
        "basic_title_search": {
            "description": "Search for patents with keyword in title",
            "keywords": "wireless charging",
            "search_field": "title",
            "databases": ["TWA", "USA", "EPA"],
        },
        "advanced_technical_search": {
            "description": "Search across title, abstract, and claims",
            "keywords": "lithium battery AND fast charging",
            "search_field": "title_abstract_claims",
            "databases": ["TWA", "USA", "EPA", "CNA"],
            "publication_date_from": "20200101",
            "publication_date_to": "20231231",
        },
        "inventor_by_abstract": {
            "description": "Search in abstract field for specific technology",
            "keywords": "neural network AND image processing",
            "search_field": "abstract",
            "databases": ["USA", "EPA"],
        },
        "recent_patents": {
            "description": "Find recently published patents",
            "keywords": "quantum computing",
            "search_field": "title_abstract_claims",
            "publication_date_from": "20230101",
        },
    }
    return {"success": True, "examples": examples}


# Register MCP tools
@app.post("/tools/search_patents", response_model=SearchPatentsResult)
async def tool_search_patents(payload: SearchPatentsRequest) -> SearchPatentsResult:
    """MCP Tool endpoint for patent search.

    This tool searches the GPSS (Global Patent Search System) for patents matching
    your keywords. Authentication is handled automatically via the USER_CODE
    environment variable—you don't need to provide credentials in your request.

    Simply provide your search keywords and optional filters. The tool will:
    1. Automatically read USER_CODE from the environment
    2. Send the request to GPSS API
    3. Return parsed results with patent numbers, titles, abstracts, and inventor info
    """

    result = await search_patents(**payload.model_dump())
    return SearchPatentsResult.model_validate(result)


@app.post("/tools/get_available_databases", response_model=DatabasesResponse)
async def tool_get_databases() -> DatabasesResponse:
    """MCP Tool endpoint for getting available databases."""

    result = await get_available_databases()
    return DatabasesResponse.model_validate(result)


@app.post("/tools/get_search_examples", response_model=SearchExamplesResponse)
async def tool_get_examples() -> SearchExamplesResponse:
    """MCP Tool endpoint for getting search examples."""

    result = await get_search_examples()
    return SearchExamplesResponse.model_validate(result)


# Initialize FastMCP
mcp = FastMCP.from_fastapi(app=app)

if __name__ == "__main__":
    mcp.run()
    # import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
