-----
#Predictive maintenance repo

--> The repo contains the code used for the solution, a detailed document can be found inside the "Documents" folder

Problem we are addressing :

The time consuming nature of machine maintenance in large manufacturing and industrial
processes, most of the troubleshooting and fault finding when a machine fails is done
manually and as a result requires long hours and sometimes days. To address this we
propose a solution to enable individuals with the foresight to rapidly resolve issues.

### Why manufacturing you might ask?

[Source : https://www.siemens.com/global/en/products/automation/topic-areas/artificial-intelligence-in-industry.html](https://www.siemens.com/global/en/products/automation/topic-areas/artificial-intelligence-in-industry.html)

The manufacturing industry faces challenges in :

   - The trustworthiness of the AI systems(should it be trusted over human intuition)

   - Lack of experts in the field working in these companies

   - Producing reliable insights with the data

AI/ML will be tools that enhance overall work in terms of production forecasting and
machine maintenance. Most manufacturing companies use IOT enabled devices to allow for
communication between different components on their factory floor. This presents us with
the opportunity not just to gather the different data points and gain meaningful insights from
them but also as a way to educate individuals from floor managers to machine operators to
become more familiar with the systems. At the core the predictive maintenance solution aims
to address a common issue in the field of industrial automation where fault finding and
repairs in large machines are time consuming, the solution aims to reduce the overall
duration of the process

Recently Siemens has partnered with Microsoft to create an Industrial copilot, Combining
Siemens’ unique domain know-how across industries with Microsoft Azure OpenAI Service,


-----

the Copilot further improves handling of rigorous requirements in manufacturing and
automation. Which has shown the overall appetite for AI/ML solutions in the Industry.

**_“The collaboration between Siemens and Microsoft marks a pivotal moment in the_**
**_industrial sector; one where AI Transformation becomes a cornerstone for innovation_**
**_and operational efficiency,” said Judson Althoff, executive vice president and chief_**
**_commercial officer at Microsoft._**
**_Source :_**
**_[https://press.siemens.com/global/en/pressrelease/siemens-and-microsoft-scale-industrial-ai?%3Fstc=press_cm](https://press.siemens.com/global/en/pressrelease/siemens-and-microsoft-scale-industrial-ai?%3Fstc=press_cm)_**

Note : access to the S7-1200 PLC was restricted and for demo purposes we will be using a publicly
available dataset

Solution :
A Webapp that can predict the machines overall likelihood of failure and visualise important KPIs

Working methodology :

   - Data from the PLC (Siemens S7 1200) is put into onelake via a tabular data stream

from the siemens PLC

Full documentation can be found :
[Connecting a S7-1200 PLC / S7-1500 PLC to a SQL Database - ID: 109779336 -](https://support.industry.siemens.com/cs/document/109779336/connecting-a-s7-1200-plc-s7-1500-plc-to-a-sql-database-?dti=0&lc=en-IN)
[Industry Support Siemens](https://support.industry.siemens.com/cs/document/109779336/connecting-a-s7-1200-plc-s7-1500-plc-to-a-sql-database-?dti=0&lc=en-IN)

   - The data in OneLake is then preprocessed, as well as engineered with new features
the preprocessed data is then used to train a machine learning model, the model is
then saved and used to make predictions of data that can either be uploaded as a
csv or manually input

   - Visualisations will be handled inside the webapp by the individual toggling on which
visualisations they want


-----

To visualise the flow of data from start to finish see image below :

## The Web App :

On the landing page the user is prompted to upload a dataset


-----

The moment the CSV is uploaded you get notified, with a small tabular visualisation

On the analytics side, the the moment the user clicks on the analytics a new window
pops up and gives different visualisations available to the user


-----

Other Visualization


-----
