from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import Document, AnalysisResult, RewriteSuggestion, LearningProgress
from .services import PlagiarismDetector, AIDetector, Humanizer


def home(request):
    """Landing page"""
    return render(request, 'analyzer/home.html')


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'analyzer/register.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard showing recent documents and progress"""
    documents = Document.objects.filter(user=request.user)[:10]
    progress, _ = LearningProgress.objects.get_or_create(user=request.user)

    context = {
        'documents': documents,
        'progress': progress,
        'total_documents': documents.count(),
    }
    return render(request, 'analyzer/dashboard.html', context)


@login_required
def analyze_text(request):
    """Main analysis page"""
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled')
        text = request.POST.get('text', '')

        if not text.strip():
            messages.error(request, 'Please enter some text to analyze.')
            return render(request, 'analyzer/analyze.html')

        # Create document
        document = Document.objects.create(
            user=request.user,
            title=title,
            original_text=text
        )

        # Run analysis
        plagiarism_detector = PlagiarismDetector()
        ai_detector = AIDetector()
        humanizer = Humanizer()

        plag_result = plagiarism_detector.analyze(text)
        ai_result = ai_detector.analyze(text)
        humanize_result = humanizer.analyze_and_suggest(text, ai_result)

        # Save analysis results
        analysis = AnalysisResult.objects.create(
            document=document,
            plagiarism_score=plag_result['score'],
            plagiarism_details=plag_result,
            ai_score=ai_result['score'],
            ai_details=ai_result
        )

        # Save rewrite suggestions
        for i, suggestion in enumerate(humanize_result.get('suggestions', [])):
            RewriteSuggestion.objects.create(
                analysis=analysis,
                original_sentence=suggestion.get('original', ''),
                suggested_rewrites=suggestion.get('suggestions', []),
                explanation=json.dumps(suggestion),
                sentence_index=i
            )

        # Update learning progress
        _update_progress(request.user)

        return redirect('analysis_result', document_id=document.id)

    return render(request, 'analyzer/analyze.html')


@login_required
def analysis_result(request, document_id):
    """Display analysis results"""
    document = get_object_or_404(Document, id=document_id, user=request.user)

    try:
        analysis = document.analysis
    except AnalysisResult.DoesNotExist:
        messages.error(request, 'Analysis not found.')
        return redirect('dashboard')

    # Re-run humanizer for display
    humanizer = Humanizer()
    humanize_result = humanizer.analyze_and_suggest(
        document.original_text,
        analysis.ai_details
    )

    # Generate writing exercises
    writing_exercises = humanizer.generate_writing_exercises(
        document.original_text,
        analysis.ai_details
    )

    # Generate sentence-by-sentence breakdown
    sentence_breakdown = humanizer.generate_sentence_breakdown(document.original_text)

    context = {
        'document': document,
        'analysis': analysis,
        'humanize_suggestions': humanize_result,
        'plag_details': analysis.plagiarism_details,
        'ai_details': analysis.ai_details,
        'writing_exercises': writing_exercises,
        'sentence_breakdown': sentence_breakdown,
    }
    return render(request, 'analyzer/result.html', context)


@login_required
def document_history(request):
    """View all past documents"""
    documents = Document.objects.filter(user=request.user)
    return render(request, 'analyzer/history.html', {'documents': documents})


@login_required
@require_POST
def quick_analyze(request):
    """API endpoint for quick text analysis without saving"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')

        if not text.strip():
            return JsonResponse({'error': 'No text provided'}, status=400)

        ai_detector = AIDetector()
        ai_result = ai_detector.analyze(text)

        plagiarism_detector = PlagiarismDetector()
        plag_result = plagiarism_detector.analyze(text)

        return JsonResponse({
            'ai_score': ai_result['score'],
            'plagiarism_score': plag_result['score'],
            'ai_indicators': ai_result.get('indicators', []),
            'explanation': ai_result.get('explanation', [])
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@login_required
def learning_center(request):
    """Educational resources and tips"""
    progress, _ = LearningProgress.objects.get_or_create(user=request.user)
    recent_analyses = AnalysisResult.objects.filter(
        document__user=request.user
    ).order_by('-analyzed_at')[:5]

    context = {
        'progress': progress,
        'recent_analyses': recent_analyses,
    }
    return render(request, 'analyzer/learning.html', context)


def _update_progress(user):
    """Update user's learning progress statistics"""
    progress, _ = LearningProgress.objects.get_or_create(user=user)

    documents = Document.objects.filter(user=user)
    analyses = AnalysisResult.objects.filter(document__user=user)

    progress.total_documents = documents.count()

    if analyses.exists():
        progress.average_plagiarism_score = sum(a.plagiarism_score for a in analyses) / analyses.count()
        progress.average_ai_score = sum(a.ai_score for a in analyses) / analyses.count()

        # Calculate improvement trend (compare last 5 vs previous 5)
        recent = list(analyses.order_by('-analyzed_at')[:5])
        older = list(analyses.order_by('-analyzed_at')[5:10])

        if len(recent) >= 3 and len(older) >= 3:
            recent_avg = sum(a.ai_score for a in recent) / len(recent)
            older_avg = sum(a.ai_score for a in older) / len(older)
            progress.improvement_trend = older_avg - recent_avg  # Positive = improving

    progress.save()
