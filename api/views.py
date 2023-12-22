from django.views.generic import View
from django.http import JsonResponse, HttpResponseServerError, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from public.models import PublicEntry, Author, Song, Tuning, Capo, Strumming, Comment
from private.models import PrivateEntry

from django.shortcuts import get_object_or_404
import json


class SaveEntryView(LoginRequiredMixin, UserPassesTestMixin, View):
    """View for save entry endpoint"""
    def post(self, request):
        type = request.GET.get('type')
        pk = request.GET.get('id')
        if type == 'private':
            entry = get_object_or_404(PrivateEntry, pk=pk)
            entry.is_saved = True
            entry.save()
            return HttpResponse(status=200)
        
        if type == 'public':
            entry = get_object_or_404(PublicEntry, pk=pk)
            entry.user_set.add(request.user)
            return HttpResponse(status=200)
        
        return HttpResponseServerError()
    
    
    def delete(self, request):
        type = request.GET.get('type')
        pk = request.GET.get('id')
        if type == 'private':
            entry = get_object_or_404(PrivateEntry, pk=pk)
            entry.is_saved = False
            entry.save()
            return HttpResponse(status=200)
        
        if type == 'public':
            entry = get_object_or_404(PublicEntry, pk=pk)
            entry.user_set.remove(request.user)
            return HttpResponse(status=200)
        
        return HttpResponseServerError()
    
    def test_func(self):
        if self.request.GET.get('type') == 'private':
            return PrivateEntry.objects.get(pk=self.request.GET.get('id')).added_by == self.request.user
        
        return True


class AuthorsAutocompleteView(View):
    """View for authors autocomplete by term"""
    def get(self, request):
        term = request.GET.get('term')
        if term:
            authors = Author.objects.filter(name__icontains=term).values_list('name', flat=True)
            return JsonResponse(list(authors), safe=False)
        else:
            return JsonResponse([], safe=False)


class SongsAutocompleteView(View):
    """View for songs autocomplete by term"""
    def get(self, request):
        term = request.GET.get('term')
        if term:
            songs = Song.objects.filter(title__icontains=term).values_list('title', flat=True)
            return JsonResponse(list(songs), safe=False)
        else:
            return JsonResponse([], safe=False)
        
class TuningsAutocompleteView(View):
    """View for tunings autocomplete by term"""
    def get(self, request):
        term = request.GET.get('term')
        if term:
            tunings = Tuning.objects.filter(title__icontains=term).values_list('title', flat=True)
            return JsonResponse(list(tunings), safe=False)
        else:
            return JsonResponse([], safe=False)


class CaposAutocompleteView(View):
    """View for capos autocomplete by term"""
    def get(self, request):
        term = request.GET.get('term')
        if term:
            capos = Capo.objects.filter(title__icontains=term).values_list('title', flat=True)
            return JsonResponse(list(capos), safe=False)
        else:
            return JsonResponse([], safe=False)

class StrummingsAutocompleteView(View):
    """View for strummings autocomplete by term"""
    def get(self, request):
        term = request.GET.get('term')
        if term:
            strummings = Strumming.objects.filter(title__icontains=term).values_list('title', flat=True)
            return JsonResponse(list(strummings), safe=False)
        else:
            return JsonResponse([], safe=False)
        

class CheckDbView(View):
    """View for endpoint which checks author, song, tuning, capo, strumming in database and returns string with text describing the consequent warnings"""
    def get(self, request):
        author = request.GET.get('author')
        song = request.GET.get('song')
        tuning = request.GET.get('tuning')
        capo = request.GET.get('capo')
        strumming = request.GET.get('strumming')

        author = Author.objects.filter(name=author).exists() if author else True
        song =  Song.objects.filter(title=song, author=Author.objects.get(name=request.GET.get('author'))).exists() \
              if song and author and request.GET.get('author') else False
        tuning = Tuning.objects.filter(title=tuning).exists() if tuning else True
        capo = Capo.objects.filter(title=capo).exists() if capo else True
        strumming = Strumming.objects.filter(title=strumming).exists() if strumming else True

        if all([author, song, tuning, capo, strumming]):
            return JsonResponse({'msg': ''}, safe=False)
        
        result = "Warning:\n"

        if not author:
            result += "Chosen author is not in the database.\n"
        if not song:
            result += "Chosen song is not in the database\n"
        if not tuning:
            result += "Chosen tuning is not in the database\n"
        if not capo:
            result += "Chosen capo is not in the database\n"
        if not strumming:
            result += "Chosen strumming is not in the database\n"
        
        result += "Don't worry, if you choose to publish, if the moderators see that the song or another field is actually present under different name, the name will be changed, if the song is not present, it will be added to the library."
        return JsonResponse({'msg': result}, safe=False)
    

class AddCommentView(LoginRequiredMixin, View):
    """View for add comment endpoint"""
    def post(self, request):
        pk = request.GET.get('id')
        body = json.loads(request.body.decode('utf-8'))['body']
        print(pk, body)
        if not pk or not body:
            return HttpResponseServerError()

        entry = get_object_or_404(PublicEntry, pk=pk)

        comment = Comment.objects.create(entry=entry, body=body, added_by=request.user)

        return JsonResponse({
            'user': comment.added_by.username,
            'pfp': comment.added_by.pfp.__str__(),
            'body': comment.body,
            'added_date': comment.added_date.strftime("%d.%m.%y %H:%M")
        })
