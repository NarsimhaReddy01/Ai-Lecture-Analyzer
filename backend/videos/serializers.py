from rest_framework import serializers
from .models import LectureVideo

class LectureVideoSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    processed = serializers.SerializerMethodField()
    
    class Meta:
        model = LectureVideo
        fields = [
            'id',
            'title',
            's3_url',
            'status',               # Replacing 'processed' with 'status'
            'transcription_status',
            'quiz_questions',
            'summary',
            'transcript',
            'uploaded_at',
            'user'
        ]
        
    def get_processed(self, obj):
        return obj.status == 'done'
