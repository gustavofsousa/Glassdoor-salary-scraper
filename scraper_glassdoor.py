#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# In[2]:


def print_information(job_info):
    print("\n\tRESULT OF ROUND")
    print("Job Title:", job_info['job_title'])
    print("Salary Estimate:", job_info['salary_estimate'])
    print("Rating:", job_info['rating'])
    print("Company Name:", job_info['company_name'])
    print("Location:", job_info['location'])
    print("Job description:", job_info['job_description'])
    print("\n")


# In[35]:


def close_login(driver):
    # check open Window
    try:
        WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ModalContainer"))
        )
    except:
        return
    # Close window
    try:
        button = driver.find_element_by_class_name("CloseButton")
        driver.execute_script("arguments[0].click();", button)
    except:
        print("Fail to close login")


# In[15]:


def catch_information(driver):
    job_info = {
        'job_title': driver.find_element(By.CLASS_NAME, "JobDetails_jobTitle__Rw_gn").text,
        'salary_estimate': "",
        'job_description': "",
        'rating': driver.find_element(By.CLASS_NAME, "EmployerProfile_employerRating__3ADTJ").text,
        'company_name': driver.find_element(By.CLASS_NAME, "EmployerProfile_profileContainer__d5rMb").text,
        'location': driver.find_element(By.CLASS_NAME, "JobDetails_location__MbnUM").text
    }
    try:
        job_info['salary_estimate'] = driver.find_element(By.CLASS_NAME, "SalaryEstimate_averageEstimate__xF_7h").text
    except:
        pass
    try:
        job_info['job_description'] = driver.find_element_by_xpath('.//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/section/div/div[1]').text
    except:
        pass
    return (job_info)


# In[5]:


# intent to save information and, if nonexist, let it empty.
def save_information(jobs_result, job_info):
    jobs_result.append({
        "Job Title": job_info.get("job_title", ""),
        "Salary Estimate" : job_info.get("salary_estimate", ""),
        "Job description" : job_info.get("job_description", ""),
        "Rating": job_info.get("rating", ""),
        "Company Name" : job_info.get("company_name", ""),
        "Location": job_info.get("location", "")
    })


# In[46]:


def get_jobs(role):
    #keyword = "data+scientist"
    # url = f"https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={role}&sc.keyword={role}&locT=&locId=&jobType="
    url = f"https://www.glassdoor.com/Job/brazil-{role}-SRCH_IL.0,6_IN36_KO7,25.htm"
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        jobs_result = []
        num_jobs = 5
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "JobsList_jobListItem__JBBUV"))
        )
        verbose = True
        jobs_list = driver.find_elements_by_class_name("JobsList_jobListItem__JBBUV")
        for job in jobs_list:
            print("Progress: {}".format("" + str(len(jobs_result)) + "/" + str(num_jobs)))
            close_login(driver)
            job.click()
            job_info = catch_information(driver)
            if (verbose):
                print_information(job_info)
            save_information(jobs_result, job_info)
            if (len(jobs_result) == num_jobs):
                break
    except NoSuchWindowException as e:
        print("Window closed")
    finally:
        # Close the browser
        driver.quit()
        print("Complete")
        return pd.DataFrame(jobs_result)


# In[47]:


if __name__ == "__main__":
    get_jobs("cientista de dados")

