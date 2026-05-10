"""Seed the database with initial DGD Consulting data (services, blog, partners).

Run:  python manage.py seed_data
      python manage.py seed_data --reset
"""
import shutil
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from django.utils.timezone import make_aware

from services.models import Service
from blog.models import Category, BlogPost
from partners.models import Partner


# Common SVG icon snippets (inner markup, used in <svg width=22 height=22 viewBox=24>)
ICON = {
    'consulting': '<rect x="8" y="3" width="8" height="4" rx="1"/><path d="M16 5h2a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h2"/><path d="m9 13 2 2 4-4"/>',
    'docs':       '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/>',
    'drill':      '<rect x="9" y="3" width="12" height="12" rx="2"/><path d="M3 9h6v12H3z"/>',
    'chart':      '<path d="M3 3v18h18"/><path d="m7 15 3-3 3 3 5-5"/>',
    'flask':      '<path d="M10 2v6.5L4 19a2 2 0 0 0 1.7 3h12.6a2 2 0 0 0 1.7-3L14 8.5V2"/><path d="M8 2h8"/>',
    'radar':      '<path d="M5 12a7 7 0 0 1 7-7"/><path d="M3 12a9 9 0 0 1 9-9"/><circle cx="12" cy="12" r="2"/><path d="M8 16h8"/>',
    'structural': '<circle cx="12" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="M12 7v3l-5 7M12 10l5 7"/>',
    'crystal':    '<path d="m12 2 8 7-8 13L4 9z"/><path d="m4 9 8 4 8-4M9 6l3 3 3-3"/>',
    'cube':       '<path d="m12 2 9 5v10l-9 5-9-5V7z"/><path d="M12 22V12M3 7l9 5M21 7l-9 5"/>',
    'brain':      '<path d="M12 2a4 4 0 0 0-4 4 3 3 0 0 0-3 3 3 3 0 0 0 1 5.5A3.5 3.5 0 0 0 9 21h6a3.5 3.5 0 0 0 3-6.5 3 3 0 0 0 1-5.5 3 3 0 0 0-3-3 4 4 0 0 0-4-4z"/><path d="M9 10v2M15 10v2M12 16h.01"/>',
    'report':     '<rect x="8" y="3" width="8" height="4" rx="1"/><path d="M16 5h2a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h2"/><path d="M9 12h6M9 16h4"/>',
}


# ─── SERVICES (11 new design with outcome + stages) ──────────────────────────
SERVICES = [
    {
        'number': '01', 'order': 1, 'icon_svg': ICON['consulting'],
        'stages': 'desktop,target,explore,mre,scoping,pfs',
        'title': {
            'uz': 'Loyihaning har bir bosqichida geologik konsalting',
            'ru': 'Геологический консалтинг на каждом этапе проекта',
            'en': 'Geological Consulting at Every Project Stage',
            'tr': 'Her Proje Aşamasında Jeolojik Danışmanlık',
        },
        'description': {
            'uz': "Geologik tadqiqotning barcha bosqichlarida mustaqil ekspert maslahati va texnik nazorat — dastlabki maqsad tanlashdan resurs baholash va texnik-iqtisodiy asoslashgacha.",
            'ru': 'Независимая экспертная консультация и технический надзор на всех этапах геологических работ — от выбора целей на ранней стадии до оценки ресурсов и технико-экономической оценки.',
            'en': 'Independent expert advice and technical supervision throughout all phases of geological study — from early-stage target selection through to resource estimation and feasibility.',
            'tr': 'Erken aşama hedef seçiminden kaynak tahmini ve fizibiliteye kadar tüm jeolojik çalışma aşamalarında bağımsız uzman tavsiyesi ve teknik denetim.',
        },
        'outcome': {
            'uz': "Har bir bosqichda asoslangan qarorlar; mustaqil texnik nazorat orqali risklarni kamaytirish.",
            'ru': 'Обоснованные решения на каждом этапе; снижение рисков благодаря независимому техническому контролю.',
            'en': 'Informed decisions at each milestone; risk reduction through independent technical oversight.',
            'tr': 'Her aşamada bilinçli kararlar; bağımsız teknik gözetim yoluyla risk azaltma.',
        },
    },
    {
        'number': '02', 'order': 2, 'icon_svg': ICON['docs'],
        'stages': 'desktop,target,explore,scoping,pfs',
        'title': {
            'uz': "Loyihaning to'liq hujjatlashtirilishi",
            'ru': 'Комплексная проектная документация',
            'en': 'Comprehensive Project Documentation',
            'tr': 'Kapsamlı Proje Dokümantasyonu',
        },
        'description': {
            'uz': "Texnik dasturlar, ish jadvallari, byudjet hisoblari va milliy hamda xalqaro talablarga mos ruxsat hujjatlarini o'z ichiga olgan to'liq loyiha paketlarini tayyorlash.",
            'ru': 'Подготовка полных проектных пакетов: технические программы, графики работ, бюджетные оценки и регуляторные документы, соответствующие национальным и международным требованиям.',
            'en': 'Preparation of full project packages including technical programmes, work schedules, budget estimates, and regulatory submissions aligned with national and international requirements.',
            'tr': 'Teknik programlar, iş takvimleri, bütçe tahminleri ve ulusal ve uluslararası gereksinimlere uygun düzenleyici belgeleri içeren tam proje paketlerinin hazırlanması.',
        },
        'outcome': {
            'uz': "Investorlar uchun tayyor hujjatlar; ruxsat olish va manfaatdor tomonlar tasdig'ining oson kechishi.",
            'ru': 'Документация, готовая к инвестициям; беспрепятственное получение разрешений и одобрения заинтересованных сторон.',
            'en': 'Investment-ready documentation; smooth permitting and stakeholder approval.',
            'tr': 'Yatırıma hazır dokümantasyon; sorunsuz izin ve paydaş onayı.',
        },
    },
    {
        'number': '03', 'order': 3, 'icon_svg': ICON['drill'],
        'stages': 'target,explore',
        'title': {
            'uz': "Trench ochish va burg'ilash — qidiruv ishlarini bajarish",
            'ru': 'Канавы и бурение — выполнение разведки',
            'en': 'Trenching & Drilling — Exploration Execution',
            'tr': 'Hendek ve Sondaj — Keşif Yürütme',
        },
        'description': {
            'uz': "Trench ochish va burg'ilash kampaniyalarini boshidan oxirigacha boshqarish: quduq dizayni, pudratchini nazorat qilish, xavfsizlik talablariga rioya, dalada real vaqt geologik nazorati.",
            'ru': 'Управление кампаниями канавных и буровых работ «под ключ»: проектирование скважин, контроль подрядчиков, соблюдение норм безопасности и геологический контроль в реальном времени.',
            'en': 'End-to-end management of trenching and drilling campaigns: hole design, contractor supervision, safety compliance, and real-time geological control on site.',
            'tr': 'Hendek ve sondaj kampanyalarının uçtan uca yönetimi: kuyu tasarımı, yüklenici denetimi, güvenlik uyumu ve sahada gerçek zamanlı jeolojik kontrol.',
        },
        'outcome': {
            'uz': "Yuqori sifatli yer osti ma'lumotlari belgilangan muddat va byudjet doirasida.",
            'ru': 'Качественные подповерхностные данные в срок и в рамках бюджета.',
            'en': 'High-quality subsurface data delivered on time and within budget.',
            'tr': 'Zamanında ve bütçe dahilinde yüksek kaliteli yeraltı verisi.',
        },
    },
    {
        'number': '04', 'order': 4, 'icon_svg': ICON['chart'],
        'stages': 'explore,mre',
        'title': {
            'uz': 'Geologik logging va namuna olish (QA/QC)',
            'ru': 'Геологическое описание и опробование (QA/QC)',
            'en': 'Geological Logging & Sampling (QA/QC)',
            'tr': 'Jeolojik Loglama ve Örnekleme (QA/QC)',
        },
        'description': {
            'uz': "Tizimli kern va chip logging, tuzilgan namunalash dasturlari va to'liq QA/QC protokollari — standartlar, blanklar va dublikatlar — laboratoriya ma'lumotlari ishonchligini ta'minlash.",
            'ru': 'Систематическое описание керна и шламов, структурированные программы опробования и полные протоколы QA/QC — стандарты, бланки и дубликаты — для обеспечения целостности лабораторных данных.',
            'en': 'Systematic core and chip logging, structured sampling programmes, and full QA/QC protocols — including standards, blanks, and duplicates — to ensure laboratory data integrity.',
            'tr': 'Sistemli karot ve şlam loglama, yapılandırılmış örnekleme programları ve tam QA/QC protokolleri — standartlar, blanklar ve dubliketler — laboratuvar verisinin bütünlüğünü sağlamak için.',
        },
        'outcome': {
            'uz': "JORC / NI 43-101 resurs baholash uchun mos, auditga tayyor ma'lumotlar bazasi.",
            'ru': 'Готовый к аудиту набор данных, пригодный для оценки ресурсов по JORC / NI 43-101.',
            'en': 'Audit-ready dataset suitable for JORC / NI 43-101 resource estimation.',
            'tr': 'JORC / NI 43-101 kaynak tahmini için uygun, denetime hazır veri seti.',
        },
    },
    {
        'number': '05', 'order': 5, 'icon_svg': ICON['flask'],
        'stages': 'target,explore',
        'title': {
            'uz': 'Geokimyoviy tadqiqot — birlamchi va ikkilamchi oreol',
            'ru': 'Геохимические исследования — первичные и вторичные ореолы',
            'en': 'Geochemical Research — Primary & Secondary Halos',
            'tr': 'Jeokimyasal Araştırma — Birincil ve İkincil Halolar',
        },
        'description': {
            'uz': "Birlamchi (hypogene) va ikkilamchi (supergene) dispersiya oreollarini aniqlash uchun tizimli ko'p elementli geokimyoviy namunalash va talqin — ruda zonalariga yo'l ko'rsatish.",
            'ru': 'Систематическое многоэлементное геохимическое опробование и интерпретация первичных (гипогенных) и вторичных (супергенных) ореолов рассеяния для выхода на рудные зоны.',
            'en': 'Systematic multi-element geochemical sampling and interpretation of primary (hypogene) and secondary (supergene) dispersion halos to vector towards ore zones.',
            'tr': 'Cevher zonlarına yönelmek için sistematik çok elementli jeokimyasal örnekleme ve birincil (hipojen) ve ikincil (süperjen) dağılım halolarının yorumlanması.',
        },
        'outcome': {
            'uz': "Aniq minerallashtirish maqsadlari; burg'ulash maqsadlarining noaniqligini kamaytirish.",
            'ru': 'Чёткие цели минерализации; снижение неопределённости буровых целей.',
            'en': 'Clear mineralisation targets; reduction of drill-target uncertainty.',
            'tr': 'Net mineralleşme hedefleri; sondaj hedef belirsizliğinin azaltılması.',
        },
    },
    {
        'number': '06', 'order': 6, 'icon_svg': ICON['radar'],
        'stages': 'desktop,target,explore',
        'title': {
            'uz': 'Geofizik tadqiqotlar — UAV, yer usti va quduq ichi',
            'ru': 'Геофизические съёмки — БПЛА, наземные и скважинные',
            'en': 'Geophysical Surveys — UAV, Surface & Downhole',
            'tr': 'Jeofizik Araştırmalar — İHA, Yüzey ve Kuyu İçi',
        },
        'description': {
            'uz': "Havoda (UAV-da) magnit va radiometriya, yer usti IP, gravitatsion va EM tadqiqotlari, struktura va litologiyani talqin qilish uchun quduq ichi geofizikasi.",
            'ru': 'Аэромагнитные и радиометрические съёмки с БПЛА, наземные ВП, гравиметрия и ЭМ, а также скважинная геофизика для структурной и литологической интерпретации.',
            'en': 'Airborne (UAV-mounted) magnetics and radiometrics, ground-based IP, gravity and EM surveys, and downhole geophysics for structural and lithological interpretation.',
            'tr': 'Havadan (İHA) manyetik ve radyometrik ölçümler, yerden IP, gravite ve EM araştırmaları, yapısal ve litolojik yorumlama için kuyu içi jeofizik.',
        },
        'outcome': {
            'uz': "Mustaqil fizik o'lchovlar bilan tasdiqlangan yer osti geologik modeli.",
            'ru': 'Подповерхностная геологическая модель, подтверждённая независимыми физическими измерениями.',
            'en': 'Subsurface geological model validated by independent physical measurements.',
            'tr': 'Bağımsız fiziksel ölçümlerle doğrulanmış yeraltı jeolojik modeli.',
        },
    },
    {
        'number': '07', 'order': 7, 'icon_svg': ICON['structural'],
        'stages': 'desktop,target,explore',
        'title': {
            'uz': "Strukturaviy geologiya va sun'iy yo'ldosh tasvirini tahlili",
            'ru': 'Структурная геология и анализ спутниковых снимков',
            'en': 'Structural Geology & Satellite Image Analysis',
            'tr': 'Yapısal Jeoloji ve Uydu Görüntüsü Analizi',
        },
        'description': {
            'uz': "Batafsil strukturaviy xaritalash, kinematik tahlil va masofadan zondlash — multispektral va giperspektral sun'iy yo'ldosh tasvirini qayta ishlash — ruda nazorat qiluvchi tuzilmalarni aniqlash.",
            'ru': 'Детальное структурное картирование, кинематический анализ и дистанционное зондирование — включая обработку мультиспектральных и гиперспектральных снимков — для определения рудоконтролирующих структур.',
            'en': 'Detailed structural mapping, kinematic analysis, and remote sensing — including multispectral and hyperspectral satellite imagery processing — to define ore-controlling structures.',
            'tr': 'Detaylı yapısal haritalama, kinematik analiz ve uzaktan algılama — multispektral ve hiperspektral uydu görüntüsü işleme dahil — cevher kontrolü yapan yapıları tanımlamak için.',
        },
        'outcome': {
            'uz': "Burg'ulash maqsadini belgilash va kon geometriyasini talqin qilishga yo'l ko'rsatuvchi strukturaviy asos.",
            'ru': 'Структурный каркас, направляющий выбор буровых целей и интерпретацию геометрии месторождения.',
            'en': 'Structural framework guiding drill targeting and deposit geometry interpretation.',
            'tr': 'Sondaj hedefleme ve yatak geometrisi yorumunu yönlendiren yapısal çerçeve.',
        },
    },
    {
        'number': '08', 'order': 8, 'icon_svg': ICON['crystal'],
        'stages': 'target,explore,mre',
        'title': {
            'uz': 'Yupqa va silliqlangan kesim tayyorlash va petrografiya',
            'ru': 'Подготовка шлифов, аншлифов и петрография',
            'en': 'Production of Thin, Polished Sections & Mineralogical Petrographic Study',
            'tr': 'İnce ve Parlatılmış Kesit Hazırlama ve Petrografi',
        },
        'description': {
            'uz': "Burg'ulash kerni yoki yer usti namunalaridan yupqa va silliqlangan kesimlar tayyorlash, so'ngra qaytaruvchi va o'tuvchi yorug'lik ostida mineralogik va petrografik tahlil.",
            'ru': 'Подготовка прозрачных и полированных шлифов из бурового керна или поверхностных проб, с последующим минералогическим и петрографическим анализом в проходящем и отражённом свете.',
            'en': 'Preparation of thin and polished sections from drill core or surface samples, followed by mineralogical and petrographic analysis under reflected and transmitted light.',
            'tr': 'Sondaj karotu veya yüzey numunelerinden ince ve parlatılmış kesitlerin hazırlanması, ardından geçen ve yansıyan ışıkta mineralojik ve petrografik analiz.',
        },
        'outcome': {
            'uz': "Mineral paragenez, o'zgarish zonalanishi va ruda mineralogiyasi tavsiflangan.",
            'ru': 'Минеральный парагенезис, зональность изменений и рудная минералогия охарактеризованы.',
            'en': 'Mineral paragenesis, alteration zonation, and ore mineralogy characterised.',
            'tr': 'Mineral parajenezi, alterasyon zonlanması ve cevher mineralojisi karakterize edildi.',
        },
    },
    {
        'number': '09', 'order': 9, 'icon_svg': ICON['cube'],
        'stages': 'explore,mre,scoping',
        'title': {
            'uz': '3D geologik modellashtirish',
            'ru': '3D геологическое моделирование',
            'en': '3D Geological Modelling',
            'tr': '3D Jeolojik Modelleme',
        },
        'description': {
            'uz': "Sanoatda qabul qilingan dasturiy ta'minot (Leapfrog, Surpac yoki ekvivalent) yordamida litologik, strukturaviy va minerallashtirish solid modellarini qurish — barcha mavjud burg'ulash va yer usti ma'lumotlarini integratsiya qilish.",
            'ru': 'Построение литологических, структурных и рудных тел в индустриальном ПО (Leapfrog, Surpac или аналоги), интегрируя все доступные буровые и поверхностные данные.',
            'en': 'Construction of lithological, structural, and mineralisation solid models using industry-standard software (Leapfrog, Surpac or equivalent), integrating all available drill and surface data.',
            'tr': 'Sektör standardı yazılım (Leapfrog, Surpac veya muadili) kullanılarak litolojik, yapısal ve mineralleşme katı modellerinin oluşturulması; tüm sondaj ve yüzey verilerinin entegrasyonu.',
        },
        'outcome': {
            'uz': "Vizual va miqdoriy geologik asos; resurs baholashga bevosita kirish ma'lumoti.",
            'ru': 'Визуальный и количественный геологический каркас; прямой ввод данных для оценки ресурсов.',
            'en': 'Visual and quantitative geological framework; direct input to resource estimation.',
            'tr': 'Görsel ve nicel jeolojik çerçeve; kaynak tahmini için doğrudan girdi.',
        },
    },
    {
        'number': '10', 'order': 10, 'icon_svg': ICON['brain'], 'is_featured': True,
        'stages': 'desktop,target,explore',
        'title': {
            'uz': 'AI va ML — bashoratli kon modellashtirish',
            'ru': 'AI и ML — предиктивное моделирование месторождений',
            'en': 'AI & ML — Predictive Deposit Modelling',
            'tr': 'AI ve ML — Tahminsel Yatak Modelleme',
        },
        'description': {
            'uz': "Mashinaviy o'qitish algoritmlari va AI-yo'naltirilgan fazoviy tahlilni qo'llash — yangi kon joylashuvini bashorat qilish, qidiruv maqsadlarini saralash va burg'ulash joyini optimallashtirish.",
            'ru': 'Применение алгоритмов машинного обучения и AI-пространственного анализа для прогноза новых месторождений, ранжирования целей и оптимизации расположения скважин.',
            'en': 'Application of machine learning algorithms and AI-driven spatial analysis to predict new deposit locations, rank exploration targets, and optimise drill-hole placement.',
            'tr': 'Yeni yatak konumlarını tahmin etmek, keşif hedeflerini sıralamak ve sondaj konumlarını optimize etmek için makine öğrenmesi algoritmalarının ve AI tabanlı mekansal analizin uygulanması.',
        },
        'outcome': {
            'uz': "Ma'lumotlarga asoslangan maqsad yaratish; kashfiyot xarajati past, muvaffaqiyat darajasi yuqori.",
            'ru': 'Генерация целей на основе данных; более высокий процент успеха при меньшей стоимости открытия.',
            'en': 'Data-driven target generation; higher exploration success rate with lower cost per discovery.',
            'tr': 'Veriye dayalı hedef üretimi; daha düşük keşif maliyeti ile daha yüksek başarı oranı.',
        },
    },
    {
        'number': '11', 'order': 11, 'icon_svg': ICON['report'],
        'stages': 'mre,scoping,pfs',
        'title': {
            'uz': 'MRE, Scoping Study va PFS/FS hisobotlarini tayyorlash',
            'ru': 'Подготовка отчётов MRE, Scoping Study и PFS/FS',
            'en': 'MRE, Scoping Study & PFS/FS Report Preparation',
            'tr': 'MRE, Scoping Study ve PFS/FS Rapor Hazırlama',
        },
        'description': {
            'uz': "JORC Code yoki NI 43-101 standartiga muvofiq Mineral Resurs Baholash va texnik-iqtisodiy tadqiqotlarni (Scoping, Pre-Feasibility, Feasibility) tayyorlash — Kompetent shaxs tomonidan yozilgan yoki ko'rib chiqilgan.",
            'ru': 'Подготовка отчётов по оценке минеральных ресурсов и технико-экономических исследований (Scoping, Pre-Feasibility, Feasibility), соответствующих JORC Code или NI 43-101, выполненных или проверенных Компетентным Лицом.',
            'en': 'Preparation of Mineral Resource Estimates and technical-economic studies (Scoping, Pre-Feasibility, Feasibility) compliant with JORC Code or NI 43-101, authored or reviewed by a Competent Person.',
            'tr': 'JORC Code veya NI 43-101 ile uyumlu Mineral Kaynak Tahminleri ve teknik-ekonomik çalışmaların (Scoping, Pre-Feasibility, Feasibility) Yetkili Kişi tarafından hazırlanması veya gözden geçirilmesi.',
        },
        'outcome': {
            'uz': "Bankka topshirishga tayyor, investor darajasidagi texnik hisobotlar — loyiha moliyalashtirishi va rivojlantirish qarorlari uchun asos.",
            'ru': 'Bankable, инвестиционного уровня технические отчёты, обеспечивающие финансирование проекта и принятие решений о развитии.',
            'en': 'Bankable, investor-grade technical reports enabling project financing and development decisions.',
            'tr': 'Bankable, yatırım sınıfı teknik raporlar — proje finansmanı ve gelişim kararlarını mümkün kılar.',
        },
    },
]


# ─── BLOG CATEGORIES ────────────────────────────────────────────────────────
CATEGORIES = [
    {'slug': 'method',    'name': {'uz': 'Metod',   'ru': 'Метод',       'en': 'Method',    'tr': 'Yöntem'}},
    {'slug': 'ai-ml',     'name': {'uz': 'AI / ML', 'ru': 'AI / ML',     'en': 'AI / ML',   'tr': 'AI / ML'}},
    {'slug': 'reporting', 'name': {'uz': 'Hisobot', 'ru': 'Отчётность',  'en': 'Reporting', 'tr': 'Raporlama'}},
]


# ─── BLOG POSTS ─────────────────────────────────────────────────────────────
POSTS = [
    {
        'category_slug': 'method', 'read_time': 7,
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
            'tr': "Jeokimya, yapısal haritalama ve gradient-boosted ML'yi nasıl birleştirerek aylarca süren saha çalışmasını savunulabilir bir hedef sıralamasına sıkıştırıyoruz.",
        },
        'content': {
            'uz': "<p>Maqola matni bu yerda...</p><p>Admin paneli orqali kontentni to'liq tahrirlay olasiz.</p>",
            'ru': "<p>Содержание статьи здесь...</p><p>Полное содержимое можно редактировать через админ-панель.</p>",
            'en': "<p>Article content goes here...</p><p>You can edit the full content via the admin panel.</p>",
            'tr': "<p>Makale içeriği burada...</p><p>İçeriği yönetim paneli üzerinden tam olarak düzenleyebilirsiniz.</p>",
        },
    },
    {
        'category_slug': 'ai-ml', 'read_time': 5,
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
        'content': {'uz':'<p>Maqola matni...</p>','ru':'<p>Содержание статьи...</p>','en':'<p>Article content...</p>','tr':'<p>Makale içeriği...</p>'},
    },
    {
        'category_slug': 'reporting', 'read_time': 9,
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
        'content': {'uz':'<p>Maqola matni...</p>','ru':'<p>Содержание статьи...</p>','en':'<p>Article content...</p>','tr':'<p>Makale içeriği...</p>'},
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

    def _seed_services(self):
        self.stdout.write('\n→ Seeding services...')
        for data in SERVICES:
            svc, created = Service.objects.get_or_create(number=data['number'])
            svc.icon_svg    = data['icon_svg']
            svc.order       = data['order']
            svc.stages      = data.get('stages', '')
            svc.is_active   = True
            svc.is_featured = data.get('is_featured', False)
            _set_translations(svc, 'title',       data['title'])
            _set_translations(svc, 'description', data['description'])
            _set_translations(svc, 'outcome',     data['outcome'])
            svc.save()
            self.stdout.write(f'  {"✓" if created else "↻"} {svc.number}  {svc.title_uz[:60]}')

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
