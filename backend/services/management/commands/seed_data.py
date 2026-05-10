"""Seed the database with initial DGD Consulting data (services, blog, partners).

Run:  python manage.py seed_data
"""
import shutil
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from django.utils.text import slugify
from django.utils.timezone import make_aware

from services.models import Service
from blog.models import Category, BlogPost
from partners.models import Partner


# ─── SERVICES ───────────────────────────────────────────────────────────────
SERVICES = [
    {
        'number': '01',
        'icon_svg': '<path d="M21 15a4 4 0 0 1-4 4H8l-5 3V6a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4v9z"/><circle cx="9" cy="11" r="1"/><circle cx="13" cy="11" r="1"/><circle cx="17" cy="11" r="1"/>',
        'order': 1,
        'title': {
            'uz': 'Geologik konsalting xizmatlari',
            'ru': 'Геологические консультационные услуги',
            'en': 'Geological consulting services',
            'tr': 'Jeolojik danışmanlık hizmetleri',
        },
        'description': {
            'uz': "Loyiha hayotiy davri bo'ylab strategik maslahat — kontseptual skrining va konsessiya tekshirishidan tortib data-room sharhlari va mustaqil texnik fikrgacha.",
            'ru': 'Стратегические консультации на всём жизненном цикле проекта — от концептуального скрининга и due diligence концессий до обзора data-room и независимого технического заключения.',
            'en': 'Strategic advisory across project lifecycle — from concept screening and concession due diligence to data-room reviews and independent technical opinion.',
            'tr': "Proje yaşam döngüsü boyunca stratejik danışmanlık — kavram taraması ve imtiyaz due diligence'tan veri-odası incelemelerine ve bağımsız teknik görüşe kadar.",
        },
    },
    {
        'number': '02',
        'icon_svg': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/>',
        'order': 2,
        'title': {
            'uz': 'Kompleks loyihalarni tayyorlash',
            'ru': 'Подготовка комплексных проектов',
            'en': 'Preparation of comprehensive projects',
            'tr': 'Kapsamlı proje hazırlama',
        },
        'description': {
            'uz': "Tadqiqot loyihalari uchun to'liq fayllar — geologik modellar, burg'ulash sxemalari, namuna olish protokollari, byudjetlar va muddatlar — ruxsat olish va investorlar uchun tayyor.",
            'ru': 'Полные файлы разведочных проектов — геологические модели, схемы бурения, протоколы опробования, бюджеты и сроки — упакованные для согласований и инвесторов.',
            'en': 'End-to-end exploration project files — geological models, drilling layouts, sampling protocols, budgets and timelines — packaged for permitting and investor review.',
            'tr': 'Uçtan uca araştırma proje dosyaları — jeolojik modeller, sondaj düzenleri, numune protokolleri, bütçeler ve zaman çizelgeleri — izin ve yatırımcı incelemesi için paketlenmiş.',
        },
    },
    {
        'number': '03',
        'icon_svg': '<path d="M12 2L4 7v10l8 5 8-5V7z"/><path d="M12 22V12M4 7l8 5 8-5"/>',
        'order': 3,
        'title': {
            'uz': 'Samarali geologik tadqiqot ishlari',
            'ru': 'Эффективные геологоразведочные работы',
            'en': 'Efficient geological exploration works',
            'tr': 'Verimli jeolojik araştırma çalışmaları',
        },
        'description': {
            'uz': "Trench ochish, xaritalash va burg'ulash dasturlarini dala bajarish va nazorat qilish — kashfiyot xarajati va tezroq qaror qabul qilish uchun optimallashtirilgan.",
            'ru': 'Полевое выполнение и контроль программ канав, картирования и бурения — оптимизация по стоимости открытия и ускорение точек принятия решений.',
            'en': 'Field execution and supervision of trenching, mapping, and drilling programs — optimized for cost-per-discovery and accelerated decision points.',
            'tr': 'Hendek, haritalama ve sondaj programlarının saha uygulaması ve denetimi — keşif başına maliyet ve hızlandırılmış karar noktaları için optimize edilmiş.',
        },
    },
    {
        'number': '04',
        'icon_svg': '<path d="M3 3v18h18"/><path d="M7 14l4-4 4 4 5-6"/>',
        'order': 4,
        'title': {
            'uz': 'MRE hisobot tayyorlash',
            'ru': 'Подготовка отчёта MRE',
            'en': 'MRE report preparation',
            'tr': 'MRE rapor hazırlama',
        },
        'description': {
            'uz': 'JORC / CIM standartlariga muvofiq tayyorlangan Mineral Resurs Baholash hisobotlari — blok modellashtirish, tasniflash, sezgirlik tahlili va kompetent shaxs imzosi.',
            'ru': 'Отчёты по оценке минеральных ресурсов по стандартам JORC / CIM — блочное моделирование, классификация, анализ чувствительности и подпись компетентного лица.',
            'en': 'Mineral Resource Estimation reports prepared to JORC / CIM standards — block modeling, classification, sensitivity analysis and competent-person sign-off.',
            'tr': 'JORC / CIM standartlarına göre hazırlanan Maden Kaynak Tahmini raporları — blok modelleme, sınıflandırma, hassasiyet analizi ve yetkili kişi imzası.',
        },
    },
    {
        'number': '05',
        'icon_svg': '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
        'order': 5,
        'title': {
            'uz': 'Maxsus geologik tadqiqot ishlari',
            'ru': 'Специальные геологические исследования',
            'en': 'Special geological research works',
            'tr': 'Özel jeolojik araştırma çalışmaları',
        },
        'description': {
            'uz': "Standart tadqiqotni to'ldiruvchi ixtisoslashgan tadqiqotlar — ko'p usulli dalillar orqali maqsadlarni aniqlashtirish va talqinlarni xavfsizlantirish.",
            'ru': 'Специализированные исследования, дополняющие стандартную разведку — уточнение целей и снижение рисков интерпретации через мульти-методические доказательства.',
            'en': 'Specialist studies that complement standard exploration — sharpening targets and de-risking interpretations through multi-method evidence.',
            'tr': 'Standart araştırmayı tamamlayan uzman çalışmalar — çoklu yöntemli kanıtlar yoluyla hedefleri keskinleştirme ve yorumların risklerini azaltma.',
        },
        'sub_services': [
            {
                'number': '5.1',
                'order': 1,
                'title': {'uz':'Geokimyoviy tadqiqot','ru':'Геохимические исследования','en':'Geochemical research','tr':'Jeokimyasal araştırma'},
                'description': {
                    'uz': "Tuproq, daryo cho'kindi va tosh-bo'lakli surveylar ICP-MS ko'p elementli talqini bilan.",
                    'ru': 'Опробование почв, донных отложений и сколов с многоэлементной интерпретацией ICP-MS.',
                    'en': 'Soil, stream-sediment & rock-chip surveys with multi-element ICP-MS interpretation.',
                    'tr': 'Toprak, dere sediman ve kaya parçası araştırmaları, çok elementli ICP-MS yorumlamasıyla.',
                },
            },
            {
                'number': '5.2',
                'order': 2,
                'title': {'uz':'Geofizik tadqiqot','ru':'Геофизические исследования','en':'Geophysical research','tr':'Jeofizik araştırma'},
                'description': {
                    'uz': 'Yer osti maqsadlash uchun magnit, IP/qarshilik va tortishish surveylari.',
                    'ru': 'Магнитная, ВП/сопротивление и гравиразведка для подповерхностного нацеливания.',
                    'en': 'Magnetic, IP/Resistivity, and gravity surveys for sub-surface targeting.',
                    'tr': 'Yer altı hedefleme için manyetik, IP/dirençölçüm ve gravite araştırmaları.',
                },
            },
            {
                'number': '5.3',
                'order': 3,
                'title': {'uz':'Maxsus strukturaviy tadqiqotlar','ru':'Специальные структурные исследования','en':'Special structural studies','tr':'Özel yapısal çalışmalar'},
                'description': {
                    'uz': 'Mineralizatsiya nazoratini cheklash uchun yoriq, burma va siljish zonalarini batafsil xaritalash.',
                    'ru': 'Детальное картирование разломов, складок и зон сдвига для контроля минерализации.',
                    'en': 'Detailed fault, fold and shear-zone mapping to constrain mineralization controls.',
                    'tr': 'Mineralleşme kontrollerini sınırlamak için ayrıntılı fay, kıvrım ve makaslama bölgesi haritalaması.',
                },
            },
            {
                'number': '5.4',
                'order': 4,
                'title': {'uz':"Sun'iy yo'ldosh tasvirini qayta ishlash",'ru':'Обработка спутниковых снимков','en':'Satellite image processing','tr':'Uydu görüntü işleme'},
                'description': {
                    'uz': "O'zgarishlarni xaritalash va lineamentlarni ajratib olish uchun multispektral va SAR tahlili.",
                    'ru': 'Мультиспектральный и SAR-анализ для картирования изменений и линеаментов.',
                    'en': 'Multispectral and SAR analysis for alteration mapping and lineament extraction.',
                    'tr': 'Bozunum haritalaması ve lineament çıkarımı için multispektral ve SAR analizi.',
                },
            },
            {
                'number': '5.5',
                'order': 5,
                'is_featured': True,
                'title': {'uz':'Yangi konlarni bashorat qilish — AI & ML','ru':'Прогноз новых месторождений — AI & ML','en':'Prediction of new deposits — AI & ML','tr':'Yeni yatak tahmini — AI & ML'},
                'description': {
                    'uz': "Ko'p manbali geologiya ma'lumotlarida o'rgatilgan Random-forest, CNN va gradient-boosting modellari istiqbolli maqsadlarni baholash uchun.",
                    'ru': 'Модели Random-forest, CNN и градиентного бустинга, обученные на мультисурс-данных, для ранжирования перспективных целей.',
                    'en': 'Random-forest, CNN and gradient-boosting models trained on multi-source geoscience data to rank prospective targets.',
                    'tr': 'Çok kaynaklı jeo-bilim verileri üzerinde eğitilmiş Random-forest, CNN ve gradient-boosting modelleri ile umut verici hedefleri sıralama.',
                },
            },
        ]
    },
    {
        'number': '06',
        'icon_svg': '<path d="M9 12l2 2 4-4"/><path d="M21 12c0 5-4 9-9 9s-9-4-9-9 4-9 9-9c2.4 0 4.6.95 6.2 2.5"/>',
        'order': 6,
        'title': {
            'uz': "QA/QC va CRM qo'llab-quvvatlash",
            'ru': 'QA/QC и поддержка CRM',
            'en': 'QA/QC & CRM support',
            'tr': 'QA/QC ve CRM desteği',
        },
        'description': {
            'uz': "Namuna olish, laboratoriya samaradorligi va CRM/blank/duplikat dasturlarining mustaqil nazorati — birinchi kundan boshlab auditga tayyor ma'lumotlar.",
            'ru': 'Независимый надзор за опробованием, лабораторной работой и программами вставок CRM/blank/duplicate — данные готовы к аудиту с первого дня.',
            'en': 'Independent oversight of sampling, lab performance and CRM/blank/duplicate insertion programs — keeping data audit-ready from day one.',
            'tr': "Numune alımı, laboratuvar performansı ve CRM/blank/duplicate yerleştirme programlarının bağımsız denetimi — ilk günden itibaren denetime hazır veriler.",
        },
    },
]


# ─── BLOG CATEGORIES ────────────────────────────────────────────────────────
CATEGORIES = [
    {
        'slug': 'method',
        'name': {'uz': 'Metod', 'ru': 'Метод', 'en': 'Method', 'tr': 'Yöntem'},
    },
    {
        'slug': 'ai-ml',
        'name': {'uz': 'AI / ML', 'ru': 'AI / ML', 'en': 'AI / ML', 'tr': 'AI / ML'},
    },
    {
        'slug': 'reporting',
        'name': {'uz': 'Hisobot', 'ru': 'Отчётность', 'en': 'Reporting', 'tr': 'Raporlama'},
    },
]


# ─── BLOG POSTS ─────────────────────────────────────────────────────────────
POSTS = [
    {
        'category_slug': 'method',
        'read_time': 7,
        'published_at': datetime(2026, 4, 15, 9, 0),
        'title': {
            'uz': "Outcrop'dan ruda tanasiga: zamonaviy maqsadlash ish jarayoni",
            'ru': 'От обнажения к рудному телу: современный воркфлоу нацеливания',
            'en': 'From outcrop to ore body: a modern targeting workflow',
            'tr': 'Mostradan cevher kütlesine: modern bir hedefleme iş akışı',
        },
        'excerpt': {
            'uz': "Geokimyo, strukturaviy xaritalash va gradient-boosted ML'ni qanday birlashtirib, oylab davom etadigan dala ishlarini aniq maqsad reytingiga qisqartiramiz.",
            'ru': 'Как мы объединяем геохимию, структурное картирование и градиентный бустинг, чтобы сжать месяцы полевой работы в защищаемое ранжирование целей.',
            'en': 'How we combine geochemistry, structural mapping and gradient-boosted ML to compress months of fieldwork into a defensible target ranking.',
            'tr': 'Jeokimya, yapısal haritalama ve gradient-boosted ML\'yi nasıl birleştirerek aylarca süren saha çalışmasını savunulabilir bir hedef sıralamasına sıkıştırıyoruz.',
        },
        'content': {
            'uz': '<p>Maqola matni bu yerda...</p><p>Admin paneli orqali kontentni to\'liq tahrirlay olasiz.</p>',
            'ru': '<p>Содержание статьи здесь...</p><p>Полное содержимое можно редактировать через админ-панель.</p>',
            'en': '<p>Article content goes here...</p><p>You can edit the full content via the admin panel.</p>',
            'tr': '<p>Makale içeriği burada...</p><p>İçeriği yönetim paneli üzerinden tam olarak düzenleyebilirsiniz.</p>',
        },
    },
    {
        'category_slug': 'ai-ml',
        'read_time': 5,
        'published_at': datetime(2026, 3, 10, 9, 0),
        'title': {
            'uz': 'Nima uchun keyingi geologingiz yarmi model, yarmi xarita',
            'ru': 'Почему ваш следующий геолог наполовину модель, наполовину карта',
            'en': 'Why your next geologist is half model, half map',
            'tr': 'Bir sonraki jeologunuz neden yarı model, yarı harita',
        },
        'excerpt': {
            'uz': "Mashinaviy o'qitish dala tajribasini almashtirmaydi — uni kuchaytiradi. Multispektral sun'iy yo'ldosh stacklarida CNN klassifikatorlarini joylashtirish.",
            'ru': 'Машинное обучение не заменяет полевую экспертизу — оно её усиливает. Практический взгляд на CNN-классификаторы по мультиспектральным спутниковым стекам.',
            'en': 'Machine learning is not replacing field expertise — it is amplifying it. A practical look at deploying CNN classifiers on multispectral satellite stacks.',
            'tr': 'Makine öğrenmesi saha uzmanlığının yerini almıyor — onu güçlendiriyor. Multispektral uydu yığınlarında CNN sınıflandırıcıları konuşlandırmaya pratik bir bakış.',
        },
        'content': {
            'uz': '<p>Maqola matni bu yerda...</p>',
            'ru': '<p>Содержание статьи здесь...</p>',
            'en': '<p>Article content goes here...</p>',
            'tr': '<p>Makale içeriği burada...</p>',
        },
    },
    {
        'category_slug': 'reporting',
        'read_time': 9,
        'published_at': datetime(2026, 2, 20, 9, 0),
        'title': {
            'uz': 'JORC-tayyor: investorlar haqiqatdan ishonadigan MRE hisobotlari',
            'ru': 'JORC-готовый: MRE-отчёты, которым доверяют инвесторы',
            'en': 'JORC-ready: building MRE reports investors actually trust',
            'tr': "JORC'a hazır: yatırımcıların gerçekten güvendiği MRE raporları oluşturma",
        },
        'excerpt': {
            'uz': "Texnik tekshiruvdan o'tadigan MRE hujjatlarini ishlab chiqarish uchun dalada sinovdan o'tgan tekshiruv ro'yxati — ma'lumotlarni tekshirishdan kompetent shaxs ko'rib chiqishigacha.",
            'ru': 'Полевой чек-лист подготовки документации MRE, выдерживающей техническую проверку — от валидации данных до проверки компетентным лицом.',
            'en': 'A field-tested checklist for producing MRE documentation that survives technical due diligence — from data validation to competent-person review.',
            'tr': 'Teknik incelemeden geçen MRE belgelerini üretmek için sahada test edilmiş bir kontrol listesi — veri doğrulamadan yetkili kişi incelemesine.',
        },
        'content': {
            'uz': '<p>Maqola matni bu yerda...</p>',
            'ru': '<p>Содержание статьи здесь...</p>',
            'en': '<p>Article content goes here...</p>',
            'tr': '<p>Makale içeriği burada...</p>',
        },
    },
]


# ─── PARTNERS ───────────────────────────────────────────────────────────────
PARTNERS = [
    {'name': 'Ocean Recycling & Mining & Chemistry', 'logo': 'ocean.png',        'order': 1},
    {'name': 'Türk Altın',                           'logo': 'turkaltin.png',    'order': 2},
    {'name': 'CAKA Mining',                          'logo': 'caka.png',         'order': 3},
    {'name': 'ALS Minerals',                         'logo': 'als-minerals.png', 'order': 4},
]


def _set_translations(obj, field, values):
    """Set <field>_uz / _ru / _en / _tr on a model instance."""
    for lang, value in values.items():
        setattr(obj, f'{field}_{lang}', value)


class Command(BaseCommand):
    help = 'Seed the database with initial DGD Consulting data'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Delete existing data first')

    def handle(self, *args, **opts):
        if opts['reset']:
            self.stdout.write(self.style.WARNING('Resetting all data...'))
            Service.objects.all().delete()
            BlogPost.objects.all().delete()
            Category.objects.all().delete()
            Partner.objects.all().delete()

        self._seed_services()
        self._seed_blog()
        self._seed_partners()
        self.stdout.write(self.style.SUCCESS('\n✓ All seed data created successfully!'))

    # ── Services ─────────────────────────────────────────────
    def _seed_services(self):
        self.stdout.write('\n→ Seeding services...')
        for data in SERVICES:
            svc, created = Service.objects.get_or_create(number=data['number'])
            svc.icon_svg   = data['icon_svg']
            svc.order      = data['order']
            svc.is_active  = True
            svc.is_featured = data.get('is_featured', False)
            _set_translations(svc, 'title',       data['title'])
            _set_translations(svc, 'description', data['description'])
            svc.save()
            self.stdout.write(f'  {"✓" if created else "↻"} {svc.number}  {svc.title_uz}')

            for sub_data in data.get('sub_services', []):
                sub, sub_created = Service.objects.get_or_create(
                    number=sub_data['number'], defaults={'parent': svc}
                )
                sub.parent     = svc
                sub.order      = sub_data['order']
                sub.is_active  = True
                sub.is_featured = sub_data.get('is_featured', False)
                _set_translations(sub, 'title',       sub_data['title'])
                _set_translations(sub, 'description', sub_data['description'])
                sub.save()
                self.stdout.write(f'    {"✓" if sub_created else "↻"} {sub.number}  {sub.title_uz}')

    # ── Blog ─────────────────────────────────────────────────
    def _seed_blog(self):
        self.stdout.write('\n→ Seeding blog categories & posts...')

        cats = {}
        for cd in CATEGORIES:
            cat, _ = Category.objects.get_or_create(slug=cd['slug'])
            _set_translations(cat, 'name', cd['name'])
            cat.save()
            cats[cd['slug']] = cat
            self.stdout.write(f'  ✓ category: {cat.name_uz}')

        for pd in POSTS:
            slug = slugify(pd['title']['en'])
            post, created = BlogPost.objects.get_or_create(slug=slug)
            post.category     = cats.get(pd['category_slug'])
            post.read_time    = pd['read_time']
            post.published_at = make_aware(pd['published_at']) if pd['published_at'].tzinfo is None else pd['published_at']
            post.is_published = True
            _set_translations(post, 'title',   pd['title'])
            _set_translations(post, 'excerpt', pd['excerpt'])
            _set_translations(post, 'content', pd['content'])
            post.save()
            self.stdout.write(f'  {"✓" if created else "↻"} post: {post.title_uz[:50]}...')

    # ── Partners ─────────────────────────────────────────────
    def _seed_partners(self):
        self.stdout.write('\n→ Seeding partners...')
        src_dir = Path(settings.BASE_DIR).parent / 'assets' / 'partners'
        media_partners = Path(settings.MEDIA_ROOT) / 'partners'
        media_partners.mkdir(parents=True, exist_ok=True)

        for pd in PARTNERS:
            partner, created = Partner.objects.get_or_create(name=pd['name'])
            partner.order     = pd['order']
            partner.is_active = True

            src = src_dir / pd['logo']
            if src.exists():
                dst = media_partners / pd['logo']
                shutil.copy(src, dst)
                partner.logo.name = f'partners/{pd["logo"]}'
                partner.save()
                self.stdout.write(f'  {"✓" if created else "↻"} {partner.name}  →  {pd["logo"]}')
            else:
                partner.save()
                self.stdout.write(self.style.WARNING(f'  ⚠ {partner.name}  (logo not found: {src})'))
