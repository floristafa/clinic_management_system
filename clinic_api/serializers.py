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
        fields = ('id', 'name', 'address', 'contact_nr', 'email', 'website')


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient
        fields = ('id', 'first_name', 'last_name', 'age', 'gender','height','weight', 'BMI', 'contact_nr', 'email', 'problem')
        extra_kwargs = {'BMI': {'read_only': True}}

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = ('id', 'user', 'patient', 'service', 'invoice', 'date', 'time', 'price', 'quantity', 'total')

        extra_kwargs = {'total': {'read_only': True}, 'price ': {'read_only': True}}


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ('id', 'name', 'price', 'quantity')

        def validate(self, data):
            if data['quantity'] < 0:
                raise serializers.ValidationError("Service quantity can't be negative")
            return data


class ReporttSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = ('id', 'appointment', 'medication', 'comments')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = ('id', 'name')


class InvoiceSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()


    def get_items(self, invoice):
        return AppointmentSerializer(invoice.appointment_set.all(), many=True).data

    class Meta:
        model = models.Invoice
        fields = ('id', 'date', 'patient', 'clinic', 'total','items')
