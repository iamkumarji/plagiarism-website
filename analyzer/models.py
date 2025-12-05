from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    """Stores submitted documents for analysis"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    original_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class AnalysisResult(models.Model):
    """Stores analysis results for a document"""
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='analysis')

    # Plagiarism detection results
    plagiarism_score = models.FloatField(default=0.0)
    plagiarism_details = models.JSONField(default=dict)

    # AI detection results
    ai_score = models.FloatField(default=0.0)
    ai_details = models.JSONField(default=dict)

    # Analysis metadata
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.document.title}"


class RewriteSuggestion(models.Model):
    """Stores humanization/rewrite suggestions for flagged content"""
    analysis = models.ForeignKey(AnalysisResult, on_delete=models.CASCADE, related_name='suggestions')
    original_sentence = models.TextField()
    suggested_rewrites = models.JSONField(default=list)
    explanation = models.TextField()
    sentence_index = models.IntegerField()

    class Meta:
        ordering = ['sentence_index']

    def __str__(self):
        return f"Suggestion for sentence {self.sentence_index}"


class LearningProgress(models.Model):
    """Tracks student learning progress over time"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    total_documents = models.IntegerField(default=0)
    average_plagiarism_score = models.FloatField(default=0.0)
    average_ai_score = models.FloatField(default=0.0)
    improvement_trend = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress for {self.user.username}"
