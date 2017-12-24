from django import forms

class NewCourseForm(forms.Form):
    topic = forms.CharField(label='Тема курсовика', max_length=600, widget=forms.Textarea)
    university = forms.CharField(label='Университет',max_length=40,required=False)
    teacher = forms.CharField(label='Преподаватель',max_length=40,required = False)
    min_price = forms.IntegerField(label='Минимальная предлагаемая цена')
    max_price =forms.IntegerField(label='Максимальная предлагаемая цена')
    
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user',None)
        super(NewCourseForm, self).__init__(*args,**kwargs)

    def is_valid(self):
        valid = super(NewCourseForm, self).is_valid()
        
        if not valid:
            return valid
        balance = self.user.profile.wallet.balance
        if balance < self.cleaned_data['max_price']:
            self.errors['Недостаточно средств']='Недостаточно средств'
            return False
        if self.cleaned_data['max_price'] < self.cleaned_data['min_price']:
            self.errors['Неверно указаны цены']='Неверно указаны цены'
            return False
        
