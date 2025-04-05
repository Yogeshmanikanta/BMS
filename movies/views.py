from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Movie, Theater, Seat, Booking, Showtime

def movie_list(request):
    search_query = request.GET.get('search')
    movies = Movie.objects.filter(name__icontains=search_query) if search_query else Movie.objects.all()
    
    paginator = Paginator(movies, 6)  
    page_number = request.GET.get('page')
    page_movies = paginator.get_page(page_number)

    return render(request, 'movies/movie_list.html', {'movies': page_movies})

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})

@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)

    if theater.is_fully_booked:
        return render(request, "movies/seat_selection.html", {'theater': theater, 'error': "Theater is fully booked!"})

    seats = Seat.objects.filter(theater=theater)
    
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []

        if not selected_seats:
            return render(request, "movies/seat_selection.html", {'theater': theater, "seats": seats, 'error': "No seat selected"})

        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=int(seat_id), theater=theater)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue

            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater
                )
                seat.is_booked = True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)

        # Check if all seats are booked, update theater status
        theater.check_fully_booked()

        if error_seats:
            error_message = f"The following seats are already booked: {', '.join(error_seats)}"
            return render(request, 'movies/seat_selection.html', {'theater': theater, "seats": seats, 'error': error_message})
        
        return redirect('profile')

    return render(request, 'movies/seat_selection.html', {'theater': theater, "seats": seats})

def profile(request):
    bookings = Booking.objects.filter(user=request.user).select_related('theater', 'movie', 'seat')
    return render(request, 'movies/profile.html', {'bookings': bookings})

def showtime_list(request):
    showtimes = Showtime.objects.all()
    for showtime in showtimes:
        showtime.status = "Fully Booked" if showtime.is_fully_booked() else "Seats Available"
    
    return render(request, "showtimes.html", {"showtimes": showtimes})

def book_ticket(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    
    if showtime.is_fully_booked():
        return JsonResponse({"error": "No seats available"}, status=400)

    showtime.booked_seats += 1
    showtime.save()

    return JsonResponse({"success": "Ticket booked successfully"})