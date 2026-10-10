# Credit Card Fraud Detection

A web-based fraud detection system that scores credit card transactions and sends uncertain cases to a human reviewer instead of deciding them automatically.

**Live Demo:** Add your Vercel link here

## Features

- **Single Check**
  - Score one transaction and get a verdict (likely fraud, looks genuine, or needs review).
  - View the fraud probability and a suggested action.

- **Bulk Analysis**
  - Upload a CSV of transactions.
  - Get a summary and a table of flagged rows.
  - Download the results.

- **Review Queue**
  - Transactions the model is unsure about wait here for a person to mark them fraud or genuine.

- **Feedback Log**
  - Every human decision is recorded:
    - Time
    - Model probability
    - Model's guess
    - Reviewer's decision
    - Whether they matched
  - Download the feedback log as CSV.

- **Two Views of the Inputs**
  - Simple view (amount in ₹, time in IST).
  - Original dataset values.

## How the Review Band Works

The Random Forest outputs a fraud probability for each transaction.

| Probability | Decision |
|---|---|
| 0.2 or below | Approved automatically |
| 0.8 or above | Flagged as fraud |
| Between 0.2 and 0.8 | Sent to a human reviewer |

- The thresholds were chosen on a validation set carved out of the training data.
- The test set stayed untouched.

## Method

- **Dataset:** ULB Credit Card Fraud (284,807 transactions, 492 frauds).
- **Duplicate Removal:** Removed 1,081 duplicate rows (283,726 rows, 473 frauds left).
- **Train/Test Split:** 80/20 stratified train/test split, done before anything else.
- **Feature Scaling:** RobustScaler on Time and Amount, fitted on the training set only.
- **Class Imbalance Handling:** SMOTE on the training set only.
- **Test Set:** Never resampled.
- **Classifiers Trained and Compared:**
  - Logistic Regression
  - Linear SVM
  - Random Forest
  - XGBoost
- **Evaluation Metrics:** Precision, recall, F1 and PR-AUC on the untouched test set (56,746 rows, 95 frauds).

### Results (Test Set, Default 0.5 Threshold)

| Model | Precision | Recall | F1 | PR-AUC | Missed Frauds | False Alarms |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.054 | 0.874 | 0.101 | 0.673 | 12 | 1,463 |
| Linear SVM (100K sample) | 0.055 | 0.874 | 0.103 | 0.658 | 12 | 1,432 |
| Random Forest | 0.914 | 0.779 | 0.841 | 0.807 | 21 | 7 |
| XGBoost | 0.743 | 0.789 | 0.765 | 0.820 | 20 | 26 |

The deployed model is a Random Forest refit on 80% of the training data (to leave a validation set for choosing the band). On the test set:

### Comparison: Plain Threshold vs. Review Band

| Metric | Plain 0.5 Threshold | With Review Band (0.2 / 0.8) |
|---|---:|---:|
| Frauds Caught Automatically | 72 | 63 |
| Frauds Sent to a Human | 0 | 14 |
| Frauds Missed | 23 | 18 |
| False Alarms Reaching Customers | 9 | 2 |
| Genuine Transactions Sent to a Human | 0 | 26 |

If reviewers decide correctly, the band catches 77 of 95 frauds (recall about 0.81). With only 95 frauds in the test set, small differences between models are noise.

**Tech stack**
**Training**: Python, pandas, NumPy, scikit-learn 1.6.1, imbalanced-learn, XGBoost, joblib (Google Colab)
**Backend**: Python function on Vercel (api/predict.py)
**Frontend**: HTML, CSS and JavaScript (public/index.html)**
Storage**: review queue and feedback log are kept in the browser (localStorage)

**Project structure**
## Project Structure

```text
fraud-detection/
├── api/
│   └── predict.py                  # Prediction API and review-band logic
├── model/
│   └── fraud_model.joblib          # Trained model, scaler, column order, thresholds
├── public/
│   ├── index.html                  # Web interface
│   └── sample_transactions.csv     # 30 sample transactions for testing
├── Notebooks/
│   └── training.ipynb              # Model training (Google Colab)
├── test_local.py                   # Tests the saved model on 30 samples
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project configuration
└── vercel.json                     # Vercel deployment configuration
```

**Run it**

**Check the model locally**
### 

Install the required dependencies:

```bash
pip install scikit-learn==1.6.1 pandas joblib
```

Run the local test script:

```bash
python test_local.py
```

The model only loads reliably with scikit-learn 1.6.1, the version it was trained with.

**Deploy to Vercel**

```bash
npm install -g vercel
vercel login
vercel
```

**Retrain**: open the notebook in Notebooks/ in Google Colab, upload creditcard.csv, and run the cells in order.

**Dataset**

The ULB dataset is not included in this repository. Download "Credit Card Fraud Detection" (Machine Learning Group, ULB) from Kaggle. Its columns are Time (seconds since the first transaction), Amount, V1 to V28 (anonymised PCA features) and Class.

### Limitations

- **Anonymised Features:** V1 to V28 are anonymised, so users cannot meaningfully enter them manually.
- **Single Transaction Check:** Works with the sample buttons or an edited sample.
- **₹ and IST Display:** A demo convenience that assumes the data starts at 12:00 AM IST on the first day and that ₹100 equals 1 unit of the dataset's amount. The dataset specifies neither assumption.
- **Original Model Values:** The model remains unchanged and was trained on the original values.
- **Feedback Logging:** The feedback log is stored in the browser and does not retrain the model. Retraining on reviewed cases is future work.
- **Linear SVM:** Trained on a 100K sample because a kernel SVM is too slow on the full training set.
- **Review Band Limitation:** Frauds scored below 0.2 are approved automatically, so the review band cannot catch cases the model is confidently wrong about (18 in the test set).
- **Future Work:** Real-time monitoring, explainable AI, spending-pattern analysis, and live banking API integration.

## Team

- Addepalli Sreekar
- Adepoju Sandeep Chary
- Bushipaka Vamshi
- Nara Abhirama

**Guide:** Ms. V. Veda Sri

- **Designation:** Assistant Professor
- **Department:** CSE (AI & ML)
- **Institution:** Samskruti College of Engineering & Technology, Hyderabad
