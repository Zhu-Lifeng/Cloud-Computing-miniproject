<h1 align="center">Bevervage Nutrition Calculator Application based on Flask using Coffee API</h1>

# Architecture
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p1.png" alt="Architecture">
</p>

# Interduction
This project is a HTTPS webpage application based on Docker Technique. We provide a useful daily tool to estimate some nutrition you will gain from your daily beverage intake.

# How to Install<br>

## 1. make sure you have connected to your GCP instance.<br>

## 2. finish the initial setting and installation.<br>

  ```sh
  sudo apt−get update
  sudo apt update
  sudo apt install python3-pip
  sudo apt install install git
  ```

## 3. download the application files from git<br>

  ```sh
  git clone https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject.git
  ```

## 4. install the docker<br>

  ```sh
  sudo apt install docker.io
  ```

## 5. create the docker container entity<br>

  ```sh
  sudo docker build -t your-image-name .
  ```
(you can name your docker whatever you want)
## 6. run the docker<br>
  ```sh
  sudo docker run -p 8080:8080 your-image-name
  ```

# System Overview and function introduction<br>
## 1. Start page
This is the start page.
Users can sign up here, or log in if they have had an account.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p2.png" alt="Architecture">
</p>

## 2.Sign up page
For signing up, users need to provide their email address, create an User Name and their User Password. The password will be The password will be hashed encrypted.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p3.png" alt="Architecture">
</p>

## 3.Log in page
If you have signed in before, you can use the "log in" button, type in your email address and your password and log in the system.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p10.png" alt="Architecture">
</p>

## 4.Filling page
After signing up, the user will be required to input their height, weight, age and gender. These information will be used to estimate the recommended daily intake of nurtritions.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p4.png" alt="Architecture">
</p>

## 5. Main page
In the main page, users can choose the nurtritions they want to estimate and input how much beverage they have drank or plan to drink today. <br>
Users can search the name of beverage with the search box.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p5.png" alt="Architecture">
</p>
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p6.png" alt="Architecture">
</p>

## 6. Result page
After clicked the "Calculate" button, they will see how much nutrition they have intaken from the beverage they choose, and the application will produce some suggestions or commends about it.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p7.png" alt="Architecture">
</p>

## 7. New Beverage submiting model
If the user find themselves being not able to find their beverage in the table, they can click the "Toggle Drink Form" buttom to release the new beverage submiting model. The name and the nutrition content of the new beverage will be collected here. <br>
Aftter this, all later users(including the one who submit it) will be able to find the new beverage from the table.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p8.png" alt="Architecture">
</p>

## 8. Personal information amending model
Besides, if you click the "View my personal information" button, you will view your height, weight, age and gender, and you can change it if you want.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p9.png" alt="Architecture">
</p>

# External API
You should notice that everytime we change to another page, the background picture is changing too. Because everytime we load a new page, the application will ask the coffee API for a random picture about coffee, and that picture will become the background of next page.
