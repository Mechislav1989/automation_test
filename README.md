# 🧪 Automation Assignment: Playwright + Python – Saucedemo.com

## 📋 Overview

Your task is to build a basic browser automation script using **Playwright in Python** to interact with a public web app: [https://www.saucedemo.com](https://www.saucedemo.com).

This should demonstrate your ability to:

* Navigate and interact with UI elements
* Automate form submissions
* Handle validation errors
* Extract and export structured data
  
We expect you to spend one hour on this assignment. You're free to spend more time if you’d like. You can start whenever you're ready and do not need to start this today.
You can use any tool(s) or AI you want to complete this assignment.

---

## 🎯 Goals

1. Attempt login with both valid and invalid inputs
2. Capture and log any form validation errors
3. After successful login, extract product names and prices
4. Simulate a checkout attempt with missing data and log validation results
5. Save product data to a `.csv` file
6. Log all major steps and actions taken

---

## ✅ Requirements

### Technical

* Use **Python + Playwright**
* Use the built-in `logging` module for logging
* Save logs to a `.log` file
* Save product data to a `.csv` file
* Include a `requirements.txt` file with all dependencies
* Script must be runnable via CLI using: `python main.py`

---

## 🧪 Testing & Validation

* Include logs at each step, including validation errors
* Capture screenshots when validation errors are triggered *(optional extra credit)*
* Ensure the `.csv` data file is generated and contains accurate, expected content

---

## 📤 Submission Instructions

1. **Fork this repository**
2. Complete your implementation and commit your changes
3. Send us your name and a link to your GitHub repo once you're done to careers@lamarhealth.com

---

## 📂 Deliverables

* `main.py` – your main automation script
* `products.csv` – product data output
* `automation.log` – log of all steps and errors
* `automation_screenshots/` – *(optional)* directory of screenshots
* `README.md` – summary of the project + answers to the reflection questions below

---

## 💭 Reflection Questions (Add you answer into your `README.md`)

* What steps did you prioritize first? Why?
  I prioritized designing the application architecture. This was crucial to ensure modularity and scalability, making it easier to add new features later. After that, I analyzed the structure of the website to identify key elements for automation, such as the login page, product inventory, and checkout process. This sequence allowed me to understand the domain fully before implementing the automation steps like login, product data extraction, and order simulation.
* What was critical to complete in the 1 hour?
  The website is relatively simple, so the critical tasks within the 1-hour coding window were implementing the core functionalities: logging in with valid and invalid credentials, extracting product data and saving it to a CSV file, and simulating a checkout process with missing data to trigger validation errors.
* How long did you actually spend on the project?
  I spent 1 hours on preparation and studying, which included analyzing the website and planning the architecture. The actual coding took 1 hour. Documenting and testing 1 hour.
* How did you know your automation was working?
  I verified the automation worked by checking multiple outputs: the logs in automation.log confirmed successful operations and flagged errors, the products.csv file contained accurate product data, and screenshots in automation_screenshots captured validation errors as expected. Additionally, I ran the script with headless=False in the browser configuration to visually confirm the automation steps executed correctly.
* What would you improve with more time?
  With additional time, I would enhance the script by adding more test cases, improving error handling for edge cases. 
