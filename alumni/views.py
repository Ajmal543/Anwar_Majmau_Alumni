import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count

from .models import Student, News, Album, GalleryImage, Video, Donation, ContactMessage
from .forms import StudentSearchForm, DonationForm, ContactForm, StudentExcelImportForm
from .utils import generate_donation_receipt_pdf, export_students_to_excel, export_donations_to_excel, import_students_from_excel

def home_view(request):
    latest_news = News.objects.filter(is_active=True)[:3]
    gallery_preview = GalleryImage.objects.all()[:6]
    videos_preview = Video.objects.all()[:2]
    search_form = StudentSearchForm()
    
    total_students = Student.objects.count()
    total_batches = Student.objects.values('batch').distinct().count() or 15
    active_members = max(total_students, 250)
    
    context = {
        'latest_news': latest_news,
        'gallery_preview': gallery_preview,
        'videos_preview': videos_preview,
        'search_form': search_form,
        'total_students': total_students,
        'total_batches': total_batches,
        'active_members': active_members,
    }
    return render(request, 'alumni/home.html', context)

def about_view(request):
    return render(request, 'alumni/about.html')

def student_search_view(request):
    student = None
    searched = False
    query = request.GET.get('serial_number', '').strip()
    
    if query:
        searched = True
        student = Student.objects.filter(serial_number__iexact=query).first()
        
    form = StudentSearchForm(initial={'serial_number': query})
    
    context = {
        'form': form,
        'student': student,
        'searched': searched,
        'query': query,
    }
    return render(request, 'alumni/student_search.html', context)

def donate_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save()
            # Generate PDF Receipt
            try:
                generate_donation_receipt_pdf(donation)
            except Exception as e:
                print(f"Error generating PDF receipt: {e}")
                
            messages.success(request, f"Thank you, {donation.donor_name}! Your donation of ₹{donation.amount:,.2f} has been recorded successfully.")
            return redirect('donation_success', donation_id=donation.id)
    else:
        form = DonationForm()
        
    bank_details = {
        'account_name': 'Anwar Majmau Alumni Association',
        'account_number': '40996860614',
        'ifsc_code': 'SBIN0001234',
        'branch_name': 'Nilambur Main Branch',
        'upi_id': 'anwaralumni@upi',
    }
    
    context = {
        'form': form,
        'bank_details': bank_details,
    }
    return render(request, 'alumni/donate.html', context)

def donation_success_view(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    return render(request, 'alumni/donation_success.html', {'donation': donation})

def download_receipt_view(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    if not donation.receipt_file:
        generate_donation_receipt_pdf(donation)
        donation.refresh_from_db()
        
    response = FileResponse(donation.receipt_file.open(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{donation.receipt_number}.pdf"'
    return response

def gallery_view(request):
    albums = Album.objects.prefetch_related('images').all()
    all_images = GalleryImage.objects.all()
    videos = Video.objects.all()
    
    context = {
        'albums': albums,
        'all_images': all_images,
        'videos': videos,
    }
    return render(request, 'alumni/gallery.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Thank you! Your message has been sent successfully.'})
            messages.success(request, "Thank you! Your message has been submitted successfully.")
            return redirect('contact')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = ContactForm()
        
    return render(request, 'alumni/contact.html', {'form': form})

# Admin / Staff Utility Views
@staff_member_required
def export_students_view(request):
    excel_buffer = export_students_to_excel()
    response = HttpResponse(
        excel_buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Anwar_Alumni_Students.xlsx"'
    return response

@staff_member_required
def export_donations_view(request):
    excel_buffer = export_donations_to_excel()
    response = HttpResponse(
        excel_buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Anwar_Alumni_Donations.xlsx"'
    return response

@staff_member_required
def import_students_view(request):
    if request.method == 'POST':
        form = StudentExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            result = import_students_from_excel(request.FILES['excel_file'])
            if result['errors']:
                messages.warning(request, f"Imported with some notices: Created {result['created']} records, Updated {result['updated']}. Errors: {', '.join(result['errors'])}")
            else:
                messages.success(request, f"Successfully imported Excel data! Created: {result['created']}, Updated: {result['updated']} student records.")
            return redirect('admin:alumni_student_changelist')
    else:
        form = StudentExcelImportForm()
    return render(request, 'admin/import_students.html', {'form': form})

@staff_member_required
def custom_admin_dashboard_view(request):
    total_students = Student.objects.count()
    total_donations_count = Donation.objects.count()
    total_donation_amount = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0.00
    total_images = GalleryImage.objects.count()
    total_videos = Video.objects.count()
    
    latest_students = Student.objects.all()[:5]
    latest_donations = Donation.objects.all()[:5]
    
    context = {
        'total_students': total_students,
        'total_donations_count': total_donations_count,
        'total_donation_amount': total_donation_amount,
        'total_images': total_images,
        'total_videos': total_videos,
        'latest_students': latest_students,
        'latest_donations': latest_donations,
    }
    return render(request, 'admin/dashboard.html', context)
