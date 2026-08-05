import re
import uuid
from django.db import models
from django.utils.text import slugify

class Student(models.Model):
    serial_number = models.CharField(max_length=50, unique=True, db_index=True, help_text="Unique Serial Number (e.g. ANWAR001)")
    name = models.CharField(max_length=150)
    batch = models.CharField(max_length=50, help_text="e.g. 2018-2021 or Batch 12")
    photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.serial_number} - {self.name}"

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "News & Announcements"
        ordering = ['-date_posted']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Album(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/albums/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    album = models.ForeignKey(Album, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='gallery/photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title or f"Photo {self.id}"

class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField(help_text="Paste YouTube video link (e.g. https://www.youtube.com/watch?v=...)")
    youtube_id = models.CharField(max_length=50, blank=True, help_text="Extracted automatically from YouTube URL")
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        if self.youtube_url:
            match = re.search(r'(?:v=|\/embed\/|\/youtu\.be\/|\/v\/|\/e\/|watch\?v=|\&v=)([^#\&\?]*)*', self.youtube_url)
            if match:
                self.youtube_id = match.group(1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Donation(models.Model):
    receipt_number = models.CharField(max_length=50, unique=True, editable=False)
    donor_name = models.CharField(max_length=150, verbose_name="Full Name")
    batch = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Transaction ID / UTR")
    payment_screenshot = models.ImageField(upload_to='donations/screenshots/', blank=True, null=True)
    receipt_file = models.FileField(upload_to='donations/receipts/', blank=True, null=True)
    receipt_status = models.CharField(max_length=20, default='Generated', choices=[
        ('Generated', 'Generated'),
        ('Verified', 'Verified'),
        ('Pending', 'Pending'),
    ])
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"ANW-REC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receipt_number} - {self.donor_name} (₹{self.amount})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
