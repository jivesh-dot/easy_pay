from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny


from core.generic_responses import success_response, error_response
from .models import PaymentIntent
import payments.serializers as payment_serializers
from users.models import Merchant 


import logging
import traceback



class PaymentIntentView(APIView):
    """
        POST   /payment-intents/ -> Auth Required
        GET    /payment-intents/{id}/ -> Public
        PATCH  /payment-intents/ -> Public
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
        

    def post(self, request):
        try:
            merchant = Merchant.objects.get(user=request.user)
        except Merchant.DoesNotExist:
            return error_response('Merchant profile not found', status_code=403, generic=True)

        payment_create_serializer = payment_serializers.PaymentIntentCreateSerializer(data=request.data)
        if payment_create_serializer.is_valid():
            obj = PaymentIntent(
                merchant=merchant,
                **payment_create_serializer.validated_data,
            )
            obj.save()
            return success_response(payment_serializers.PaymentIntentSerializer(obj).data, status_code=201)
        else:
            return error_response(payment_create_serializer.errors, status_code=400)

    def get(self, request, pk=None):
        validation_serializer = payment_serializers.PaymentIdentifierSerializer(data={'identifier': pk})
        if not validation_serializer.is_valid():
            return error_response(validation_serializer.errors, status_code=400)
        try:
            obj = PaymentIntent.objects.get(pk=pk)
        except PaymentIntent.DoesNotExist:
            return error_response({'payment_intent_id': 'Invalid payment intent id'}, status_code=404)
        return success_response(payment_serializers.PaymentIntentSerializer(obj).data)
    
    # Note This should be a webhook in real world scenarios (Eg: Stripe integrations)
    # TODO hardcoded messages to be moved to constants
    def patch(self, request):
        try:
            validation_serializer = payment_serializers.PaymentStatusUpdateSerializer(data=request.data)
            if not validation_serializer.is_valid():
                return error_response(validation_serializer.errors, status_code=400)
            
            payment_intent_id = validation_serializer.data.get('identifier')
            payment_status= validation_serializer.data.get('status')

            try:
                obj = PaymentIntent.objects.get(pk=payment_intent_id)
            except PaymentIntent.DoesNotExist:
                return error_response({'payment_intent_id': 'Invalid payment intent id'}, status_code=404)
            
            if obj.status != PaymentIntent.Status.PENDING:
                return error_response({'status': 'status transitioned to next stage'}, status_code=400)

            obj.status = payment_status
            obj.save(update_fields=['status', 'updated_at'])

            return success_response(payment_serializers.PaymentIntentSerializer(obj).data)
        except Exception:
            logging.error(f'#payments#views#PaymentIntentView#patch#exception={str(traceback.format_exc())}')
            return error_response('Server Error', status_code=500, generic=True)