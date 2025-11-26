# Data Models

This page contains all the data models used in the API.

## DatabasesResponse

**Schema:**
```json
{
  "success": boolean (required)  // 
  "databases": object (required),  // 
}
```

**Properties:**

- **success** *(required)*: `boolean`

- **databases** *(required)*: `object`

---

## GPSSAPIResponse

**Description:** GPSS API response wrapper.

**Schema:**
```json
{
  "total_count": unknown  // Total number of matching records
  "returned_count": unknown,  // Number of records in this response
  "records": unknown,  // List of patent records
}
```

**Properties:**

- **total_count**: `unknown`
  - Description: Total number of matching records

- **returned_count**: `unknown`
  - Description: Number of records in this response

- **records**: `unknown`
  - Description: List of patent records

---

## HTTPValidationError

**Schema:**
```json
{
  "detail": [ValidationError]  // 
}
```

**Properties:**

- **detail**: `[ValidationError]`

---

## PatentRecord

**Description:** Single patent record from API response.

**Schema:**
```json
{
  "PN": unknown  // Publication/announcement number (公開/公告號)
  "ID": unknown,  // Publication/announcement date (公開/公告日)
  "AN": unknown,  // Application number (申請號)
  "AD": unknown,  // Application date (申請日)
  "PA": unknown,  // Applicant name (申請人名)
  "AF": unknown,  // First applicant name (第一申請人名)
  "AY": unknown,  // Applicant country (申請人國別)
  "AZ": unknown,  // First applicant country (第一申請人國別)
  "IN": unknown,  // Inventor name (發明人名)
  "IY": unknown,  // Inventor country (發明人國別)
  "LX": unknown,  // Agent / attorney name (代理人名)
  "EX": unknown,  // Examiner (審查委員)
  "PR": unknown,  // Priority claim (優先權)
  "DR": unknown,  // Priority date (優先權日)
  "IC": unknown,  // IPC classification (IPC)
  "FC": unknown,  // First IPC (第一 IPC)
  "CS": unknown,  // CPC classification (CPC)
  "TS": unknown,  // First CPC (第一 CPC)
  "IQ": unknown,  // LOC classification (LOC)
  "FI": unknown,  // FI classification (FI)
  "FT": unknown,  // F-TERM (F-TERM)
  "IR": unknown,  // D-TERM (D-TERM)
  "UC": unknown,  // USPC classification (USPC)
  "TI": unknown,  // Patent title (專利名稱)
  "AB": unknown,  // Abstract (摘要)
  "CL": unknown,  // Claims / patent scope (專利範圍)
  "CI": unknown,  // Cited patents / references (引用專利)
}
```

**Properties:**

- **PN**: `unknown`
  - Description: Publication/announcement number (公開/公告號)

- **ID**: `unknown`
  - Description: Publication/announcement date (公開/公告日)

- **AN**: `unknown`
  - Description: Application number (申請號)

- **AD**: `unknown`
  - Description: Application date (申請日)

- **PA**: `unknown`
  - Description: Applicant name (申請人名)

- **AF**: `unknown`
  - Description: First applicant name (第一申請人名)

- **AY**: `unknown`
  - Description: Applicant country (申請人國別)

- **AZ**: `unknown`
  - Description: First applicant country (第一申請人國別)

- **IN**: `unknown`
  - Description: Inventor name (發明人名)

- **IY**: `unknown`
  - Description: Inventor country (發明人國別)

- **LX**: `unknown`
  - Description: Agent / attorney name (代理人名)

- **EX**: `unknown`
  - Description: Examiner (審查委員)

- **PR**: `unknown`
  - Description: Priority claim (優先權)

- **DR**: `unknown`
  - Description: Priority date (優先權日)

- **IC**: `unknown`
  - Description: IPC classification (IPC)

- **FC**: `unknown`
  - Description: First IPC (第一 IPC)

- **CS**: `unknown`
  - Description: CPC classification (CPC)

- **TS**: `unknown`
  - Description: First CPC (第一 CPC)

- **IQ**: `unknown`
  - Description: LOC classification (LOC)

- **FI**: `unknown`
  - Description: FI classification (FI)

- **FT**: `unknown`
  - Description: F-TERM (F-TERM)

- **IR**: `unknown`
  - Description: D-TERM (D-TERM)

- **UC**: `unknown`
  - Description: USPC classification (USPC)

- **TI**: `unknown`
  - Description: Patent title (專利名稱)

- **AB**: `unknown`
  - Description: Abstract (摘要)

- **CL**: `unknown`
  - Description: Claims / patent scope (專利範圍)

- **CI**: `unknown`
  - Description: Cited patents / references (引用專利)

---

## SearchExample

**Description:** Example search configuration for quick reference.

**Schema:**
```json
{
  "description": string (required)  // 
  "keywords": string (required),  // 
  "search_field": unknown (required),  // 
  "databases": unknown,  // 
  "publication_date_from": unknown,  // 
  "publication_date_to": unknown,  // 
}
```

**Properties:**

- **description** *(required)*: `string`

- **keywords** *(required)*: `string`

- **search_field** *(required)*: `unknown`

- **databases**: `unknown`

- **publication_date_from**: `unknown`

- **publication_date_to**: `unknown`

---

## SearchExamplesResponse

**Schema:**
```json
{
  "success": boolean (required)  // 
  "examples": object (required),  // 
}
```

**Properties:**

- **success** *(required)*: `boolean`

- **examples** *(required)*: `object`

---

## SearchPatentsData

**Description:** Container for the GPSS raw payload and optional parsed response.

Note: `parsed` is typed as `GPSSAPIResponse | None` so OpenAPI can fully
document the nested `PatentRecord` fields and their descriptions. When the
MCP receives JSON from GPSS we attempt to validate into `GPSSAPIResponse`.

**Schema:**
```json
{
  "raw": unknown (required)  // Raw GPSS response (JSON dict or XML text)
  "parsed": unknown,  // Parsed GPSS payload when JSON mode succeeds
}
```

**Properties:**

- **raw** *(required)*: `unknown`
  - Description: Raw GPSS response (JSON dict or XML text)

- **parsed**: `unknown`
  - Description: Parsed GPSS payload when JSON mode succeeds

---

## SearchPatentsRequest

**Description:** Provide patent search criteria only. Authentication is handled internally by reading the USER_CODE environment variable; callers must not supply userCode in the request.

**Schema:**
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

**Properties:**

- **keywords** *(required)*: `string`
  - Description: Keyword expression understood by GPSS (e.g., '雲端 AND 轉型')

- **search_field**: `unknown`
  - Description: Which GPSS field group(s) to search. Provide a single value or a list to reuse the same keywords across multiple fields (additional fields are combined with OR per GPSS API rules). Supported values include single fields such as: title, abstract, claims, patent_number, publication_date, application_number, application_date, applicant_name, first_applicant_name, applicant_country, first_applicant_country, inventor_name, inventor_country, agent_name, examiner, priority, priority_date, ipc, first_ipc, cpc, first_cpc, loc, fi, f_term, d_term, uspc, and cited_patents.

- **databases**: `unknown`
  - Description: Optional list of GPSS database codes (patDB)

- **application_types**: `unknown`
  - Description: Optional list of GPSS application type codes (patAG)

- **patent_types**: `unknown`
  - Description: Optional list of GPSS patent type codes (patTY)

- **publication_date_from**: `unknown`
  - Description: Lower bound for publication date (YYYYMMDD)

- **publication_date_to**: `unknown`
  - Description: Upper bound for publication date (YYYYMMDD)

- **max_results**: `integer`
  - Description: Maximum number of results to request from GPSS

---

## SearchPatentsResult

**Description:** Standard return model for MCP tool operations.

**Schema:**
```json
{
  "success": boolean (required)  // 
  "data": unknown,  // 
  "request_params": unknown,  // 
  "error": unknown,  // 
}
```

**Properties:**

- **success** *(required)*: `boolean`

- **data**: `unknown`

- **request_params**: `unknown`

- **error**: `unknown`

---

## ValidationError

**Schema:**
```json
{
  "loc": [unknown] (required)  // 
  "msg": string (required),  // 
  "type": string (required),  // 
}
```

**Properties:**

- **loc** *(required)*: `[unknown]`

- **msg** *(required)*: `string`

- **type** *(required)*: `string`

---
