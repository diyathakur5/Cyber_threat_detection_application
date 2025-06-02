import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

# Step 1: Define rule-based spam message detection function
def is_suspicious_message(msg):
    spam_keywords = [
        'win', 'prize', 'congratulations', 'urgent', 'offer', 'reward',
        'click here', 'limited', 'claim', 'free', 'gift', 'buy 1 get 1',
        'money', 'loan', 'lucky', 'selected', 'exclusive', 'call now'
    ]
    return any(keyword in msg.lower() for keyword in spam_keywords)

# Step 2: Dummy data
dummy_data = {
    "label": ['spam'] * 25 + ['ham'] * 25,
    "message": [
        "Win a brand new car now!", "Claim your free iPhone today!", "Congratulations, you've won!",
        "You have been selected for a $1000 reward.", "Act now! Limited offer only.",
        "Click here to claim your prize.", "You've been chosen!", "Urgent: update your account info.",
        "Earn money from home!", "Lowest loan rates available!", "Exclusive deal for you!",
        "Your number was picked!", "Don't miss this opportunity.", "You've won a vacation!",
        "Free entry in contest!", "Call now to receive your gift!", "Buy 1 get 1 free today only!",
        "This is not a scam!", "Congratulations! You're lucky!", "Win gift cards now!",
        "Limited time prize claim!", "Hurry! Offer ends soon!", "Get paid instantly!", 
        "Final notice: redeem your reward.", "You’re a lucky winner!",

        "Hey, how are you?", "Let's meet for lunch today.", "Can you call me back?", 
        "Meeting is rescheduled to 3 PM.", "Happy birthday, enjoy your day!",
        "I'll be there in 10 minutes.", "Don't forget the groceries.", "Can we talk later?",
        "I sent you the files.", "Looking forward to the trip!", "Thanks for your help.",
        "Yes, I got your message.", "I'll check and get back to you.", "Great job on the presentation!",
        "How's your weekend going?", "Sure, let's catch up soon.", "Did you complete the task?",
        "It was nice seeing you today.", "All the best for your exam!", 
        "Let’s watch a movie tonight.", "Don’t worry, things will be fine.", 
        "I’m running late, sorry!", "Take care and rest well.", "Just checking in with you.", 
        "What time is the event tomorrow?"
    ]
}

# Step 3: Convert to DataFrame
data = pd.DataFrame(dummy_data)
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# Step 4: Apply rule-based spam detection
data['rule_flag'] = data['message'].apply(is_suspicious_message)

# Optional: Print suspicious messages detected by rule-based function
print("\nSuspicious messages detected by rules:")
print(data[data['rule_flag'] == True][['message', 'label']])

# Step 5: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(data['message'], data['label'], test_size=0.2, random_state=42)

# Step 6: Vectorization
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

# Step 7: Model Training
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Step 8: Save Model and Vectorizer
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/spam_message_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("\nModel and vectorizer trained and saved using dummy data with rule-based logic.")
