# sortext

This Django application allows you to conduct raffles based on a list of participants. It supports various game modes to suit different raffle requirements.

## 🎰 Features 🎰

- **Soft Mode**: Three results are calculated randomly with a bias towards participants with more tickets. (Not recommended when everyone has the same number of tickets)
- **Half Mode**: Two of the three results are calculated randomly with a bias towards participants with more tickets. (Not recommended when everyone has the same number of tickets)
- **Hard Mode**: Three results are calculated randomly with different algorithms for each.
- **Elimination Mode**: Tickets are subtracted from participants, and the participant without tickets is eliminated. (Inverts the criteria of Soft and Half so that the bias is towards participants with fewer tickets).
- **2 out of 3 Mode**: Only two matches are needed to declare a winner (Minimum 3 participants).

## 📋 Requirements 📋

- Python 3.x
- Django 3.x or 4.x
- Other dependencies listed in `requirements.txt`

## 🏗️ Installation 🏗️

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply the migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## ⚙️ Configuration ⚙️

Ensure you have configured your Django settings correctly, including the database and logging configurations. By default, logs are stored in `/var/log/django.log`.

## 🛫 Usage 🛫

1. **Access the main page**:
    Open your browser and go to `http://127.0.0.1:8000/` to access the main page displaying all raffles.

2. **Create a Raffle**:
    Use the + New button to create a new raffle and upload a participant list [example_file.xlsx](/example_file.xlsx).

3. **Run the Raffle**:
    Follow the instructions on the interface to operate the raffle.

