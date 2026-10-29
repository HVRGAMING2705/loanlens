from pptx import Presentation
from pptx.util import Inches, Pt
prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
def slide(title, bullets, sub=None):
    s = prs.slides.add_slide(BLANK)
    t = s.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12), Inches(1))
    t.text_frame.word_wrap = True; t.text_frame.text = title
    t.text_frame.paragraphs[0].font.size = Pt(36); t.text_frame.paragraphs[0].font.bold = True
    y = 1.6
    if sub:
        b = s.shapes.add_textbox(Inches(0.6), Inches(y), Inches(12), Inches(0.7)); b.text_frame.word_wrap=True; b.text_frame.text=sub; b.text_frame.paragraphs[0].font.size=Pt(20); y += 0.9
    for line in bullets:
        b = s.shapes.add_textbox(Inches(0.8), Inches(y), Inches(11.8), Inches(0.8)); b.text_frame.word_wrap=True; b.text_frame.text="•  "+line; b.text_frame.paragraphs[0].font.size=Pt(20); y += 0.85
    return s
slide("LoanLens", ["Loan Approval Predictor"], "An AI/ML project by Vikranth Reddy — B.Tech CSE (AI & ML), Woxsen University")
slide("The Problem", ["Loan applicants wait days to learn if their application will be approved", "Banks weigh income, credit score, debt and history together — hard to judge by hand", "A simple, transparent model shows which factors actually move the decision"])
slide("The Solution", ["LoanLens estimates the approval chance (0–100%) from 7 application details", "Annual income, credit score, loan amount, employment years, existing debt, dependents, past default", "Interactive demo: change any detail, see the approval chance instantly — fully in the browser"])
slide("Tech Stack", ["Python + scikit-learn: logistic regression", "Synthetic dataset: 900 loan applications (seed 42)", "HTML + CSS + vanilla JavaScript demo", "GitHub + Vercel hosting"])
slide("Architecture", ["Inputs: 7 application features → standardization (train mean / std) → logistic regression → sigmoid → approval probability", "Model exported as model.json; the browser demo reproduces it exactly", "Strongest drivers: credit score, loan amount and employment years"])
slide("Demo", ["Try the presets: strong applicant, weak applicant, average applicant", "Strong applicant (Rs 30 lakh income, 780 credit score, Rs 10 lakh loan) → 99.0% approval chance", "Weak applicant (Rs 5 lakh income, 520 credit score, past default) → 0.3% approval chance"])
slide("Results", ["5-fold cross-validated accuracy = 83.6%", "AUC = 0.91 (majority-class baseline: 54.7% — about 1.5x better)", "Approval rate in training data: 45.3%", "Strongest drivers: credit score, loan size and employment — matching real lending behaviour"])
slide("Future Scope", ["Train on real (anonymised) loan-application data with bank approval outcomes", "Add features: loan purpose, property value, co-applicant income", "Explain each prediction: which factor pushed the chance up or down", "Add a fairness check across applicant groups before any real-world use"])
slide("Thank You", ["LoanLens — will this loan be approved? Now you can check in seconds."], "Vikranth Reddy · github.com/HVRGAMING2705/loanlens")
out = "/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_LoanLens_2026-10-29.pptx"
prs.save(out); print("saved", out, "slides:", len(prs.slides._sldIdLst))
