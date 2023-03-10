# Flask Audio Uploader

This respository is a Flask webpage used to upload audio files to a server. It's based on an interally used website I built (originally on a WAMP stack) back in 2018 as a research assistant at the Child Mind Institute, specifically for the [Healthy Brain Network Initiative](https://childmind.org/science/global-open-science/healthy-brain-network/), a large-scale research study on biomarkers of mental health disorders and part of an intiative to openly share anonymized research data with the scientific community. 

The study includes voice data collected from patients while they verbaly respond to a series of questionnaire from research staff. Because of the high participant volume of the study, I was tasked with creating this website in order to allow research staff to upload audio files without having to worry about organizing or naming them, as well as save time for whomever would be analyzing the data in the future. I also added checks to make sure users wouldn't enter incorrect information like participant ID's.

### Python Packages
- Flask
- WTForm
- Werkzeug
- os
- json

### Misc
I ran the following Python code to generate a list of random participant ID's, then manually imported it into a database:

```
import pandas as pd
import random`
df = pd.DataFrame(data = {'id': range(1, 201), 'participant_id': random.sample(range(10000, 100000), k = 200)})
df.to_csv('participant_id.csv', index = False)
```
