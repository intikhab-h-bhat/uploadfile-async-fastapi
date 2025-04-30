from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import asyncio
from docx import Document

import io
from fastapi.responses import JSONResponse



app= FastAPI()



async def read_file(file: UploadFile):
    content = await file.read()
    if file.filename.endswith(".docx"):
        doc = Document(io.BytesIO(content))
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return full_text
    else:
        # Assume it's plain text
        return content.decode('utf-8', errors='ignore')


async def summarize_resume(resume_text: str) -> str:
    # Dummy summary logic
    return f"General Summary: Resume mentions {len(resume_text.split())} words."

async def summarize_resume_with_jd(resume_text: str, jd_text: str) -> str:
    # Dummy matching logic
    common_words = set(resume_text.split()) & set(jd_text.split())
    return f"Contextual Summary: Found {len(common_words)} common keywords."

@app.post("/upload/")
async def upload_resume_and_jd(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    # Read files concurrently
    resume_text, jd_text = await asyncio.gather(
        read_file(resume),
        read_file(jd)
    )

    # Summarize concurrently
    general_summary, contextual_summary = await asyncio.gather(
        summarize_resume(resume_text),
        summarize_resume_with_jd(resume_text, jd_text)
    )

    return JSONResponse(content={
        "general_summary": general_summary,
        "contextual_summary": contextual_summary
    })
