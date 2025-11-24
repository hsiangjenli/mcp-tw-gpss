import asyncio
import xml.dom.minidom
from mcp_tools.main import search_patents


async def main():
    # USER_CODE is read automatically from environment
    result = await search_patents(
        keywords="雲端",
        search_field="title_abstract_claims",
        max_results=10,
    )

    if result["success"]:
        print("✅ Search successful!")
        print(f"Request params: {result.get('request_params', {}).keys()}")
        temp = xml.dom.minidom.parseString(result["data"]["raw"])
        pretty_xml = temp.toprettyxml(indent="  ", newl="")
        print(pretty_xml)

    else:
        print(f"❌ Error: {result.get('error')}")


asyncio.run(main())
