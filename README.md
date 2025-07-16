1.Clone the Repository

git clone https://github.com/TejasriPinnam07/AI-POWERED-INTERVIEW-PREPARATION-PLATFORM

cd interview-prep/backend


2.Create and Activate Virtual Environment

python -m venv interview

source interview/bin/activate  # On Windows: interview\Scripts\activate


3.Install Dependencies

pip install -r requirements.txt


4.Set Up Environment Variables

Create a file named .env in the root level (same directory as manage.py) and add your Hugging Face API key:

HF_API_KEY=your_huggingface_api_key_here


5.Run Migrations

python manage.py makemigrations

python manage.py migrate


6.Load Sample Data

python manage.py loaddata coding_problems.json


7.Start the Server

python manage.py runserver

