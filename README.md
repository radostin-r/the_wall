### Installation

To be able to run the project you should have a virtual environment created.
Project is created with Python 3.12.

To create a new virtual environment and to install python 3.12 you can download
pyenv and venv. Please refer to their respective documentation to install them.

After the virtual env is installed and active we have to install the requirements
by running the following command:

```python
pip install -r /path/to/requirements.txt
```

Run migration to setup the database:
```bash
python manage.py migrate
```

After everything is installed we can run the project using the following command in terminal
from within the root folder:

```bash
python manage.py runserver
```

### Usage

In order to have data for the API to return we have to run the Django commands.
First run the insert_profiles than start_work to ingest data into the db.


### Django Commands

We have two Django commands. One for creating profiles by reading a txt document called insert_profiles.
Second for calculating costs and doing the work which also includes multiprocessing work and it is called start_work

Usage for insert_profiles command:
```bash
python manage.py insert_profiles /path/to/file
```

Usage for start_work command where the keyword argument is optional and is used only to trigger the multiprocessing work:
```bash
python manage.py start_work --num-teams=4
```


### Running Tests
Run command in root folder:
```bash
python manage.py test wall
```