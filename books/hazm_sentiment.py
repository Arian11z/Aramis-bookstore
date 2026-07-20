from hazm import Normalizer, word_tokenize

class HazmSentimentAnalyzer:
    
    def __init__(self):
        self.normalizer = Normalizer()
        
        self.positive_words = set([
            'عالی', 'خوب', 'فوق‌العاده', 'محشر', 'جالب', 'باحال',
            'دوست_داشتنی', 'زیبا', 'لذت‌بخش', 'کامل', 'بی‌نظیر',
            'آموزنده', 'مفید', 'ارزشمند', 'گیرا', 'هیجان‌انگیز',
            'تاثیرگذار', 'الهام‌بخش', 'قشنگ', 'شگفت‌انگیز', 'عالیه',
            'خوشم_اومد', 'توصیه', 'حتما', 'پسندیدم', 'راضی', 'بهترین'
        ])
        
        self.negative_words = set([
            'بد', 'افتضاح', 'ضعیف', 'بی‌کیفیت', 'مسخره', 'چرت',
            'حوصله‌سربر', 'کسل‌کننده', 'خسته‌کننده', 'ناامید_کننده',
            'گرون', 'ارزش_نداره', 'نخرید', 'پشیمون', 'وقت_تلف',
            'نامفهوم', 'گنگ', 'قدیمی', 'تکراری', 'بی‌فایده',
            'دوست_نداشتم', 'راضی_نیستم', 'اشتباه'
        ])
    
    def analyze(self, text):
        if not text:
            return 'neutral', 0.0
        
        try:
            normalized_text = self.normalizer.normalize(text)
            tokens = word_tokenize(normalized_text)
            
            positive_count = sum(1 for token in tokens if token in self.positive_words)
            negative_count = sum(1 for token in tokens if token in self.negative_words)
            
            total = positive_count + negative_count
            
            if total == 0:
                return 'neutral', 0.0
            
            if positive_count > negative_count:
                confidence = positive_count / total
                return 'positive', confidence
            elif negative_count > positive_count:
                confidence = negative_count / total
                return 'negative', confidence
            else:
                return 'neutral', 0.5
                
        except Exception as e:
            print(f"Error: {e}")
            return 'neutral', 0.0
    

    
    def get_sentiment_label(self, sentiment):
        labels = {
            'positive': 'مثبت',
            'negative': 'منفی',
            'neutral': 'خنثی'
        }
        return labels.get(sentiment, 'خنثی')
