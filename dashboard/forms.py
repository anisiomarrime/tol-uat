from django import forms


class FormLogin(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password')

class FormPasswordRecover(forms.Form):
    password = forms.CharField(label='password', max_length=255, required=False)
    recover_password = forms.CharField(label='recover_password', max_length=255, required=False)

class FormRegister(forms.Form):
    name = forms.CharField(label='name', max_length=250)
    photo = forms.CharField(label="photo", required=False)
    province = forms.IntegerField(label='province')
    mobile = forms.CharField(label='mobile', max_length=9)
    mobile_alternative = forms.CharField(label='mobile_alternative', max_length=9, required=False)
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password', max_length=255, required=False)
    address = forms.CharField(label='address', max_length=255, required=False)


class FormPost(forms.Form):
    photo1 = forms.CharField(label="photo1", required=False)
    photo2 = forms.CharField(label="photo2", required=False)
    photo3 = forms.CharField(label="photo3", required=False)
    title = forms.CharField(label='title', max_length=250)
    category = forms.IntegerField(label='category')
    price = forms.DecimalField(label='price')
    description = forms.CharField(label='description')

