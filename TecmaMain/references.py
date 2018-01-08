from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import arrow

#
# Modelos de referencia para los selectores
#



'''
    @receiver(post_save, sender=User)
    def create_estado(sender, instance, created, **kwargs):
        #Crear una instancia de estado por cada ciudad
        if created:
            Estados.objects.create(estado=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        Se extienden el metodo save para los dos modelos
        instance.perfil.save()
'''