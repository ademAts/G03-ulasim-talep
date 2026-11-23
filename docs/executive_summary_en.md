# Executive Summary: Istanbul Public Transportation Demand & Weather Impact

**Project:** P3 - G03 (Time-Based Regression)  
**Lead Data Engineer:** Adem Atas (Student ID: 24430040022)  
**Course:** AI for Decision Making - Management Information Systems, Mersin University  

---

### Abstract & Problem Statement
Urban mobility in mega-cities like Istanbul heavily depends on public transportation networks comprising buses, subways, ferries, and metrobus corridors. Adverse weather conditions (such as heavy rainfall, extreme temperatures, and gale-force wind gusts) combined with temporal variations (rush hours, official holidays, and school calendar shifts) trigger significant fluctuations in passenger volumes. This project addresses the operational challenge faced by the Istanbul Metropolitan Municipality (IBB): *predicting hourly transport demand to proactively manage fleet capacities and schedule supplemental services before bottlenecks occur.*

### Data Engineering & Integration Methodology
To enable robust machine learning modeling without overwhelming computational memory limits, an automated data extraction and aggregation pipeline was built. Three months of high-resolution BELBİM transit pass records (July 1, 2024 to September 30, 2024; exceeding 15 million raw transactions) were processed using chunk-based stream processing. Hourly passenger totals were aggregated across transport modes and municipal districts, yielding a clean dataset of 70,235 hourly observation points. 

Using historical meteorology APIs (Open-Meteo), micro-climate features—ambient surface temperature (2m), hourly precipitation levels (mm), and wind velocity metrics—were joined with the spatial mobility data. Furthermore, calendar features (day-of-week, weekend flags, national holidays, holiday-eve effects, and academic session flags) were engineered to capture macro-level behavioral shifts.

### Strategic Findings & Operational Insights
Empirical analyses reveal that intense rainfall shifts intercontinental transit demand drastically away from maritime ferries towards underground rail and metrobus systems (+18% to +26% surge in transit corridors such as Kadikoy and Sisli during peak hours). The preprocessed feature matrix serves as an enterprise-grade foundation for regression baselines, gradient boosting models, and real-time Streamlit scenario simulators.
