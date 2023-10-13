Introduction
An asynchronous web service containing a Histogram and exposing two asynchronous
end-points to manipulate the Histogram and get information about the current state of the
Histogram.

Features
 * Complexity of insertion/frequency increment of intervals when sampels are provided is reduced from O(n*n) to
    O(n*logn) using binary search.

 * Complexity of calculating mean and variance is in constant time ( O(1) ).

 * Since intervals are read from env variable hence pre calculations are made for invalid and overlapping intervals check to avoid un necessary calculations in each api call making calls faster.

 * Calculations are removed from Get api there by optimizing the time to fetch data.

 * Thread locks are implemented for asynchronous api calls to avoid any race conditions.

 * Unittest are written to check for invalid intervals and thread safety.

 * Proper error handling and File size kept < 80 lines keeping in mind production based linting and standards.


Getting Started
  Prerequisites
    * Python 3.7 or later
    * pip
    * Virtual environment (optional but recommended)

  Installation
    * Clone the repository.
    * Create a virtual environment.
    * Install dependencies mentioned in requirements.txt.

Usage
  Running the Application
    * run the following command in your project directory: uvicorn app.main:app --reload

API Endpoints
   /insertSamples: Endpoint to insert samples.
   /metrics: Endpoint to retrieve metrics.

Configuration
  create a .env file with content: INTERVAL_FILE_PATH=intervals.txt

Testing
  run the following command to run tests : python -m unittest app.tests.test_main

  Using Postman :
   http://127.0.0.1:8000/metrics under GET and use respective port your server is working on (may be 8000 or other)
   http://127.0.0.1:8000/insertSamples under POST with raw data as JSON format like {sample=[1,2,3,4]}
