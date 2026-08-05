from django import forms
from .models import Donation, Student, ContactMessage, News, Album, GalleryImage, Video

class StudentSearchForm(forms.Form):
    serial_number = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-center font-monospace shadow-sm',
            'placeholder': 'Enter Serial Number (e.g. ANWAR001)',
            'autocomplete': 'off',
            'id': 'studentSearchInput'
        })
    )

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor_name', 'batch', 'phone_number', 'amount', 'transaction_id', 'payment_screenshot']
        widgets = {
            'donor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name', 'required': 'required'}),
            'batch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2018-2021 or Batch 12', 'required': 'required'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210', 'required': 'required'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount in ₹', 'min': '1', 'required': 'required'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UTR Number / UTR / Reference ID (Optional)'}),
            'payment_screenshot': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject', 'required': 'required'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Type your message here...', 'required': 'required'}),
        }

class StudentExcelImportForm(forms.Form):
    excel_file = forms.FileField(
        label="Upload Excel File (.xlsx)",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['serial_number', 'name', 'batch', 'photo', 'address', 'phone_number']
        widgets = {
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
