# Sprint 1 Raporu

## Takım İsmi
*CVil Society*

## Product Backlog
👉 https://ai-grup76-yzt.atlassian.net/jira/core/projects/RE/board?groupBy=status
---

## Sprint Planlaması

- *Sprint İçinde Tamamlanması Tahmin Edilen Puan:* 20  
- *Toplam Proje Puanı:* 100  
- *Tahmin Mantığı:*  
  Proje toplamda 100 puan üzerinden planlanmıştır. 3 sprint boyunca farklı ağırlıklarla ilerlenmesi hedeflenmektedir. Bu ilk sprintte temel altyapıya odaklanılmıştır.

---

## Daily Scrum Bilgileri

- *İletişim Kanalları:* WhatsApp, Trello, Slack  
- *Toplantı Zamanı:* Genellikle her gün akşam 20:00 - 21:00  
- *Görüşülen Konular:*
  - Proje fikrinin son haliyle netleştirilmesi
  - Arayüzde PDF yükleme modülü hakkında fikir alışverişi
  - NLP modülünde kullanılacak kütüphanelerin belirlenmesi

---

## Sprint Board Durumu

### ✅ Tamamlananlar
- Proje fikrinin belirlenmesi  
- Veri seti seçimi  
- Kullanılacak teknolojilerin belirlenmesi  

### 🚧 Üzerinde Çalışılanlar
- PDF / Metin yükleme modülünün geliştirilmesi  
- CV'den metin çıkarımı ve Named Entity Recognition (NER) işlemleri  

---

## Ürün Durumu

- Arayüz taslağı çizildi  
- PDF yükleme modülünün ilk prototipi oluşturuldu  

---

## Sprint Review

- *Proje Fikri:*  
  Kullanıcının yüklediği CV'yi analiz ederek güçlü/zayıf yönlerini çıkaran bir AI sistemi geliştirilecek.

- *Veri Seti:*  
  Open Source Resume Dataset seçildi ve ön incelemesi yapıldı.

- *Teknoloji ve Yöntemler:*  
  - Doğal Dil İşleme (NLP)  
  - Named Entity Recognition (NER)  
  - TF-IDF  
  - Flask ve Streamlit alternatifleri değerlendirildi

- *Modül Geliştirmeleri:*  
  PDF to Text dönüştürme modülünün geliştirilmesine başlandı.

---

## Sprint Katılımcıları

- Tuana Korkmazyürek - Aktif
- Edanur Tekçe -  Aktif
- Yunus Emre Açıkoğlu - Aktif
- Meriç Özcan - Aktif

---

## Sprint Retrospective

### ✅ İyi Olanlar
- Proje fikri çok kısa sürede netleştirildi.  
- İletişim verimli geçti, herkes sorumluluğunu aldı.  
- Veri seti uygun bulundu ve hızlıca indirildi.

### ⚠ Geliştirilmesi Gerekenler
- Final haftası ve staj başlangıcı nedeniyle kod geliştirme kısmı yetersiz kaldı.  
- Arayüz tasarımı konusunda görüş farklılıkları zaman kaybettirdi.  
- Zaman yönetimi için bir sonraki sprintte daha net görev dağılımı yapılacak.

# Sprint 2 Raporu

## Sprint Notları
Karar verilen proje için uygun veri setleri bulundu. Toplanılan verilerle model geliştirilmeye başlandı. Web uygulamasının arayüz kodları yazılmaya başlandı. 

## Tahmin Edilen Tamamlanacak Puan
Toplam proje iş yükü 100 puan olarak planlanmıştır. İkinci sprintte veri setlerinin toplanması model geliştirmeye başlanması ve web uygulamasının arayüz tasarımının oluşturulması hedeflenmiştir. Bu işler toplam projenin yaklaşık %35’unu kapsadığından bu sprintte tamamlanması hedeflenen puan 35 olarak belirlenmiştir.

## Daily Scrum
Proje sürecinde ekip üyeleri genellikle WhatsApp üzerinden günlük iletişim kurarak görevlerin ilerleyişi hakkında bilgi paylaştı.
İhtiyaç halinde Google Meet üzerinden çevrim içi toplantılar yapıldı. Bu toplantılarda tamamlanan işler karşılaşılan problemler ve bir sonraki adımlar değerlendirildi.
Toplantılar genellikle 18.00 ile 20.00 arasında gerçekleştirildi.
Toplantılarla alakalı ekran görüntüleri bir sonraki bölümde bulunan linke eklenmiştir. 

## Sprint Board Updates
Aşağıdaki linkte uygulamanın arayüz görüntülerine ve geliştirilen modelle ilgili görüntülere ulaşabilirsiniz.
https://drive.google.com/drive/folders/1ISEpIOwXcuzbl3RS_DKlopBywuVwm0Eg?usp=sharing

## Sprint Review
- Proje için kullanılacak uygun veri setleri araştırıldı ve seçildi.
- Seçilen veri setleri başarıyla toplandı ve ön işleme (temizleme ve dönüştürme) süreci başlatıldı.
-Model denemeleri yapılarak algoritma test edildi.
-Web uygulaması için arayüz tasarımı yapıldı.
-Backend ve frontend arasındaki temel bağlantı yapısı planlandı.
-Takım içi görev dağılımı netleştirildi ve günlük ilerleme takibi yapıldı.
-Gelecek geliştirmeler planlandı. Planlanan geliştirmeler aşağıda madde madde yer almaktadır
-•	Flask/FastAPI Web API entegrasyonu:
-•	CV yüklenip JSON raporu alınabilecek web servisi.
-•	İmla ve dil bilgisi kontrolü (Java 17 ile LanguageTool).
-•	Derin öğrenme tabanlı bölüm ayıklama (BERT fine-tune).
-•	Web arayüzü (React + backend API).
-•	Puanlama optimizasyonu için ML modeli (örneğin iyi CV örnekleriyle eğitilmiş bir regresyon veya sınıflandırma modeli).

## Sprint Katılımcıları
- Edanur Tekçe(Aktif)
- Meriç Özcan(Aktif)
- Tuana Korkmazyürek(Aktif)
- Yunus Emre Açıkoğlu(Aktif)

## Sprint Retrospective
## İyi Olanlar:
-Uygun ve kaliteli veri setleri zamanında bulundu.
-Model geliştirme sürecine planlandığı gibi başlandı.
-Web uygulaması için arayüz kodlamasına başlanarak ön yüz tasarımı yapıldı.
-Ekip içi iletişim ve görev paylaşımı uyumlu şekilde ilerledi.
## Geliştirilmesi Gerekenler:
-Model eğitimi sırasında yaşanan bazı teknik sorunlar çözüm sürecini yavaşlattı.
-Geliştirilen modüllerin entegrasyonu için daha erken testler yapılmalı.
-Dokümantasyonun güncel tutulması konusunda daha dikkatli olunmalı.

