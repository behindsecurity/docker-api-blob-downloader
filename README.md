# Docker Registry Blob Downloader

This Python script is designed to download all blobs associated with a specific Docker image from a Docker registry. It handles authentication, retrieves the latest image tag (if not specified), downloads the image manifest, and then downloads each blob to a local directory.

## Features

- Support for basic authentication to access private registries.
- Option to specify a particular tag or automatically use the latest tag.
- Downloads all layers (blobs) of the specified Docker image.
- Saves blobs locally in a compressed `.tar.gz` format.

## Requirements

- Python 3.x
- `requests` library
- `urllib3` library
- `argparse` library

Ensure that you have the required libraries installed by running:

```bash
pip install requests urllib3 argparse
```

## Usage

To use the script, you will need to provide the Docker registry URL and the image name at a minimum. You can optionally specify the image tag, username, and password. If no tag is specified, the script will retrieve the latest tag available.

### Command Line Arguments

- `--registry_url`: The FULL URL for the Docker registry (required)
- `--image`: Name of the image (required)
- `--tag`: Specific tag of the image (optional, tries to get latest tag if not specified)
- `--username`: Username for authentication (default: `admin`)
- `--password`: Password for authentication (default: `admin`)

### Example Command

```bash
python3 blob_downloader.py --registry_url https://example.com:5000/v2 --image myapp --username user --password pass
```

This command downloads all blobs for the latest tag of the `myapp` image from the registry hosted at `https://example.com`.

## Important Notes

- The script is configured to suppress SSL certificate verification warnings due to `verify=False` in HTTP requests. This is not recommended for production use as it makes the connection susceptible to man-in-the-middle attacks.
- Blobs are downloaded to a subdirectory named `downloaded_blobs` within the directory from which the script is run.
- Error handling is built into the script to manage HTTP and general exceptions gracefully.

## License

This project is open-sourced under the MIT license. Feel free to fork and modify for your own use.
