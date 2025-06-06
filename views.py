from django.http import Http404
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
# Create your views here.

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    List all code snippets, or create a new snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request : Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request : Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class SnippetDetail(APIView):
    """
    Retrieve, update or delete a code snippet.
    """
    def get_object(self, pk) -> Response:
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist as exc:
            raise Http404 from exc
        
    def get(self, request : Request, pk, format=None) -> Response:
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request : Request, pk, format=None) -> Response:
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        