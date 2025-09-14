# generate_data.py
import numpy as np
import pandas as pd

def generate_insurance_data(n=10000, seed=42):
    np.random.seed(seed)

    customer_id = np.arange(100000, 100000 + n)
    age = np.random.randint(18, 85, size=n)
    gender = np.random.choice(["M","F"], size=n, p=[0.55,0.45])
    tenure = np.random.randint(0, 20, size=n)
    num_claims = np.random.poisson(0.8, size=n)
    claim_amount_total = np.round(np.abs(np.random.normal(2000, 5000, size=n) + num_claims*1500), 2)
    policy_type = np.random.choice(["basic","standard","premium"], size=n, p=[0.4,0.45,0.15])
    premium = np.round(np.clip(np.random.normal(3000 + (policy_type=="premium")*2000 + tenure*20, 400), 300, 15000),2)
    payment_method = np.random.choice(["credit_card","bank_transfer","cash"], size=n, p=[0.6,0.3,0.1])
    region = np.random.choice(["north","south","east","west"], size=n)
    previous_renewals = np.maximum(0, tenure + np.random.randint(-2,3,size=n))
    satisfaction_score = np.round(np.clip(np.random.normal(7 - num_claims*0.5 + (policy_type=="premium")*0.5, 1.5), 1, 10),1)
    has_complaint = (np.random.rand(n) < (0.08 + (satisfaction_score<5)*0.12)).astype(int)

    # churn probability influenced by features
    p = 0.08 + (age<25)*0.05 + (tenure<1)*0.10 + (num_claims>2)*0.12 + (satisfaction_score<4)*0.15 + (has_complaint==1)*0.10
    p += (policy_type=="basic")*0.03 + (premium>7000)*-0.05
    p = np.clip(p, 0.01, 0.9)
    churn = (np.random.rand(n) < p).astype(int)

    df = pd.DataFrame({
        "customer_id": customer_id,
        "age": age,
        "gender": gender,
        "tenure": tenure,
        "num_claims": num_claims,
        "claim_amount_total": claim_amount_total,
        "policy_type": policy_type,
        "premium": premium,
        "payment_method": payment_method,
        "region": region,
        "previous_renewals": previous_renewals,
        "satisfaction_score": satisfaction_score,
        "has_complaint": has_complaint,
        "churn": churn
    })

    return df

if __name__ == "__main__":
    df = generate_insurance_data()
    df.to_csv("synthetic_insurance_claims.csv", index=False)
    print("✅ Synthetic dataset saved as synthetic_insurance_claims.csv")
