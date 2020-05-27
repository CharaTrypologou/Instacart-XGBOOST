{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "_uuid": "443133c6e567ca1e3bf8d14626e52a2b39dc5ee4"
   },
   "source": [
    "# Introduction\n",
    "This kernel has been created by the [Information Systems Lab](http://islab.uom.gr) to introduce students of the [University of Macedonia](http://www.uom.gr/index.php?tmima=2&categorymenu=2), Greece to Machine Learning & Data Science.\n",
    "\n",
    "## The Instacart competition\n",
    "Instacart is an American company that operates as a same-day grocery delivery service. Customers select groceries through a web application from various retailers and delivered by a personal shopper. Instacart's service is mainly provided through a smartphone app, available on iOS and Android platforms, apart from its website.\n",
    "\n",
    "In 2017 Instacart organised a Kaggle competition and provided to the community a sample dataset of over 3 million grocery orders from more than 200,000 Instacart users. The orders include 32 million basket items and 50,000 unique products. The objective of the competition was participants to **predict which previously purchased products will be in a user’s next order**.\n",
    "\n",
    "## Objective\n",
    "The objective of this Kernel is to introduce students to predictive business analytics with Python through the Instacart case. \n",
    "\n",
    "By the time you finish this example, you will be able to:\n",
    "* Describe the steps of creating a predictive analytics model\n",
    "* Use Python and Pandas package to manipulate data\n",
    "* Use Python and Pandas package to create, combine, and delete DataFrames\n",
    "* Use Random Forests to create a predictive model\n",
    "* Apply the predictive model in order to make a prediction\n",
    "* Create a submission file for the competition of Instacart\n",
    "\n",
    "## Problem definition\n",
    "The data that Instacart opened up include orders of 200,000 Instacart users with each user having between 4 and 100 orders. Instacart indicates each order in the data as prior, train or test. Prior orders describe the **past behaviour** of a user while train and test orders regard the **future behaviour that we need to predict**. \n",
    "\n",
    "As a result, we want to predict which previously purchased products (prior orders) will be in a user’s next order (train and test orders). \n",
    "\n",
    "For the train orders Instacart reveals the results (i.e., the ordered products) while for the test orders we do not have this piece of information. Moreover, the future order of each user can be either train or test meaning that each user will be either a train or a test user. \n",
    "\n",
    "The setting of the Instacart problem is described in the figure below (orders with yellow color denotes future orders of a user). \n",
    "\n",
    "<img src=\"https://i.imgur.com/S0Miw3m.png\" width=\"350\">\n",
    "\n",
    "Each user has purchased various products during their prior orders. Moreover, for each user we know the order_id of their future order. The goal is to predict which of these products will be in a user's future order. \n",
    "\n",
    "This is a **classification problem** because we need to predict whether each pair of user and product is a reorder or not. This is indicated by the value of the reordered variable, i.e. reordered=1 or reordered=0 (see figure below). \n",
    "\n",
    "<img src=\"https://i.imgur.com/SxK2gsR.png\" width=\"350\">\n",
    "\n",
    "As a result we need to come up and calculate various **predictor variables (X)** that will describe the characteristics of a product and the behaviour of a user regarding one or multiple products. We will do so by analysing the prior orders of the dataset. We will then use the train users to create a predictive model and the test users to make our actual prediction. As a result we create a table as the following one and we train an algorithm based on predictor variables (X) and response variable (Y).\n",
    "\n",
    "<img src=\"https://i.imgur.com/Yb1CKAF.png\" width=\"600\">\n",
    "\n",
    "## Method\n",
    "Our method includes the following steps:\n",
    "1. <b>Import and reshape data</b>: This step includes loading CSV files into pandas DataFrames, tranform character variables to categorical variables, and create a supportive table.\n",
    "2. <b>Create predictor variables</b>: This step includes identifying and calculating predictor variables (aka features) from the initial datasets provided by Instacart. \n",
    "3. <b>Create train and test DataFrames</b>: In this step we create two distinct pandas DataFrames that will be used in the creation and the use of the predictive model.\n",
    "4. <b>Create predictive model (fit)</b>: In this step we train a predictive model through the train dataset.\n",
    "5. <b>Apply predictive model (predict)</b>: This step includes applying the model to predict the 'reordered' variable for the test dataset.\n",
    "6. <b>Create submission file</b>: In this final step we create the submission file with our predictions for Instacart's competition.\n",
    "7. <b>Get F1 score</b>: In this step we submit the produced and file and get the F1 score describing the accuracy of our prediction model."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "_cell_guid": "79c7e3d0-c299-4dcb-8224-4455121ee9b0",
    "_uuid": "d629ff2d2480ee46fbb7e2d37f6b5fab8052498a"
   },
   "source": [
    "# 1. Import and Reshape Data \n",
    "First we load the necessary Python packages and then we import the CSV files that were provided by Instacart.\n",
    "\n",
    "## 1.1 Import the required packages\n",
    "The garbage collector (package gc), attempts to reclaim garbage, or memory occupied by objects (e.g., DataFrames) that are no longer in use by Python ([ref1](https://www.techopedia.com/definition/1083/garbage-collection-gc-general-programming), [ref2](https://en.wikipedia.org/wiki/Garbage_collection_(computer_science)). This package will eliminate our risk to exceed the 16GB threshold of available RAM that Kaggle offers.\n",
    "\n",
    "The **\"as\"** reserved word is to define an alias to the package. The alias help us to call easier a package in our code."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "_uuid": "ade7494679114eee3921819b364693735e49bc5f"
   },
   "outputs": [],
   "source": [
    "# For data manipulation\n",
    "import pandas as pd         \n",
    "\n",
    "# Garbage Collector to free up memory\n",
    "import gc                         \n",
    "gc.enable()                       # Activate "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "_uuid": "fb44963ea70a3c8e599e6a02332af8eb5ac2c462"
   },
   "source": [
    "## 1.2 Load data from the CSV files\n",
    "Instacart provides 6 CSV files, which we have to load into Python. Towards this end, we use the .read_csv() function, which is included in the Pandas package. Reading in data with the .read_csv( ) function returns a DataFrame.\n",
    "\n",
    "First we connect to the Kaggle API in order to download the zip file with the 6 CSVs. Then we unzip it in a new folder named input, and we unzip all the zip files."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'google'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-5-1f91c8dc83b1>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;31m#This is for Google Colab\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 2\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0mgoogle\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcolab\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mfiles\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      3\u001b[0m \u001b[0mfiles\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mupload\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;31m#upload kaggle.json\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0mget_ipython\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msystem\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'pip install -q kaggle'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'google'"
     ]
    }
   ],
   "source": [
    "#This is for Google Colab\n",
    "from google.colab import files\n",
    "files.upload() #upload kaggle.json\n",
    "\n",
    "!pip install -q kaggle\n",
    "!mkdir -p ~/.kaggle\n",
    "!cp kaggle.json ~/.kaggle/\n",
    "!ls ~/.kaggle\n",
    "!chmod 600 /root/.kaggle/kaggle.json"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# connect to kaggle api and download files (zip)\n",
    "from kaggle.api.kaggle_api_extended import KaggleApi\n",
    "api = KaggleApi({\"username\":\"evangeloskalampokis\",\"key\":\"227307bd0d825ea8f784cb00dc373357\"})\n",
    "api.authenticate()\n",
    "files = api.competition_download_files(\"Instacart-Market-Basket-Analysis\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import zipfile\n",
    "with zipfile.ZipFile('Instacart-Market-Basket-Analysis.zip', 'r') as zip_ref:\n",
    "    zip_ref.extractall('./input')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "working_directory = os.getcwd()+'/input'\n",
    "os.chdir(working_directory)\n",
    "for file in os.listdir(working_directory):   # get the list of files\n",
    "    if zipfile.is_zipfile(file): # if it is a zipfile, extract it\n",
    "        with zipfile.ZipFile(file) as item: # treat the file as a zip\n",
    "           item.extractall()  # extract it in the working directory"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "_uuid": "3fd1053c5df37c229f665db95a5de680ecb13490"
   },
   "outputs": [],
   "source": [
    "orders = pd.read_csv('../input/orders.csv' )\n",
    "order_products_train = pd.read_csv('../input/order_products__train.csv')\n",
    "order_products_prior = pd.read_csv('../input/order_products__prior.csv')\n",
    "products = pd.read_csv('../input/products.csv')\n",
    "aisles = pd.read_csv('../input/aisles.csv')\n",
    "departments = pd.read_csv('../input/departments.csv')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This step results in the following DataFrames:\n",
    "* <b>orders</b>: This table includes all orders, namely prior, train, and test. It has single primary key (<b>order_id</b>).\n",
    "* <b>order_products_train</b>: This table includes training orders. It has a composite primary key (<b>order_id and product_id</b>) and indicates whether a product in an order is a reorder or not (through the reordered variable).\n",
    "* <b>order_products_prior </b>: This table includes prior orders. It has a composite primary key (<b>order_id and product_id</b>) and indicates whether a product in an order is a reorder or not (through the reordered variable).\n",
    "* <b>products</b>: This table includes all products. It has a single primary key (<b>product_id</b>)\n",
    "* <b>aisles</b>: This table includes all aisles. It has a single primary key (<b>aisle_id</b>)\n",
    "* <b>departments</b>: This table includes all departments. It has a single primary key (<b>department_id</b>)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "If you want to reduce the execution time of this Kernel you can use the following piece of code by uncomment it. This will trim the orders DataFrame and will keep a 10% random sample of the users. You can use this for experimentation."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "#### Remove triple quotes to trim your dataset and experiment with your data\n",
    "### COMMANDS FOR CODING TESTING - Get 10% of users \n",
    "###orders = orders.loc[orders.user_id.isin(orders.user_id.drop_duplicates().sample(frac=0.1, random_state=25))] \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We now use the .head( ) method in order to visualise the first 10 rows of these tables. Click the Output button below to see the tables."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "_kg_hide-output": true
   },
   "outputs": [],
   "source": [
    "orders.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "_kg_hide-output": true
   },
   "outputs": [],
   "source": [
    "order_products_train.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "_kg_hide-output": true
   },
   "outputs": [],
   "source": [
    "order_products_prior.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "_kg_hide-output": true
   },
   "outputs": [],
   "source": [
    "products.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "_kg_hide-output": true
   },
   "outputs": [],
   "source": [
    "aisles.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "_kg_hide-output": true
   },
   "outputs": [],
   "source": [
    "departments.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1.3 Reshape data\n",
    "We transform the data in order to facilitate their further analysis. First, we convert character variables into categories so we can use them in the creation of the model. In Python, a categorical variable is called category and has a fixed number of different values."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'aisles' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-6-8df6f60717ac>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;31m# We convert character variables into category.\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0;31m# In Python, a categorical variable is called category and has a fixed number of different values\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 3\u001b[0;31m \u001b[0maisles\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'aisle'\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0maisles\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'aisle'\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mastype\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'category'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      4\u001b[0m \u001b[0mdepartments\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'department'\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdepartments\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'department'\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mastype\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'category'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0morders\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'eval_set'\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0morders\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'eval_set'\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mastype\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'category'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mNameError\u001b[0m: name 'aisles' is not defined"
     ]
    }
   ],
   "source": [
    "# We convert character variables into category. \n",
    "# In Python, a categorical variable is called category and has a fixed number of different values\n",
    "aisles['aisle'] = aisles['aisle'].astype('category')\n",
    "departments['department'] = departments['department'].astype('category')\n",
    "orders['eval_set'] = orders['eval_set'].astype('category')\n",
    "products['product_name'] = products['product_name'].astype('category')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1.4 Create a DataFrame with the orders and the products that have been purchased on prior orders (op)\n",
    "We create a new DataFrame, named <b>op</b> which combines (merges) the DataFrames <b>orders</b> and <b>order_products_prior</b>. Bear in mind that <b>order_products_prior</b> DataFrame includes only prior orders, so the new DataFrame <b>op</b>  will contain only these observations as well. Towards this end, we use pandas' merge function with how='inner' argument, which returns records that have matching values in both DataFrames. \n",
    "<img src=\"https://i.imgur.com/zEK7FpY.jpg\" width=\"400\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Merge the orders DF with order_products_prior by their order_id, keep only these rows with order_id that they are appear on both DFs\n",
    "op = orders.merge(order_products_prior, on='order_id', how='inner')\n",
    "op.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The table contains for all the customers **(user_id)**: <br>\n",
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ➡︎ the orders **(order_id)** that they have placed accompanied with: <br>\n",
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ➡︎ the products **(product_id)** that have been bought in each order"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 2. Create Predictor Variables\n",
    "We are now ready to identify and calculate predictor variables based on the provided data. We can create various types of predictors such as:\n",
    "* <b>User predictors</b> describing the behavior of a user e.g. total number of orders of a user.\n",
    "* <b>Product predictors</b> describing characteristics of a product e.g. total number of times a product has been purchased.\n",
    "* <b>User & product predictors</b> describing the behavior of a user towards a specific product e.g. total times a user ordered a specific product."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2.1 Create user predictors\n",
    "We create the following predictors:\n",
    "- 2.1.1 Number of orders per customer\n",
    "- 2.1.2 How frequent a customer has reordered products\n",
    "\n",
    "### 2.1.1 Number of orders per customer\n",
    "We calculate the total number of placed orders per customer. We create a **user** DataFrame to store the results."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## First approach in one step:\n",
    "# Create distinct groups for each user, identify the highest order number in each group, save the new column to a DataFrame\n",
    "user = op.groupby('user_id')['order_number'].max().to_frame('u_total_orders')\n",
    "user.head()\n",
    "\n",
    "## Second approach in two steps: \n",
    "#1. Save the result as DataFrame with Double brackets --> [[ ]] \n",
    "#user = op.groupby('user_id')[['order_number']].max()\n",
    "#2. Rename the label of the column\n",
    "#user.columns = ['u_total_orders']\n",
    "#user.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Reset the index of the DF so to bring user_id from index to column (pre-requisite for step 2.4)\n",
    "user = user.reset_index()\n",
    "user.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.1.2 How frequent a customer has reordered products\n",
    "\n",
    "This feature is a ratio which shows for each user in what extent has products that have been reordered in the past: <br>\n",
    "So we create the following ratio: <br>\n",
    "\n",
    "<img src=\"https://latex.codecogs.com/gif.latex?\\dpi{120}&space;\\large&space;probability\\&space;reordered\\&space;(user\\_id)=&space;\\frac{total\\&space;times\\&space;of\\&space;reorders}{total\\&space;number\\&space;of\\&space;purchased\\&space;products\\&space;from\\&space;all\\&space;baskets}\" title=\"probability\\ reordered\\ (user\\_id)= \\frac{total\\ times\\ of\\ reorders}{total\\ number\\ of\\ purchased\\ products\\ from\\ all\\ baskets}\" />\n",
    "\n",
    "The nominator is a counter for all the times a user has reordered products (value on reordered=1), the denominator is a counter of all the products that have been purchased on all user's orders (reordered=0 & reordered=1).\n",
    "\n",
    "E.g., for a user that has ordered 6 products in total, where 3 times were reorders, the ratio will be:\n",
    "\n",
    "![example ratio](https://latex.codecogs.com/gif.latex?\\dpi{120}&space;\\large&space;&space;mean=&space;\\frac{0&plus;1&plus;0&plus;0&plus;1&plus;1}{6}&space;=&space;0,5) \n",
    "\n",
    "To create the above ratio we .groupby() order_products_prior by each user and then calculate the mean of reordered.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "u_reorder = op.groupby('user_id')['reordered'].mean().to_frame('u_reordered_ratio')\n",
    "u_reorder = u_reorder.reset_index()\n",
    "u_reorder.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The new feature will be merged with the user DataFrame (section 2.1.1) which keep all the features based on users. We perform a left join as we want to keep all the users that we have created on the user DataFrame\n",
    "\n",
    "<img src=\"https://i.imgur.com/wMmC4hb.jpg\" width=\"400\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "user = user.merge(u_reorder, on='user_id', how='left')\n",
    "\n",
    "del u_reorder\n",
    "gc.collect()\n",
    "\n",
    "user.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2.2 Create product predictors\n",
    "We create the following predictors:\n",
    "- 2.2.1 Number of purchases for each product\n",
    "- 2.2.2 What is the probability for a product to be reordered\n",
    "\n",
    "### 2.2.1 Number of purchases for each product\n",
    "We calculate the total number of purchases for each product (from all customers). We create a **prd** DataFrame to store the results."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create distinct groups for each product, count the orders, save the result for each product to a new DataFrame  \n",
    "prd = op.groupby('product_id')['order_id'].count().to_frame('p_total_purchases')\n",
    "prd.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Reset the index of the DF so to bring product_id rom index to column (pre-requisite for step 2.4)\n",
    "prd = prd.reset_index()\n",
    "prd.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2.2.2 What is the probability for a product to be reordered\n",
    "In this section we want to find the products which have the highest probability of being reordered. Towards this end it is necessary to define the probability as below:\n",
    "<img src=\"https://latex.codecogs.com/gif.latex?\\dpi{150}&space;\\large&space;probability\\&space;reordered\\&space;(product\\_id)=&space;\\frac{number\\&space;of\\&space;reorders}{total\\&space;number\\&space;of\\&space;orders\\&space;}\" title=\"probability\\ reordered\\ (product\\_id)= \\frac{number\\ of\\ reorders}{total\\ number\\ of\\ orders\\ }\" />\n",
    "\n",
    "Example: The product with product_id=2 is included in 90 purchases but only 12 are reorders. So we have:  \n",
    "\n",
    "<img src=\"https://latex.codecogs.com/gif.latex?\\dpi{150}&space;\\large&space;p\\_reorder\\(product\\_id\\mathop{==}&space;2&space;)=&space;\\frac{12}{90}=&space;0,133\" title=\"\\large p\\_reorder\\(product\\_id\\mathop{==} 2 )= \\frac{12}{90}= 0,133\" />\n",
    "\n",
    "### 2.2.2.1 Remove products with less than 40 purchases - Filter with .shape[0]\n",
    "Before we proceed to this estimation, we remove all these products that have less than 40 purchases in order the calculation of the aforementioned ratio to be meaningful.\n",
    "\n",
    "Using .groupby() we create groups for each product and using .filter( ) we keep only groups with more than 40 rows. Towards this end, we indicate a lambda function."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# execution time: 25 sec\n",
    "# the x on lambda function is a temporary variable which represents each group\n",
    "# shape[0] on a DataFrame returns the number of rows\n",
    "p_reorder = op.groupby('product_id').filter(lambda x: x.shape[0] >40)\n",
    "p_reorder.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.2.2.2 Group products, calculate the mean of reorders\n",
    "\n",
    "To calculate the reorder probability we will use the aggregation function mean() to the reordered column. In the reorder data frame, the reordered column indicates that a product has been reordered when the value is 1.\n",
    "\n",
    "The .mean() calculates how many times a product has been reordered, divided by how many times has been ordered in total. \n",
    "\n",
    "E.g., for a product that has been ordered 9 times in total, where 4 times has been reordered, the ratio will be:\n",
    "\n",
    "![example ratio](https://latex.codecogs.com/gif.latex?\\dpi{120}&space;\\large&space;&space;mean=&space;\\frac{0&plus;1&plus;0&plus;0&plus;1&plus;1&plus;0&plus;0&plus;1}{9}&space;=&space;0,44) \n",
    "\n",
    "We calculate the ratio for each product. The aggregation function is limited to column 'reordered' and it calculates the mean value of each group."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "p_reorder = p_reorder.groupby('product_id')['reordered'].mean().to_frame('p_reorder_ratio')\n",
    "p_reorder = p_reorder.reset_index()\n",
    "p_reorder.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.2.2.3 Merge the new feature on prd DataFrame\n",
    "The new feature will be merged with the prd DataFrame (section 2.2.1) which keep all the features based on products. We perform a left join as we want to keep all the products that we have created on the prd DataFrame\n",
    "<img src=\"https://i.imgur.com/dOVWPKb.jpg\" width=\"400\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Merge the prd DataFrame with reorder\n",
    "prd = prd.merge(p_reorder, on='product_id', how='left')\n",
    "\n",
    "#delete the reorder DataFrame\n",
    "del p_reorder\n",
    "gc.collect()\n",
    "\n",
    "prd.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 2.2.2.4 Fill NaN values\n",
    "As you may notice, there are product with NaN values. This regards the products that have been purchased less than 40 times from all users and were not included in the p_reorder DataFrame. **As we performed a left join with prd DataFrame, all the rows with products that had less than 40 purchases from all users, will get a NaN value.**\n",
    "\n",
    "For these products we their NaN value with zero (0):"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "prd['p_reorder_ratio'] = prd['p_reorder_ratio'].fillna(value=0)\n",
    "prd.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "> Our final DataFrame should not have any NaN values, otherwise the fitting process (chapter 4) will throw an error!"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2.3 Create user-product predictors\n",
    "We create the following predictors:\n",
    "- 2.3.1 How many times a user bought a product\n",
    "- 2.3.2 How frequently a customer bought a product after its first purchase\n",
    "- 2.3.3 How many times a customer bought a product on its last 5 orders\n",
    "\n",
    "### 2.3.1 How many times a user bought a product\n",
    "We create different groups that contain all the rows for each combination of user and product. With the aggregation function .count( ) we get how many times each user bought a product. We save the results on new **uxp** DataFrame."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create distinct groups for each combination of user and product, count orders, save the result for each user X product to a new DataFrame \n",
    "uxp = op.groupby(['user_id', 'product_id'])['order_id'].count().to_frame('uxp_total_bought')\n",
    "uxp.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Reset the index of the DF so to bring user_id & product_id rom indices to columns (pre-requisite for step 2.4)\n",
    "uxp = uxp.reset_index()\n",
    "uxp.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.3.2 How frequently a customer bought a product after its first purchase\n",
    "This ratio is a metric that describes how many times a user bought a product out of how many times she had the chance to a buy it (starting from her first purchase of the product):\n",
    "\n",
    "<img src=\"https://latex.codecogs.com/gif.latex?\\dpi{120}&space;\\large&space;probability\\&space;reordered\\&space;(user\\_id\\&space;,&space;product\\_id)&space;=&space;\\frac{Times\\_Bought\\_N}{Order\\_Range\\_D}\" title=\"\\large probability\\ reordered\\ (user\\_id\\ , product\\_id) = \\frac{Times\\_Bought\\_N}{Order\\_Range\\_D}\" />\n",
    "\n",
    "* Times_Bought_N = Times a user bought a product\n",
    "* Order_Range_D = Total orders placed since the first user's order of a product\n",
    "\n",
    "To clarify this, we examine the use with user_id:1 and the product with product_id:13032. User 1 has made 10 orders in total.She has bought the product 13032 **for first time in her 2nd order** and she has bought the same product 3 times in total. The user was able to buy the product 9 times (starting from her 2nd order until her last order). As a result, she has bought it 3 out of 9 times, meaning reorder_ratio=3/9= 0,333.\n",
    "\n",
    "The Order_Range_D variable is created using two supportive variables:\n",
    "* Total_orders = Total number of orders of each user\n",
    "* First_order_number = The order number where the customer bought a product for first time\n",
    "\n",
    "In the next blocks we show how we create:\n",
    "1. The numerator 'Times_Bought_N'\n",
    "2. The denumerator 'Order_Range_D' with the use of the supportive variables 'total_orders' & 'first_order_number' \n",
    "3. Our final ratio 'uxp_order_ratio'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.3.2.1 Calculate the numerator ('Times_Bought_N')\n",
    "\n",
    "To answer this question we simply .groupby( ) user_id & product_id and we count the instances of order_id for each group."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "times = op.groupby(['user_id', 'product_id'])[['order_id']].count()\n",
    "times.columns = ['Times_Bought_N']\n",
    "times.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.3.2.2 Calculate the denumerator ('Order_Range_D')\n",
    "To calculate the denumerator, we first calculate the total orders of each user & first order number for each user and every product purchase.\n",
    "\n",
    "In order to calculate the total number of orders of each cutomer ('total_orders') we .groupby( ) only by the user_id, we keep the column order_number and we get its highest value with the aggregation function .mean()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "total_orders = op.groupby('user_id')['order_number'].max().to_frame('total_orders')\n",
    "total_orders.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "In order to calculate the order number where the user bought a product for first time ('first_order_number') we .groupby( ) by both user_id & product_id and we select the order_number column and we retrieve the .min( ) value."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "first_order_no = op.groupby(['user_id', 'product_id'])['order_number'].min().to_frame('first_order_number')\n",
    "first_order_no  = first_order_no.reset_index()\n",
    "first_order_no.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We merge the first order number with the total_orders DataFrame. As total_orders refers to all users, where first_order_no refers to unique combinations of user & product, we perform a right join:\n",
    "<img src=\"https://i.imgur.com/bhln0tn.jpg\" width=\"250\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "span = pd.merge(total_orders, first_order_no, on='user_id', how='right')\n",
    "span.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The denominator ('Order_Range_D') now can be created with simple operations between the columns of span DataFrame:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# The +1 includes in the difference the first order were the product has been purchased\n",
    "span['Order_Range_D'] = span.total_orders - span.first_order_number + 1\n",
    "span.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.3.2.3 Create the final ratio \"uxp_reorder_ratio\"\n",
    "\n",
    "We merge **times** DataFrame, which contains the numerator, and **span** DataFrame, which contains the denumerator of our desired ratio. **As both variables derived from the combination of users & products, any type of join will keep all the combinations.**\n",
    "\n",
    "<img src=\"https://i.imgur.com/h7m1bFh.jpg\" width=\"250\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "uxp_ratio = pd.merge(times, span, on=['user_id', 'product_id'], how='left')\n",
    "uxp_ratio.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "\n",
    "We divide the Times_Bought_N by the Order_Range_D for each user and product."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "uxp_ratio['uxp_reorder_ratio'] = uxp_ratio.Times_Bought_N / uxp_ratio.Order_Range_D\n",
    "uxp_ratio.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "\n",
    "We select to keep only the 'user_id', 'product_id' and the final feature 'uxp_reorder_ratio'\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "uxp_ratio = uxp_ratio.drop(['Times_Bought_N', 'total_orders', 'first_order_number', 'Order_Range_D'], axis=1)\n",
    "uxp_ratio.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Remove temporary DataFrames\n",
    "del [times, first_order_no, span]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.3.2.4 Merge the final feature with uxp DataFrame\n",
    "The new feature will be merged with the uxp DataFrame (section 2.3.1) which keep all the features based on combinations of user-products. We perform a left join as we want to keep all the user-products that we have created on the uxp DataFrame\n",
    "\n",
    "<img src=\"https://i.imgur.com/hPJXBuB.jpg\" width=\"250\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "uxp = uxp.merge(uxp_ratio, on=['user_id', 'product_id'], how='left')\n",
    "\n",
    "del uxp_ratio\n",
    "uxp.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.3.3 How many times a customer bought a product on its last 5 orders\n",
    "For this feature, we want to keep the last five orders for each customer and get how many times bought any product on them. To achieve this we need to:\n",
    "* Create a new variable ('order_number_back') which keeps the order_number for each order in reverse order\n",
    "* Keep only the last five orders for each order\n",
    "* Perform a .groupby( ) on users and products to get how many times each customer bought a product.\n",
    "* Create the following ratio:\n",
    "\n",
    "![](https://latex.codecogs.com/gif.latex?times%5C%20last%20%5C5%5C%20%28of%5C%20a%5C%20purchased%5C%20product%5C%20from%5C%20a%5C%20user%29%3D%5Cfrac%7BTimes%5C%20a%5C%20user%5C%20bought%5C%20a%5C%20product%5C%20on%5C%20its%5C%20last%5C%205%5C%20orders%7D%7BTotal%5C%20orders%5C%20%3D5%7D)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 2.3.3.1 Create a new variable ('order_number_back') which keeps the order_number for each order in reverse order\n",
    "In this step we show how we create a reverse order_number for each customer. <br>\n",
    "Have a look at the orders of customer 1 (user_id == 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "op[op.user_id==1].head(45)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Our goal is a to create a new column ('order_number_back') which indicates the last order as first, the second from the end as second and so on. To achieve this, we get the highest order_number (max) for user_id==1 and we subtract the order_number of each order from it. Thus for last order (order_number == 10) that will be: \n",
    "<br>\n",
    "<br>\n",
    "\n",
    "![order_number_back](https://latex.codecogs.com/png.latex?%5Cdpi%7B200%7D%20%5Ctiny%20%5Cfontsize%7B%20%7D%7Bbaselineskip%7D%20order%5C_number%5C_back%28x%29%3D%20order%5C_number.max%28%29%20-order%5C_number%28x%29%3D10%20-%2010%20%3D%200)\n",
    "\n",
    "And as we want the last order to be marked as first, rather than zeroth, the previous formula will be:\n",
    "\n",
    "![](https://latex.codecogs.com/png.latex?%5Cdpi%7B200%7D%20%5Ctiny%20%5Cfontsize%7B%20%7D%7Bbaselineskip%7D%20order%5C_number%5C_back%28x%29%3D%20order%5C_number.max%28%29%20-order%5C_number%28x%29%3D10%20-%2010%20&plus;1%3D%201)\n",
    "\n",
    "> Note that order_number.max( ) is a single value, where order_number is a 1-D array (column/Series)\n",
    "\n",
    "By applying the above formula to the orders of user_id == 1 we get the following results:\n",
    "![](https://i.imgur.com/toda8ay.png)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "In the next code block we perform the same calculations for all users. We .groupby( ) op by the user_id and we select the column order_number. With .transform(max) we request to get the highest number of the column order_number for each group & with minus (-) op.order_number we substract the order_number of each row. Finally we add 1 for the reason mentioned above.\n",
    "\n",
    "> .transform( ) perform some group-specific computations and return a like-indexed object. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "op['order_number_back'] = op.groupby('user_id')['order_number'].transform(max) - op.order_number +1 \n",
    "op.head(15)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Check that the formula has been applied to all users. Here we check the new column for a random user (user_id== 7):"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "op[op.user_id==7].head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 2.3.3.2 Keep only the last five orders for each customer\n",
    "With the use of order_number_back we can now select to keep only the last five orders of each customer:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "op5 = op[op.order_number_back <= 5]\n",
    "op5.head(15)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 2.3.3.3 Perform a .groupby( ) on users and products to get how many times each customer bought every product.\n",
    "Having kept the last 5 orders for each user, we perform a .groupby( ) on user_id & product_id. With .count( ) we get how many times each customer bought a product."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "last_five = op5.groupby(['user_id','product_id'])[['order_id']].count()\n",
    "last_five.columns = ['times_last5']\n",
    "last_five.head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "So for user_id==1, the product 196 has been ordered on all of its last five orders, where the product 35951 has been ordered only one time."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 2.3.3.5 Merge the final feature with uxp DataFrame\n",
    "The new feature will be merged with the uxp DataFrame (section 2.3.1) which keep all the features based on combinations of user-products. We perform a left join as we want to keep all the user-products that we have created on the uxp DataFrame\n",
    "\n",
    "<img src=\"https://i.imgur.com/ObfHDPl.jpg\" width=\"400\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "uxp = uxp.merge(last_five, on=['user_id', 'product_id'], how='left')\n",
    "\n",
    "del [op5 , last_five]\n",
    "uxp.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 2.3.3.6 Fill NaN values\n",
    "If you check uxp DataFrame you will notice that some rows have NaN values for our new feature. This happens as there might be products that the customer did not buy on its last five orders. For these cases, we turn NaN values into zero (0) with .fillna(0) method."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "uxp = uxp.fillna(0)\n",
    "uxp.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2.4 Merge all features\n",
    "We now merge the DataFrames with the three types of predictors that we have created (i.e., for the users, the products and the combinations of users and products).\n",
    "\n",
    "We will start from the **uxp** DataFrame and we will add the user and prd DataFrames. We do so because we want our final DataFrame (which will be called **data**) to have the following structure: \n",
    "\n",
    "<img style=\"float: left;\" src=\"https://i.imgur.com/mI5BbFE.jpg\" >\n",
    "\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.4.1 Merge uxp with user DataFrame\n",
    "Here we select to perform a left join of uxp with user DataFrame based on matching key \"user_id\"\n",
    "\n",
    "<img src=\"https://i.imgur.com/WlI84Ud.jpg\" width=\"400\">\n",
    "\n",
    "Left join, ensures that the new DataFrame will have:\n",
    "- all the observations of the uxp (combination of user and products) DataFrame \n",
    "- all the **matching** observations of user DataFrame with uxp based on matching key **\"user_id\"**\n",
    "\n",
    "The new DataFrame as we have already mentioned, will be called **data**."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Merge uxp features with the user features\n",
    "#Store the results on a new DataFrame\n",
    "data = uxp.merge(user, on='user_id', how='left')\n",
    "data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.4.1 Merge data with prd DataFrame\n",
    "In this step we continue with our new DataFrame **data** and we perform a left join with prd DataFrame. The matching key here is the \"product_id\".\n",
    "<img src=\"https://i.imgur.com/Iak6nIz.jpg\" width=\"400\">\n",
    "\n",
    "Left join, ensures that the new DataFrame will have:\n",
    "- all the observations of the data (features of userXproducts and users) DataFrame \n",
    "- all the **matching** observations of prd DataFrame with data based on matching key **\"product_id\"**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Merge uxp & user features (the new DataFrame) with prd features\n",
    "data = data.merge(prd, on='product_id', how='left')\n",
    "data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.4.2 Delete previous DataFrames"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The information from the DataFrames that we have created to store our features (op, user, prd, uxp) is now stored on **data**. \n",
    "\n",
    "As we won't use them anymore, we now delete them."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "del op, user, prd, uxp\n",
    "gc.collect()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 3. Create train and test DataFrames\n",
    "## 3.1 Include information about the last order of each user\n",
    "\n",
    "The **data** DataFrame that we have created on the previous chapter (2.4) should include two more columns which define the type of user (train or test) and the order_id of the future order.\n",
    "This information can be found on the initial orders DataFrame which was provided by Instacart: \n",
    "\n",
    "<img style=\"float: left;\" src=\"https://i.imgur.com/jbatzRY.jpg\" >\n",
    "\n",
    "\n",
    "Towards this end:\n",
    "1. We select the **orders** DataFrame to keep only the future orders (labeled as \"train\" & \"test). \n",
    "2. Keep only the columns of our desire ['eval_set', 'order_id'] <span style=\"color:red\">**AND** </span> 'user_id' as is the matching key with our **data** DataFrame\n",
    "2. Merge **data** DataFrame with the information for the future order of each customer using as matching key the 'user_id'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To filter and select the columns of our desire on orders (the 2 first steps) there are numerous approaches:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## First approach:\n",
    "# In two steps keep only the future orders from all customers: train & test \n",
    "orders_future = orders[((orders.eval_set=='train') | (orders.eval_set=='test'))]\n",
    "orders_future = orders_future[ ['user_id', 'eval_set', 'order_id'] ]\n",
    "orders_future.head(10)\n",
    "\n",
    "## Second approach (if you want to test it you have to re-run the notebook):\n",
    "# In one step keep only the future orders from all customers: train & test \n",
    "#orders_future = orders.loc[((orders.eval_set=='train') | (orders.eval_set=='test')), ['user_id', 'eval_set', 'order_id'] ]\n",
    "#orders_future.head(10)\n",
    "\n",
    "## Third approach (if you want to test it you have to re-run the notebook):\n",
    "# In one step exclude all the prior orders so to deal with the future orders from all customers\n",
    "#orders_future = orders.loc[orders.eval_set!='prior', ['user_id', 'eval_set', 'order_id'] ]\n",
    "#orders_future.head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To fulfill step 3, we merge on **data** DataFrame the information for the last order of each customer. The matching key here is the user_id and we select a left join as we want to keep all the observations from **data** DataFrame.\n",
    "\n",
    "<img src=\"https://i.imgur.com/m3pNVDW.jpg\" width=\"400\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# bring the info of the future orders to data DF\n",
    "data = data.merge(orders_future, on='user_id', how='left')\n",
    "data.head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3.2 Prepare the train DataFrame\n",
    "In order to prepare the train Dataset, which will be used to create our prediction model, we need to include also the response (Y) and thus have the following structure:\n",
    "\n",
    "<img style=\"float: left;\" src=\"https://i.imgur.com/PDu2vfR.jpg\" >\n",
    "\n",
    "Towards this end:\n",
    "1. We keep only the customers who are labelled as \"train\" from the competition\n",
    "2. For these customers we get from order_products_train the products that they have bought, in order to create the response variable (reordered:1 or 0)\n",
    "3. We make all the required manipulations on that dataset and we remove the columns that are not predictors\n",
    "\n",
    "So now we filter the **data** DataFrame so to keep only the train users:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Keep only the customers who we know what they bought in their future order\n",
    "data_train = data[data.eval_set=='train']\n",
    "data_train.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "For these customers we get from order_products_train the products that they have bought. The matching keys are here two: the \"product_id\" & \"order_id\". A left join keeps all the observations from data_train DataFrame\n",
    "\n",
    "<img src=\"https://i.imgur.com/kndys9d.jpg\" width=\"400\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Get from order_products_train all the products that the train users bought bought in their future order\n",
    "data_train = data_train.merge(order_products_train[['product_id','order_id', 'reordered']], on=['product_id','order_id'], how='left' )\n",
    "data_train.head(15)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "On the last columm (reordered) you can find out our response (y). \n",
    "There are combinations of User X Product which they were reordered (1) on last order where other were not (NaN value).\n",
    "\n",
    "Now we manipulate the data_train DataFrame, to bring it into a structure for Machine Learning (X1,X2,....,Xn, y):\n",
    "- Fill NaN values with value zero (regards reordered rows without value = 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Where the previous merge, left a NaN value on reordered column means that the customers they haven't bought the product. We change the value on them to 0.\n",
    "data_train['reordered'] = data_train['reordered'].fillna(0)\n",
    "data_train.head(15)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "- Set as index the column(s) that describe uniquely each row (in our case \"user_id\" & \"product_id\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#We set user_id and product_id as the index of the DF\n",
    "data_train = data_train.set_index(['user_id', 'product_id'])\n",
    "data_train.head(15)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "- Remove columns which are not predictors (in our case: 'eval_set','order_id')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#We remove all non-predictor variables\n",
    "data_train = data_train.drop(['eval_set', 'order_id'], axis=1)\n",
    "data_train.head(15)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3.3 Prepare the test DataFrame\n",
    "The test DataFrame must have the same structure as the train DataFrame, excluding the \"reordered\" column (as it is the label that we want to predict).\n",
    "<img style=\"float: left;\" src=\"https://i.imgur.com/lLJ7wpA.jpg\" >\n",
    "\n",
    " To create it, we:\n",
    "- Keep only the customers who are labelled as test"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Keep only the future orders from customers who are labelled as test\n",
    "data_test = data[data.eval_set=='test']\n",
    "data_test.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "- Set as index the column(s) that uniquely describe each row (in our case \"user_id\" & \"product_id\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#We set user_id and product_id as the index of the DF\n",
    "data_test = data_test.set_index(['user_id', 'product_id'])\n",
    "data_test.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "- Remove the columns that are predictors (in our case:'eval_set', 'order_id')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#We remove all non-predictor variables\n",
    "data_test = data_test.drop(['eval_set','order_id'], axis=1)\n",
    "#Check if the data_test DF, has the same number of columns as the data_train DF, excluding the response variable\n",
    "data_test.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 4. Create predictive model (fit)\n",
    "The Machine Learning model that we are going to create is based on the XGBoost algorithm.\n",
    "\n",
    "\n",
    "## 4.1 Train XGBoost\n",
    "XGBoost stands for e**X**treme **G**radient **Boost**ing, an algorithm that is used in many winning solutions for Kaggle competitions [(ref)](https://github.com/dmlc/xgboost/tree/master/demo#machine-learning-challenge-winning-solutions). \n",
    "\n",
    "XGBoost is an implementation of gradient boosted decision trees designed for speed and performance.\n",
    "\n",
    "Gradient boosting is an approach where new models are created that predict the residuals or errors of prior models and then added together to make the final prediction. It is called gradient boosting because it uses a gradient descent algorithm to minimize the loss when adding new models.\n",
    "\n",
    "To create the predictive model we:\n",
    "\n",
    "**1** - Load XGBoost's package (is not includes in scikit-learn, but it can interact with it)\n",
    "\n",
    "**2** - Separate predictors from response and store them into an optimized data structure which works with XGBoost\n",
    "\n",
    "**3** - Set the hyperparameters of the booster\n",
    ">> - eval_metric: Evaluation metrics for validation data, a default metric will be assigned according to objective (rmse for regression, and error for classification, mean average precision for ranking)\n",
    ">> - max_depth: Maximum depth of a tree\n",
    ">> - colsample_bytree: Denotes the fraction of columns to be randomly samples for each tree.\n",
    ">> - subsample:  Denotes the fraction of observations to be randomly samples for each tree.\n",
    "Lower values make the algorithm more conservative and prevents overfitting but too small values might lead to under-fitting.\n",
    "\n",
    "**4** - We instantiate a XGBClassifier( ) where you will notice different arguments:\n",
    ">> - objective: This defines the loss function to be minimized. In our example we use binary:logistic –logistic regression for binary classification, returns predicted probability (not class)\n",
    ">> - parameters: Includes all the hyperparameters that were defined in the step 3 - these are special parameters only for our classification problem\n",
    ">> - num_boost_round: Number of boosting iterations\n",
    "\n",
    "\n",
    "**5** - Finally we train our model with the X_train and y_train data.\n",
    "\n",
    "**6** - Get the feature importance that yields from our model\n",
    "\n",
    "You can read in more detail how to use XGBoost in Python in the following [link](https://www.datacamp.com/community/tutorials/xgboost-in-python)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TRAIN FULL \n",
    "###########################\n",
    "## IMPORT REQUIRED PACKAGES\n",
    "###########################\n",
    "import xgboost as xgb\n",
    "\n",
    "##########################################\n",
    "## SPLIT DF TO: X_train, y_train (axis=1)\n",
    "##########################################\n",
    "X_train, y_train = data_train.drop('reordered', axis=1), data_train.reordered\n",
    "\n",
    "########################################\n",
    "## SET BOOSTER'S PARAMETERS\n",
    "########################################\n",
    "parameters = {'eval_metric':'logloss', \n",
    "              'max_depth': 5, \n",
    "              'colsample_bytree': 0.4,\n",
    "              'subsample': 0.75,\n",
    "             }\n",
    "\n",
    "########################################\n",
    "## INSTANTIATE XGBClassifier()\n",
    "########################################\n",
    "xgbc = xgb.XGBClassifier(objective='binary:logistic', parameters=parameters, num_boost_round=10, \n",
    "                         gpu_id=0, tree_method = 'gpu_hist')\n",
    "\n",
    "########################################\n",
    "## TRAIN MODEL\n",
    "########################################\n",
    "model = xgbc.fit(X_train, y_train)\n",
    "\n",
    "##################################\n",
    "# FEATURE IMPORTANCE - GRAPHICAL\n",
    "##################################\n",
    "xgb.plot_importance(model)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4.2 Fine-tune your model\n",
    "\n",
    "Most algorithms have their own parameters that we need to declare. With method .get_params() we can retrieve the parameters of our fitting model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "model.get_xgb_params()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "These parameters do not necessarily create the best fitting model (in terms of prediction score). The method .GridSearchCV( ) can make several trials to define the best parameters for our fitting model. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "###########################\n",
    "## DISABLE WARNINGS\n",
    "###########################\n",
    "import sys\n",
    "import warnings\n",
    "\n",
    "if not sys.warnoptions:\n",
    "    warnings.simplefilter(\"ignore\")\n",
    "\n",
    "###########################\n",
    "## IMPORT REQUIRED PACKAGES\n",
    "###########################\n",
    "import xgboost as xgb\n",
    "from sklearn.model_selection import GridSearchCV\n",
    "\n",
    "####################################\n",
    "## SET BOOSTER'S RANGE OF PARAMETERS\n",
    "# IMPORTANT NOTICE: Fine-tuning an XGBoost model may be a computational prohibitive process with a regular computer or a Kaggle kernel. \n",
    "# Be cautious what parameters you enter in paramiGrid section.\n",
    "# More paremeters means that GridSearch will create and evaluate more models.\n",
    "####################################    \n",
    "paramGrid = {\"max_depth\":[5,10],\n",
    "            \"colsample_bytree\":[0.3,0.4]}  \n",
    "\n",
    "########################################\n",
    "## INSTANTIATE XGBClassifier()\n",
    "########################################\n",
    "xgbc = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss', num_boost_round=10, gpu_id=0, tree_method = 'gpu_hist')\n",
    "\n",
    "##############################################\n",
    "## DEFINE HOW TO TRAIN THE DIFFERENT MODELS\n",
    "#############################################\n",
    "gridsearch = GridSearchCV(xgbc, paramGrid, cv=3, verbose=2, n_jobs=1)\n",
    "\n",
    "################################################################\n",
    "## TRAIN THE MODELS\n",
    "### - with the combinations of different parameters\n",
    "### - here is where GridSearch will be exeucuted\n",
    "#################################################################\n",
    "model = gridsearch.fit(X_train, y_train)\n",
    "\n",
    "##################################\n",
    "## OUTPUT(S)\n",
    "##################################\n",
    "# Print the best parameters\n",
    "print(\"The best parameters are: /n\",  gridsearch.best_params_)\n",
    "\n",
    "# Store the model for prediction (chapter 5)\n",
    "model = gridsearch.best_estimator_\n",
    "\n",
    "# Delete X_train , y_train\n",
    "del [X_train, y_train]\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The model has now the new parameters from GridSearchCV:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "model.get_params()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 5. Apply predictive model (predict)\n",
    "The model that we have created is stored in the **model** object.\n",
    "At this step we predict the values for the test data and we store them in a new column in the same DataFrame.\n",
    "\n",
    "For better results, we set a custom threshold to 0.21. The best custom threshold can be found through a grid search."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "'''\n",
    "# Predict values for test data with our model from chapter 5 - the results are saved as a Python array\n",
    "test_pred = model.predict(data_test).astype(int)\n",
    "test_pred[0:20] #display the first 20 predictions of the numpy array\n",
    "'''"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## OR set a custom threshold (in this problem, 0.21 yields the best prediction)\n",
    "test_pred = (model.predict_proba(data_test)[:,1] >= 0.21).astype(int)\n",
    "test_pred[0:20] #display the first 20 predictions of the numpy array"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Save the prediction (saved in a numpy array) on a new column in the data_test DF\n",
    "data_test['prediction'] = test_pred\n",
    "data_test.head(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Reset the index\n",
    "final = data_test.reset_index()\n",
    "# Keep only the required columns to create our submission file (for chapter 6)\n",
    "final = final[['product_id', 'user_id', 'prediction']]\n",
    "\n",
    "gc.collect()\n",
    "final.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 6. Creation of Submission File\n",
    "To submit our prediction to Instacart competition we have to get for each user_id (test users) their last order_id. The final submission file should have the test order numbers and the products that we predict that are going to be bought.\n",
    "\n",
    "To create this file we retrieve from orders DataFrame all the test orders with their matching user_id:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "orders_test = orders.loc[orders.eval_set=='test',(\"user_id\", \"order_id\") ]\n",
    "orders_test.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We merge it with our predictions (from chapter 5) using a left join:\n",
    "<img src=\"https://i.imgur.com/KJubu0v.jpg\" width=\"400\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "final = final.merge(orders_test, on='user_id', how='left')\n",
    "final.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "And we move on with two final manipulations:\n",
    "- remove any undesired column (in our case user_id)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#remove user_id column\n",
    "final = final.drop('user_id', axis=1)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "- set product_id column as integer (mandatory action to proceed to the next step)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#convert product_id as integer\n",
    "final['product_id'] = final.product_id.astype(int)\n",
    "\n",
    "## Remove all unnecessary objects\n",
    "del orders\n",
    "del orders_test\n",
    "gc.collect()\n",
    "\n",
    "final.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "For our submission file we initiate an empty dictionary. In this dictionary we will place as index the order_id and as values all the products that the order will have. If none product will be purchased, we have explicitly to place the string \"None\". This syntax follows the submission's file standards defined by the competition."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "_kg_hide-output": true
   },
   "outputs": [],
   "source": [
    "d = dict()\n",
    "for row in final.itertuples():\n",
    "    if row.prediction== 1:\n",
    "        try:\n",
    "            d[row.order_id] += ' ' + str(row.product_id)\n",
    "        except:\n",
    "            d[row.order_id] = str(row.product_id)\n",
    "\n",
    "for order in final.order_id:\n",
    "    if order not in d:\n",
    "        d[order] = 'None'\n",
    "        \n",
    "gc.collect()\n",
    "\n",
    "#We now check how the dictionary were populated (open hidden output)\n",
    "d"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We convert the dictionary to a DataFrame and prepare it to extact it into a .csv file"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Convert the dictionary into a DataFrame\n",
    "sub = pd.DataFrame.from_dict(d, orient='index')\n",
    "\n",
    "#Reset index\n",
    "sub.reset_index(inplace=True)\n",
    "#Set column names\n",
    "sub.columns = ['order_id', 'products']\n",
    "\n",
    "sub.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**The submission file should have 75.000 predictions to be submitted in the competition**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Check if sub file has 75000 predictions\n",
    "sub.shape[0]\n",
    "print(sub.shape[0]==75000)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The DataFrame can now be converted to .csv file. Pandas can export a DataFrame to a .csv file with the .to_csv( ) function."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'sub' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-7-e7fadfef0214>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0msub\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mto_csv\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'sub.csv'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mindex\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mFalse\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m: name 'sub' is not defined"
     ]
    }
   ],
   "source": [
    "sub.to_csv('sub.csv', index=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 7. Get F1 Score"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Before you are ready to submit your prediction to the competion, **ensure that**:\n",
    "- **You have used all of the offered data and not the 10% that was defined as an optional step on section 1.2**\n",
    "\n",
    "To submit your prediction and get the F1 score you have to:\n",
    "1. Commit this notebook and wait for the results \n",
    "2. Go to view mode (where you see your notebook but you can't edit it)\n",
    "3. Click on the data section from your left panel\n",
    "4. Find the sub.csv (on outputs), below the section with the data from Instacart\n",
    "5. Click on \"Submit to competition\" button\n",
    "\n",
    "Regarding step 1:\n",
    ">This step might take long. If it exceeds 20-30 minutes it would be wise to check your code again. Kaggle won't inform you during commit if the notebook has:\n",
    "- syntax errors\n",
    "- if it exceeds 16 GB RAM\n",
    "- if it takes an algorirthms too much to train or predict\n",
    "\n",
    ">Any new commit:\n",
    "- can't take more than 9 hours\n",
    "- doesn't stop if it exceeds the 16 GB RAM - you will just receive an error of unsuccesful commit after 9 hours"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
