from rest_framework import serializers
from .models import LectureVideo

class LectureVideoSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display username instead of user ID
    processed = serializers.SerializerMethodField()        # Derived field (True if status == 'done')

    class Meta:
        model = LectureVideo
        fields = [
            'id',
            'title',
            's3_url',
            'status',
            'transcription_status',
            'quiz_questions',
            'summary',
            'transcript',
            'uploaded_at',
            'user',
            'processed',  # ✅ include the custom SerializerMethodField here
        ]
        read_only_fields = ['id', 'uploaded_at', 'user', 'processed']

    def get_processed(self, obj):
        """Return True if video processing is fully completed."""
        return obj.status == 'done'
