<h1 align="center">Bevervage Nutrition Calculator Application based on Flask using Coffee API</h1>

<B style="font-size: 50px;">Architecture</B>
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p1.png" alt="Architecture">
</p>
<B style="font-size: 50px;">How to Install</B><br>
1. make sure you have connected to your GCP instance.<br>
2. finish the initial setting and installation.<br>

  ```sh
  sudo apt−get update
  sudo apt install python3-pip
  pip3 install git
  ```

3. download the application files from git<br>

  ```sh
  git clone https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject.git
  ```

4. finish the library installation<br>

  ```sh
  pip install -r requirements.txt
  ```

5. run the trigger, start the application<br>

  ```sh
  python3 MainProject/main.py
  ```

<B>System Overview and function introduction</B><br>
This is the start page.
Users can sign up here, or log in if they have had an account.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p2.png" alt="Architecture">
</p>
For signing up, users need to provide their email address, create an User Name and their User Password. The password will be The password will be hashed encrypted.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p3.png" alt="Architecture">
</p>
If you have signed in before, you can use the "log in" button, type in your email address and your password and log in the system.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p10.png" alt="Architecture">
</p>
After signing up, the user will be required to input their height, weight, age and gender. These information will be used to estimate the recommended daily intake of nurtritions.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p4.png" alt="Architecture">
</p>
In the main page, users can choose the nurtritions they want to estimate and input how much beverage they have drank or plan to drink today. <br>
Users can search the name of beverage with the search box.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p5.png" alt="Architecture">
</p>
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p6.png" alt="Architecture">
</p>
After clicked the "Calculate" button, they will see how much nutrition they have intaken from the beverage they choose, and the application will produce some suggestions or commends about it.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p7.png" alt="Architecture">
</p>
If the user find themselves being not able to find their beverage in the table, they can click the "Toggle Drink Form" buttom to release the new beverage submiting model. The name and the nutrition content of the new beverage will be collected here. <br>
Aftter this, all later users(including the one who submit it) will be able to find the new beverage from the table.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p8.png" alt="Architecture">
</p>
Besides, if you click the "View my personal information" button, you will view your height, weight, age and gender, and you can change it if you want.
<p align="center">
  <img width="700" src="https://github.com/Zhu-Lifeng/Cloud-Computing-miniproject/blob/main/Readme/p9.png" alt="Architecture">
</p>
