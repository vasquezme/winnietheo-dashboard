# winnietheo-dashboard

https://winnietheo-dashboard-31rk.onrender.com/

Instructions:

Log-in to Render
Select Repository
Create New Web Service
Select Github repo with .py file
Ensure requirements.txt, ProcFile and data files are uploaded to your repo. (ensure that your .py file points to your data)
 - your requirements.txt file must include: dash, pandas, plotly, geopandas, gunicorn
 - ProcFile will contain the following text with no extention to the file name: web: gunicorn winnietheodashboard:server

On the configuration page, specify:

After you select and connect the repository, you'll be taken to a configuration page. This is where you tell Render the details about your application within that repository.
On this configuration page, you'll specify:
Name: winnietheo-dashboard (used as URL in next steps)
Branch: (e.g., main or master)
Root Directory: If the necessary files (requirements.txt, ProcFile and data files are directly located in the top-level (root), leave option blank.
If files are within subfolder (i.e. data) then use my-dash-app (or e.g. winnietheo-dashboard).
Runtime: Render should likely auto-detect Python.
Build Command: Usually pip install -r requirements.txt (auto-populated).
Start Command: This is where you specifically reference your Python file name. It should be gunicorn winnietheo-dashboard:server.

Recap:
GitHub Account -> Select Repository -> Configure Service (tell Render about the winnietheo-dashboard.py within that repo via the Start Command and Root Directory).
