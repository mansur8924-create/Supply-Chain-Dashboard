Aura Electronics: Warehouse & Shipping Dashboard

What is this?
I built this interactive tool to help Aura Electronics figure out where their warehouse is getting stuck and how to handle their busiest seasons. Instead of just looking at spreadsheets, this dashboard lets you filter by city and see exactly how fast products are moving in real-time.

The Tools I Used
Python (The engine)

Streamlit (To turn the code into a clean web app)

Pandas (To clean and organize the messy sales data)

Plotly (To make the charts interactive and easy to read)
 What I Discovered (The "So What?")
After digging into the data, I found three major things that the business needs to act on:

The Holiday Rush is Real: Shipping goes crazy in November and December. My advice? Get all seasonal hiring and training done by mid-October so the team isn't overwhelmed when the rush hits.

Batteries are the Secret MVP: Even though they’re cheap, batteries and cables are our #1 sellers by volume. If we run out, customers might abandon their entire cart. I recommended an automated re-order system so we never hit zero.

The Lunch & Dinner Spikes: Orders predictably spike at 12 PM and 7 PM. To keep things moving, we should stagger warehouse shifts so we have the most people on the floor during those exact windows.

Want to run it yourself?
Clone the repo.

Install the requirements: pip install -r requirements.txt

Launch the app: python -m streamlit run app.py
