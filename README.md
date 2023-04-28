# UTME Warmer Application

This application is used to control the heating and cooling beverage appliance. Below, we will discuss how to access and operate the application on your device.

## Getting Started

Throughout the development of the graphical user interface, we utilized Git to manage version control and simplify collaboration. The entirety of our code (including previous version history) is stored in this Git repository. You can either clone the repository directly onto your device or access the repository online and download the files from there.

`git clone https://github.com/justin72835/utme-warmer.git`

When running the application, you should make sure that you are in the `main` branch and that your local repository (the cloned repository) is up-to-date. You can check the state of the working directory using the following command.

`git status`

Depending on the response, you may need to switch to the `main` branch and perform a git pull in order to update the local repository to match the contents of the most up-to-date remote repository.

```
git checkout main
git pull
```

Lastly, when you want to run the application, you must first navigate to the same directory as the script within the terminal using `cd`. In this case, make sure you are in the 'utme_warmer' directory. You can then run the python file using the following command.

`sudo python main.py`

The `sudo` command allows authorized users to execute commands with elevated privileges, typically as a system administrator or a root user. This can be useful for performing administrative tasks, such as installing software, modifying system settings, or managing system resources.

## Data Storage using CSV

When using the application, a new CSV file will be generated and filled with the time and temperature data from each heating/cooling cycle. The CSV files are stored in a folder called 'temp_data' and are named utilizing the date/time for when the file was created.
