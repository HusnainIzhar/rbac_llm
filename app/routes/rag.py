from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.llm import document_chat, document_loader
from app.middleware.authentication import require_auth
import os
import uuid
from typing import Optional

router = APIRouter(prefix="/rag", tags=["rag"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/query")
async def rag_query(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    current_user: dict = Depends(require_auth),
):
    file_path = None
    try:

        if file:

            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)

            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            response = document_chat(file_path, message)

            return {
                "response": response,
                "user": current_user["full_name"],
                "document": file.filename,
            }
        else:

            from app.services.llm import handle_chat

            response = handle_chat(None, message)

            return {
                "response": response,
                "user": current_user["full_name"],
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )

    finally:

        if file_path and os.path.exists(file_path):
            os.remove(file_path)
