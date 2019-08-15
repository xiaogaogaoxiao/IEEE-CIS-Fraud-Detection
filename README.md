# IEEE-CIS Fraud Detection

## Google Drive data upload

To support uploading files to Google Drive from Python you need to create a project in Google Developers Console. Great guide explaining the configuration part of the project is on [medium.com](https://medium.com/@annissouames99/how-to-upload-files-automatically-to-drive-with-python-ee19bb13dda). After successful configuration you should save your client ID and the secret key to the `client_secrets.json` file.

When running the main `fraudiee package` script you will explicitly specify an argument indicating the directory of the JSON file mentioned above. The first time you run the Google Drive uploading script manual authorization from the browser level will be necessary. If specified by the `--credentials` command line argument, your credentials will be saved inside the `fraudieee` package into `mycreds.json` file and each subsequent data transfer will be done automatically. You can achieve this by calling:

```bash
python -m fraudieee upload --data-path=/path/to/kaggle/data/ --client-secrets-path=/path/to/client_secrets.json --credentials
```

The proper `kaggle-api` configuration is also recommended. Going through this [repository guide](https://github.com/Kaggle/kaggle-api) will show you how to achieve this. When this is done you can download the IEEE-CIS Fraud Detection data by calling:

```bash
kaggle competitions download -c ieee-fraud-detection
```

For more informations about feeding the fraudieee main script with the command line arguments just type:

```bash
python -m fraudieee -h
```
