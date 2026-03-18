# Aura Electronics Warehouse and Shipping Dashboard

### What is this project?
I built this interactive tool to help Aura Electronics identify where their warehouse operations are slowing down and how to better prepare for their busiest seasons. Instead of static spreadsheets, this dashboard allows users to filter by city and see exactly how fast products are moving in real-time.

### The Tools I Used
* **Python** for the backend logic and data processing.
* **Streamlit** to build the interactive web interface.
* **Pandas** to clean and transform the raw electronic sales data.
* **Plotly** to create the dynamic, high-contrast visualizations.

---

### What I Discovered
After analyzing the data, I identified three major areas where the business can improve its operations:

1. **The Holiday Rush:** Shipping volume spikes significantly in November and December. My recommendation is to have all seasonal hiring and training finalized by mid-October to ensure the team is ready before the peak hits.
2. **Inventory for Small Staples:** Batteries and charging cables are the highest-volume sellers. While they have lower margins, they are essential for cart conversions. I suggested an automated re-ordering system to ensure these items never hit zero stock.
3. **Daily Peak Times:** Orders predictably spike around 12 PM and 7 PM. To maintain efficiency, the warehouse should stagger staff shifts so the maximum number of people are on the floor during these specific windows.

---

### How to Run This Locally
1. Clone the repository to your machine.
2. Install the necessary libraries:
   `pip install -r requirements.txt`
3. Launch the application:
   `python -m streamlit run app.py`
