import re
import pdfplumber
from langdetect import detect
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import language_tool_python

# ============================
# 1. Anahtar Kelimeler ve Ağırlıklar
# ============================
criteria_labels = {
    "iş_deneyimi": ["İş Deneyimi", "Work Experience", "Career History", "Experience"],
    "egitim": ["Eğitim", "Education", "Academic Background", "University"],
    "teknik_beceriler": ["Teknik Beceriler", "Technical Skills", "Skills"],
    "ozet": ["Özet", "Hakkımda", "Summary", "Profile", "Objective"],
    "liderlik": ["Liderlik", "Leadership", "Organization Experience"],
    "sertifikalar": ["Sertifikalar", "Certificates", "Certifications", "Courses"],
    "iletisim": ["İletişim", "Contact", "Phone", "Email"],
    "portfolyo": ["Portfolyo", "Portfolio", "GitHub", "Website"],
    "diller": ["Diller", "Languages"],
    "referanslar": ["Referanslar", "References"]
}

criteria_weights = {
    "iş_deneyimi": 25,
    "egitim": 15,
    "teknik_beceriler": 15,
    "ozet": 10,
    "liderlik": 10,
    "sertifikalar": 10,
    "iletisim": 5,
    "portfolyo": 5,
    "diller": 3,
    "referanslar": 2
}

# ============================
# 2. Modeller
# ============================
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

# ============================
# 3. PDF Metin Çıkarma
# ============================
def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# ============================
# 4. İmla ve Dilbilgisi Kontrolü
# ============================
def grammar_check(text, lang_code):
    tool = language_tool_python.LanguageTool("en-US" if lang_code == "en" else "tr")
    matches = tool.check(text[:5000])  # ilk 5000 karaktere bak
    return [m.message for m in matches]


def has_meaningful_content(section_keywords, text):
    try:
        for kw in section_keywords:
            pattern = rf"{kw}[\s\S]{{0,5000}}"  
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                following_text = match.group()
                content_lines = following_text.split('\n')[1:]
                lines = [line.strip() for line in content_lines if line.strip()]
                real_lines = [line for line in lines if not re.match(r"^\w+:?$", line)]
                content_text = " ".join(real_lines).strip()

                total_words = sum(len(line.split()) for line in real_lines)
                sentence_count = len([s for s in re.split(r'(?<=[.!?])\s+', content_text) if s])

                print(f" '{kw}' için içerik bulundu mu? {len(real_lines)} satır, {total_words} kelime, {sentence_count} cümle")


                if total_words >= 10 and sentence_count >= 2:
                    return True
        return False
    except Exception as e:
        print(" has_meaningful_content HATASI:", str(e))
        raise e


# ============================
# 5. CV Analizi
# ============================
def analyze_cv(text):
    try:
        lang = detect(text)
        text_lower = text.lower()
        total_score = 0
        strengths, weaknesses = [], []

        for section, labels in criteria_labels.items():
            max_score = 0

            if has_meaningful_content(labels, text):
                max_score = 1.0
            else:
                for kw in labels:
                    if kw.lower() in text_lower:
                        max_score = 0.4
                        break

                if max_score < 0.4:
                    try:
                        e1 = semantic_model.encode(text, convert_to_tensor=True)
                        e2 = semantic_model.encode(" ".join(labels), convert_to_tensor=True)
                        sim = float(util.cos_sim(e1, e2))
                        if sim > 0.4:
                            max_score = sim
                    except Exception as e:
                        print(f" Semantik benzerlik hatası ({section}):", str(e))

                if max_score < 0.4:
                    try:
                        result = classifier(text[:512], candidate_labels=labels, multi_label=True)
                        max_score = max(result["scores"])
                    except Exception as e:
                        print(f" Zero-shot hatası ({section}):", str(e))

            score = round(criteria_weights[section] * max_score, 2)
            total_score += score

            if max_score >= 0.9:
                strengths.append(f"{section.replace('_',' ').title()} bölümü mevcut ve içeriği güçlü.")
            elif max_score >= 0.6:
                strengths.append(f"{section.replace('_',' ').title()} bölümü mevcut ancak geliştirilebilir.")
            elif max_score >= 0.4:
                weaknesses.append(f"{section.replace('_',' ').title()} başlığı var ancak içerik yetersiz.")
            else:
                weaknesses.append(f"{section.replace('_',' ').title()} bölümü eksik.")

        total_score = round(total_score, 2)

        has_any_content = any(has_meaningful_content(labels, text) for labels in criteria_labels.values())
        if not has_any_content:
            print(" CV hiç anlamlı içerik içermiyor. Puan sıfırlandı.")
            total_score = 0
            strengths = []  


        try:
            recommendations = generate_recommendations(text)
        except Exception as e:
            print(" Öneri üretimi hatası:", str(e))
            recommendations = []

        return {
            "language": "English" if lang == "en" else "Türkçe",
            "score": total_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "grammar_issues": grammar_check(text, lang),
            "recommendations": recommendations
        }

    except Exception as e:
        print(" analyze_cv içinde hata oluştu:", str(e))
        raise e




def generate_recommendations(text):
    recs = []
    text_lower = text.lower()

    if "python" not in text_lower:
        recs.append({
            "message": "CV’nizde Python yetkinliği belirtilmemiş. Python becerilerinizi öne çıkarın.",
            "resources": ["https://www.learnpython.org/", "LeetCode", "Kaggle"]
        })

    if "github" not in text_lower and "gitlab" not in text_lower:
        recs.append({
            "message": "Projelerinizi göstermek için GitHub veya GitLab profilinizi ekleyin.",
            "resources": ["https://github.com/", "https://gitlab.com/"]
        })

    if "proje" not in text_lower and "project" not in text_lower:
        recs.append({
            "message": "CV’nizde yer alan projeler, yetkinliklerinizi göstermek için önemlidir.",
            "resources": ["Kendi kişisel portföy siteniz", "Notion, Behance gibi araçlar"]
        })

    if "ingilizce" not in text_lower and "english" not in text_lower:
        recs.append({
            "message": "Dil becerilerinizi belirtmeniz işe alım uzmanları için önemlidir.",
            "resources": ["https://www.duolingo.com/", "IELTS/TOEFL sertifika programları"]
        })

    return recs




