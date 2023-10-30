from django.db import models


class UploadedFile(models.Model):
    file = models.FileField(upload_to="mixed/")
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uploaded_on.date()
