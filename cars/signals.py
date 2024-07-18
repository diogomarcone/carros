from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from cars.models import Car, CarInvetory
from django.db.models import Sum
from openai_api.client import get_car_ai_bio
from placafipy import PlacaFipy
import re

tokens = ["07061d50757c4b529458c8c784ce97e6"]
placafipy = PlacaFipy(tokens)

def car_invetory_update():
    cars_count = Car.objects.all().count()
    cars_value = Car.objects.aggregate(
        total_value = Sum('value')
    )['total_value']
    CarInvetory.objects.create(
        cars_count = cars_count,
        cars_value = cars_value
    )

@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):    

        placa = instance.plate
        informacoes_veiculo = placafipy.consulta(placa)

        instance.model = informacoes_veiculo['detalhes']['modelo']
        instance.factory_year = informacoes_veiculo['detalhes']['ano']
        instance.model_year = informacoes_veiculo['detalhes']['ano_modelo']
        valor = informacoes_veiculo['tabela_fipe']['valores'][0]['valor']

        valor_limpo = re.sub(r'[^0-9]', '', valor)
        if len(valor_limpo) > 2:
            valor_formatado = valor_limpo[:-2] + '.' + valor_limpo[-2:]
        else:
            valor_formatado = '0.' + valor_limpo.zfill(2)
            
        instance.value = float(valor_formatado)

        if not instance.bio:
            ai_bio = get_car_ai_bio(instance.model, instance.brand, instance.model_year)
            instance.bio = ai_bio

        
    

@receiver(post_save, sender=Car)
def car_post_save(sender, instance, **kwargs):
    car_invetory_update()


@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    car_invetory_update()