from rest_framework import serializers
from clinic_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing out APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user




class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clinic
        fields = ('name', 'address', 'contact_nr', 'email', 'website')

    # def validate(self, data):
    #     if data['quantity'] < 0:
    #         raise serializers.ValidationError("Product quantity can't be negative")
    #     return data





class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient
        fields = ('first_name', 'last_name', 'age', 'gender', 'contact_nr', 'email', 'problem')

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = ('user', 'patient', 'service', 'invoice', 'date', 'time', 'price')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = ('name', 'price')
class ReporttSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = ('appointment', 'medication', 'comments')
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = ('name')
class InvoiceSerializer(serializers.ModelSerializer):
    # items = serializers.SerializerMethodField()
    # quantity = serializers.FloatField(validators=['check_positive'])
    #
    # def get_items(self, invoice):
    #     return InvoiceItemSerializer(invoice.invoiceitem_set.all(), many=True).data

    class Meta:
        model = models.Invoice
        fields = ('date', 'patient', 'clinic')

        # fields = ('id', 'product', 'invoice', 'quantity', 'price', 'total')
        # extra_kwargs = {'total': {'read_only': True}, 'price ': {'read_only': True}}
