from django.core.management.base import BaseCommand
from movies.models import Category, Genre, Movie, MovieLink
from accounts.models import User


class Command(BaseCommand):
    help = 'افزودن فیلم‌های نمونه به دیتابیس'

    def handle(self, *args, **kwargs):
        self.stdout.write('در حال ایجاد داده‌های نمونه...')

        # Create categories
        categories_data = [
            {'name': 'اکشن', 'slug': 'action', 'icon': 'bolt', 'description': 'فیلم‌های اکشن و هیجانی'},
            {'name': 'کمدی', 'slug': 'comedy', 'icon': 'laugh', 'description': 'فیلم‌های کمدی و سرگرم‌کننده'},
            {'name': 'درام', 'slug': 'drama', 'icon': 'theater-masks', 'description': 'فیلم‌های درام و احساسی'},
            {'name': 'ترسناک', 'slug': 'horror', 'icon': 'ghost', 'description': 'فیلم‌های ترسناک و وحشت'},
            {'name': 'علمی تخیلی', 'slug': 'sci-fi', 'icon': 'rocket', 'description': 'فیلم‌های علمی تخیلی'},
            {'name': 'انیمیشن', 'slug': 'animation', 'icon': 'magic', 'description': 'انیمیشن‌های جذاب'},
            {'name': 'مستند', 'slug': 'documentary', 'icon': 'video', 'description': 'فیلم‌های مستند'},
            {'name': 'عاشقانه', 'slug': 'romance', 'icon': 'heart', 'description': 'فیلم‌های عاشقانه'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, _ = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = cat

        self.stdout.write(f'  {len(categories)} دسته‌بندی ایجاد/بروزرسانی شد')

        # Get existing genres by name to avoid duplicates
        genres = {}
        genre_names = ['اکشن', 'ماجراجویی', 'کمدی', 'درام', 'ترسناک', 'علمی تخیلی', 'هیجانی', 'جنایی', 'خانوادگی', 'تاریخی']
        for name in genre_names:
            genre = Genre.objects.filter(name=name).first()
            if genre:
                genres[name] = genre

        self.stdout.write(f'  {len(genres)} ژانر یافت شد')

        # Get admin user
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

        # Create movies
        movies_data = [
            {
                'title': 'اینسرشن',
                'slug': 'inception',
                'description': 'دوم کاب یک دزد حرفه‌ای است که در دنیای رؤیاها تخصص دارد. او توانایی نفوذ به رؤیاهای دیگران و دزدیدن اسرار آنها را دارد. اما آخرین ماموریت او کاری غیرممکن است: به جای دزدیدن یک ایده، باید یک ایده را در ذهن کسی کاشته کند.',
                'short_description': 'دوم کاب یک دزد حرفه‌ای است که در دنیای رؤیاها تخصص دارد.',
                'category': categories['sci-fi'],
                'genres': ['علمی تخیلی', 'اکشن', 'ماجراجویی'],
                'release_date': '2010-07-16',
                'duration': 148,
                'director': 'کریستوفر نولان',
                'actors': 'لئوناردو دی‌کاپریو، توم هاردی، الیوت پیج',
                'language': 'انگلیسی (دوبله فارسی)',
                'country': 'آمریکا',
                'quality': '1080p',
                'imdb_rating': 8.8,
                'is_featured': True,
            },
            {
                'title': 'پدرخوانده',
                'slug': 'godfather',
                'description': 'داستان خانواده کورلئونه، یکی از قدرتمندترین خانواده‌های مافیایی آمریکا.',
                'short_description': 'داستان خانواده کورلئونه و مایکل که به رهبر مافیا تبدیل می‌شود.',
                'category': categories['drama'],
                'genres': ['درام', 'جنایی', 'تاریخی'],
                'release_date': '1972-03-15',
                'duration': 175,
                'director': 'فرانسیس فورد کوپولا',
                'actors': 'مارلون براندو، آل پاچینو، جیمز کان',
                'language': 'انگلیسی (دوبله فارسی)',
                'country': 'آمریکا',
                'quality': '1080p',
                'imdb_rating': 9.2,
                'is_featured': True,
            },
            {
                'title': 'شیرشاه',
                'slug': 'lion-king',
                'description': 'سیمبا، شیر کوچکی است که پدرش موفاسا را از دست می‌دهد و باید تاج و تخت خود را پس بگیرد.',
                'short_description': 'سیمبا شیر کوچکی است که باید تاج و تخت خود را پس بگیرد.',
                'category': categories['animation'],
                'genres': ['خانوادگی', 'ماجراجویی', 'درام'],
                'release_date': '2019-07-19',
                'duration': 118,
                'director': 'جان فاورو',
                'actors': 'دونالد گلاور، بیانسه، جیمز ارل جونز',
                'language': 'انگلیسی (دوبله فارسی)',
                'country': 'آمریکا',
                'quality': '1080p',
                'imdb_rating': 6.8,
                'is_featured': False,
            },
            {
                'title': 'جوکر',
                'slug': 'joker',
                'description': 'آرتور فلک، یک کمدین شکست خورده در شهر گاتهام، به یک جنایتکار ترسناک تبدیل می‌شود.',
                'short_description': 'آرتور فلک پس از تحمل بی‌توجهی به یک جنایتکار تبدیل می‌شود.',
                'category': categories['drama'],
                'genres': ['درام', 'جنایی', 'هیجانی'],
                'release_date': '2019-10-04',
                'duration': 122,
                'director': 'تاد فیلیپس',
                'actors': 'واکین فینیکس، رابرت دنیرو',
                'language': 'انگلیسی (دوبله فارسی)',
                'country': 'آمریکا',
                'quality': '1080p',
                'imdb_rating': 8.4,
                'is_featured': True,
            },
            {
                'title': 'انتقام‌جویان: پایان بازی',
                'slug': 'avengers-endgame',
                'description': 'پس از نابودی نیمی از جهان توسط تانوس، انتقام‌جویان باید جهان را نجات دهند.',
                'short_description': 'انتقام‌جویان باید از طریق سفر در زمان جهان را نجات دهند.',
                'category': categories['action'],
                'genres': ['اکشن', 'ماجراجویی', 'علمی تخیلی'],
                'release_date': '2019-04-26',
                'duration': 181,
                'director': 'برادران روسو',
                'actors': 'رابرت داونی جونیور، کریس ایوانز',
                'language': 'انگلیسی (دوبله فارسی)',
                'country': 'آمریکا',
                'quality': '1080p',
                'imdb_rating': 8.4,
                'is_featured': True,
            },
            {
                'title': 'تلقین',
                'slug': 'interstellar',
                'description': 'زمین در حال نابودی است و فضانوردان باید سیاره جدیدی پیدا کنند.',
                'short_description': 'گروهی از فضانوردان برای نجات بشریت به فضا سفر می‌کنند.',
                'category': categories['sci-fi'],
                'genres': ['علمی تخیلی', 'ماجراجویی', 'درام'],
                'release_date': '2014-11-07',
                'duration': 169,
                'director': 'کریستوفر نولان',
                'actors': 'متیو مک‌کانهی، آن هاتاوی',
                'language': 'انگلیسی (دوبله فارسی)',
                'country': 'آمریکا',
                'quality': '1080p',
                'imdb_rating': 8.6,
                'is_featured': False,
            },
        ]

        for movie_data in movies_data:
            genre_names = movie_data.pop('genres')
            movie, created = Movie.objects.update_or_create(
                slug=movie_data['slug'],
                defaults={**movie_data, 'created_by': admin_user, 'status': 'published'}
            )
            if created:
                self.stdout.write(f'  فیلم {movie.title} ایجاد شد')
            else:
                self.stdout.write(f'  فیلم {movie.title} بروزرسانی شد')

            # Set genres
            movie_genres = Genre.objects.filter(name__in=genre_names)
            movie.genres.set(movie_genres)

            # Create download links if not exists
            if not movie.links.exists():
                MovieLink.objects.create(
                    movie=movie,
                    quality='1080p',
                    link_type='direct',
                    url='https://example.com/download',
                    file_size='2.5GB',
                    subtitle=True,
                    language='فارسی (دوبله)',
                )
                MovieLink.objects.create(
                    movie=movie,
                    quality='720p',
                    link_type='direct',
                    url='https://example.com/download',
                    file_size='1.2GB',
                    subtitle=True,
                    language='فارسی (دوبله)',
                )

        self.stdout.write(self.style.SUCCESS('داده‌های نمونه با موفقیت ایجاد شد!'))
