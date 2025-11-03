from fastapi import FastAPI, Response, Request
from fastapi.responses import FileResponse
import json
import requests
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
website = ""

loginUrlTemplate = "https://DOMAIN_PLACEHOLDER.api.altius.finance/api/v0.0.2/login"
getDealsUrlTemplate = "https://DOMAIN_PLACEHOLDER.api.altius.finance/api/v0.0.2/deals-list"
getAttachmentsUrlTemplate = "https://DOMAIN_PLACEHOLDER.api.altius.finance/api/v0.0.3/deals/DEAL_ID_PLACEHOLDER/files"

mimetypesDict = {
    "pdf": "application/pdf",
    "txt": "text/plain"
}

class DealsResponse(BaseModel):
    data: list

class Account(BaseModel):
    name: str | None = ""
    domain: str | None = ""
    api_domain: str | None = ""
    company_type: str | None = ""
    trusted_email_domain: str | None = ""
    dataroom_phone_number: str | None = ""
    report_url: str | None = ""
    account_date_format: str | None = ""
    html_template: str | None = ""
    html_template2: str | None = ""
    investment_details_prompt: str | None = ""
    created_at: str | None = ""
    updated_at: str | None = ""
    logo_url: str | None = ""
    under_maintenance: bool | None = False
    is_report_enabled: bool | None = False
    external_report: bool | None = False
    show_benchmark: bool | None = False
    show_batch_id: bool | None = False
    show_plaid: bool | None = False
    allow_dataroom: bool | None = False
    allow_fees_calc: bool | None = False
    allow_social: bool | None = False
    show_global_investor_filter: bool | None = False
    support_investor_groups: bool | None = False
    investor_level_characteristics: bool | None = False
    allow_account_invitation: bool | None = False
    allow_gpt: bool | None = False
    look_through_investments: bool | None = False
    hedge_fund: bool | None = False
    show_correlations: bool | None = False
    adjustable_columns: bool | None = False
    allow_use_date_range_switch: bool | None = False
    batch_runtime_summary: bool | None = False
    enable_crypto: bool | None = False
    enable_user_management: bool | None = False
    nullify_unfunded_commitment: bool | None = False
    show_profit_calculations: bool | None = False
    allow_effective_range: bool | None = False
    show_hcs_view: bool | None = False
    show_meitav_management_fees: bool | None = False
    show_debt: bool | None = False
    show_cashflow: bool | None = False
    show_calc_fields_copy: bool | None = False
    saml_sso_enabled: bool | None = False
    sanitize_emails: bool | None = False
    sanitize_documents: bool | None = False
    allow_news: bool | None = False
    allow_ai_extraction: bool | None = False
    add_classification_task: bool | None = False
    disable_apply_filters: bool | None = False
    hide_global_asset_class: bool | None = False
    single_asset_report: bool | None = False
    view_only_account: bool | None = False
    allow_deal_tab_open: bool | None = False
    prioritize_accounting_date: bool | None = False
    show_ff_model: bool | None = False
    allow_external_apis: bool | None = False
    show_secondary_pricing: bool | None = False
    show_telescope: bool | None = False
    azure_sso_enabled: bool | None = False
    id: int | None = -1
    allow_teams: int | None = -1
    check_session_lifetime: int | None = -1
    batch_id: int | None = -1
    split_id: int | None = -1

class FilesResponse(BaseModel):
    data: dict | None = None

class AttachmentData(BaseModel):
    name: str | None = None
    file_url: str | None = None
    type: str | None = None
    id: int | None = None

class FilesRequest(BaseModel):
    dealId: str
    website: str
    token: str

class LoginRequest(BaseModel):
    website: str
    username: str
    password: str

class Settings(BaseModel):
    dealsTableColumns: list | None = []

class User(BaseModel):
    id: int
    last_account_id: int
    wrong_password_count: int
    opportunity_id: int
    account_id: int
    role_id: int
    blank_template_id: int
    created_at: str
    updated_at: str
    first_name: str
    last_name: str
    company_name: str
    phone_number: str
    email: str
    password_updated_at: str
    profile_photo_path: str
    avatar_type: str
    last_seen: str
    profile_photo_url: str
    full_name: str
    show_social_profile: bool
    enable_2fa: bool
    email_notification: bool
    has_only_external_accounts: bool
    settings: Settings | None = {}
    account: Account | None = {}

class Success(BaseModel):
    token: str | None = None
    broadcast_token: str | None = None
    user: User | None = None

class Error(BaseModel):
    login: list | None = None

class Fo1LoginResponse(BaseModel):
    success: Success | None = (Success)(**{})
    status: str | None = None
    errors: Error | None = None

async def getDeals(token: str, website: str):
    if (not token or token == None):
        return []
    endpoint: str = getDealsUrlTemplate.replace("DOMAIN_PLACEHOLDER", website)
    print(endpoint)
    headers = {
        "Content-type": "application/json"
    }
    cookies = {
        'Authorization2': token
    }
    responseObj: dict = requests.post(endpoint, headers=headers, cookies=cookies).json()
    dealsResponse: DealsResponse = (DealsResponse)(**responseObj)
    for deal in dealsResponse.data:
        # filesRequest: dict = {
        #     "dealId": str(deal["id"]),
        #     "website": website,
        #     "token": token
        # }
        deal["fileUrl"] = await getAttachment(dealId=str(deal["id"]), website=website, token=token)
    print(dealsResponse)
    return dealsResponse.data

@app.post("/login")
async def login(response: Response, req: Request):
    modelRequest = (LoginRequest)(**(await req.json()))
    endpoint = loginUrlTemplate.replace("DOMAIN_PLACEHOLDER", modelRequest.website)
    payload = {
        "email": modelRequest.username,
        "password": modelRequest.password,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    loginResponse = requests.post(endpoint, json=payload, headers=headers)
    responseObj: dict = loginResponse.json()
    fo1LoginResponse: Fo1LoginResponse = (Fo1LoginResponse)(**responseObj)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.set_cookie(
        key="token",
        value=fo1LoginResponse.success.token,
        httponly=True,
        secure=True,
    )

    errorMsg: str = ""
    if fo1LoginResponse.errors != None and not fo1LoginResponse.errors == None:
        errorMsg = " ".join(fo1LoginResponse.errors.login)
    return {
            "ok": loginResponse.status_code == 200,
            "errorMessage": errorMsg,
            "token": fo1LoginResponse.success.token,
            "user": fo1LoginResponse.success.user,
            "deals": await getDeals(token=fo1LoginResponse.success.token, website=modelRequest.website)
        }

async def getAttachment(dealId, website, token):
    print("IN GET ATTACHMENT")
    try:
        endpoint = getAttachmentsUrlTemplate.replace("DOMAIN_PLACEHOLDER", website).replace("DEAL_ID_PLACEHOLDER", dealId)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        cookies = {
            'Authorization2': token
        }
        filesRawResponse = requests.get(endpoint, headers=headers, cookies=cookies)
        filesResponse: FilesResponse = (FilesResponse)(**filesRawResponse.json())
        for attachmentId in filesResponse.data:
            attachmentObj = filesResponse.data[attachmentId]
            attachment: AttachmentData = (AttachmentData)(**attachmentObj)
            return attachment.file_url
            # fileResponseRaw = requests.get(attachment.file_url)
            # fileResponseBlob = fileResponseRaw.text
            # fileName: str = attachment.name
            # fileTxt = open(fileName, "w")
            # fileTxt.write(fileResponseBlob)
            # fileTxt.close()
            # return fileName
        return False
    except Exception as e:
        print(e)

@app.get("/download")
def downloadFile(f: str):
    return FileResponse(path=f, filename=f)
    # return response