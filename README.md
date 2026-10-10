**Credit Card Fraud Detection**

A web-based fraud detection system that scores credit card transactions and sends uncertain cases to a human reviewer instead of deciding them automatically.

**Live demo**: add your Vercel link here

**What it does**
**Single check**: score one transaction and get a verdict (likely fraud, looks genuine, or needs review) with the fraud probability and a suggested action.
**Bulk analysis**: upload a CSV of transactions, get a summary and a table of flagged rows, and download the results.
**Review queue**: transactions the model is unsure about wait here for a person to mark them fraud or genuine.
**Feedback log**: every human decision is recorded (time, model probability, model's guess, reviewer's decision, whether they matched) and can be downloaded as CSV.
**Two views of the inputs**: a simple view (amount in ₹, time in IST) and the original dataset values.
**How the review band works**

The Random Forest outputs a fraud probability for each transaction.

**Probability**	            **Decision**
0.2 or below	        Approved automatically
0.8 or above	        Flagged as fraud
Between 0.2 and 0.8   	Sent to a human reviewer

The thresholds were chosen on a validation set carved out of the training data, so the test set stayed untouched.

**Method**
Dataset: ULB Credit Card Fraud (284,807 transactions, 492 frauds).
Removed 1,081 duplicate rows (283,726 rows, 473 frauds left).
80/20 stratified train/test split, done before anything else.
RobustScaler on Time and Amount, fitted on the training set only.
SMOTE on the training set only. The test set is never resampled.
Four classifiers trained and compared: Logistic Regression, linear SVM, Random Forest, XGBoost.
Evaluated with precision, recall, F1 and PR-AUC on the untouched test set (56,746 rows, 95 frauds).

**Results (test set, default 0.5 threshold)**
**Model	                    Precision	Recall	F1		PR-AUC	Missed frauds|	False alarms**
-----------------------------------------------------------------------------------------------
Logistic Regression	        0.054	    0.874	0.101	0.673	12			 |1,463
Linear SVM (100K sample)	0.055	    0.874	0.103	0.658	12			 |1,432
Random Forest	            0.914	    0.779	0.841	0.807	21			 |7
XGBoost                 	0.743		0.789	0.765	0.820	20			 |26

The deployed model is a Random Forest refit on 80% of the training data (to leave a validation set for choosing the band). On the test set:

	Plain 0.5 threshold	With review band (0.2 / 0.8)
Frauds caught automatically	72	63
Frauds sent to a human	0	14
Frauds missed	23	18
False alarms reaching customers	9	2
Genuine transactions sent to a human	0	26

If reviewers decide correctly, the band catches 77 of 95 frauds (recall about 0.81). With only 95 frauds in the test set, small differences between models are noise.

Tech stack
Training: Python, pandas, NumPy, scikit-learn 1.6.1, imbalanced-learn, XGBoost, joblib (Google Colab)
Backend: Python function on Vercel (api/predict.py)
Frontend: HTML, CSS and JavaScript (public/index.html)
Storage: review queue and feedback log are kept in the browser (localStorage)
Project structure
api/predict.py            scoring function (loads the model, applies the review band)
model/fraud_model.joblib  trained model, scaler, column order and thresholds
public/index.html         web interface
public/sample_transactions.csv   30 test transactions for the sample buttons
Notebooks/                training notebook (Google Colab)
test_local.py             checks the saved model on the 30 samples
requirements.txt, pyproject.toml, vercel.json   deployment settings
Run it

Check the model locally

pip install scikit-learn==1.6.1 pandas joblib
python test_local.py

The model only loads reliably with scikit-learn 1.6.1, the version it was trained with.

Deploy to Vercel

npm install -g vercel
vercel login
vercel

Retrain: open the notebook in Notebooks/ in Google Colab, upload creditcard.csv, and run the cells in order.

Dataset

The ULB dataset is not included in this repository. Download "Credit Card Fraud Detection" (Machine Learning Group, ULB) from Kaggle. Its columns are Time (seconds since the first transaction), Amount, V1 to V28 (anonymised PCA features) and Class.

Limitations
V1 to V28 are anonymised, so a person cannot meaningfully type them in. The single check works with the sample buttons or an edited sample.
The ₹ and IST view is a demo convenience. It assumes the data starts at 12:00 am IST on the first day and that ₹100 equals 1 unit of the dataset's amount. The dataset states neither, and the model is unchanged and was trained on the original values.
The feedback log is stored in the browser and does not retrain the model. Retraining on reviewed cases is future work.
The SVM is linear and trained on a 100K sample, because a kernel SVM is too slow on the full training set.
Frauds the model scores below 0.2 are approved automatically, so the review band cannot catch cases the model is confidently wrong about (18 in the test set).
Real-time monitoring, explainable AI, spending-pattern analysis and live banking API integration are future work.
Team

Addepalli Sreekar, Adepoju Sandeep Chary, Bushipaka Vamshi, Nara Abhirama

Guide: Ms. V. Veda Sri, Assistant Professor, Department of CSE (AI & ML), Samskruti College of Engineering & Technology, Hyderabad
