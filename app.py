from flask import Flask, render_template_string
import os

app = Flask(__name__)

# كود منصة GlobalX Pro المحدثة
html_content = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GlobalX Pro | المنصة المالية العالمية</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #c5a059; --dark: #0f172a; --card: rgba(255, 255, 255, 0.05); --ad-bg: rgba(255, 255, 255, 0.02); }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Tajawal', sans-serif; }
        body { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; min-height: 100vh; }
        
        header { padding: 30px 20px; text-align: center; border-bottom: 2px solid var(--gold); background: rgba(15, 23, 42, 0.8); }
        .logo { font-size: 2.5rem; font-weight: 700; color: var(--gold); }
        
        .img-container { 
            width: 100%; max-width: 800px; margin: 0 auto; 
            mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 70%, rgba(0,0,0,0));
            -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 70%, rgba(0,0,0,0));
            opacity: 0.6;
        }
        .currency-img { width: 100%; height: auto; border-radius: 0 0 50px 50px; }

        .container { max-width: 1000px; margin: -50px auto 20px; padding: 20px; position: relative; z-index: 5; }
        
        /* مساحة الإعلانات */
        .ad-space { 
            background: var(--ad-bg); border: 1px dashed rgba(197, 160, 89, 0.2); 
            margin: 20px 0; padding: 15px; text-align: center; border-radius: 12px; 
            color: #475569; font-size: 0.8rem;
        }

        .lang-switch { text-align: left; margin-bottom: 15px; }
        .lang-btn { background: var(--gold); border: none; padding: 8px 20px; border-radius: 20px; cursor: pointer; font-weight: bold; color: #0f172a; transition: 0.3s; }
        
        .converter-card { background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(197, 160, 89, 0.2); border-radius: 24px; padding: 40px; box-shadow: 0 25px 50px rgba(0,0,0,0.6); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .input-box { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
        label { color: var(--gold); font-weight: bold; font-size: 0.9rem; }
        
        input, select { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.2); padding: 15px; border-radius: 12px; color: white; font-size: 1.1rem; outline: none; transition: 0.3s; cursor: pointer; }
        option { background: #1e293b; color: white; }
        
        .result-container { margin-top: 30px; text-align: center; padding: 30px; border-radius: 15px; background: rgba(197, 160, 89, 0.1); border: 1px solid var(--gold); }
        .res-value { font-size: 2.8rem; font-weight: 700; color: #fff; }
        
        .status-badge { display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; margin-top: 10px; background: rgba(255,255,255,0.05); color: var(--gold); border: 1px solid var(--gold); }

        footer { text-align: center; padding: 40px; color: #475569; font-size: 0.8rem; }
    </style>
</head>
<body>

<header>
    <div class="logo" id="mainTitle">GLOBALX PRO</div>
    <p style="color: #94a3b8;" id="subTitle">البيانات المالية المحدثة لحظياً لكافة البورصات العالمية</p>
</header>

<div class="img-container">
    <img src="https://images.unsplash.com/photo-1518186285589-2f7649de83e0?q=80&w=1374&auto=format&fit=crop" alt="Trading" class="currency-img">
</div>

<div class="container">
    <div class="ad-space" id="adTop">مساحة إعلانية علوية - Advertisement Space</div>
    
    <div class="lang-switch"><button class="lang-btn" onclick="toggleLang()" id="langBtn">English</button></div>

    <div class="converter-card">
        <div class="input-box">
            <label id="lblAmount">المبلغ</label>
            <input type="number" id="amount" placeholder="..." oninput="calculate()">
        </div>

        <div class="grid">
            <div class="input-box">
                <label id="lblFrom">من عملة</label>
                <select id="from" onchange="calculate()">
                    <option value="" disabled selected id="optFrom">-- اضغط للاختيار --</option>
                    <option value="USD">🇺🇸 <span class="cn">دولار أمريكي</span> (USD)</option>
                    <option value="EUR">🇪🇺 <span class="cn">يورو</span> (EUR)</option>
                    <option value="SAR">🇸🇦 <span class="cn">ريال سعودي</span> (SAR)</option>
                    <option value="AED">🇦🇪 <span class="cn">درهم إماراتي</span> (AED)</option>
                    <option value="SDG">🇸🇩 <span class="cn">جنيه سوداني</span> (SDG)</option>
                    <option value="GBP">🇬🇧 <span class="cn">جنيه إسترليني</span> (GBP)</option>
                    <option value="TRY">🇹🇷 <span class="cn">ليرة تركية</span> (TRY)</option>
                    <option value="BTC">₿ <span class="cn">بيتكوين</span> (BTC)</option>
                </select>
            </div>
            <div class="input-box">
                <label id="lblTo">إلى عملة</label>
                <select id="to" onchange="calculate()">
                    <option value="" disabled selected id="optTo">-- اضغط للاختيار --</option>
                    <option value="SDG">🇸🇩 <span class="cn">جنيه سوداني</span> (SDG)</option>
                    <option value="SAR">🇸🇦 <span class="cn">ريال سعودي</span> (SAR)</option>
                    <option value="USD">🇺🇸 <span class="cn">دولار أمريكي</span> (USD)</option>
                    <option value="AED">🇦🇪 <span class="cn">درهم إماراتي</span> (AED)</option>
                    <option value="EGP">🇪🇬 <span class="cn">جنيه مصري</span> (EGP)</option>
                    <option value="QAR">🇶🇦 <span class="cn">ريال قطري</span> (QAR)</option>
                    <option value="EUR">🇪🇺 <span class="cn">يورو</span> (EUR)</option>
                    <option value="BTC">₿ <span class="cn">بيتكوين</span> (BTC)</option>
                </select>
            </div>
        </div>

        <div class="result-container">
            <div id="resLabel" style="color: var(--gold); margin-bottom: 10px;">بانتظار الاختيار...</div>
            <div class="res-value" id="resValue">0.00</div>
            <div id="marketStatus" class="status-badge" style="display:none;">تحليل حالة السوق...</div>
        </div>
    </div>

    <div class="ad-space" id="adBottom">مساحة إعلانية سفلية - Advertisement Space</div>
</div>

<footer>
    <p id="footerText">© 2026 GlobalX Finance | تحديثات البنوك العالمية والبورصات الدولية</p>
</footer>

<script>
    let currentLang = 'ar';
    
    const currencyNames = {
        'USD': {ar: 'دولار أمريكي', en: 'US Dollar'},
        'EUR': {ar: 'يورو', en: 'Euro'},
        'SAR': {ar: 'ريال سعودي', en: 'Saudi Riyal'},
        'AED': {ar: 'درهم إماراتي', en: 'UAE Dirham'},
        'SDG': {ar: 'جنيه سوداني', en: 'Sudanese Pound'},
        'GBP': {ar: 'جنيه إسترليني', en: 'British Pound'},
        'TRY': {ar: 'ليرة تركية', en: 'Turkish Lira'},
        'BTC': {ar: 'بيتكوين', en: 'Bitcoin'},
        'EGP': {ar: 'جنيه مصري', en: 'Egyptian Pound'},
        'QAR': {ar: 'ريال قطري', en: 'Qatari Riyal'}
    };

    async function calculate() {
        const amt = document.getElementById('amount').value;
        const from = document.getElementById('from').value;
        const to = document.getElementById('to').value;
        const display = document.getElementById('resValue');
        const resLabel = document.getElementById('resLabel');
        const status = document.getElementById('marketStatus');

        if (!amt || !from || !to) return;

        resLabel.innerText = currentLang === 'ar' ? "النتيجة النهائية" : "Final Result";

        try {
            const res = await fetch(`https://api.exchangerate-api.com/v4/latest/${from}`);
            const data = await res.json();
            let rate = data.rates[to];

            if (from === "USD" && to === "SDG") rate = 3350.00;
            if (from === "SAR" && to === "SDG") rate = 893.33;
            if (from === "SDG" && to === "USD") rate = 1 / 3350;

            const total = (amt * rate).toLocaleString(undefined, {minimumFractionDigits: 2});
            display.innerText = `${total} ${to}`;
            
            status.style.display = 'inline-block';
            status.innerText = currentLang === 'ar' ? "💡 استقرار في سعر الصرف الحالي" : "💡 Current exchange stability";
        } catch (e) {
            display.innerText = "Error";
        }
    }

    function toggleLang() {
        const isAr = currentLang === 'ar';
        currentLang = isAr ? 'en' : 'ar';
        
        document.documentElement.lang = currentLang;
        document.documentElement.dir = isAr ? 'ltr' : 'rtl';
        
        document.getElementById('mainTitle').innerText = "GLOBALX PRO";
        document.getElementById('subTitle').innerText = isAr ? "Real-time accuracy for global markets" : "البيانات المالية المحدثة لحظياً لكافة البورصات العالمية";
        document.getElementById('lblAmount').innerText = isAr ? "Amount" : "المبلغ";
        document.getElementById('lblFrom').innerText = isAr ? "From Currency" : "من عملة";
        document.getElementById('lblTo').innerText = isAr ? "To Currency" : "إلى عملة";
        document.getElementById('optFrom').innerText = isAr ? "-- Click to Select --" : "-- اضغط للاختيار --";
        document.getElementById('optTo').innerText = isAr ? "-- Click to Select --" : "-- اضغط للاختيار --";
        document.getElementById('resLabel').innerText = isAr ? "Waiting for selection..." : "بانتظار الاختيار...";
        document.getElementById('langBtn').innerText = isAr ? "العربية" : "English";
        document.getElementById('footerText').innerText = isAr ? "© 2026 GlobalX Finance | Global Banking Data" : "© 2026 GlobalX Finance | تحديثات البنوك العالمية والبورصات الدولية";
        
        const selects = ['from', 'to'];
        selects.forEach(sId => {
            const select = document.getElementById(sId);
            for (let i = 1; i < select.options.length; i++) {
                const val = select.options[i].value;
                const flag = select.options[i].innerText.split(' ')[0];
                select.options[i].innerText = `${flag} ${currencyNames[val][currentLang]} (${val})`;
            }
        });
        calculate();
    }
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_content)

if __name__ == "__main__":
    # الحصول على المنفذ من Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
