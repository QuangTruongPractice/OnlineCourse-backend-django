from django.core.management.base import BaseCommand
from courses.models import Category, Course, User, Role, Chapter, Lesson, CourseStatus
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import random

class Command(BaseCommand):
    help = 'Seeds the database with high quality course data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding high quality data...')
        
        # 1. Roles
        roles = ['Admin', 'Teacher', 'Student']
        role_objects = {}
        for role_name in roles:
            role, created = Role.objects.get_or_create(name=role_name)
            role_objects[role_name] = role

        # 2. Users (Ensure teacher1 exists)
        teacher, created = User.objects.get_or_create(
            username='teacher1',
            defaults={
                'email': 'teacher1@example.com',
                'first_name': 'Teacher',
                'last_name': 'One',
                'user_role': role_objects['Teacher'],
                'password': make_password('123456')
            }
        )

        # 3. Categories
        cat_design, _ = Category.objects.get_or_create(name='Design')
        cat_prog, _ = Category.objects.get_or_create(name='Programming')

        # 4. Cleanup old data
        self.stdout.write('Cleaning up old data...')
        Lesson.objects.all().delete()
        Chapter.objects.all().delete()
        Course.objects.all().delete()
        courses_data = [
            {
                "name": "COURSE 1 – DESIGN (UI/UX)",
                "category": cat_design,
                "thumbnail": "https://res.cloudinary.com/dabb0yavq/image/upload/v1770641722/thumbnail_design_vlhblb.jpg",
                "chapters": [
                    {"name": "Chapter 1 – UI/UX Basics", "video": "https://www.youtube.com/watch?v=BU_afT-aIn0"},
                    {"name": "Chapter 2 – Figma for Beginners", "video": "https://www.youtube.com/watch?v=1SNZRCVNizg"},
                    {"name": "Chapter 3 – UX Research & Design Thinking", "video": "https://www.youtube.com/watch?v=Ovj4hFxko7c"},
                ]
            },
            {
                "name": "COURSE 2 – DESIGN (GRAPHIC / PRODUCT DESIGN)",
                "category": cat_design,
                "thumbnail": "https://res.cloudinary.com/dabb0yavq/image/upload/v1770641750/thumbnail_programming_fyfvj1.avif",
                "chapters": [
                    {"name": "Chapter 1 – Graphic Design Fundamentals", "video": "https://www.youtube.com/watch?v=GQS7wPujL2k"},
                    {"name": "Chapter 2 – Typography & Color Theory", "video": "https://www.youtube.com/watch?v=Qj1FK8n7WgY"},
                    {"name": "Chapter 3 – Photoshop Basics", "video": "https://www.youtube.com/watch?v=IyR_uYsRdPs"},
                ]
            },
            {
                "name": "COURSE 3 – PROGRAMMING (PYTHON)",
                "category": cat_prog,
                "thumbnail": "https://res.cloudinary.com/dabb0yavq/image/upload/v1770641760/thumbnail_python_zuhn2z.webp",
                "chapters": [
                    {"name": "Chapter 1 – Python Full Course", "video": "https://www.youtube.com/watch?v=rfscVS0vtbw"},
                    {"name": "Chapter 2 – Python OOP", "video": "https://www.youtube.com/watch?v=Ej_02ICOIgs"},
                    {"name": "Chapter 3 – Python Projects", "video": "https://www.youtube.com/watch?v=8ext9G7xspg"},
                ]
            }
        ]

        # Optional: Delete old courses to replace them
        # Course.objects.all().delete() 

        for c_data in courses_data:
            course, created = Course.objects.update_or_create(
                name=c_data["name"],
                defaults={
                    "category": c_data["category"],
                    "lecturer": teacher,
                    "subject": c_data["category"].name,
                    "description": f"High quality course on {c_data['name']}",
                    "price": 500000,
                    "thumbnail_url": c_data["thumbnail"],
                    "image": c_data["thumbnail"],
                    "video_url": c_data["chapters"][0]["video"],  # Gắn link youtube minh họa
                    "level": Course.Level.TRUNG_CAP,
                    "duration": 180
                }
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} Course: {course.name}")

            # Clear existing chapters to avoid duplicates if re-running
            course.chapters.all().delete()

            for i, ch_data in enumerate(c_data["chapters"]):
                chapter = Chapter.objects.create(
                    course=course,
                    name=ch_data["name"],
                    description=f"Learn about {ch_data['name']}",
                    is_published=True
                )
                
                Lesson.objects.create(
                    chapter=chapter,
                    name=f"Lesson: {ch_data['name']}",
                    video_url=ch_data["video"],
                    duration=30,
                    is_published=True
                )
                self.stdout.write(f"  Added Chapter: {chapter.name}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded high quality database'))
