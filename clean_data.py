from scraper_glassdoor import get_jobs

if __name__ == "__main__":
    db_jobs = get_jobs("data engineer", 50)
    db_jobs.to_csv("database_of_jobs.csv")
    print(db_jobs.head())
