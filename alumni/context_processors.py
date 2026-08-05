from alumni.models import Student, Donation, GalleryImage, Video

def site_stats(request):
    total_students = Student.objects.count()
    # Unique batches
    total_batches = Student.objects.values('batch').distinct().count()
    active_members = max(total_students, 250) # Representative count
    
    return {
        'STAT_TOTAL_ALUMNI': total_students,
        'STAT_TOTAL_BATCHES': total_batches if total_batches > 0 else 15,
        'STAT_ACTIVE_MEMBERS': active_members,
        'SITE_COLLEGE_NAME': "Anwar Majmau Shariath & Dawa College Alumni",
        'SITE_LOCATION': "Vidyanagar, Nilambur, Malappuram, Kerala",
        'SITE_PHONE': "+91 8606 140 996",
        'SITE_EMAIL': "anwarmajmau01@gmail.com",
    }
