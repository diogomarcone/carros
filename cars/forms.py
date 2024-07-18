from django import forms
from cars.models import Brand, Car
from placafipy import PlacaFipy

tokens = ["07061d50757c4b529458c8c784ce97e6"]
placafipy = PlacaFipy(tokens)
    
class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('plate', 'photo', 'brand')

    def clean_plate(self):
        plate = self.cleaned_data.get('plate')           
            
        placa = plate
        informacoes_veiculo = placafipy.consulta(placa)
        print(informacoes_veiculo)

        if informacoes_veiculo:
            pass
        else:
            self.add_error('plate', 'Placa não encontrada')
    
        return plate
    
    # def clean_value(self):
    #     value = self.cleaned_data.get('value')
    #     if value < 20000:
    #         self.add_error('value', 'Valor mínimo do carro deve ser de R$20.000,00')
    #     return value
    
    # def clean_factory_year(self):
    #     factory_year = self.cleaned_data.get('factory_year')

    #     if factory_year < 1975:
    #         self.add_error('factory_year', 'Não é possível cadastar carros fabricados antes de 1975')
    #     return factory_year