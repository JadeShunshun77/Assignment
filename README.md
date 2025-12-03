# readme.py
# Run this script to generate README.md for SDPA Coursework (Part 1 + Part 2).
# The README fully complies with the official coursework instructions.

README_CONTENT = SDPA Coursework – Part 1 & Part 2  
This repository contains my full solution to the SDPA coursework.  
The project is split into two major components:

- **Part 1 — Flower Shop Simulation**
- **Part 2 — Loan Analytics (World Bank API)**

This README explains:
- the design of my code,
- the classes and methods I implemented,
- the purpose of each script,
- design decisions I made and why,
- instructions for running both Part 1 and Part 2,
- and all external libraries required for reproducibility.

The documentation in this README complements the docstrings and inline comments inside the code itself, as required by the coursework specification.

---

# 1. Project Structure
```
Assignment
│
├── task1
│   ├── bouquet.py
│   ├── config.py
│   ├── florist.py
│   ├── inventory.py
│   ├── main.py
│   ├── overview.txt
│   ├── prompts.py
│   └── shop.py
│
├── task2
│   ├── loan_worldbank_dataset.csv
│   ├── part2_loan_analytics.ipynb
│   └── step1_fetch_loan_data.py
│
└── README.md
```

**Part 1 files:** `main.py`, `config.py`, `bouquet.py`, `florist.py`, `inventory.py`, `shop.py`, `prompts.py`

**Part 2 files:** `step1_fetch_loan_data.py`, `loan_worldbank_dataset.csv`, `part2_loan_analytics.ipynb`

**Documentation:** `README.md` , `overview.txt`

---

# 2. Part 1 – Flower Shop Simulation 

## 2.1 Overview

Part 1 is a full simulation of a flower shop that operates month by month.  
The player manages florists, greenhouse inventory, bouquet production, supplier choices, and finances.  
The simulation includes:

- Demand constraints  
- Vendor price differences  
- Inventory decay (depreciation)  
- Storage costs  
- Labour capacity constraints  
- Cash flow tracking  
- Bankruptcy termination
---

# 2.2 Code Design, Classes, and Responsibilities

### **config.py**
This file centralizes all project constants:
- Bouquet definitions and recipes (flowers required per bouquet type)
- Demand per bouquet type and production time per bouquet 
- Sales prices per bouquet
- Vendor pricing for each flower
- Greenhouse capacities, depreciation rates, and storage cost
- Starting cash, rent, florist wages, and monthly working hours

Keeping all numeric settings in one file separates configuration from business logic 
and makes the simulator easy to tweak.

---

### **bouquet.py**
Defines the `Bouquet` class.

- Store bouquet name, recipe, production time, and sales price

- Compute total supplies needed for a given production quantity

- Compute revenue for a given production quantity

This class ensures that bouquet-related logic is self-contained rather than scattered
across the simulation.

---

### **florist.py**
Defines the `Florist` class.

- Represent a florist with name and available labour time per month
- Optionally record a speciality bouquet type
- Contribute labour capacity to the shop  


Florists are individual objects rather than integers to allow future extensibility 
(e.g., special skills or productivity).

---

### **inventory.py**
Defines the `Inventory` class.

- Track current greenhouse stock  
- Check supply sufficiency before monthly production  
- Deduct supplies when bouquets are produced  
- Apply depreciation (stock loss)  
- Compute monthly storage cost  
- Restock to capacity using configurable vendor prices and return total restocking cost

All physical stock logic is grouped here to keep the design cohesive and easier to 
reason about.

---

### **prompts.py**
Provides reusable and validated input methods:

- `ask_int` – prompts for integer with min/max checks  
- `ask_yes_no` – strict boolean input  
- `ask_months_to_run` – asks for simulation length  

Separating input handling from simulation logic avoids cluttering shop.py and makes 
the code easier to test.

---

### **shop.py**
This is the core engine of the simulation.  
Defines the `FlowerShop` class.

- Manage the list of florists, the bouquet catalogue, the inventory and the cash balance
- Handle hiring and firing decisions and calculate labour capacity
- Ask the user for monthly production decisions and validate them against:
  - demand limits
  - inventory constraints
  - labour constraints
- Compute monthly revenue from bouquet sales
- Apply costs (wages, rent, storage, restocking)
- Apply depreciation and vendor-based restocking
- Produce a monthly report summarising income, costs, and remaining cash
- Detect bankruptcy (negative cash) and terminate the simulation early if it happens

The simulation logic is intentionally kept inside one orchestrating class to prevent
scattering logic across modules, which keeps state transitions transparent and maintainable.

---

### **main.py**
Entry point of the program (Part 1).

**Program Flow:**
1. Print a welcome message.
2. Ask the user how many months to simulate.
3. Create a FlowerShop instance.
4. Run the monthly loop  
5. Run the monthly loop until either:
   - all months are completed, or
   - the shop goes bankrupt.

`main.py` is intentionally kept small: it delegates all real work to the classes 
described above.

---

# 2.3 How to Run Part 1

You need only standard Python (no external libraries).

```bash      
  python main.py
```
Follow on-screen instructions to hire florists, produce bouquets, and manage finances.

# 3. Part 2 – Loan Analytics (World Bank Data)
## 3.1 Overview

Part 2 performs a complete data analytics workflow:

- Data acquisition using a real API (World Bank Open Data)
- Cleaning and preparation of the dataset
- Exploratory Data Analysis (EDA)
- Regression modelling
- Interpretation of the empirical results and their limitations
---

## 3.2 Step 1 – Data Acquisition Script (`step1_fetch_loan_data.py`)

This script retrieves three macro-financial indicators via the World Bank Open Data API:

- Lending interest rate (`FR.INR.LEND`)
- Non-performing loans (% of total gross loans) (`FB.AST.NPER.ZS`)
- Domestic credit to private sector (% of GDP) (`FS.AST.PRVT.GD.ZS`)

The indicators are collected for seven countries:

- United States (US)
- United Kingdom (GB)
- Germany (DE)
- France (FR)
- Canada (CA)
- Japan (JP)
- Australia (AU)

### Process

- Loop over each indicator and country code.
- Call the API endpoint:  
  `https://api.worldbank.org/v2/country/<code>/indicator/<indicator>?format=json&per_page=2000`
- Parse the JSON response and collect year–value pairs.
- Build a pandas DataFrame for each indicator.
- Merge all indicator tables on `(country_code, country_name, year)`.
- Rename the indicator columns to readable names.
- Sort the dataset by country and year.
- Save the merged dataset to `loan_worldbank_dataset.csv`.

This satisfies the requirement of using a real-world dataset with more than 150 rows and multiple countries.

---

## 3.3 Notebook (`part2_loan_analytics.ipynb`)

The notebook implements the rest of the workflow.

### Step 1 – Dataset extraction (documentation)

- Describes the goal of the dataset and the indicator choices.
- Explains that extraction is handled by `step1_fetch_loan_data.py`.

### Step 2 – Data cleaning and preparation

- Load `loan_worldbank_dataset.csv`
- Inspect structure and missing values
- Convert indicator columns to numeric types
- Filter early years with low coverage
- Drop rows with missing core indicators when necessary
- Impute remaining values (e.g. using country-level medians)
- Optional engineered features (e.g. decade grouping)

### Step 3 – Exploratory Data Analysis (EDA)

- Summary statistics
- Histograms
- Time series by country
- Scatterplots (e.g. interest rate vs NPL)
- Correlation matrix + heatmap for all indicators

### Step 4 – Regression modelling

- Simple regression: lending interest rate → non-performing loan ratio
- Multiple regression: lending interest rate + private credit → non-performing loan ratio
- Report coefficients and R²
- Display residual plots and actual–vs–predicted plots

### Step 5 – Conclusions

- Summarise the main findings
- Interpret the signs/magnitudes of coefficients
- Discuss limitations (low R², omitted variables, small sample of countries)
- Suggest potential extensions

---

## 3.4 Required External Libraries (Part 2 only)

Part 1 uses **no external libraries** beyond the Python standard library.

Part 2 requires:
```
pandas
requests
matplotlib
seaborn
scikit-learn
statsmodels
jupyter (for running the notebook)
```
Install with:

```bash
   pip install pandas requests matplotlib seaborn scikit-learn statsmodels jupyter
```
## 4. How to Run Part 2

Inside the `Assignment/task2` directory:

### Option A — Rebuild the dataset
`python step1_fetch_loan_data.py`

This downloads data from World Bank and regenerates loan_worldbank_dataset.csv.

### Option B — Run the notebook
`jupyter notebook part2_loan_analytics.ipynb`

Run all notebook cells from top to bottom.

## 5.External Code Use

World Bank Open Data – https://data.worldbank.org/

