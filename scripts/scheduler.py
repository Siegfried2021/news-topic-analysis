import schedule
import time
from datetime import datetime
from scripts.scrape_news import run_scraping
from scripts.preprocess_text import run_preprocessing
from scripts.topic_modelling import run_modeling

def pipeline():
    print(f"Starting pipeline at {datetime.now()}")
    run_scraping()
    run_preprocessing()
    run_modeling()
    print(f"Pipeline completed at {datetime.now()}")

# Run the pipeline immediately on startup
pipeline()

# Schedule the job to run every day
schedule.every(1).days.do(pipeline)

# Initial wait for one day after the first execution
time.sleep(86400)  # 86400 seconds = 1 day

# Continuous loop for all subsequent scheduled jobs
while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour for accuracy
