import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from alumni.models import Student, News, Album, GalleryImage, Video, Donation
from alumni.utils import generate_donation_receipt_pdf

class Command(BaseCommand):
    help = 'Seed initial realistic data for Anwar Alumni Network website'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # 1. Create Superuser admin/admin123 if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@anwaralumni.org', 'admin123')
            self.stdout.write(self.style.SUCCESS("Superuser created: admin / admin123"))
        else:
            self.stdout.write("Superuser 'admin' already exists.")

        # 2. Seed Students
        sample_students = [
            {
                'serial_number': 'ANWAR-2024-001',
                'name': 'Muhammad Shafiq',
                'batch': '2020-2024',
                'phone_number': '+91 98471 23456',
                'address': 'Green Valley, Nilambur, Malappuram, Kerala - 679329',
            },
            {
                'serial_number': 'ANWAR-2024-002',
                'name': 'Abdul Rahman Al-Qasimi',
                'batch': '2020-2024',
                'phone_number': '+91 98472 34567',
                'address': 'Vidyanagar Road, Nilambur, Kerala - 679329',
            },
            {
                'serial_number': 'ANWAR-2023-015',
                'name': 'Usman Farooq',
                'batch': '2019-2023',
                'phone_number': '+91 98473 45678',
                'address': 'Town Hall Junction, Manjeri, Malappuram, Kerala',
            },
            {
                'serial_number': 'ANWAR-2022-008',
                'name': 'Bilal Ahmed Wafa',
                'batch': '2018-2022',
                'phone_number': '+91 98474 56789',
                'address': 'Al-Huda Villa, Calicut Road, Kozhikode, Kerala',
            },
            {
                'serial_number': 'ANWAR-2021-042',
                'name': 'Zaid ibn Thabit',
                'batch': '2017-2021',
                'phone_number': '+91 98475 67890',
                'address': 'Main Market, Wandoor, Malappuram, Kerala',
            },
        ]

        for st in sample_students:
            obj, created = Student.objects.get_or_create(
                serial_number=st['serial_number'],
                defaults={
                    'name': st['name'],
                    'batch': st['batch'],
                    'phone_number': st['phone_number'],
                    'address': st['address'],
                }
            )
            if created:
                self.stdout.write(f"Created student: {obj.serial_number} ({obj.name})")

        # 3. Seed News & Announcements
        news_items = [
            {
                'title': 'Annual Grand Alumni Meet 2026 Scheduled',
                'content': 'We are excited to announce the Annual Grand Alumni Gathering of Anwar Majmau Shariath & Dawa College at Vidyanagar Campus. All batch representatives and alumni members are cordially invited.',
            },
            {
                'title': 'New Digital Library Wing Inauguration',
                'content': 'The college management and alumni association have successfully inaugurated the modern Digital Library and Islamic Research Center. The facility houses thousands of manuscripts and digital journals.',
            },
            {
                'title': 'Scholarship Fund Drive Launched for 2026 Academic Year',
                'content': 'Anwar Alumni Network has officially launched the Student Support & Welfare Scholarship Drive to support deserving scholars in their higher studies.',
            },
        ]

        for n in news_items:
            news_obj, created = News.objects.get_or_create(
                title=n['title'],
                defaults={'content': n['content'], 'is_active': True}
            )

        # 4. Seed Gallery Albums & Images
        album, _ = Album.objects.get_or_create(
            title="Campus Programmes 2025-2026",
            defaults={'description': "Highlights of major conferences, convocations, and alumni events."}
        )

        # 5. Seed YouTube Videos
        videos = [
            {
                'title': 'Anwar Majmau Annual Convocation & Dawa Conference',
                'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'description': 'Keynote address by respected scholars at Vidyanagar campus auditorium.',
            },
            {
                'title': 'Alumni Meet Highlights & Cultural Evening',
                'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'description': 'Brotherhood gathering and interactive sessions with former graduates.',
            },
        ]

        for v in videos:
            Video.objects.get_or_create(
                title=v['title'],
                defaults={'youtube_url': v['youtube_url'], 'description': v['description']}
            )

        # 6. Seed Sample Donations with PDF Receipts
        sample_donations = [
            {
                'donor_name': 'Dr. Abdul Qadir',
                'batch': '2015-2019',
                'phone_number': '+91 98470 11223',
                'amount': 10000.00,
                'transaction_id': 'UTR9847123984',
            },
            {
                'donor_name': 'Muhammed Fayis',
                'batch': '2018-2022',
                'phone_number': '+91 98470 44556',
                'amount': 5000.00,
                'transaction_id': 'UPI2026080512',
            },
        ]

        for d in sample_donations:
            don_obj, created = Donation.objects.get_or_create(
                donor_name=d['donor_name'],
                batch=d['batch'],
                defaults={
                    'phone_number': d['phone_number'],
                    'amount': d['amount'],
                    'transaction_id': d['transaction_id'],
                    'receipt_status': 'Verified',
                }
            )
            if created:
                try:
                    generate_donation_receipt_pdf(don_obj)
                    self.stdout.write(f"Generated PDF receipt for donation {don_obj.receipt_number}")
                except Exception as e:
                    self.stdout.write(f"Notice generating PDF: {e}")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
