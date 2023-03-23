def check_password(form):
        password = form.cleaned_data.get('password')
        confirm_password = form.cleaned_data.get('confirm_password')
        if password != confirm_password:
            # (À définir) Choisir la forme d'erreur entre ces deux options : 
            form.add_error('confirm_password', 'La confirmation du mot de passe n\'est pas correcte')
            # - raise forms.ValidationError('La confirmation du mot de passe n\'est pas correcte')
            pass