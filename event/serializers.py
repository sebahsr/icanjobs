from rest_framework import routers, serializers, viewsets
from event import models
class AppointmentSerializer(serializers.ModelSerializer):
    need = serializers.StringRelatedField()
    user =  serializers.StringRelatedField()
    slot = serializers.StringRelatedField()
    userID = serializers.SerializerMethodField('userIdentification')
    full_name = serializers.SerializerMethodField('userFullName')

    def userIdentification(self, appointment):
        return appointment.user.pk
    
    def userFullName(self, appointment):
        return "%s %s" %(appointment.user.first_name, appointment.user.last_name)

    class Meta:
        model = models.Appointment
        fields = '__all__'