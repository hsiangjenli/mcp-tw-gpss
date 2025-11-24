"""
GPSS API Schema Definitions using Pydantic and Enum
Based on GPSS API Service Documentation v1.4
"""

from enum import Enum
from typing import List, Optional, Literal
from pydantic import AliasChoices, BaseModel, Field


# ==================== Enumerations ====================


class PatDB(str, Enum):
    """Patent databases."""

    TWA = "TWA"  # 台灣公開
    TWB = "TWB"  # 台灣公告
    TWD = "TWD"  # 台灣設計
    USA = "USA"  # 美國公開
    USB = "USB"  # 美國公告
    USD = "USD"  # 美國設計
    JPA = "JPA"  # 日本公開
    JPB = "JPB"  # 日本公告
    JPD = "JPD"  # 日本意匠
    EPA = "EPA"  # 歐洲公開
    EPB = "EPB"  # 歐洲公告
    EUIPO = "EUIPO"  # 歐盟外觀設計
    KPA = "KPA"  # 韓國公開
    KPB = "KPB"  # 韓國公告
    KPD = "KPD"  # 韓國設計
    CNA = "CNA"  # 中國公開
    CNB = "CNB"  # 中國公告
    CND = "CND"  # 中國設計
    WO = "WO"  # WIPO 公開
    SEAA = "SEAA"  # 東南亞公開(無全文)
    SEAB = "SEAB"  # 東南亞公告(無全文)
    OTA = "OTA"  # 其他國家公開(無全文)
    OTB = "OTB"  # 其他國家公告(無全文)


class PatAG(str, Enum):
    """Patent application type (patent aggregation)."""

    A = "A"  # 公開案
    B = "B"  # 公告案


class PatTY(str, Enum):
    """Patent document type."""

    I = "I"  # 發明
    M = "M"  # 新型
    D = "D"  # 設計


class OutputFormat(str, Enum):
    """Output format for API response."""

    XML = "xml"
    JSON = "json"


class SearchLogicOperator(str, Enum):
    """Logic operators for combining search fields."""

    AND = "AND"
    OR = "OR"
    NOT = "NOT"


# ==================== Output Fields ====================


class OutputFieldCode(str, Enum):
    """Available output field codes."""

    PN = "PN"  # 公開/公告號
    ID = "ID"  # 公開/公告日
    AN = "AN"  # 申請號
    AD = "AD"  # 申請日
    PA = "PA"  # 申請人名 (輸出欄位代碼)
    AX = "AX"  # 申請人名 (部分文件使用)
    AF = "AF"  # 第一申請人名
    AY = "AY"  # 申請人國別
    AZ = "AZ"  # 第一申請人國別
    IN = "IN"  # 發明人名 (輸出欄位代碼)
    IV = "IV"  # 發明人名 (部分文件使用)
    IY = "IY"  # 發明人國別
    LX = "LX"  # 代理人名
    EX = "EX"  # 審查委員
    PR = "PR"  # 優先權
    DR = "DR"  # 優先權日
    IC = "IC"  # IPC
    FC = "FC"  # 第一 IPC
    CS = "CS"  # CPC
    TS = "TS"  # 第一 CPC
    IQ = "IQ"  # LOC
    FI = "FI"  # FI
    FT = "FT"  # F-TERM
    IR = "IR"  # D-TERM
    UC = "UC"  # USPC
    TI = "TI"  # 專利名稱
    AB = "AB"  # 摘要
    CL = "CL"  # 專利範圍
    CI = "CI"  # 引用專利


# ==================== API Request Models ====================


class SearchCondition(BaseModel):
    """Search condition parameters for GPSS API."""

    model_config = {"populate_by_name": True, "extra": "ignore"}

    # Patent document identifiers
    patent_number: Optional[str] = Field(
        None, alias="PN", description="公開/公告號 (e.g., TW201644272A)"
    )
    publication_date: Optional[str] = Field(
        None, alias="ID", description="公開/公告日 (e.g., 2020:2021)"
    )
    application_number: Optional[str] = Field(
        None, alias="AN", description="申請號 (e.g., TW105131793)"
    )
    application_date: Optional[str] = Field(
        None, alias="AD", description="申請日 (e.g., 20191107:)"
    )

    # Applicant information
    applicant_name: Optional[str] = Field(
        None, alias="AX", description="申請人名 (e.g., 林大成 AND 陳曉明)"
    )
    first_applicant_name: Optional[str] = Field(
        None, alias="AF", description="第一申請人名"
    )
    applicant_country: Optional[str] = Field(
        None, alias="AY", description="申請人國別 (e.g., US OR TW)"
    )
    first_applicant_country: Optional[str] = Field(
        None, alias="AZ", description="第一申請人國別 (e.g., US OR 美國)"
    )

    # Inventor information
    inventor_name: Optional[str] = Field(None, alias="IV", description="發明人名")
    inventor_country: Optional[str] = Field(None, alias="IY", description="發明人國別")

    # Other information
    agent_name: Optional[str] = Field(None, alias="LX", description="代理人名")
    examiner: Optional[str] = Field(None, alias="EX", description="審查委員")
    priority: Optional[str] = Field(
        None, alias="PR", description="優先權 (e.g., US201514879928)"
    )
    priority_date: Optional[str] = Field(
        None, alias="DR", description="優先權日 (e.g., 202001:202012)"
    )

    # Classification
    ipc: Optional[str] = Field(
        None, alias="IC", description="IPC (e.g., G01S 5/02 AND G01S 1/00)"
    )
    first_ipc: Optional[str] = Field(None, alias="FC", description="第一 IPC")
    cpc: Optional[str] = Field(None, alias="CS", description="CPC")
    first_cpc: Optional[str] = Field(None, alias="TS", description="第一 CPC")
    loc: Optional[str] = Field(None, alias="IQ", description="LOC")
    fi: Optional[str] = Field(None, alias="FI", description="FI")
    f_term: Optional[str] = Field(None, alias="FT", description="F-TERM")
    d_term: Optional[str] = Field(None, alias="IR", description="D-TERM")
    uspc: Optional[str] = Field(None, alias="UC", description="USPC")

    # Patent content
    title: Optional[str] = Field(
        None, alias="TI", description="專利名稱 (e.g., 無線裝置 OR 通訊裝置)"
    )
    abstract: Optional[str] = Field(None, alias="AB", description="摘要")
    claims: Optional[str] = Field(None, alias="CL", description="專利範圍")
    cited_patents: Optional[str] = Field(None, alias="CI", description="引用專利")

    # Combined fields
    title_abstract: Optional[str] = Field(
        None, alias="TI/AB", description="專利名稱/摘要"
    )
    title_abstract_claims: Optional[str] = Field(
        None, alias="TI/AB/CL", description="專利名稱/摘要/專利範圍"
    )


class SearchSettings(BaseModel):
    """Search settings (filtering parameters)."""

    model_config = {"populate_by_name": True, "extra": "ignore"}

    databases: Optional[List[PatDB]] = Field(
        None, alias="patDB", description="資料庫 (default: all databases)"
    )
    application_type: Optional[List[PatAG]] = Field(
        None, alias="patAG", description="案件類型 (default: A,B)"
    )
    patent_type: Optional[List[PatTY]] = Field(
        None, alias="patTY", description="專利類型 (default: I,M,D)"
    )


class OutputSettings(BaseModel):
    """Output settings for API response."""

    model_config = {"populate_by_name": True, "extra": "ignore"}

    fields: Optional[List[OutputFieldCode]] = Field(
        None, alias="expFld", description="輸出欄位 (default: PN,ID,AN,AD,TI)"
    )
    format: OutputFormat = Field(
        OutputFormat.XML, alias="expFmt", description="輸出格式"
    )
    quantity: int = Field(30, alias="expQty", description="輸出筆數 (default: 30)")
    skip: int = Field(0, alias="expSkip", description="跳躍筆數 (default: 0)")


class GPSSAPIRequest(BaseModel):
    """Complete GPSS API request model (excluding authentication)."""

    model_config = {"populate_by_name": True, "extra": "ignore"}

    search_settings: Optional[SearchSettings] = Field(
        default=None, description="搜尋設定"
    )
    search_condition: Optional[SearchCondition] = Field(
        default=None, description="搜尋條件 (必填)"
    )
    output_settings: Optional[OutputSettings] = Field(
        default=None, description="輸出設定"
    )


# ==================== API Response Models ====================


class PatentRecord(BaseModel):
    """Single patent record from API response."""

    model_config = {"populate_by_name": True, "extra": "ignore"}

    patent_number: Optional[str] = Field(None, alias="PN")
    publication_date: Optional[str] = Field(None, alias="ID")
    application_number: Optional[str] = Field(None, alias="AN")
    application_date: Optional[str] = Field(None, alias="AD")
    applicant_name: Optional[str] = Field(
        None,
        alias="PA",
        validation_alias=AliasChoices("PA", "AX"),
    )
    first_applicant: Optional[str] = Field(None, alias="AF")
    applicant_country: Optional[str] = Field(None, alias="AY")
    first_applicant_country: Optional[str] = Field(None, alias="AZ")
    inventor_name: Optional[str] = Field(
        None,
        alias="IN",
        validation_alias=AliasChoices("IN", "IV"),
    )
    inventor_country: Optional[str] = Field(None, alias="IY")
    agent_name: Optional[str] = Field(None, alias="LX")
    examiner: Optional[str] = Field(None, alias="EX")
    priority: Optional[str] = Field(None, alias="PR")
    priority_date: Optional[str] = Field(None, alias="DR")
    ipc: Optional[str] = Field(None, alias="IC")
    first_ipc: Optional[str] = Field(None, alias="FC")
    cpc: Optional[str] = Field(None, alias="CS")
    first_cpc: Optional[str] = Field(None, alias="TS")
    loc: Optional[str] = Field(None, alias="IQ")
    fi: Optional[str] = Field(None, alias="FI")
    f_term: Optional[str] = Field(None, alias="FT")
    d_term: Optional[str] = Field(None, alias="IR")
    uspc: Optional[str] = Field(None, alias="UC")
    title: Optional[str] = Field(None, alias="TI")
    abstract: Optional[str] = Field(None, alias="AB")
    claims: Optional[str] = Field(None, alias="CL")
    cited_patents: Optional[str] = Field(None, alias="CI")


class GPSSAPIResponse(BaseModel):
    """GPSS API response wrapper."""

    model_config = {"populate_by_name": True, "extra": "ignore"}

    total_count: Optional[int] = Field(
        None, description="Total number of matching records"
    )
    returned_count: Optional[int] = Field(
        None, description="Number of records in this response"
    )
    records: Optional[List[PatentRecord]] = Field(
        None, description="List of patent records"
    )


class APIError(BaseModel):
    """API error response."""

    model_config = {"populate_by_name": True, "extra": "ignore"}

    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Error message")


# ==================== Helper Models ====================


class DateRange(BaseModel):
    """Date range model for flexible date parameters."""

    start_date: Optional[str] = Field(None, description="Start date (format: YYYYMMDD)")
    end_date: Optional[str] = Field(None, description="End date (format: YYYYMMDD)")

    def to_string(self) -> str:
        """Convert date range to GPSS API format (e.g., '20100101:20201231')."""
        if self.start_date and self.end_date:
            return f"{self.start_date}:{self.end_date}"
        if self.start_date:
            return f"{self.start_date}:"
        if self.end_date:
            return f":{self.end_date}"
        return ""


class SearchQuery(BaseModel):
    """Helper model for building complex search queries."""

    keywords: List[str] = Field(..., description="Search keywords")
    operator: SearchLogicOperator = Field(
        default=SearchLogicOperator.AND, description="Logic operator between keywords"
    )

    def to_string(self) -> str:
        """Convert search query to GPSS API format."""
        op = f" {self.operator.value} "
        return op.join(self.keywords)
