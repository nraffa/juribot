from pydantic import BaseModel
import io as _io


class DocumentUploadRequest(BaseModel):
    fileName: str
    file: _io.BufferedReader
