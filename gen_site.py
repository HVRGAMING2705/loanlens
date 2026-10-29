import json
m = json.load(open("model.json"))
MEANS, STDS, COEF, INT = m["means"], m["stds"], m["coef"], m["intercept"]
DOMAIN = "https://loanlens.vercel.app"
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LoanLens — Loan Approval Predictor | AI/ML Project by Vikranth Reddy</title>
<meta name="description" content="LoanLens predicts whether a loan application would be approved, from income, credit score, loan amount, employment, debt, dependents and past defaults, using logistic regression. Try the interactive browser demo.">
<meta property="og:title" content="LoanLens — Loan Approval Predictor">
<meta property="og:description" content="Logistic regression estimates loan approval chance in seconds. Try the interactive demo.">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="LoanLens — Loan Approval Predictor">
<meta name="twitter:description" content="Logistic regression estimates loan approval chance in seconds.">
<link rel="canonical" href="{DOMAIN}/">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebApplication","name":"LoanLens","applicationCategory":"AI/ML demo","author":{{"@type":"Person","name":"Vikranth Reddy"}},"description":"Loan approval predictor using logistic regression."}}
</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:760px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em;margin-bottom:0}}.sub{{color:#333;margin-top:4px}}
label{{display:block;margin:14px 0 2px;font-weight:bold}}
input,select{{width:100%;padding:8px;font-size:16px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
button{{margin-top:18px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:0;border-radius:4px;cursor:pointer}}
button.preset{{background:#fff;color:#000;border:1px solid #000;margin-right:8px}}
#out{{margin-top:22px;padding:18px;border:2px solid #000;border-radius:6px;font-size:1.3em}}
small{{color:#333}}.row{{display:grid;grid-template-columns:1fr 1fr;gap:0 16px}}
@media(max-width:600px){{.row{{grid-template-columns:1fr}}}}
.bar{{height:18px;background:#eee;border:1px solid #000;margin-top:10px}}#fill{{height:100%;background:#000;width:0%}}
</style>
</head>
<body>
<h1>LoanLens</h1>
<p class="sub">Loan Approval Predictor — logistic regression, trained on 900 synthetic loan applications. All prediction happens in your browser; no data leaves this page.</p>
<div class="row">
<div><label>Annual income (Rs lakh)</label><input id="income" type="number" min="2" max="50" value="20"></div>
<div><label>Credit score (300–900)</label><input id="credit" type="number" min="300" max="900" value="700"></div>
<div><label>Loan amount (Rs lakh)</label><input id="loan" type="number" min="1" max="50" value="15"></div>
<div><label>Employment years</label><input id="employ" type="number" min="0" max="40" value="8"></div>
<div><label>Existing debt (Rs lakh)</label><input id="debt" type="number" min="0" max="20" value="3"></div>
<div><label>Dependents</label><input id="depend" type="number" min="0" max="4" value="1"></div>
<div><label>Past loan default?</label><select id="prev"><option value="0" selected>No</option><option value="1">Yes</option></select></div>
</div>
<button onclick="predict()">Predict approval</button>
<div>
<button class="preset" onclick="preset(30,780,10,12,1,0,0)">Strong applicant</button>
<button class="preset" onclick="preset(5,520,30,1,12,3,1)">Weak applicant</button>
<button class="preset" onclick="preset(20,700,15,8,3,1,0)">Average applicant</button>
</div>
<div id="out">Enter the application details and press Predict approval.</div>
<div class="bar"><div id="fill"></div></div>
<p><small>Model: 5-fold cross-validated accuracy = 83.6%, AUC = 0.91 (always guessing the majority class: 54.7% — about 1.5&times; better). A chance above 50% is flagged as approval likely. Trained on synthetic data for learning purposes; real loan decisions also use verified documents, bank statements and bank policy.</small></p>
<p><small>By Vikranth Reddy — B.Tech CSE (AI &amp; ML), Woxsen University. <a href="https://github.com/HVRGAMING2705/loanlens">GitHub repo</a></small></p>
<script>
const MEANS={MEANS};
const STDS={STDS};
const COEF={COEF};
const INTERCEPT={INT};
function modelProb(v){{let s=INTERCEPT;for(let i=0;i<7;i++)s+=COEF[i]*((v[i]-MEANS[i])/STDS[i]);return 1/(1+Math.exp(-s));}}
function predict(){{const v=[+document.getElementById('income').value,+document.getElementById('credit').value,+document.getElementById('loan').value,+document.getElementById('employ').value,+document.getElementById('debt').value,+document.getElementById('depend').value,+document.getElementById('prev').value];
const p=modelProb(v);const verdict=p>=0.5?'Approval likely':'Approval unlikely';
document.getElementById('out').innerHTML='Approval chance: <b>'+(p*100).toFixed(1)+'%</b> — '+verdict;
document.getElementById('fill').style.width=(p*100)+'%';}}
function preset(a,b,c,d,e,f,g){{document.getElementById('income').value=a;document.getElementById('credit').value=b;document.getElementById('loan').value=c;document.getElementById('employ').value=d;document.getElementById('debt').value=e;document.getElementById('depend').value=f;document.getElementById('prev').value=g;predict();}}
</script>
</body>
</html>
"""
open("index.html","w").write(index)
vercel = {"headers":[{"source":"/(.*)","headers":[
 {"key":"Strict-Transport-Security","value":"max-age=63072000; includeSubDomains; preload"},
 {"key":"X-Content-Type-Options","value":"nosniff"},
 {"key":"X-Frame-Options","value":"SAMEORIGIN"},
 {"key":"Referrer-Policy","value":"strict-origin-when-cross-origin"},
 {"key":"Permissions-Policy","value":"camera=(), microphone=(), geolocation=()"},
 {"key":"Cross-Origin-Opener-Policy","value":"same-origin"},
 {"key":"Access-Control-Allow-Origin","value":DOMAIN},
 {"key":"Content-Security-Policy","value":"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}]}]}
json.dump(vercel, open("vercel.json","w"), indent=1)
open("404.html","w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page not found — LoanLens</title><link rel="canonical" href="{DOMAIN}/"></head><body style="font-family:Arial,sans-serif;color:#000;max-width:600px;margin:40px auto;padding:24px"><h1>Page not found</h1><p>This page does not exist on LoanLens.</p><p><a href="{DOMAIN}/">Back to the LoanLens demo</a></p></body></html>\n""")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
open("sitemap.xml","w").write(f"""<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>{DOMAIN}/</loc></url>\n</urlset>\n""")
open("README.md","w").write("""# LoanLens — Loan Approval Predictor

Logistic regression (C=1.0) predicts whether a loan application would be approved, from annual income, credit score, loan amount, employment years, existing debt, dependents and past defaults.

- 900 synthetic loan applications (seed 42)
- 5-fold cross-validated accuracy: 83.6%, AUC: 0.91 (majority-class baseline: 54.7%)
- Interactive demo runs entirely in the browser — no backend, no data leaves the page.

Live demo: https://loanlens.vercel.app

By Vikranth Reddy — B.Tech CSE (AI & ML), Woxsen University.
""")
print("site written")
