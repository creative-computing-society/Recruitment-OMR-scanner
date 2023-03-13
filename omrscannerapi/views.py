from rest_framework.views import APIView, Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import MultiPartRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer

from django.shortcuts import render

from .serializers import RecordSerializer
from .models import Record

from .omr_scanner.omr2 import analyseSheet

# Create your views here.

class OMRScannerAPIView(APIView):

    # permission_classes = [IsAuthenticated, ]

    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):

        serializer = RecordSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            filename = serializer.data.get('sheet')
            
            try:
                
                result = analyseSheet(filename)
                
                record = Record.objects.filter(id=serializer.data.get('id')).first()
                
                record.roll_no = result.get('roll_no')
                record.score = result.get('score')
                
                record.save()
                
                if record.roll_no==None or record.score==None:
                    return Response({'status': 'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response({'status': 'success', 'roll_no': record.roll_no, 'score': record.score}, status=status.HTTP_200_OK)
            
            except BaseException as err:
                
                response = {
                    'status': 'error',
                    'error_type': str(type(err)),
                    'error': str(err)
                }
                
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response = serializer.errors
        response['status'] = 'error'
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

def index(request):
    return render(request, 'form.html')
