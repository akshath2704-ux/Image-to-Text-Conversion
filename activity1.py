from config import HF_API_KEY
import requests, base64, os, re, time
from PIL import Image
from colorama import init,Fore,Style
init(autoreset=True)
ROUTER_URL="https://router.huggingface.co/v1/chat/complletions"
HEADERS={"Authorization":f"Bearer{HF_API_KEY}","Content-Type":"applications/json"}
VISION_MODELS = [
"moonshotai/Kimi-K2.6:novita",
"meta-llama/Llama-4-Maverick-17B-128E-Instruct:sambanova",
"meta-llama/Llama-3.2-11B-Vision-Instruct:sambanova",
]
TEXT_MODELS = [
"Qwen/Qwen2.5-7B-Instruct:together",
"Qwen/Qwen2.5-14B-Instruct:together",
"Qwen/Qwen2.5-32B-Instruct:together",
"mistralai/Mistral-7B-Instruct-v0.3:together",
"mistralai/Mixtral-8x7B-Instruct-v0.1:together",
]
def _data_url(path:str)->str:
    with open(path,"rb") as f:
        return"data:image/jpeg;base64,"+base64.b64encode(f.read()).decode("utf-8")
def query_hf_api(payload:dict):
    try:
        r=requests.post(ROUTER_URL,headers=HEADERS,json=payload,timeout=120)
    except requests.RequestException as e:
        return None,f"Request failed:{e}"
    if r.status_code !=200:
        try:
            j=r.json()
            msg=j.get("error",{}).get("message")or str(j)
        except Exception:
            msg=(r.text or"").strip()or r.reason or "Request failed."
        return None,f"Status{R.status_code}:{msg}"
    try:
        return r.json(),None
    except Exception:
        return None,"Non-JSON response recieved from the API."