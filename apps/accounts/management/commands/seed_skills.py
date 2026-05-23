"""
Management command to seed the Skill model with a comprehensive list.
Run: python manage.py seed_skills
"""
 
from django.core.management.base import BaseCommand
from apps.accounts.models import Skill
 
SKILLS = [
    # Tech & Digital
    ("Web Design", "🌐"), ("Web Development", "💻"), ("Frontend Development", "🖥️"),
    ("Backend Development", "⚙️"), ("Full Stack Development", "🔧"), ("Mobile App Development", "📱"),
    ("Android Development", "🤖"), ("iOS Development", "🍎"), ("React / Next.js", "⚛️"),
    ("Vue.js", "💚"), ("Django / Python", "🐍"), ("WordPress", "🔵"),
    ("UI/UX Design", "🎨"), ("Graphic Design", "✏️"), ("Logo Design", "🏷️"),
    ("Brand Identity", "💼"), ("Motion Graphics", "🎬"), ("Video Editing", "🎞️"),
    ("Photo Editing", "📷"), ("Photography", "📸"), ("Content Writing", "📝"),
    ("Copywriting", "🖊️"), ("SEO / Digital Marketing", "📈"), ("Social Media Management", "📲"),
    ("Data Analysis", "📊"), ("Excel / Spreadsheets", "📋"), ("PowerPoint Design", "📑"),
    ("Cybersecurity", "🔒"), ("Database Administration", "🗄️"), ("Cloud Computing", "☁️"),
    ("Machine Learning / AI", "🤖"), ("Blockchain / Web3", "🔗"), ("Game Development", "🎮"),
    ("3D Modelling / Animation", "🧊"), ("Audio Editing / Mixing", "🎵"), ("Podcast Production", "🎙️"),
    ("Voiceover / Narration", "🎤"), ("Music Production", ("🎹")),
 
    # Creative & Arts
    ("Drawing / Illustration", "🖌️"), ("Painting", "🎨"), ("Sculpting", "🗿"),
    ("Fashion Design", "👗"), ("Jewelry Making", "💍"), ("Craft / DIY", "✂️"),
    ("Interior Design", "🏠"), ("Floral Arrangement", "🌸"), ("Calligraphy", "✍️"),
    ("Comic / Cartoon Art", "💬"),
 
    # Beauty & Wellness
    ("Hairstyling", "💇"), ("Braiding / Weaving", "💈"), ("Barbing", "✂️"),
    ("Makeup Artistry", "💄"), ("Nail Art / Manicure", "💅"), ("Skincare / Facials", "🧴"),
    ("Lash Extensions", "👁️"), ("Eyebrow Shaping", "🤨"), ("Massage Therapy", "💆"),
    ("Personal Training / Fitness", "🏋️"), ("Yoga Instruction", "🧘"),
 
    # Fashion & Tailoring
    ("Tailoring / Sewing", "🪡"), ("Ankara Fashion", "🧵"), ("Embroidery", "🪢"),
    ("Shoe Making / Cobbling", "👟"), ("Leather Work", "🧳"),
 
    # Food & Catering
    ("Catering / Cooking", "🍽️"), ("Cake Baking & Decoration", "🎂"), ("Pastry Making", "🥐"),
    ("Cocktail / Bartending", "🍹"), ("Meal Prep / Delivery", "🥡"), ("Confectionery", "🍬"),
 
    # Education & Tutoring
    ("Mathematics Tutoring", "➕"), ("English Tutoring", "📖"), ("Science Tutoring", "🔬"),
    ("JAMB / WAEC Coaching", "📚"), ("French / Arabic Tutoring", "🗣️"),
    ("Music Lessons", "🎸"), ("Dance Instruction", "💃"), ("Chess Coaching", "♟️"),
    ("Public Speaking Coaching", "🎤"),
 
    # Events & Entertainment
    ("Event Planning", "🎉"), ("MC / Compere", "🎙️"), ("DJ Services", "🎧"),
    ("Live Band / Music Performance", "🎺"), ("Comedy / Entertainment", "😂"),
    ("Decoration / Styling", "🎊"), ("Ushering", "🤝"), ("Photography (Events)", "📸"),
    ("Videography", "🎥"),
 
    # Business & Admin
    ("Virtual Assistant", "🗂️"), ("Transcription", "⌨️"), ("Translation", "🌍"),
    ("Proofreading / Editing", "📝"), ("Research", "🔍"), ("Business Plan Writing", "📄"),
    ("Accounting / Bookkeeping", "💰"), ("Legal Research", "⚖️"), ("Customer Support", "📞"),
    ("Data Entry", "🖥️"),
 
    # Trades & Technical
    ("Electrical Work", "⚡"), ("Plumbing", "🔧"), ("Carpentry / Furniture", "🪑"),
    ("Welding / Fabrication", "🔩"), ("Painting / Decorating (House)", "🏠"),
    ("AC Repair / Installation", "❄️"), ("Phone / Laptop Repair", "📱"),
    ("Generator Repair", "⚙️"), ("Automobile Repair", "🚗"), ("Tiling / Masonry", "🧱"),
 
    # Transport & Logistics
    ("Dispatch / Delivery Riding", "🏍️"), ("Driving", "🚗"), ("Errand Running", "🏃"),
    ("Moving / Relocation Help", "📦"),
 
    # Agriculture & Environment
    ("Farming / Crop Production", "🌾"), ("Landscaping / Gardening", "🌿"),
    ("Poultry / Livestock Farming", "🐔"), ("Fish Farming", "🐟"),
]
 
 
class Command(BaseCommand):
    help = "Seed the database with a comprehensive list of skills"
 
    def handle(self, *args, **kwargs):
        created = 0
        for name, icon in SKILLS:
            _, was_created = Skill.objects.get_or_create(
                name=name,
                defaults={"icon": icon, "is_active": True},
            )
            if was_created:
                created += 1
 
        self.stdout.write(
            self.style.SUCCESS(f"Done! {created} new skills added ({Skill.objects.count()} total).")
        )