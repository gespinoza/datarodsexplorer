# Tips for Deploying *Data Rods Explorer*

## Authentication Requirement for Giovanni Time Series Service API

The new **Giovanni Time Series Service API** requires authentication to retrieve and display data within the **Data Rods Explorer App**.

To enable this authentication, a `.netrc` file is required. This file securely stores the credentials used by the application when communicating with the Giovanni service.

---

## Generating the `.netrc` File

A helper script named `generate_netrc_file.py` is included with this application to automate the creation of the `.netrc` file.

The script will:

1. Attempt to use the **username** and **password** defined in the app’s **settings**.
2. If those credentials are not found, it will prompt you to enter them manually in the shell.

---

## How to Run the Script

To generate the `.netrc` file, run the following command from the Data Rods Explorer project directory:

```bash
tethys manage shell < generate_netrc_file.py