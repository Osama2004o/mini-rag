from fastapi import FastAPI, APIRouter, Depends, UploadFile
from .BaseController import BaseController


class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  # 1 MB in bytes

    def validate_uploaded_file(self, file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False
        if (
            file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale
        ):  # file size in bytes
            return False
        return True
