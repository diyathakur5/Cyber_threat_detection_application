import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os
import re

# Step 1: Function to detect suspicious URLs based on patterns
def is_suspicious_url(url):
    suspicious_patterns = [
        r'bit\.ly', r'tinyurl', r't\.co', r'goo\.gl',
        r'\d+\.\d+\.\d+\.\d+',  # IP address
        r'login', r'verify', r'secure', r'update', r'confirm',
        r'free', r'win', r'prize', r'offer', r'bonus',
        r'\.tk', r'\.ml', r'\.cf', r'\.gq', r'\.xyz', r'\.buzz'
    ]
    return any(re.search(pattern, url.lower()) for pattern in suspicious_patterns)

# Step 2: Your URL dataset
data = {
    'url': [
        'http://free-money.com',
        'https://secure-login-paypal.com',
        'https://github.com',
        'https://google.com',
        'http://click-here-win-prize.net',
        'https://yourbank-login-secure.info',
        'https://openai.com',
        'http://get-rich-quick.biz',
        'https://facebook.com',
        'http://claim-your-prize-now.org',
        'https://twitter.com',
        'https://secure-account-update.com',
        'http://win-big-money.today',
        'https://linkedin.com',
        'https://paypal.com',
        'http://free-vacation-offer.com',
        'https://instagram.com',
        'http://verify-account-login.com',
        'http://cheap-medications-online.biz',
        'https://microsoft.com',
        'http://urgent-security-alert.net',
        'https://apple.com',
        'http://bonus-cash-gift.org',
        'https://netflix.com',
        'http://your-bank-account-update.info',
        'https://youtube.com',
        'http://earn-money-fast-now.biz',
        'https://amazon.com',
        'http://prize-win-online.org',
        'https://dropbox.com',
        'http://secure-update-login.com',
        'https://ebay.com',
        'http://money-back-guarantee.net',
        'https://reddit.com',
        'http://account-verification-required.biz',
        'https://quora.com',
        'http://free-gift-card-offer.org',
        'https://tumblr.com',
        'http://security-alert-login.net',
        'https://wikipedia.org',
        'http://claim-prize-money-now.biz',
        'https://stackoverflow.com',
        'http://limited-time-offer.net',
        'https://github.io',
        'http://update-your-profile.com',
        'https://medium.com',
        'http://click-to-win-prize.org',
        'https://bitbucket.org',
        'http://secure-payment-update.net',
        'https://hackernews.com'
    ],  # (your list stays the same)
    'label': [
        1,1,0,0,1,1,0,1,0,1,0,1,1,0,0,1,0,1,1,0,
        1,0,1,0,0,1,0,1,0,0,1,0,1,0,1,0,1,0,1,0,
        1,0,1,0,0,1,0,1,0,1
    ]  # 1 = spam, 0 = safe
}

df = pd.DataFrame(data)

# Step 3: Apply rule-based suspicion flag
df['rule_based_flag'] = df['url'].apply(is_suspicious_url)

# Step 4: (Optional) Log or observe suspicious URLs for future analysis
print("Suspicious URLs detected by rules:")
print(df[df['rule_based_flag'] == True][['url', 'label']])

# Step 5: Proceed with ML Vectorization and Training
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['url'])
y = df['label']  # still using the labeled column, not the rule-based flag

model = LogisticRegression()
model.fit(X, y)

# Step 6: Save the model and vectorizer
model_dir = os.path.join('app', 'models')
os.makedirs(model_dir, exist_ok=True)

joblib.dump(model, os.path.join(model_dir, 'url_model.pkl'))
joblib.dump(vectorizer, os.path.join(model_dir, 'url_vectorizer.pkl'))

print("Model and vectorizer saved successfully!")
