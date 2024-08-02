from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.
class User(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'
    ROLE_CHOICES = ((CREATOR,'CREATEUR'),
                    (SUBSCRIBER,'ABONNÉ'),
                    )
    account_number = models.CharField(max_length=10)
    profile_photo = models.ImageField(verbose_name='photo de profile')
    role = models.CharField(max_length=30,choices= ROLE_CHOICES, verbose_name='role')
    #un utilisateur peut suivre plusiers utilisateurs (un abonné peut suivre plusieurs créateurs et aussi
    #un créateur peut etre suivi par plusieurs abonnés
    # ceci se matérialise par une relation many-to-many
    follow = models.ManyToManyField(
        'self',
        limit_choices_to = {'role':CREATOR}, #on limite le choix des utilisateurs
        # suivis aux créateurs: rien que les CREATORS sont suivis (variable optionnelle)
        symmetrical = False, # plus que nous sommes dans un cas où nous avons les memes entités,
        #on doit préciser cette variable pour empècher la réciprocité
        verbose_name = 'suit'#(ce qui s'affichera')
    )

#nous surchargeons la méthode save afin de pouvoir
# attribuer un groupe à chaque utilisateur avant la sauvegarde
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == self.CREATOR:
            group = Group.objects.get(name='creators')
            group.user_set.add(self)
        elif self.role == self.SUBSCRIBER:
            group = Group.objects.get(name='subscribers')
            group.user_set.add(self)



