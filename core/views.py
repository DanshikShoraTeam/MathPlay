import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Count, Sum, Max, Q
from django.views.decorators.csrf import csrf_exempt
from .models import Game, GameSession, StudentProfile
from django.contrib.auth.models import User
import socket

def get_local_ip():
    """Returns the local network IP address of the server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable, just to determine the interface
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# ═══════════════════════════════════════════════════════
# SAMPLE GAMES — 6-7 GRADE LEVEL (one per game type)
# ═══════════════════════════════════════════════════════
SAMPLE_GAMES = [
    {
        'title': 'Алгебра негіздері — Quiz',
        'game_type': 'quiz',
        'questions': [
            {'q': '2x + 6 = 14, x = ?',        'a': '4',  'wrong': ['3', '5', '6']},
            {'q': '3x - 9 = 12, x = ?',         'a': '7',  'wrong': ['5', '8', '6']},
            {'q': 'x² = 49, x = ?',             'a': '7',  'wrong': ['6', '8', '9']},
            {'q': '5x + 3 = 28, x = ?',         'a': '5',  'wrong': ['4', '6', '7']},
            {'q': '(-3) × (-4) = ?',            'a': '12', 'wrong': ['-12', '7', '-7']},
            {'q': '15% от 80 = ?',              'a': '12', 'wrong': ['10', '14', '16']},
            {'q': '√144 = ?',                   'a': '12', 'wrong': ['11', '13', '14']},
        ]
    },
    {
        'title': 'Геометрия формулалары — Memory',
        'game_type': 'memory',
        'questions': [
            {'q': 'Шеңбер ауданы',           'a': 'S = πr²'},
            {'q': 'Үшбұрыш ауданы',          'a': 'S = ½·a·h'},
            {'q': 'Трапеция ауданы',          'a': 'S = ½(a+b)·h'},
            {'q': 'Параллелограмм ауданы',    'a': 'S = a·h'},
            {'q': 'Шаршы периметрі',          'a': 'P = 4a'},
            {'q': 'Тікбұрышты периметрі',     'a': 'P = 2(a+b)'},
        ]
    },
    {
        'title': 'Дәреже және тамыр — Froggy',
        'game_type': 'froggy',
        'questions': [
            {'q': '7² = ?',               'a': '49',  'wrong': ['42', '54', '56']},
            {'q': '2³ = ?',               'a': '8',   'wrong': ['6', '9', '16']},
            {'q': '√169 = ?',             'a': '13',  'wrong': ['11', '12', '14']},
            {'q': '(-5)² = ?',            'a': '25',  'wrong': ['-25', '10', '20']},
            {'q': '4³ = ?',               'a': '64',  'wrong': ['48', '56', '72']},
            {'q': '√256 = ?',             'a': '16',  'wrong': ['14', '15', '17']},
            {'q': '3⁴ = ?',               'a': '81',  'wrong': ['64', '72', '84']},
        ]
    },
    {
        'title': 'Теңдеу шешу — Fill Blank',
        'game_type': 'fill_blank',
        'questions': [
            {'q': '3x = 21, x = ?',         'a': '7'},
            {'q': '2x + 5 = 15, x = ?',     'a': '5'},
            {'q': '4x - 8 = 12, x = ?',     'a': '5'},
            {'q': 'x/3 + 2 = 6, x = ?',     'a': '12'},
            {'q': '5x - 3 = 22, x = ?',     'a': '5'},
            {'q': '√x = 9, x = ?',          'a': '81'},
            {'q': '2x² = 50, x = ?',        'a': '5'},
        ]
    },
    {
        'title': 'Ғылыми формулалар — Match',
        'game_type': 'match',
        'questions': [
            {'q': 'Пифагор теоремасы',       'a': 'a² + b² = c²'},
            {'q': 'Шеңбер ауданы',           'a': 'S = πr²'},
            {'q': 'Ом заңы',                 'a': 'I = U / R'},
            {'q': 'Жылдамдық формуласы',     'a': 'v = s / t'},
            {'q': 'Жұмыс формуласы',         'a': 'A = F · s'},
            {'q': 'Кинетикалық энергия',     'a': 'Eк = mv² / 2'},
        ]
    },
]


def create_sample_games(user):
    """Create one default sample game per type for a new teacher."""
    for sample in SAMPLE_GAMES:
        Game.objects.create(
            title=sample['title'],
            game_type=sample['game_type'],
            questions=sample['questions'],
            author=user,
            is_published=False,
        )


# ═══════════════════════════════════════════════════════
# AUTH VIEWS
# ═══════════════════════════════════════════════════════

def homepage(request):
    return render(request, 'homepage.html', {'hide_sidebar': True})


@csrf_exempt
def login_view(request):
    error = None
    if request.method == 'POST':
        u = request.POST.get('username', '').strip()
        p = request.POST.get('password', '')
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('dashboard')
        error = 'Қолданушы аты немесе пароль қате.'
    return render(request, 'auth/login_register.html', {'error': error, 'mode': 'login'})


@csrf_exempt
def register_view(request):
    error = None
    if request.method == 'POST':
        u = request.POST.get('username', '').strip()
        p = request.POST.get('password', '')
        p2 = request.POST.get('password2', '')
        if not u or not p:
            error = 'Қолданушы аты мен пароль міндетті.'
        elif p != p2:
            error = 'Парольдер сәйкес келмейді.'
        elif User.objects.filter(username=u).exists():
            error = 'Бұл қолданушы аты бос емес.'
        else:
            user = User.objects.create_user(username=u, password=p)
            create_sample_games(user)   # Seed default games
            login(request, user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'redirect': '/dashboard/'})
            return redirect('dashboard')
    return render(request, 'auth/login_register.html', {'error': error, 'mode': 'register'})


def logout_view(request):
    logout(request)
    return redirect('homepage')


# ═══════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════

@login_required
def dashboard(request):
    games = Game.objects.filter(author=request.user).order_by('-created_at')
    sessions = GameSession.objects.filter(game__author=request.user)
    stats = {
        'total_games': games.count(),
        'total_plays': games.aggregate(Sum('play_count'))['play_count__sum'] or 0,
        'total_sessions': sessions.values('student_name').distinct().count(),
        'avg_score': sessions.aggregate(Avg('score_percent'))['score_percent__avg'] or 0,
    }
    return render(request, 'dashboard/main.html', {
        'games': games, 
        'stats': stats,
        'local_ip': get_local_ip()
    })


@login_required
def game_create_type(request):
    return render(request, 'dashboard/game_create_type.html')


@login_required
def game_create_form(request, gtype):
    if request.method == 'POST':
        title = request.POST.get('title')
        game = Game.objects.create(title=title, game_type=gtype, author=request.user)
        return redirect('game_edit', pk=game.pk)
    return render(request, 'dashboard/game_create_form.html', {'gtype': gtype})


@login_required
def game_edit(request, pk):
    game = get_object_or_404(Game, pk=pk, author=request.user)
    if request.method == 'POST':
        questions_raw = request.POST.get('questions', '[]')
        game.questions = json.loads(questions_raw)
        new_title = request.POST.get('title', '').strip()
        if new_title:
            game.title = new_title
        if request.POST.get('is_published') == 'on':
            game.is_published = True
        game.save()
        return redirect('dashboard')
    return render(request, 'dashboard/game_edit.html', {'game': game})


@login_required
def game_detail(request, pk):
    return redirect('game_stats', pk=pk)


@login_required
def game_quick_publish(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    game = get_object_or_404(Game, pk=pk, author=request.user)
    game.is_published = True
    game.save()
    return JsonResponse({'status': 'ok', 'publish_code': game.publish_code})


@login_required
def game_unpublish(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    game = get_object_or_404(Game, pk=pk, author=request.user)
    game.is_published = False
    game.save()
    return JsonResponse({'status': 'ok'})


@login_required
def game_delete(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    game = get_object_or_404(Game, pk=pk, author=request.user)
    game.delete()
    return JsonResponse({'status': 'ok'})


@login_required
def game_stats(request, pk):
    game = get_object_or_404(Game, pk=pk, author=request.user)
    sessions = game.sessions.all().order_by('-completed_at')
    stats = {
        'max_score': sessions.aggregate(Max('score_percent'))['score_percent__max'] or 0,
        'avg_score': sessions.aggregate(Avg('score_percent'))['score_percent__avg'] or 0,
        'avg_time':  sessions.aggregate(Avg('time_seconds'))['time_seconds__avg'] or 0,
    }
    chart_labels = [s.student_name for s in sessions[:10]]
    chart_scores = [s.score_percent for s in sessions[:10]]
    return render(request, 'dashboard/game_stats.html', {
        'game': game, 'sessions': sessions, 'stats': stats,
        'chart_labels': json.dumps(chart_labels),
        'chart_scores': json.dumps(chart_scores),
    })


@login_required
def full_stats(request):
    games = Game.objects.filter(author=request.user)
    sessions = GameSession.objects.filter(game__in=games).order_by('-completed_at')
    
    # Aggregates
    stats = {
        'total_xp': sessions.aggregate(Sum('xp_earned'))['xp_earned__sum'] or 0,
        'total_plays': sessions.count(),
        'avg_score': sessions.aggregate(Avg('score_percent'))['score_percent__avg'] or 0,
        'total_time': sessions.aggregate(Sum('time_seconds'))['time_seconds__sum'] or 0,
    }
    
    # Distribution by game type
    type_labels = []
    type_data = []
    for gtype, name in Game.GAME_TYPES:
        count = sessions.filter(game__game_type=gtype).count()
        if count > 0:
            type_labels.append(name)
            type_data.append(count)
            
    # Daily activity (last 7 days)
    from django.utils import timezone
    import datetime
    daily_labels = []
    daily_data = []
    for i in range(6, -1, -1):
        day = timezone.now().date() - datetime.timedelta(days=i)
        daily_labels.append(day.strftime('%d.%m'))
        daily_data.append(sessions.filter(completed_at__date=day).count())

    return render(request, 'dashboard/full_stats.html', {
        'stats': stats,
        'recent_sessions': sessions[:15],
        'type_labels': json.dumps(type_labels),
        'type_data': json.dumps(type_data),
        'daily_labels': json.dumps(daily_labels),
        'daily_data': json.dumps(daily_data),
    })


@login_required
def student_list(request):
    return render(request, 'dashboard/student_list.html')


# ═══════════════════════════════════════════════════════
# STUDENT / PLAY
# ═══════════════════════════════════════════════════════

def play_entry(request, code):
    clean_code = code.replace('MP', '') if code.startswith('MP') else code
    try:
        game = Game.objects.get(Q(publish_code=code) | Q(pk=clean_code))
    except (Game.DoesNotExist, ValueError):
        return render(request, 'student/game_not_found.html', {**{'code': code}, 'hide_sidebar': True}, status=404)
    if not game.is_published:
        return render(request, 'student/game_not_found.html', {**{'code': code}, 'hide_sidebar': True}, status=404)
    return render(request, 'student/play_entry.html', {**{'game': game}, 'hide_sidebar': True})


@csrf_exempt
def play_game(request, code):
    game = get_object_or_404(Game, publish_code=code, is_published=True)
    student_name = request.GET.get('name', 'Оқушы')

    if request.method == 'POST':
        data = json.loads(request.body)
        session = GameSession.objects.create(
            game=game,
            student_name=student_name,
            score_percent=data.get('score_percent', 0),
            xp_earned=data.get('xp', 0),
            time_seconds=data.get('time_seconds', 0),
        )
        game.play_count += 1
        game.save()
        return JsonResponse({'status': 'ok', 'session_id': session.id})

    return render(request, f'games/{game.game_type}.html', {
        'game': game,
        'student_name': student_name,
        'hide_sidebar': True,
    })


def play_result(request, code, session_id):
    session = get_object_or_404(GameSession, id=session_id)
    return render(request, 'student/play_result.html', {**{
        'session': session,
        'hide_sidebar': True,
    }, 'hide_sidebar': True})
