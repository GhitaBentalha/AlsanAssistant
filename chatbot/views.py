# chatbot/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MessageSerializer

@api_view(['POST'])
def chat_view(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.validated_data['message']
        # Logique de traitement du message (ex: appeler un modèle de chatbot)
        response_message = f"Réponse au message: {message}"  # Remplacez par la réponse de votre modèle
        return Response({'response': response_message})
    return Response(serializer.errors, status=400)
