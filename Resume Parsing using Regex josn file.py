{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"name":"python","version":"3.10.12","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"},"kaggle":{"accelerator":"none","dataSources":[{"sourceId":10572034,"sourceType":"datasetVersion","datasetId":6541965}],"dockerImageVersionId":30839,"isInternetEnabled":true,"language":"python","sourceType":"notebook","isGpuEnabled":false}},"nbformat_minor":4,"nbformat":4,"cells":[{"source":"<a href=\"https://www.kaggle.com/code/bharathkumar1011/resume-parsing-using-regex-josn-file?scriptVersionId=222466202\" target=\"_blank\"><img align=\"left\" alt=\"Kaggle\" title=\"Open in Kaggle\" src=\"https://kaggle.com/static/images/open-in-kaggle.svg\"></a>","metadata":{},"cell_type":"markdown"},{"cell_type":"code","source":"!pip install -qU langchain_community\n!pip install pdfplumber","metadata":{"trusted":true,"execution":{"iopub.status.busy":"2025-02-14T05:20:08.195026Z","iopub.execute_input":"2025-02-14T05:20:08.195262Z","iopub.status.idle":"2025-02-14T05:20:25.113588Z","shell.execute_reply.started":"2025-02-14T05:20:08.195236Z","shell.execute_reply":"2025-02-14T05:20:25.112485Z"}},"outputs":[],"execution_count":null},{"cell_type":"code","source":"import re\nfrom langchain_community.document_loaders import PDFPlumberLoader","metadata":{"trusted":true,"execution":{"iopub.status.busy":"2025-02-14T05:22:03.811447Z","iopub.execute_input":"2025-02-14T05:22:03.811888Z","iopub.status.idle":"2025-02-14T05:22:05.220975Z","shell.execute_reply.started":"2025-02-14T05:22:03.811854Z","shell.execute_reply":"2025-02-14T05:22:05.219949Z"}},"outputs":[],"execution_count":null},{"cell_type":"code","source":"pdf_path = \"/kaggle/input/test-res-regex/Steve Sun - Resume (2).pdf\"","metadata":{"trusted":true,"execution":{"iopub.status.busy":"2025-02-14T05:22:15.582899Z","iopub.execute_input":"2025-02-14T05:22:15.583401Z","iopub.status.idle":"2025-02-14T05:22:15.58751Z","shell.execute_reply.started":"2025-02-14T05:22:15.583366Z","shell.execute_reply":"2025-02-14T05:22:15.586606Z"}},"outputs":[],"execution_count":null},{"cell_type":"code","source":"def extract_text_pdf(pdf_path):\n        loader = PDFPlumberLoader(pdf_path)\n        docs = loader.load()\n        text = ''\n        for doc in docs:\n            text += doc.page_content # Append extracted text\n        return text \n\n\ndef extract_name_from_resume(text):\n    name = None\n\n    # Use regex pattern to find a potential name\n    pattern = r\"(\\b[A-Z][a-z]+\\b)\\s(\\b[A-Z][a-z]+\\b)\"\n    match = re.search(pattern, text)\n    if match:\n        name = match.group()\n\n    return name\n\ndef extract_email_from_resume(text):\n    email = None\n\n    # Use regex pattern to find a potential email address\n    pattern = r\"\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\\b\"\n    match = re.search(pattern, text)\n    if match:\n        email = match.group()\n\n    return email\n\n\ndef extract_skills_from_resume(text, skills_list):\n    skills = []\n\n    # Search for skills in the resume text\n    for skill in skills_list:\n        pattern = r\"\\b{}\\b\".format(re.escape(skill))\n        match = re.search(pattern, text, re.IGNORECASE)\n        if match:\n            skills.append(skill)\n\n    return skills\n\n\ndef extract_education_details(text):\n\n    pattern = r\"(?P<university>[\\w\\s,&]+(?:University|College|Institute|Academy))\\n(?P<degree>.+?)\\s(?:-\\s(?P<gpa>\\d\\.\\d{1,2}\\sGPA))?\\s(?P<start_date>\\w+\\s\\d{4})\\s(?:[-–]\\s(?P<end_date>\\w+\\s\\d{4}))?\"\n\n    matches = re.finditer(pattern, text)\n    \n    education_dict = {\n        \"University\": [],\n        \"Degree\": [],\n        \"GPA\": [],\n        \"Start Date\": [],\n        \"End Date\": [],\n    }\n    \n    # Extract and organize data\n    for match in matches:\n        education_dict[\"University\"].append(match.group(\"university\").strip())\n        education_dict[\"Degree\"].append(match.group(\"degree\").strip())\n        education_dict[\"GPA\"].append(match.group(\"gpa\").strip() if match.group(\"gpa\") else \"N/A\")\n        education_dict[\"Start Date\"].append(match.group(\"start_date\").strip())\n        education_dict[\"End Date\"].append(match.group(\"end_date\").strip() if match.group(\"end_date\") else \"Present\")\n    \n    return education_dict\n\n\ndef extracting_experirnce(text):\n        \n    matches = re.search(pattern, text, re.DOTALL)\n    \n    if matches:\n        work = matches.group(1).strip()\n        return work\n","metadata":{"trusted":true,"execution":{"iopub.status.busy":"2025-02-14T05:22:21.011108Z","iopub.execute_input":"2025-02-14T05:22:21.01145Z","iopub.status.idle":"2025-02-14T05:22:21.100441Z","shell.execute_reply.started":"2025-02-14T05:22:21.011419Z","shell.execute_reply":"2025-02-14T05:22:21.099401Z"}},"outputs":[],"execution_count":null},{"cell_type":"code","source":"text = extract_text_pdf(pdf_path)\nskills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau','AI',\n'Data Visualization','Statistical Analysis','Big Data','Cloud Technologies''Problem-Solving','Critical Thinking',\n'Storytelling']\npattern = r\"WORK EXPERIENCE\\n(.*?)\\nEDUCATION\"\n\n# below is the general pattern for the experience extraction\n# pattern =  r\"(?i)(work\\s*experience|professional\\s*experience|employment\\s*history)[\\s\\S]*?(?=(education|skills|projects|$))\"","metadata":{"trusted":true,"execution":{"iopub.status.busy":"2025-02-14T05:22:25.110866Z","iopub.execute_input":"2025-02-14T05:22:25.11121Z","iopub.status.idle":"2025-02-14T05:22:25.39875Z","shell.execute_reply.started":"2025-02-14T05:22:25.11118Z","shell.execute_reply":"2025-02-14T05:22:25.397813Z"}},"outputs":[],"execution_count":null},{"cell_type":"code","source":"output = {\n    \"Name\": extract_name_from_resume(text),\n    \"Email\": extract_email_from_resume(text),\n    \"Skills\":extract_skills_from_resume(text, skills_list),\n    \"Education\": extract_education_details(text),\n    \"Experience\": extracting_experirnce(text),\n}","metadata":{"trusted":true,"execution":{"iopub.status.busy":"2025-02-14T05:22:25.399828Z","iopub.execute_input":"2025-02-14T05:22:25.400205Z","iopub.status.idle":"2025-02-14T05:22:25.409813Z","shell.execute_reply.started":"2025-02-14T05:22:25.400182Z","shell.execute_reply":"2025-02-14T05:22:25.408658Z"}},"outputs":[],"execution_count":null},{"cell_type":"code","source":"import json","metadata":{"trusted":true,"execution":{"iopub.status.busy":"2025-02-14T05:22:50.882702Z","iopub.execute_input":"2025-02-14T05:22:50.883034Z","iopub.status.idle":"2025-02-14T05:22:50.887227Z","shell.execute_reply.started":"2025-02-14T05:22:50.883008Z","shell.execute_reply":"2025-02-14T05:22:50.886232Z"}},"outputs":[],"execution_count":null},{"cell_type":"code","source":"with open('resume_Regex.json', 'w') as json_file:\n    json.dump(output, json_file, indent=4)","metadata":{"trusted":true,"execution":{"iopub.status.busy":"2025-02-14T05:22:52.120721Z","iopub.execute_input":"2025-02-14T05:22:52.121037Z","iopub.status.idle":"2025-02-14T05:22:52.125651Z","shell.execute_reply.started":"2025-02-14T05:22:52.121014Z","shell.execute_reply":"2025-02-14T05:22:52.124807Z"}},"outputs":[],"execution_count":null},{"cell_type":"code","source":"print(output)","metadata":{"trusted":true,"execution":{"iopub.status.busy":"2025-02-14T05:23:09.950956Z","iopub.execute_input":"2025-02-14T05:23:09.951302Z","iopub.status.idle":"2025-02-14T05:23:09.955952Z","shell.execute_reply.started":"2025-02-14T05:23:09.951272Z","shell.execute_reply":"2025-02-14T05:23:09.954896Z"}},"outputs":[],"execution_count":null},{"cell_type":"code","source":"","metadata":{"trusted":true},"outputs":[],"execution_count":null}]}