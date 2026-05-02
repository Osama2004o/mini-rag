from enum import Enum


class ResponseSignal(Enum):
    SUCCESS = "success"
    ERROR_File_Size_Exceeded = "error_file_size_exceeded"
    ERROR_Invalid_File_Type = "error_invalid_file_type"
    FILE_UPLOADED_SUCCESSFULLY = "file_uploaded_successfully"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_SUCCESS = "processing_successful"
    PROCESSING_FAILED = "processing_failed"
    NO_FILES_ERROR = "not_files_found"
    FILE_ID_ERROR = "file_id_error"