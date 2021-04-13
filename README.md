#

<h1 align="center" style="color:#894b9d; font-weight:bold;">
     <img 
    src="https://user-images.githubusercontent.com/42190754/114031694-fda2a600-9851-11eb-9d06-279ffc5122b9.png"
    float="center"
    width="100" height="100"
    />
    <br/>
  Prediction Service
</h1>

<p align="center" style="color:#894b9d">
 <a style="color:#894b9d" href="#ℹ%EF%B8%8F-about">About</a> •
 <a style="color:#894b9d" href="#-how-it-works">How it works</a> •
 <a style="color:#894b9d" href="#-documentation">Documentation</a> •
 <a style="color:#894b9d" href="#-authors">Authors</a> •
 <a style="color:#894b9d" href="#-license">License</a>
</p>

## ℹ️ About

API Restful to add and predict data temperature and humidity, using stack with Python, Flask and MLPRegressor for predict model.

---

## 🚀 How it works

### 👉 Pre-requisites

Before you begin, you will need to have the following tools installed on your machine: [Git](https://git-scm.com), [Python](https://www.python.org/) and [Pip](https://pypi.org/project/pip/). In addition, it is good to have an editor to work with the code like [VSCode](https://code.visualstudio.com/).

#### 🏁 Start

```bash
# Clone this repository
$ git clone https://github.com/BiaChacon/prediction-service.git

# Access the project folder cmd/terminal
$ cd prediction-service
```

First, create an .env file locally. You can duplicate .env.example and name the new .env copy. Note that you need to fill the env DB_URL variable with your MongoDB connection string.

#### 🎲 Running the server

```bash
# install the dependencies
$ pip install requirements.txt

# Run the application
$ python app.py

# The server will start at port: 5000 - go to http://localhost:5001
```

---

## 🖥️ Client

### 👉 Pre-requisites

Is running the [Weather API](https://github.com/BiaChacon/weather-api)

```bash
# go to the project folder
$ cd client

#Run the application
$ python client.py
```

---

 ### 📈 [Results analysis](https://colab.research.google.com/drive/1xN178kNBumWwN9lC-DSP5vgQfaYQR-5K?usp=sharing)

Analysis of prediction results according to times of increment of new data to the model.
- X = 5 minutes
- Y = 1 hour
- Z = 6 hours

---

## 🗎 Documentation

🚀 [Postman Collection](https://github.com/BiaChacon/prediction-service/blob/master/postman_collection.json)

---

## 👩🏽‍💻 Authors

<table>
  <tr>
    <td align="center"><a href="https://github.com/biachacon"><img src="https://avatars1.githubusercontent.com/u/42190754?s=460&u=a5cbe42a4868b2bac9615226044b9cec15cee418&v=4" width="100px;" alt=""/><br /><sub><b>Bia Chacon</b></sub></a><br /><a href="https://github.com/BiaChacon/prediction-service" title="Code">💻</a></td>
  <tr>
</table>

---

## 📝 License

This project is under MIT. See at here [LICENSE](https://github.com/BiaChacon/prediction-service/blob/master/LICENSE) for more information.

---
