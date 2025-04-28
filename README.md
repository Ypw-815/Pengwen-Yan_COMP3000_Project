SUPPORT SENSE --Efficient sentiment analysis tools
1. Project Overview
	This project focuses on building an innovative sentiment analysis system that can efficiently and accurately classify the sentiment of texts, and provides a valuable reference for practical applications in the field of natural language processing.
2. the technology stack
	1. Development tools: PyCharm is used as the main development tool, and its powerful code editing, debugging and project management functions are used to improve development efficiency.
	2. Backend framework: Using the Django framework to build the backend, Django provides rich built-in functions, such as database management, user authentication, etc., to facilitate the implementation of the system's business logic.
	3. Front-end technology: use HTML/CSS/JS for front-end page development. HTML is responsible for building the page structure, CSS is used for page style design, and JS realizes front-end interaction to provide users with a good operation experience.
	4. Database: The SQLite database system is used to store the data needed to run, and its lightweight features are suitable for the needs of the project, and it is easy to deploy and manage.
	5. Models: Explore the application of DeepSeek and Transform models in sentiment analysis tasks, and use the advantages of these models to achieve accurate text sentiment classification.
3. Project structure
	1. Backend: In the Django project directory, there are multiple application modules. For example, the "sentiment_analysis_app" application is responsible for handling the core business logic of sentiment analysis, including invoking models for text analysis, interacting with databases, and so on. The "admin" app is used to manage the background settings of the system; The "urls.py" file configures the URL route of the project and maps different requests to the corresponding view functions for processing.
	2. Front-end: The front-end files are stored in the "templates" folder, which are divided into different HTML pages according to function, such as "input.html" for user input text, and "result.html" to display sentiment analysis results. The CSS style file is placed in the "static/css" directory to manage the page style in a unified manner. The JS script file is located in the "static/js" directory and implements page interaction functions, such as button click event processing, asynchronous data transfer, etc.
	3. Database: The SQLite database file is stored in the root directory of the project, containing user input records, model training data and other related data tables, and the data can be added, deleted, modified and queried through Django's database operation interface.
4.the operating environment
	1. Software requirements: Make sure that the system is installed with Python environment, and it is recommended to use Python 3.8 or later. At the same time, you need to install the PyCharm development tools, as well as various libraries required by the project, which can be installed with the following commands:
```bash
pip install django
pip install sqlite3
```
	2. Hardware requirements: An ordinary personal computer can meet the needs of the project, and at least 4GB of memory is recommended to ensure the performance of the system when processing text analysis tasks. 
5. Project Initiation and Use 
	1. Start the backend service: Open the project in PyCharm, go to the root directory of the project, and run the following command in the terminal to start the Django service: '''bash python manage.py runserver ''' After the service is started, you can access the specified local address (such as http://127.0.0.1:8000/ in the browser to view the system front-end page. 
	2. How to use: Enter the text content to be analyzed on the front-end input page, click the "Analyze" button, the system will call the back-end sentiment analysis model for processing, and display the analysis results on the result page to determine the sentiment tendency of the text as positive, negative or neutral. 
6. Model Training and Optimization 
	1. Data preparation: A large amount of annotated text data is collected and divided into training sets, validation sets, and test sets according to a certain proportion for model training and evaluation. 
	2. Training process: Using the collected data, the model is trained based on DeepSeek and Transform, and the hyperparameters of the model, such as learning rate and iteration times, are adjusted to improve the accuracy and generalization ability of the model. During training, techniques such as cross-validation can be used to evaluate model performance. 
	3. Optimization measures: Adopt data augmentation techniques, such as randomly replaceing, inserting, and deleting words in text, to expand the diversity of training data; The model fusion strategy is used to combine multiple different models to comprehensively improve the accuracy and stability of sentiment analysis.
	
student name: Pengwen Yan student ID: 10923964
teacher name: Dr. Haoyi Wang
	
	
	
