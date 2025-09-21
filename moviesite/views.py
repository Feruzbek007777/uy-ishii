from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from .models import Genre, Movie, Profile
from .forms import MovieForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

class HomeView(ListView):
    template_name = "moviesite/main.html"
    context_object_name = "movies"
    extra_context = {
        "title": "Barcha maqolalar",
    }
    ordering = ['-created']

    def get_queryset(self):
        return Movie.objects.filter(published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["genres"] = Genre.objects.all()
        return context


def about(request: HttpRequest):
    context = {
        'title': 'about',
    }
    return render(request, 'moviesite/about.html', context)


class GenreView(HomeView):
    def get_queryset(self):
        queryset = Movie.objects.filter(published=True, category_id=self.kwargs.get("movie_id"))
        return queryset


class MovieDetailDetail(DetailView):
    model = Movie
    pk_url_kwarg = "movie_id"
    extra_context = {
        "genres": Genre.objects.all(),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        movie = context.get("news")
        context["title"] = movie.title
        return context



class MovieCreateView(PermissionRequiredMixin, CreateView) :
    model = Movie
    form_class = MovieForm
    template_name = 'moviesite/add_movie.html'
    permission_required = 'movie.add_movie'

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['title'] = 'Film qo\'shish'
        return context

    def form_valid(self, form) :
        response = super().form_valid(form)
        messages.success(self.request, "Maqola muvaffaqiyatli qo'shildi!")
        return response

#context data oldim va qanaqadir xatolik beryotgandi keyin form esimga tushdi ( ozi
# dokumentatsiyasida bor ekan form ga ham tekshirish kerak ekan osha yerdan response, from
# class oshalarni ovoldim ! )



@permission_required('movie.change_movie', raise_exception=True)
def update_movie(request: HttpRequest, movie_id: int):
    if request.user.is_staff:
        movie = get_object_or_404(Movie, pk=movie_id)

        if request.method == 'POST':
            form = MovieForm(request.POST, files=request.FILES, instance=movie)
            if form.is_valid():
                movie = form.save()
                messages.success(request, "Film muvaffaqiyatli yangilandi!")
                return redirect("by_movie", movie_id=movie.pk)
            else:
                messages.error(request, "Ma'lumotlar qo'shishda xatolik yuz berdi!.")
        else:
            form = MovieForm(instance=movie)

        context = {
            "form": form,
            "title": "Filmni yangilash"
        }
        return render(request, 'moviesite/update_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')


@permission_required('movie.delete_movie', raise_exception=True)
def delete_movie(request: HttpRequest, movie_id):
    if request.user.is_staff:
        movie = get_object_or_404(Movie, pk=movie_id)
        messages.warning(request, "Filmni o'chirmoqchimisiz?")
        if request.method == 'POST':
            movie.delete()
            messages.success(request, "Film muvaffaqiyatli o'chirildi!")
            return redirect("main")
        context = {
            'movie': movie,
            'title': "Filmni o'chirish"
        }
        return render(request, 'moviesite/delete_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')


class ProfileView(View):
    def get(self, request, username :str):
        user = get_object_or_404(User, username=username)
        context = {
            "user" : user,
            "title" : str(user.username).title() + " profili"
        }
        try :
            profile = Profile.objects.get(user=user)
            context["profile"] = profile
        except :
            pass
        return render(request, "profile.html", context)


@login_required
def logout_view(request: HttpRequest):
    logout(request)
    return redirect('main')
