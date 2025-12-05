from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Match, Attendance
import random

def match_list(request):
    matches = Match.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'core/match_list.html', {'matches': matches})

def create_match(request):
    if not request.user.is_authenticated:
        return redirect('account_login')
        
    if request.method == 'POST':
        date = request.POST.get('date')
        location = request.POST.get('location')
        total_cost = request.POST.get('total_cost')
        organizer_info = request.POST.get('organizer_info')
        
        Match.objects.create(
            date=date,
            location=location,
            total_cost=total_cost,
            organizer_info=organizer_info,
            creator=request.user
        )
        return redirect('match_list')
    return render(request, 'core/create_match.html')

def match_detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    attendances = match.attendances.all()
    confirmed_count = attendances.filter(is_confirmed=True).count()
    
    cost_per_person = 0
    if confirmed_count > 0:
        cost_per_person = match.total_cost / confirmed_count

    is_creator = request.user == match.creator

    return render(request, 'core/match_detail.html', {
        'match': match,
        'attendances': attendances,
        'confirmed_count': confirmed_count,
        'cost_per_person': int(cost_per_person),
        'is_creator': is_creator,
    })

def toggle_attendance(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if request.user.is_authenticated and not name:
            attendance, created = Attendance.objects.get_or_create(
                match=match,
                user=request.user,
                defaults={'is_confirmed': True}
            )
            if not created:
                attendance.is_confirmed = not attendance.is_confirmed
                attendance.save()
        else:
            if name:
                Attendance.objects.create(
                    match=match,
                    name=name,
                    is_confirmed=True
                )
    return redirect('match_detail', match_id=match_id)

@login_required
def mark_paid(request, match_id, attendance_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.user != match.creator:
        return redirect('match_detail', match_id=match_id)
        
    attendance = get_object_or_404(Attendance, pk=attendance_id)
    attendance.has_paid = not attendance.has_paid
    attendance.save()
    return redirect('match_detail', match_id=match_id)

@login_required
def shuffle_teams(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.user != match.creator:
        return redirect('match_detail', match_id=match_id)

    confirmed = list(match.attendances.filter(is_confirmed=True))
    random.shuffle(confirmed)
    
    mid = len(confirmed) // 2
    white_team = confirmed[:mid]
    color_team = confirmed[mid:]
    
    for p in white_team:
        p.team = 'WHITE'
        p.save()
    
    for p in color_team:
        p.team = 'COLOR'
        p.save()
        
    return redirect('match_detail', match_id=match_id)

@login_required
def reset_teams(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.user != match.creator:
        return redirect('match_detail', match_id=match_id)
    
    # Quitar todos los equipos asignados
    for attendance in match.attendances.all():
        attendance.team = None
        attendance.save()
    
    return redirect('match_detail', match_id=match_id)

@login_required
def delete_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.user == match.creator:
        match.delete()
    return redirect('match_list')

@login_required
def remove_player(request, match_id, attendance_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.user != match.creator:
        return redirect('match_detail', match_id=match_id)
    
    attendance = get_object_or_404(Attendance, pk=attendance_id)
    if attendance.match == match:
        attendance.delete()
    
    return redirect('match_detail', match_id=match_id)
