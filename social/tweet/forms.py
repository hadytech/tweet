from django import forms
from .models import Twit, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Rasm uchun forma
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profil Rasmi")
    profile_bio = forms.CharField(label="Vasf", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Vasfingiz...'}))
    telegram_link = forms.CharField(label="Telegram taxallus:", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usernameni kuchukcha(@)siz kiriting'}))
    x_link = forms.CharField(label="X(twitter) taxallus", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Twitter(X) username'}))
    website_link = forms.CharField(label="Veb-sahifa", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'https://'}))
    github_link = forms.CharField(label="Github taxallus", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Faqat username'}))


    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio', 'telegram_link', 'x_link', 'website_link', 'github_link')


class TwitForm(forms.ModelForm):
    body = forms.CharField(required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Shu yerga twitlang...",
                "class": "form-control",

            }
            ),
            label="",
        )
    class Meta:
        model = Twit
        exclude = ("user", "likes",)

class UserSignUp(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'E-manzil kiriting'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ismingizni kiriting'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sharifingizni kiriting'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserSignUp, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Taxallusingiz'
        self.fields['username'].label = 'Shaxsiy taxallus(oldin foydalanilmagan bo\'lishi kerak!)'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>To`ldirilishi shart. 150 yoki ozroq belgilardan foydalnish mumkin. Huruf, raqamlar va faqat shu belgilar: @/./+/-/_</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Sirli so`z'
        self.fields['password1'].label = 'Sirli so\'z esda qolarli bo\'lishi kerak'
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Sirli so`z - boshqa shaxsiy ma`lumotlaringiz bilan bir hil bo`lishi mumkin emas.</li><li>Sirli so`z kamida 8 ta belgidan iborat bo`lishi lozim.</li><li>Oddiy sirli so`zlar qabul qilinmaydi.</li><li>Sirli so`zda faqat raqamlardan foydalanib bo`lmag`ay</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Sirli so`zni qayta kiriting'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Tasdiqlash uchun boyagi sirli so`zni qayta yozing shu yerga.</small></span>'