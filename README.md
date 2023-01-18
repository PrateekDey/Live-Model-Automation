# LIVE-CUBE-AUTOMATION

_Automating the process of onboarding where tenant can provide inputs for the tenant_name, usecase, environment and the tenant will be automatically onboarded onto Insights environment._

---

[Repository link](https://source.syncron.team/admin/repos/pm/analytics/live-models-automation)

Repository Structure:
The structure of the project is following:
 
* dev-requirements.txt - main project requirements 
* requirements-test.txt - tests requirements for tox (no need to install them manually)
* tox.ini - the Tox configuration file 
* main.py - the main tool executable file
* app/api - contains all the API functionality(sisense API's)
* app/aws - contains usage of aws features
* tests/ - component tests and test data

---

**How to run the project?**
* Run app.main.py file


**How to run the test cases?**
* Command = pytest

