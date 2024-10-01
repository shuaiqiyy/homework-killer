import api.fangao.fangao_api as fangao_api

import log
import json


code,hear,mid,name = fangao_api.user_infotmance("13171712179","666666")
log.user_login_infomance_log("13171712179","666666",mid,name,code)
print(code)