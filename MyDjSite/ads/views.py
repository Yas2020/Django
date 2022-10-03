from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from .models import Ad, Comment, Fav
from .forms import CreateForm, CommentForm
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q

# Create your views here.
class AdListView(OwnerListView):
    model = Ad
    template_name = "ads/ad_list.html"
    def get(self, request) :
        favorites = []
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        
        # take care of search part -  a get request
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Ad.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval) 
            query.add(Q(text__icontains=strval), Q.OR)
            ad_list = Ad.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else :
            ad_list = Ad.objects.all()
            # ad_list = Ad.objects.all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in ad_list:
            obj.natural_updated = naturaltime(obj.updated_at)
        
        ctx = {'ad_list' : ad_list, 'favorites': favorites, 'search': strval}
        return render(request, self.template_name, ctx)


class AdDetailView(OwnerDetailView):
    template_name = "ads/ad_detail.html"
    def get(self, request, pk) :
        ad = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : ad, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)


class AdCreateView(LoginRequiredMixin, View):
    # Simply by including LoginRequiredMixin into my view, I'm telling django not to allow user into this view if they are not logged in. If they are not logged in, the code in get method below will not run and it will redirect user and come back when user is logged it.
    # model = Ad 
    # fields = ['title', 'price', 'text', 'tags', 'picture']
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()

        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        # Without this next line the tags won't be saved.
        form.save_m2m() 
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            # As nothing in post is not stored in data base yet, it is ok to send a 200 and render the same post page again for the user to retry.
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()

        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        # Without this next line the tags won't be saved.
        form.save_m2m()    
        # Always redirect to other page (a get page) after post is successful (data stored in database). Otherwise if the same post page in returned and user refershes it, a duplicated post request is sent, as a result a duplicate transaction would happen. This is not desired.
        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model = Ad
    # template_name = "ads/ad_confirm_delete.html"

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        # reverse looks up the full url for 'ads:ad_detail'.
        return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/
# how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK", pk)
        t = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK", pk)
        t = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()

    
def stream_file(request, pk):
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response

# We use rverse_lazy rather than reverse in the constructor attributes below because views.py is loaded by urls.py and in urls.py as_view() causes the constructor for the view class to run before urls.py has been completely loaded and urlpatterns has been processed.