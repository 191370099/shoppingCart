from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_email_task


class SendEmailView(APIView):
    def post(self, request):
        subject = request.data.get('subject')
        message = request.data.get('message')
        recipient_list = request.data.get('recipient_list')

        if subject and message and recipient_list:
            send_email_task.delay(subject, message, recipient_list)
            return Response({'message': 'Email sent successfully!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
