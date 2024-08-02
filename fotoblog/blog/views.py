from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from . import form, models
#cette nouvelle importation permettra de créeer plusieurs formulaires
# de meme type (exple télécharger plusieurs photos simultanement) sur la meme page
from django.forms import formset_factory
from django.bd.models import Q



# Create your views here.
@login_required
def home(request):
    """cette vue permet l'affichache des photos et billets de blog existant dans la
    base de données"""
    blogs = models.Blog.objects.all()
    # nous voulons recupérer les blog donc les contributeurs font
    # parti des utilisateurs(créateurs) suivis par l'utilisateur qui s'est connecté
    #blogs = models.Blog.objects.filter(
      #  contributors__in=request.user.follow.all()

    # nous voulons recupérer les blog donc les contributeurs font
    # parti des utilisateurs(créateurs) suivis par l'utilisateur qui s'est connecté
    #ou dont l'attribut starred est True
    # blogs = models.Blog.objects.filter(
    #  Q(contributors__in=request.user.follow.all())  | Q(starred=True))


    #la clause order_by permet de trier la liste par ordrer chronologique des dates de
    #création inverse d'où le '-date_created' en argument du order_by
    photos = models.Photo.objects.all().order_by('-date_created')
    #nous allons chercher les photos dons le créateur fait parti de
    #des créateurs suivient par notre user
    #Ensuite, excluez les photos qui sont déjà liées à des instances deBlog
    ## blog__in=blogs)

    return render(request,'blog/home.html', context={'photos':photos, 'blogs':blogs})

@login_required
@permission_required('blog.add_photo', raise_exception=True)
def photo_upload(request):
    """cette vue permet de télécharger une photo"""
    forms = form.PhotoForms()
    if request.method== 'POST':
        #parce qu'il y a des fichiers à associer, on ajoute le paramètre request.FILES
        forms = form.PhotoForms(request.POST, request.FILES)
        if forms.is_valid:
            photo = forms.save(commit=False)
            #ajouter l'utilisateur comme uploader avant de sauvegarder le model
            photo.uploader = request.user
            # maintenant il est temps de sauvegarder
            photo.save()
            return redirect('home')
    return render(request, 'blog/photo_upload.html', {'form':forms})

@login_required
@permission_required(['blog.add_photo','blog.add_blog'])
def blog_and_photo_upload(request):
    """cette vue permet de renseigner un blog et de télécharger la photo
    de ce billet de blog (l'interet ici est de savoir deux formulaires liés sur la meme page"""
    blog_form = form.BlogForms()
    photo_form = form.PhotoForms()
    if request.method=='POST':
        blog_form = form.BlogForms(request.POST)
        photo_form = form.PhotoForms(request.POST, request.FILES)
        if all([blog_form.is_valid,photo_form.is_valid]):
            #création des instance de model de photo et de blog sans les
            # sauvegarder dans la base
            #données
            blog = blog_form.save(commit=False)
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog.photo = photo
            blog.author = request.user
            blog.save()
            #actuallement on sauvegarde les contributeurs
            #dans la relation many to many
            blog_form.save_m2m()
            #on ajoute l'utilisateur courant comme contributeur du blog
            #il sera l'ateur principal
            #attention l'ajout d'un elet du champ manytomany
            #se fait après la sauvegarde de l'objet en base données
            #doc après l'appel de la méthode save()
            blog.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
            return redirect('home')
    return render(request,'blog/create_blog_photo.html', {'photo_blog_form':photo_form,'blog_form':blog_form})

@login_required
def view_blog(request, blog_id):
    """cettte vue permet la visualisation d'un blog
    avec son identifiant blog_id"""
    blog = get_object_or_404(models.Blog, id=blog_id)
    contributors = blog.contributors.all()
    return render(request,'blog/view_blog.html',{'blog':blog, 'contributors':contributors})

@login_required
@permission_required('blog.change_blog')
def edit_blog(request, blog_id):
    """cette vue permet la modification et la suppression
    d'un blog donc l'intégration de plusieurs formulaire sur le meme page
    ici on doit gérer plusieurs formulaires séparés sur une seule page, en
    incluant un champ caché qui identifie le formulaire envoyé."""
    blog = get_object_or_404(models.Blog, id=blog_id)
    edit_form = form.BlogForm(instance=blog)
    delete_form = form.DeleteBlogForm()
    if request.method=='POST':
        if 'edit_blog' in request.POST:
            edit_form = form.BlogForms(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_blog' in request.POST:
            delete_form = form.DeleteBlogForm(request.POST)
            if delete_form.is_valid():
                blog.delete()
                return redirect('home')
    return render(request,'blog/edit_blog.html', {'edit_form':edit_form, 'delete_form':delete_form})


@login_required
@permission_required('blog.add_photo')
def create_multiple_photos(request):
    """cette vue permet le téléchargement  de plusieurs
    photos sur la meme page
    ici on utilise des ensembles de formulaires, dits formsets, pour
    créer plusieurs instances différentes du même formulaire sur une seule page"""
    PhotoSet = formset_factory(form.PhotoForms, extra=5)
    formset = PhotoSet()
    if request.method=='POST':
        formset = PhotoSet(request.POST, request.FILES)
        if formset.is_valid():
            for form_elt in formset:
                if form_elt.cleaned_data:
                    photo = form_elt.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
    return render(request,'blog/create_multiples_photos.html', {'formset':formset})

@login_required
def follow_users(request):
    follow_form = form.FollowUserForm(instance=request.user)
    if request.method=='POST':
        follow_form = form.FollowUserForm(request.POST, instance=request.user)
        if follow_form.is_valid:
            follow_form.save()
            return redirect('home')
    return render(request,'blog/follow_users.html', {'follow_form':follow_form})

