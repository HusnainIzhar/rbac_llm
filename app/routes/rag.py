from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.llm import document_chat, document_loader
from app.middleware.authentication import require_auth
import os
import uuid
from typing import Optional

router = APIRouter(prefix="/rag", tags=["rag"])

# Directory for storing temporary uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/query")
async def rag_query(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),  # Make file optional
    current_user: dict = Depends(require_auth),
):
    """
    RAG endpoint that accepts a query and an optional document.
    If document is provided, performs RAG using the document as context.
    If no document is provided, processes the query directly.
    """
    file_path = None
    try:
        # Handle case with file
        if file:
            # Process uploaded file
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)

            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            # Use document_chat for RAG
            response = document_chat(file_path, message)
            
            return {
                "response": response, 
                "user": current_user["full_name"],
                "document": file.filename
            }
        else:
            # Handle case without file - use regular chat instead of RAG
            # You'll need a function that handles regular chat without document context
            from app.services.llm import handle_chat  # Import the regular chat function
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
        # Clean up temporary file if it exists
        if file_path and os.path.exists(file_path):
            os.remove(file_path)