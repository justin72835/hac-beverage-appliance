# UTME Warmer Application

This application is used to control the heating and cooling beverage application. Below we will talk about how to access and operate the application on your device.

## Getting Started

Throughout the development of the graphical user interface, we utilized Git for version control and collaboration. The entirety of our code (as well as previous version history) is stored in this Git repository. You can either clone the repository directly onto your device or access the repository online and download the files from there.

`git clone https://github.com/justin72835/utme-warmer.git`

When running the application, you should make sure that you are in the `main` branch and that your local repository is up-to-date. You can check the state of the working directory using the following command.

`git status`

Depending on the response, you may need to switch to the `main` branch and perform a git pull in order to update the local repository to match the contents of the more current remote repository.

```
git checkout main
git pull
```

Lastly, you can run the python file using the following command.

`sudo python main.py`

## CSV Functionality

When using the application, a new CSV file should be generated after each run. The CSV files are stored in a folder called 'temp_data' and are titled using the current date and time.
