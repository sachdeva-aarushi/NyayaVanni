from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from services.storage_service import (
    upload_to_local, save_document_record, get_document_record,
    save_cached_analysis, get_cached_analysis
)
from services.ocr_service import extract_document
from services.rag_service import retrieve_relevant_laws
from services.gemini_service import analyze_document_with_gemini, generate_chat_response
from models.schemas import ChatRequest, ChatResponse
import json
import logging

logger = logging.getLogger(__name__)

api_router = APIRouter()

@api_router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload document to S3 and return documentId"""
    try:
        contents = await file.read()
        doc_id, local_path = upload_to_local(contents, file.filename)
        # Assuming dummy user 'user_123' for MVP
        save_document_record("user_123", doc_id, file.filename, local_path)
        return {"documentId": doc_id, "message": "Uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/analyze/{document_id}")
async def analyze_document(document_id: str, language: str = "en", file: UploadFile = File(None)):
    """
    Trigger full analysis pipeline.
    For this MVP, we optionally accept the file again if we don't download from S3 to save time.
    Ideally, we read s3_key from DynamoDB and fetch from S3.
    """
    try:
        # ── Cache-first ──────────────────────────────────────────────────────────
        cached = get_cached_analysis(document_id, language)
        if cached:
            logger.info(f"Cache HIT for document {document_id} [{language}]")
            return {
                "documentId": document_id,
                "analysis": cached["analysis"],
                "extracted_text": cached["extracted_text"][:500] + "...",
                "cached": True
            }
        # ── Cache MISS: run the full pipeline ────────────────────────────────────
        # Simplify MVP: if file is not provided, we download it from local storage via SQLite metadata.
        if not file:
            record = get_document_record(document_id)
            if not record or not record.get("local_path"):
                raise HTTPException(status_code=404, detail="Document not found or file missing")
            
            try:
                with open(record["local_path"], "rb") as f:
                    contents = f.read()
            except IOError:
                raise HTTPException(status_code=500, detail="Failed to read document from storage")
            
            filename = record["filename"]
        else:
            contents = await file.read()
            filename = file.filename
        
        # 1. OCR Extraction
        text = extract_document(contents, filename)
        
        # 2. RAG Retrieval
        relevant_laws = retrieve_relevant_laws(text, k=3)
        
        # 3. Gemini Analysis
        analysis_result = analyze_document_with_gemini(text, relevant_laws, language)
        
        # 4. Persist to cache so repeat requests are served instantly
        save_cached_analysis(document_id, language, text, analysis_result)

        return {
            "documentId": document_id,
            "analysis": analysis_result,
            "extracted_text": text[:500] + "...",
            "cached": False
        }
    except Exception as e:
        import traceback
        trace = traceback.format_exc()
        logger.error(f"Analysis failed: {e}\n{trace}")
        
        detail_msg = str(e)
        if "429" in str(e) or "Quota exceeded" in str(e):
            raise HTTPException(status_code=429, detail="AI Quota limit reached. Please wait a minute and try again.")
            
        raise HTTPException(status_code=500, detail="An internal processing error occurred.")


@api_router.post("/chat/{document_id}", response_model=ChatResponse)
async def chat_with_document(document_id: str, request: ChatRequest):
    """Send chat message with context"""
    try:
        # Validate user message is not empty
        if not request.user_message or not request.user_message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # In full production, fetch analysis and history from DynamoDB
        analysis = request.document_analysis or {}
        
        # Format history
        history = [{"role": msg.role, "message": msg.message} for msg in request.chat_history]
        
        response_text = generate_chat_response(analysis, history, request.user_message, request.language)
        
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail="Chat generation failed")


@api_router.post("/chat/general", response_model=ChatResponse)
async def chat_general(request: ChatRequest):
    """Send general legal chat message without document context"""
    try:
        # Validate user message is not empty
        if not request.user_message or not request.user_message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # For general chat, document_analysis should be empty or None
        analysis = request.document_analysis or {}
        
        # Format history - handle both dict and ChatMessage objects
        history = []
        for msg in request.chat_history:
            if isinstance(msg, dict):
                history.append({"role": msg.get("role"), "message": msg.get("message")})
            else:
                history.append({"role": msg.role, "message": msg.message})
        
        # Generate response using existing service
        response_text = generate_chat_response(
            document_analysis=analysis,
            chat_history=history,
            user_message=request.user_message,
            language=request.language
        )
        
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"General chat failed: {e}")
        raise HTTPException(status_code=500, detail="Chat generation failed")
