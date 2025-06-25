from django import forms
from .models import Cliente, Producto
from datetime import date

class ClienteCreateForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['id_cliente', 'ape_nom', 'fec_reg']
        labels = {
            'id_cliente': 'DNI',
            'ape_nom': 'Apellidos y Nombres',
            'fec_reg': 'Fecha de Registro'
        }
        widgets = {
            'fec_reg': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Seleccione una fecha'}),
            'ape_nom': forms.TextInput(attrs={'placeholder': 'Ingrese los apellidos y nombres'})            
        }
        error_messages = {
            'id_cliente': {
                'required': 'El DNI es obligatorio',
                'max_length': 'El DNI debe tener un máximo de 8 caracteres'
            },
            'ape_nom': {
                'required': 'Los apellidos y nombres son obligatorios'
            },
            'fec_reg': {
                'required': 'La fecha de registro es obligatoria'
            }
        }
    def clean_id_cliente(self):
        id_cliente = self.cleaned_data.get('id_cliente')
        if not id_cliente.isdigit() or len(id_cliente) != 8:
            raise forms.ValidationError("El DNI debe contener exactamente 8 dígitos numéricos.")
        elif Cliente.objects.filter(id_cliente=id_cliente).exists():
            raise forms.ValidationError( "DNI_DUPLICADO", "0001")
        return id_cliente
    def clean_ape_nom(self):
        ape_nom = self.cleaned_data.get('ape_nom')
        if len(ape_nom) < 5:
            raise forms.ValidationError("Los apellidos y nombres deben tener al menos 5 caracteres.")
        return ape_nom
    def clean_fec_reg(self):
        fec_reg = self.cleaned_data.get('fec_reg')
        if fec_reg is None:
            raise forms.ValidationError("La fecha de registro es obligatoria.")
        return fec_reg

class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['id_cliente', 'ape_nom', 'fec_reg']
        labels = {
            'id_cliente': 'DNI',
            'ape_nom': 'Apellidos y Nombres',
            'fec_reg': 'Fecha de Registro'
        }
        widgets = {
            
            'fec_reg': forms.DateInput(attrs={'type': 'date'}, format=f'%Y-%m-%d'),                      
            'ape_nom': forms.TextInput(attrs={'placeholder': 'Ingrese los apellidos y nombres'})
        }
        error_messages = {
            'id_cliente': {
                'required': 'El DNI es obligatorio',
                'max_length': 'El DNI debe tener un máximo de 8 caracteres'
            },
            'ape_nom': {
                'required': 'Los apellidos y nombres son obligatorios'
            },
            'fec_reg': {
                'required': 'La fecha de registro es obligatoria'
            }
        }



class ProductoCreateForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nom_prod', 'des_prod', 'precio', 'stock', 'activo', 'fec_vencim']
        labels = {
            'nom_prod': 'Nombre del Producto',
            'des_prod': 'Descripción del Producto',
            'precio': 'Precio',
            'stock': 'Stock',
            'activo': 'Activo',
            'fec_vencim': 'Fecha de Vencimiento'
        }
        widgets = {
            'fec_vencim': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Seleccione una fecha'}),
            'nom_prod': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del producto'}),
            'des_prod': forms.Textarea(attrs={'placeholder': 'Ingrese la descripción del producto', 'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}), 
        }
        error_messages = {
            'nom_prod': {
                'required': 'El nombre del producto es obligatorio',
                'max_length': 'El nombre del producto debe tener un máximo de 50 caracteres'
            },
            'des_prod': {
                'required': 'La descripción del producto es obligatoria',
                'max_length': 'La descripción del producto debe tener un máximo de 500 caracteres'
            },
            'precio': {
                'required': 'El precio es obligatorio'
            },
            'stock': {
                'required': 'El stock es obligatorio'
            },
            'fec_vencim': {
                'required': 'La fecha de vencimiento es obligatoria'
            }
        }