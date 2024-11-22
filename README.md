# LLM (Llama 3.2) integration with MySQL and database administration via a web applicaton

For this project, I wanted to combine the advantages of an open-source LLM, such as Llama (from Meta) and classic SQL databases. So, I decided to implement it by setting up a project to get data from MySQL, pass it to Llama 3.2, and receive the relevant response per the prompt indications.

*Checkout the following video with a quick demo and explanation: https://drive.google.com/file/d/1p9RDVWN5ovnJHNL7I_z8_rXopNeZMfOe/view?usp=sharing*

![image](https://github.com/user-attachments/assets/84610526-8bff-4c9c-bb61-0323bb44ed5c)

## Tools:

- Python
- Flask
- HTML / CSS
- JavaScript
- LLM: Llama 3.2 in docker container
- MySQL

## General points:

- Database: cooking recipes (title, ingredients, steps).
- Prompt: I indicated Llama to review the cooking recipe as an expert cook and text editor and provide suggestions that could improve the recipes in terms of clarity, appeal, and correctness.
- Frontend: Divided into two parts: 1) left, with the interaction with Llama, and 2) right: the database “administration”. See the below diagram to get a general idea of the project.

![image](https://github.com/user-attachments/assets/34bb3141-f5e7-4a40-aeff-d278d7d5cb45)


