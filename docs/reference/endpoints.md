# API Endpoints
Version: 1.0.0
MCP tools for searching patents in the Global Patent Search System

## /tools/search_patents

### POST

**Summary:** Tool Search Patents

**Description:** MCP Tool endpoint for patent search.

This tool searches the GPSS (Global Patent Search System) for patents matching
your keywords. Authentication is handled automatically via the USER_CODE
environment variable.

Simply provide your search keywords and optional filters. The tool will:

1. Automatically read USER_CODE from the environment

2. Send the request to GPSS API

3. Return parsed results with patent numbers, titles, abstracts, and inventor info

**Request Body:**

Content-Type: `application/json`

Schema:
```json
{
  "keywords": string (required)  // Keyword expression understood by GPSS (e.g., '雲端 AND 轉型')
  "search_field": unknown,  // Which GPSS field group(s) to search. Provide a single value or a list to reuse the same keywords across multiple fields (additional fields are combined with OR per GPSS API rules). Supported values include single fields such as: title, abstract, claims, patent_number, publication_date, application_number, application_date, applicant_name, first_applicant_name, applicant_country, first_applicant_country, inventor_name, inventor_country, agent_name, examiner, priority, priority_date, ipc, first_ipc, cpc, first_cpc, loc, fi, f_term, d_term, uspc, and cited_patents.
  "databases": unknown,  // Optional list of GPSS database codes (patDB)
  "application_types": unknown,  // Optional list of GPSS application type codes (patAG)
  "patent_types": unknown,  // Optional list of GPSS patent type codes (patTY)
  "publication_date_from": unknown,  // Lower bound for publication date (YYYYMMDD)
  "publication_date_to": unknown,  // Upper bound for publication date (YYYYMMDD)
  "max_results": integer,  // Maximum number of results to request from GPSS
}
```

**Responses:**

**200**: Successful Response

Content-Type: `application/json`

Schema:
```json
{
  "success": boolean (required)  // 
  "data": unknown,  // 
  "request_params": unknown,  // 
  "error": unknown,  // 
}
```

**422**: Validation Error

Content-Type: `application/json`

Schema:
```json
{
  "detail": [ValidationError]  // 
}
```

---

## /tools/get_available_databases

### POST

**Summary:** Tool Get Databases

**Description:** MCP Tool endpoint for getting available databases.

**Responses:**

**200**: Successful Response

Content-Type: `application/json`

Schema:
```json
{
  "success": boolean (required)  // 
  "databases": object (required),  // Mapping of region -> database code -> description. Each database entry is a human-friendly description derived from the `PatDB` enum.
}
```

---

## /tools/get_search_examples

### POST

**Summary:** Tool Get Examples

**Description:** MCP Tool endpoint for getting search examples.

**Responses:**

**200**: Successful Response

Content-Type: `application/json`

Schema:
```json
{
  "success": boolean (required)  // 
  "examples": object (required),  // 
}
```

---
