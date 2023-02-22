from django import forms


class shopregforms(forms.Form):
    shopname=forms.CharField(max_length=30)
    address=forms.CharField(max_length=30)
    shopid=forms.IntegerField()
    email=forms.EmailField()
    phone=forms.IntegerField()
    pass1=forms.CharField(max_length=20)
    pass2=forms.CharField(max_length=20)

class productForms(forms.Form):
    productname=forms.CharField(max_length=30)
    price=forms.IntegerField()
    discription=forms.CharField(max_length=100)
    image=forms.FileField()

class shoplogforms(forms.Form):
    shopname=forms.CharField(max_length=30)
    pass1=forms.CharField(max_length=20)


class customercardF(forms.Form):
    cardname=forms.CharField(max_length=30)
    cardnumber=forms.IntegerField()
    carddate=forms.CharField(max_length=30)
    scode=forms.IntegerField()






