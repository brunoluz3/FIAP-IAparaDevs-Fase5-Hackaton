import os
import io
import tempfile
import uvicorn
from typing import Any, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse

import analyze_architecture

app = FastAPI(title="Architecture Analyzer API", version="1.0.0")

ALLOWED_CT = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 12 * 1024 * 1024  # 12 MB


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


def _expected_pdf_path(tmp_image_path: str) -> str:
    """
    Fallback atual: seu generate_report salva em report/<basename>.pdf.
    Mantemos essa convenção para compatibilidade.
    """
    os.makedirs("report", exist_ok=True)
    base = os.path.splitext(os.path.basename(tmp_image_path))[0]
    return os.path.join("report", f"{base}.pdf")


def _as_file_response(pdf_path: str) -> FileResponse:
    if not os.path.exists(pdf_path):
        raise HTTPException(500, f"PDF não encontrado em '{pdf_path}'")
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path),
    )


def _handle_solve_return(retval: Any, tmp_image_path: str):
    """
    Aceita múltiplos formatos de retorno de solve_vulnerabilities:
      - str: caminho do PDF
      - dict: procura chaves usuais (pdf_path, path, file, content)
      - bytes/bytearray: conteúdo do PDF em memória
      - file-like (possui .read): stream do PDF
      - None: fallback para caminho esperado
    """
    # 1) string como caminho
    if isinstance(retval, str):
        return _as_file_response(retval)

    # 2) dict com metadata
    if isinstance(retval, dict):
        # caminhos prováveis
        for k in ("pdf_path", "path", "file"):
            v = retval.get(k)
            if isinstance(v, str):
                return _as_file_response(v)

        # conteúdo binário direto
        for k in ("content", "bytes", "data"):
            v = retval.get(k)
            if isinstance(v, (bytes, bytearray)):
                return StreamingResponse(
                    io.BytesIO(v), media_type="application/pdf",
                    headers={"Content-Disposition": 'attachment; filename="resultado.pdf"'}
                )

        # se for um retorno só com status/erros
        if "error" in retval or "status" in retval:
            # responda como JSON para não mascarar um erro do worker
            return JSONResponse(retval, status_code=200)

    # 3) bytes diretos
    if isinstance(retval, (bytes, bytearray)):
        return StreamingResponse(
            io.BytesIO(retval), media_type="application/pdf",
            headers={"Content-Disposition": 'attachment; filename="resultado.pdf"'}
        )

    # 4) file-like
    if hasattr(retval, "read"):
        return StreamingResponse(
            retval, media_type="application/pdf",
            headers={"Content-Disposition": 'attachment; filename="resultado.pdf"'}
        )

    # 5) None ou tipo inesperado → fallback compatível com versão atual
    expected_pdf = _expected_pdf_path(tmp_image_path)
    return _as_file_response(expected_pdf)


@app.post("/solve", summary="Recebe imagem (multipart) e retorna o PDF gerado")
async def solve(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CT:
        raise HTTPException(415, f"Tipo não suportado: {file.content_type}. Use JPEG/PNG/WEBP.")

    suffix = os.path.splitext(file.filename or "")[1] or ".jpg"
    os.makedirs("report", exist_ok=True)

    # Salva upload sem carregar tudo na memória
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            temp_path = tmp.name
            size = 0
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > MAX_BYTES:
                    raise HTTPException(413, "Arquivo muito grande (>12MB)")
                tmp.write(chunk)
    except Exception as e:
        try:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
        except Exception:
            pass
        raise HTTPException(400, f"Falha ao salvar arquivo: {e}")

    try:
        # Chama seu pipeline; retorno pode variar (preparamos o handler)
        retval = analyze_architecture.solve_vulnerabilities(temp_path)
        # Converte o retorno na resposta HTTP adequada (PDF/file/JSON)
        return _handle_solve_return(retval, temp_path)
    finally:
        # Limpa apenas a imagem temporária; o PDF permanece
        try:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        except Exception:
            pass


if __name__ == "__main__":
    uvicorn.run(app, port=8000)