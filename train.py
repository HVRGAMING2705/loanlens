import json, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import accuracy_score, roc_auc_score

rng = np.random.default_rng(42)
n = 900
income = rng.uniform(2, 50, n)          # annual income, Rs lakh
credit = rng.uniform(300, 900, n)       # credit score
loan = rng.uniform(1, 50, n)            # loan amount, Rs lakh
employ = rng.uniform(0, 40, n)          # employment years
debt = rng.uniform(0, 20, n)            # existing debt, Rs lakh
depend = rng.integers(0, 5, n).astype(float)
prev_default = rng.integers(0, 2, n).astype(float)
# Generative approval logit: higher income/credit/employment help; bigger
# loan, more debt, more dependents and a past default hurt approval.
logit = (1.30 + 0.06*income + 0.012*(credit-650) - 0.08*loan
         + 0.08*employ - 0.12*debt - 0.20*depend - 1.5*prev_default)
p = 1/(1+np.exp(-logit))
y = (rng.random(n) < p).astype(int)
X = np.column_stack([income, credit, loan, employ, debt, depend, prev_default])
names = ["annual_income_lakh","credit_score","loan_amount_lakh","employment_years","existing_debt_lakh","dependents","prev_default"]
mu, sd = X.mean(0), X.std(0)
Xs = (X - mu)/sd
model = LogisticRegression(max_iter=1000, C=1.0).fit(Xs, y)
kf = StratifiedKFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(LogisticRegression(max_iter=1000, C=1.0), Xs, y, cv=kf)
proba_cv = cross_val_predict(LogisticRegression(max_iter=1000, C=1.0), Xs, y, cv=kf, method="predict_proba")[:,1]
acc = float(accuracy_score(y, pred_cv)); auc = float(roc_auc_score(y, proba_cv))
base = float(max(y.mean(), 1-y.mean()))
print(f"CV accuracy={acc:.3f} AUC={auc:.3f} approval_rate={y.mean():.3f} baseline={base:.3f}")
print("coef", model.coef_, "intercept", model.intercept_)
mj = {"features": names, "means": mu.tolist(), "stds": sd.tolist(),
      "coef": model.coef_[0].tolist(), "intercept": float(model.intercept_[0]),
      "metrics": {"cv_accuracy": acc, "cv_auc": auc, "approval_rate": float(y.mean()), "baseline_accuracy": base, "n": n}}
with open("model.json","w") as f: json.dump(mj, f, indent=1)
def predict(v):
    z = (np.array(v)-mu)/sd
    return float(1/(1+np.exp(-(model.intercept_[0] + z @ model.coef_[0]))))
samples = [[30,780,10,12,1,0,0],[5,520,30,1,12,3,1],[20,700,15,8,3,1,0],[45,820,20,20,0,2,0],[8,610,25,3,8,2,0]]
for s in samples: print(s, round(predict(s),4))
