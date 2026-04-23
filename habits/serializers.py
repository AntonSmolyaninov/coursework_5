from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate(self, data):
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError('Нельзя указывать и вознаграждение, и связанную привычку')
        if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
            raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')
        if data.get('related_habit') and not data['related_habit'].is_pleasant:
            raise serializers.ValidationError({'related_habit': 'Связанная привычка должна быть приятной'})
        return data


class HabitPublicSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Habit
        fields = ('id', 'action', 'place', 'time', 'user_username', 'is_pleasant', 'execution_time')
