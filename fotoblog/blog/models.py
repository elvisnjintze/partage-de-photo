from django.db import models
from django.conf import settings
#nous importons la bibliothèque Image du PIL
#pour la manipulation des images
#ceci dans le but de redimenssionner nos images avant de les sauvegarder
from PIL import Image

# Create your models here.
class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    #creation d'une constante qui gardera la taille max
    #de l'image à partir de laquelle il faut redimenssionner
    IMAGE_MAX_SIZE =(600,600)
    def resize_image(self):
        """cette fonction permet de redimensionner
        l'image contenu dans le champ image"""
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # sauvegarde de l’image redimensionnée dans le système de fichiers
        # ce n’est pas la méthode save() du modèle !
        image.save(self.image.path)
    #on doit redimensionner chaque image avant la sauvegarde et
    #éviter d'appeler la méthode à chaque fois
    #ceci se fait en surchargeant la méthode save() du model
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
    #un blog peut avoir plusieurs contributeurs
    #et cette relation est matérialisée par la table
    #BlogContributor
    #contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BlogContributor')
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='BlogContributor', related_name='contributions')

class PhotoProfil(Photo):
    pass

class BlogContributor(models.Model):
    """ceci est une table qui représente la relation manytomany
    entre un blog et un utilisateur du genre un blog peut avoir
    plusieurs contributeurs qui sont des utilisateurs dons cette classe
     represente la relation entre la table blog et la table user en principe cette table
     est dejà crée par django; afin de personnaliser et augmenter d'autre champ,
     nous prennons le soi de definir nous meme une table à cette effet
    """
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    contribution = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('blog','contributor')