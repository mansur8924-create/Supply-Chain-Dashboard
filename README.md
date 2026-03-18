# Aura Electronics: Supply Chain & Fulfillment Dashboard

##  Strategic Objective
A dynamic, interactive web application built to monitor outbound inventory velocity, regional market distribution, and operational bottlenecks for Aura Electronics. Designed for executive stakeholders to make data-driven decisions regarding Q4 surge capacity and inventory replenishment.

##  Tech Stack
* **Language:** Python 3.x
* **Framework:** Streamlit (Interactive UI & Web Hosting)
* **Data Manipulation:** Pandas
* **Data Visualization:** Plotly Express

##  Key Features & Interactive Elements
* **Executive KPI Matrix:** Real-time calculation of total units shipped, highest velocity SKUs, and average order sizes based on active market filters.
* **Dynamic Regional Filtering:** A global control panel allowing stakeholders to isolate and analyze specific geographic markets (e.g., assessing the San Francisco phenomena vs. secondary markets).
* **Fulfillment Cycle Analysis:** Area charting of intra-day order processing to identify warehouse scheduling bottlenecks.
* **Hierarchical Market Distribution:** Treemap visualization of regional freight allocation.

##  Lead Analyst Strategic Imperatives
1. **Surge Capacity Planning:** Identified a massive outbound spike in Q4 (Nov-Dec). Recommended freezing non-essential warehouse restructuring and securing seasonal labor by Oct 15th to prevent 3PL carrier rejection.
2. **SKU Velocity Replenishment:** Identified low-margin staples (batteries, cables) as the highest volume movers. Recommended automated ERP re-ordering thresholds to prevent stockouts that block high-margin add-on sales.
3. **Intra-Day Shift Optimization:** Identified bi-modal order ingestion spikes (12:00 PM and 7:00 PM). Recommended staggering warehouse picker shift-starts to align maximum headcount with peak processing hours.

##  How to Run Locally
1. Clone this repository.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Launch the dashboard: `python -m streamlit run app.py`git init
