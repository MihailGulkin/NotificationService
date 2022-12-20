from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage


class UploadMediaAPIView(APIView):
    parser_classes = (
        FileUploadParser,
    )

    def post(self, request):
        file_obj = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file_obj.name, file_obj)
        image_url = fs.url(file_obj.name)
        print(image_url)
        return Response(status=status.HTTP_201_CREATED)
