from rest_framework.reverse import reverse
from rest_framework import generics, permissions, renderers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from snippets.models import Snippet, Editor
from snippets.serializers import EditorSerializer, SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
# Create your views here.

class SnippetList(generics.ListCreateAPIView):
    """
    List all code snippets, or create a new snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    """
    List contributing Users 
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve a single contributing User
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

# @api_view(['GET'])
# def api_root(request : Request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet_list', request=request, format=format)
#     })

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]
    serializer_class = SnippetSerializer

    def get(self, request : Request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
    
class EditorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code editor.
    """
    queryset = Editor.objects.all()
    serializer_class = EditorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EditorList(generics.ListCreateAPIView):
    """
    List all code editors, or create a new editor.
    """
    queryset = Editor.objects.all()
    serializer_class = EditorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
