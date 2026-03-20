from enum import Enum


class ResponseStatus(Enum):
    SUCCESS = "success"
    ERROR_File_Size_Exceeded = "error_file_size_exceeded"
    ERROR_Invalid_File_Type = "error_invalid_file_type"
    FILE_UPLOADED_SUCCESSFULLY = "file_uploaded_successfully"
    FILE_UPLOAD_FAILED = "file_upload_failed"
