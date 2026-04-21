from fastapi import FastAPI, HTTPException
from typing import Optional
import zhconv
import re

app = FastAPI(
    title="Text Processing API",
    description="文本统计、繁简转换、格式清洗、大小写转换",
    version="1.0.0"
)

# ------------------------------
# 1. 文本字数/字符统计
# ------------------------------
@app.get("/api/text/count")
def count_text(text: str):
    if not text:
        raise HTTPException(status_code=400, detail="text cannot be empty")
    
    char_count = len(text)
    word_count = len([w for w in text.split() if w.strip()])
    line_count = len(text.splitlines())

    return {
        "code": 200,
        "data": {
            "total_characters": char_count,
            "total_words": word_count,
            "total_lines": line_count
        }
    }

# ------------------------------
# 2. 大小写转换
# ------------------------------
@app.get("/api/text/case")
def change_case(text: str, mode: str = "upper"):
    if not text:
        raise HTTPException(status_code=400, detail="text cannot be empty")
    
    mode = mode.lower()
    if mode == "upper":
        res = text.upper()
    elif mode == "lower":
        res = text.lower()
    elif mode == "capitalize":
        res = text.capitalize()
    else:
        raise HTTPException(status_code=400, detail="mode must be upper/lower/capitalize")

    return {"code": 200, "data": {"result": res}}

# ------------------------------
# 3. 繁简中文转换
# ------------------------------
@app.get("/api/text/convert")
def convert_zh(text: str, to: str = "simplified"):
    if not text:
        raise HTTPException(status_code=400, detail="text cannot be empty")
    
    to = to.lower()
    if to == "simplified":
        res = zhconv.convert(text, "zh-cn")
    elif to == "traditional":
        res = zhconv.convert(text, "zh-tw")
    else:
        raise HTTPException(status_code=400, detail="to must be simplified/traditional")

    return {"code": 200, "data": {"result": res}}

# ------------------------------
# 4. 文本清洗：去空格、去换行、去多余空白
# ------------------------------
@app.get("/api/text/clean")
def clean_text(text: str, remove_symbols: Optional[bool] = False):
    if not text:
        raise HTTPException(status_code=400, detail="text cannot be empty")
    
    # 去掉换行、制表符、多个空格
    cleaned = re.sub(r'\s+', ' ', text).strip()

    # 可选：移除特殊符号
    if remove_symbols:
        cleaned = re.sub(r'[^\w\s\u4e00-\u9fa5]', '', cleaned)

    return {"code": 200, "data": {"cleaned_text": cleaned}}
