# Sprint reports

The text below is the Turkish sprint report that previously lived in `README.md`. It is kept as the team's record of the three Scrum sprints. For a description of the code in this repository, see the README at the repository root.

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
Karar verilen proje için uygun veri setleri bulundu.Toplanılan verilerle model geliştirilmeye başlandı.Web uygulamasının arayüz kodları yazılmaya başlandı. 

## Tahmin Edilen Tamamlanacak Puan
Toplam proje iş yükü 100 puan olarak planlanmıştır.İkinci sprintte veri setlerinin toplanması model geliştirmeye başlanması ve web uygulamasının arayüz tasarımının oluşturulması hedeflenmiştir.Bu işler toplam projenin yaklaşık %35’ini kapsadığından bu sprintte tamamlanması hedeflenen puan 35 olarak belirlenmiştir.

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
- Model denemeleri yapılarak algoritma test edildi.
- Web uygulaması için arayüz tasarımı yapıldı.
- Backend ve frontend arasındaki temel bağlantı yapısı planlandı.
- Takım içi görev dağılımı netleştirildi ve günlük ilerleme takibi yapıldı.
- Gelecek geliştirmeler planlandı. Planlanan geliştirmeler aşağıda madde madde yer almaktadır
- 1. Flask/FastAPI Web API entegrasyonu
- 2. CV yüklenip JSON raporu alınabilecek web servisi.
- 3. İmla ve dil bilgisi kontrolü (Java 17 ile LanguageTool).
- 4. Derin öğrenme tabanlı bölüm ayıklama (BERT fine-tune).
- 5. Web arayüzü (React + backend API).
- 6. Puanlama optimizasyonu için ML modeli (örneğin iyi CV örnekleriyle eğitilmiş bir regresyon veya sınıflandırma modeli).

## Sprint Katılımcıları
- Edanur Tekçe(Aktif)
- Meriç Özcan(Aktif)
- Tuana Korkmazyürek(Aktif)
- Yunus Emre Açıkoğlu(Aktif)

## Sprint Retrospective
## İyi Olanlar:
- Uygun ve kaliteli veri setleri zamanında bulundu.
- Model geliştirme sürecine planlandığı gibi başlandı.
- Web uygulaması için arayüz kodlamasına başlanarak ön yüz tasarımı yapıldı.
- Ekip içi iletişim ve görev paylaşımı uyumlu şekilde ilerledi.
## Geliştirilmesi Gerekenler:
- Model eğitimi sırasında yaşanan bazı teknik sorunlar çözüm sürecini yavaşlattı.
- Geliştirilen modüllerin entegrasyonu için daha erken testler yapılmalı.
- Dokümantasyonun güncel tutulması konusunda daha dikkatli olunmalı.

 # Sprint 3 Raporu  
 
*Takım İsmi:* CVil Society  
*Sprint Süresi:* 20.07.25 – 03.08.25  
*Toplam Proje Puanı:* 100  
*Sprintte Tamamlanması Hedeflenen Puan:* 45  
*Sprintte Gerçekleşen Puan:* 45  

---

## Sprint Notları  
Bu sprintte, sistemin *kararlı ve kullanıcıya hazır* bir sürümünün oluşturulması hedeflenmiştir. Önceki sprintlerde geliştirilen altyapılar sadeleştirilmiş ve sistemin uçtan uca çalıştığı bir yapıya ulaşılmıştır.

*Öne çıkan geliştirmeler:*

•⁠  ⁠PDF’ten metin çıkarma modülü son testlerden başarıyla geçti.  
•⁠  ⁠Dil algılama özelliği Türkçe ve İngilizce için optimize edildi.  
•⁠  ⁠Semantik benzerlik analizi ile sıfır-atış sınıflandırma birleştirildi ve entegre edildi.  
•⁠  ⁠Bölüm ağırlıklandırma ve puanlama mantığı finalize edildi.  
•⁠  ⁠Dil bilgisi ve yazım kontrolü fonksiyonel hale getirildi.  
•⁠  ⁠Kullanıcıya puan, güçlü/zayıf yönler ve öneriler sunan çıktı sistemi tamamlandı.  

Bu sprint, toplam iş yükünün %45’ini kapsayacak şekilde planlanmış ve başarıyla tamamlanmıştır.

---

## Daily Scrum  

*İletişim Kanalları:* WhatsApp, Trello, Google Meet  
*Toplantı Saatleri:* 18:00 – 20:00  

*Görüşülen başlıca konular:*

•⁠  ⁠Son prototipin testleri ve hata kontrolü  
•⁠  ⁠Semantik eşleşme ve sınıflandırma çıktılarının doğruluğu  
•⁠  ⁠Anlamlı içerik kontrol fonksiyonunun son revizyonu  
•⁠  ⁠Dil bilgisi analizinde tespit edilen eksiklerin giderilmesi  
•⁠  ⁠JSON çıktı yapısının test edilmesi  
•⁠  ⁠Web arayüzü ile analiz modülünün entegrasyon planı  
•⁠  ⁠Proje sunumu için metinlerin ve videonun hazırlanması  

---

## Sprint Board Updates  
Aşağıdaki linkte  uygulamanın arayüz görüntülerine ve geliştirilen modelle ilgili görüntülere ulaşabilirsiniz.
https://drive.google.com/drive/folders/1M7C7cEocheCuRENMb2cCmQu2upuz-AsM

*Tamamlananlar:*

•⁠  ⁠PDF to Text fonksiyonunun optimizasyonu  
•⁠  ⁠Bölüm bazlı puanlama sistemi  
•⁠  ⁠Semantik analiz ve sınıflandırma entegrasyonu  
•⁠  ⁠Dil algılama ve dil bilgisi kontrolü  
•⁠  ⁠Güçlü/zayıf yön çıkarımı ve öneri listesi  
•⁠  ⁠JSON çıktı formatının sonlandırılması  
•⁠  ⁠Web arayüzü ile analiz modülünün birleştirilmesi  
•⁠  ⁠Proje sunumu ve dokümantasyonunun tamamlanması  

---

## Ürün Durumu ve Teknik Gelişmeler  
Bu sprint sonunda, sistem artık *tamamen işlevsel ve kullanıcıya hazır* bir yapay zekâ destekli CV analiz aracı haline gelmiştir.  

*Sistemin işleyiş adımları:*

1.⁠ ⁠PDF’ten metin çıkarımı  
2.⁠ ⁠Dil algılama (Türkçe/İngilizce)  
3.⁠ ⁠CV bölümlerinin sınıflandırılması (semantik benzerlik + zero-shot learning)  
4.⁠ ⁠Anlamlı içerik kontrolü  
5.⁠ ⁠Ağırlıklı puanlama  
6.⁠ ⁠Dil bilgisi denetimi  
7.⁠ ⁠Güçlü/zayıf yönlerin çıkarılması ve öneri sunumu  

*Kullanılan teknolojiler:*

•⁠  ⁠*PDF işleme:* pdfplumber  
•⁠  ⁠*Dil algılama:* langdetect  
•⁠  ⁠*NLP:* SentenceTransformer, MoritzLaurer/mDeBERTa-v3  
•⁠  ⁠*Dil bilgisi denetimi:* language_tool_python  
•⁠  ⁠*Kod yapısı:* Modüler, sadeleştirilmiş ve yorumlanabilir fonksiyonlar  

---

## Sprint Review  

*Hedeflenenler:*

•⁠  ⁠Kararlı ve sürdürülebilir bir sistem kurmak  
•⁠  ⁠Geri bildirim mekanizmasını tamamlamak  
•⁠  ⁠Kullanıcıya açık ve yönlendirici çıktılar sunmak  

*Gerçekleşenler:*

•⁠  ⁠Sistem kararlı bir şekilde çalışmaktadır  
•⁠  ⁠Semantik analiz ve sınıflandırma başarıyla entegre edilmiştir  
•⁠  ⁠JSON formatında detaylı analiz çıktısı oluşturulmuştur  
•⁠  ⁠Teknik sunum dokümanları ve tanıtım videosu hazırlanmıştır  

---

## Sprint Katılımcıları  
•⁠  ⁠Edanur Tekçe (Aktif)  
•⁠  ⁠Tuana Korkmazyürek (Aktif)  
•⁠  ⁠Meriç Özcan (Aktif)  
•⁠  ⁠Yunus Emre Açıkoğlu (Aktif)  

---

## Sprint Retrospective  

### İyi Olanlar:

•⁠  ⁠Kod tabanı sadeleştirilerek modüler hale getirildi  
•⁠  ⁠Puanlama ve içerik analizi algoritmaları başarıyla optimize edildi  
•⁠  ⁠Dil bilgisi analizi ve geri bildirim yapısı tamamlandı  
•⁠  ⁠Arayüz ve analiz modülü arasındaki bağlantı test edilerek doğrulandı  

### Geliştirilmesi Gerekenler:

•⁠  ⁠NLP modelleri daha optimize versiyonlarla güncellenebilir  
•⁠  ⁠Dokümantasyon ve sunum içerikleri daha da detaylandırılabilir  

---

## Sonuç  
Proje, Sprint 3 sonunda semantik analize dayalı, dil bağımsız ve uçtan uca çalışan bir CV analiz sistemine dönüşmüştür. Sistem; içerik değerlendirmesi, dil bilgisi kontrolü ve geliştirme önerileri sunarak yayına hazır hâle getirilmiştir.



