<div align="center">

  <h1>GPSS Patent Search MCP</h1>

</div>

> AI-ready MCP (Model Context Protocol) server for searching patents in the Global Patent Search System (GPSS) with automatic authentication handling

## 🚀 Core Features

- **Zero-Config Authentication**: Automatically reads `USER_CODE` from environment variables—no need to pass credentials in requests
- **Flexible Search**: Query patents by keywords, date range, databases, patent types, and combine results across multiple GPSS fields in one request
- **XML Response Format**: GPSS API returns XML format which is parsed and returned as raw text
- **Comprehensive Schema**: Full support for GPSS API parameters and response models
- **Docker & Local Development**: Run locally with `uv` or containerized with Docker
- **Documentation-as-Code**: Auto-generated OpenAPI docs and MkDocs documentation

## 🛠️ Setup & Usage

### Prerequisites

- Python 3.11+
- Docker (optional)
- GPSS API credentials (get from [GPSS API](https://tiponet.tipo.gov.tw/gpss1/gpsskmc/gpssapi?@@0.033993675766816334))

### Local Development

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Set your GPSS credentials**:
   ```bash
   echo "USER_CODE=your_api_code_here" >> .env
   ```

3. **Run the MCP server locally**:
   ```bash
   # Using stdio (for MCP clients)
   uv run fastmcp run mcp_tools/main.py
   
   # Or using HTTP transport
   uv run fastmcp run mcp_tools/main.py --transport http
   ```

4. **Test with a quick search**:
   ```bash
   uv run --env-file=.env scripts/example.py
   ```
   ```python
   # scripts/example.py
   import asyncio
   import os
   from mcp_tools.main import search_patents

   async def main():
       # USER_CODE is read automatically from environment
       result = await search_patents(
           keywords="雲端",
            search_field=["title", "abstract", "claims"],
           max_results=10,
       )
       
       if result["success"]:
           print("✅ Search successful!")
           print(f"Request params: {result.get('request_params', {}).keys()}")
           data = result.get("data", {})
           print(f"Response format: {'XML' if isinstance(data.get('raw'), str) and data.get('raw').strip().startswith('<') else 'JSON'}")
       else:
           print(f"❌ Error: {result.get('error')}")

   asyncio.run(main())
   ```

5. **Run tests**:
   ```bash
   uv run pytest
   ```

### Docker

1. **Build the Docker image**:
   ```bash
   ./scripts/build_image.sh
   ```

2. **Run the container with your credentials**:
   ```bash
   docker run -i --rm \
     -e USER_CODE=your_api_code_here \
     hsiangjenli/mcp-tw-gpss:latest
   ```

3. **Use with VS Code MCP Client** (add to `.vscode/settings.json` or MCP config):
   ```json
   {
     "servers": {
       "tw-gpss": {
         "type": "stdio",
         "command": "docker",
         "args": [
           "run",
           "-i",
           "-e",
           "USER_CODE=your_api_code_here",
           "--rm",
           "hsiangjenli/mcp-tw-gpss:latest"
         ]
       }
     }
   }
   ```

## 📋 Available Tools

The MCP server exposes three main tools:

### 1. **`search_patents`**
Search for patents in GPSS with flexible filtering.

**Request Parameters:**
- `keywords` *(required)*: Search query (e.g., `"雲端 OR 轉型"`, supports AND/OR/NOT)
- `search_field`: Where to search. Provide a single field or a list (combined with OR) from `title`, `abstract`, `claims`, `title_abstract`, `title_abstract_claims`, `patent_number`, `publication_date`, `application_number`, `application_date`, `applicant_name`, `first_applicant_name`, `applicant_country`, `first_applicant_country`, `inventor_name`, `inventor_country`, `agent_name`, `examiner`, `priority`, `priority_date`, `ipc`, `first_ipc`, `cpc`, `first_cpc`, `loc`, `fi`, `f_term`, `d_term`, `uspc`, `cited_patents` (default: `"title"`)
- `databases`: List of database codes (e.g., `["TWA", "USA", "EPA"]`, default: all)
- `patent_types`: Filter by type - `"I"` (invention), `"M"` (utility model), `"D"` (design)
- `application_types`: Filter by status - `"A"` (published), `"B"` (granted)
- `publication_date_from` / `publication_date_to`: Date range in YYYYMMDD format
- `max_results`: Number of results (1-500, default: 30)

**Response:**
- `success`: Boolean indicating if the search succeeded
- `data.raw`: Raw GPSS API response (XML text)
- `data.parsed`: Parsed patent records (when available)
- `request_params`: Query parameters sent to GPSS (without `userCode`)
- `error`: Error message if unsuccessful

**Example:**
```json
{
  "keywords": "雲端 OR 轉型",
   "search_field": ["title", "abstract", "claims"],
  "databases": ["TWA", "USA"],
  "publication_date_from": "20200101",
  "max_results": 50
}
```

### 2. **`get_available_databases`**
List all available patent databases and their descriptions.

**Response:**
Dictionary of regions and their database codes (e.g., TW, US, JP, EP, KR, CN, WO, etc.)

### 3. **`get_search_examples`**
Get example search configurations for common use cases.

**Response:**
Pre-built search examples you can use as templates.

## 🔐 Authentication & Security

**Key Point**: The `USER_CODE` is **NOT** part of the request schema visible to AI Agents.

- ✅ **Automatic**: `USER_CODE` is read from the `USER_CODE` environment variable
- ✅ **Secure**: Never exposed in MCP tool definitions or response data
- ✅ **Agent-Friendly**: AI agents don't see or ask for credentials

**Setup:**
- **Local**: Add to `.env`: `USER_CODE=your_code`
- **Docker**: Pass as environment variable: `-e USER_CODE=your_code`
- **VS Code**: Include in MCP config args as shown above

## 🧪 Development

## 🧪 Development

### Project Structure

```
mcp_tools/
├── main.py          # FastAPI/FastMCP server, tool endpoints, search logic
├── schemas.py       # Pydantic models, enums (PatDB, PatAG, etc.)
└── __init__.py

tests/
├── test_mcp_integration.py  # Live API integration tests
└── test_schemas.py          # Schema validation tests

docs/                # MkDocs documentation
scripts/
├── build_image.sh   # Docker image builder
└── build_docs.sh    # Documentation generator
```

### Key Implementation Details

1. **XML Format**: The GPSS API always returns XML format regardless of the requested format. The response is returned as raw XML text in `data.raw`.

2. **Credential Separation**: `USER_CODE` is:
   - Read from environment in the `search_patents` function
   - **NOT** included in the `SearchPatentsRequest` Pydantic model (with `extra="forbid"`)
   - Injected only when building the actual API call
   - Stripped from `safe_params` before returning to the caller

3. **Robust Error Handling**:
   - Checks HTTP status codes
   - Validates empty responses
   - Graceful JSON/XML parsing fallbacks
   - Meaningful error messages for debugging

### Running Tests

```bash
# Run all tests
uv run pytest

# Run only integration tests
uv run pytest tests/test_mcp_integration.py

# Run with coverage
uv run pytest --cov=mcp_tools
```

### Build Documentation

```bash
chmod +x scripts/build_docs.sh
./scripts/build_docs.sh
mkdocs serve  # View locally at http://127.0.0.1:8000
```

## 📖 Reference

- **GPSS API Documentation**: [TIPO GPSS API Guide](https://tiponet.tipo.gov.tw/gpss1/gpsskm/API/API_instructions.pdf)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **FastAPI**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Pydantic**: [docs.pydantic.dev](https://docs.pydantic.dev)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

See LICENSE file for details.
