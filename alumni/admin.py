from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect
from .models import Student, News, Album, GalleryImage, Video, Donation, ContactMessage
from .utils import export_students_to_excel, export_donations_to_excel

# Customize Admin Site Branding
admin.site.site_header = "Anwar Alumni Network Admin"
admin.site.site_title = "Anwar Alumni Portal"
admin.site.index_title = "Alumni Management Dashboard"

@admin.action(description="Export Selected Students to Excel")
def export_selected_students(modeladmin, request, queryset):
    return redirect('export_students')

@admin.action(description="Export Selected Donations to Excel")
def export_selected_donations(modeladmin, request, queryset):
    return redirect('export_donations')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name', 'batch', 'phone_number', 'photo_preview', 'created_at')
    list_filter = ('batch', 'created_at')
    search_fields = ('serial_number', 'name', 'batch', 'phone_number', 'address')
    ordering = ('-created_at',)
    actions = [export_selected_students]
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 2px solid #064E3B;" />', obj.photo.url)
        return format_html('<span style="color: #94A3B8; font-style: italic;">No Photo</span>')
    photo_preview.short_description = "Photo"

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'donor_name', 'batch', 'phone_number', 'formatted_amount', 'transaction_id', 'receipt_status', 'date', 'receipt_download_link')
    list_filter = ('receipt_status', 'batch', 'date')
    search_fields = ('receipt_number', 'donor_name', 'batch', 'phone_number', 'transaction_id')
    ordering = ('-date',)
    actions = [export_selected_donations]
    
    def formatted_amount(self, obj):
        return format_html('<strong style="color: #064E3B;">₹ {:,.2f}</strong>', obj.amount)
    formatted_amount.short_description = "Amount"

    def receipt_download_link(self, obj):
        url = reverse('download_receipt', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank" style="background-color: #064E3B; color: #fff; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">📄 PDF Receipt</a>', url)
    receipt_download_link.short_description = "Receipt"

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'date_posted')
    list_filter = ('is_active', 'date_posted')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 2

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'image_count')
    inlines = [GalleryImageInline]
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = "Total Photos"

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'photo_thumbnail', 'uploaded_at')
    list_filter = ('album', 'uploaded_at')
    search_fields = ('title',)
    
    def photo_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    photo_thumbnail.short_description = "Preview"

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_id', 'youtube_url', 'uploaded_at')
    search_fields = ('title', 'description', 'youtube_url')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('submitted_at',)
