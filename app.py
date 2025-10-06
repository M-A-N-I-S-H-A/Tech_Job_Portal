from flask import Flask, render_template, send_file, redirect, url_for, flash
import pandas as pd
import os
import sys

# Add the current directory to the system path to ensure 'scraper.py' is found
# This helps resolve the ModuleNotFoundError if the environment is slightly complex.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the scraper function from the scraper file
from scraper import scrape_indeed

# Set a secret key for flash messages
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key_here'

@app.route("/")
def home():
    csv_file = "jobs.csv"
    jobs = []
   
    if os.path.exists(csv_file):
        try:
            # Read only 100 rows for large CSV files for faster loading
            jobs = pd.read_csv(csv_file).head(100).to_dict(orient="records")
            if not jobs:
                flash("The jobs.csv file is empty. Run the scraper to fetch jobs.", "warning")
        except pd.errors.EmptyDataError:
             flash("The jobs.csv file is empty. Run the scraper to fetch jobs.", "warning")
        except Exception as e:
            flash(f"Error reading CSV: {e}", "danger")
    else:
        flash("jobs.csv not found. Run the scraper to fetch job listings.", "info")
       
    return render_template("index.html", jobs=jobs)

@app.route("/scrape")
def scrape_data():
    try:
        # Call the scraping function
        scrape_indeed()
        flash("✅ Scraped 5 pages of job listings successfully! Data updated.", "success")
    except Exception as e:
        flash(f"❌ Scraping failed: {e}", "danger")
       
    # Redirect back to the home page to display the new data
    return redirect(url_for('home'))


@app.route("/download")
def download_csv():
    csv_file = "jobs.csv"
    if os.path.exists(csv_file):
        return send_file(csv_file, as_attachment=True, download_name='job_listings.csv')
    else:
        flash("Job data not found. Run the scraper first.", "danger")
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
