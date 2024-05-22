import argparse
import requests
import urllib3
import os


def get_latest_tag(registry_url: str, image_name: str, auth: tuple) -> str:
	url = f"{registry_url}/{image_name}/tags/list"
	response = requests.get(url, auth=auth, verify=False)
	response.raise_for_status()
	tags = response.json()['tags']
	
	# Assuming the latest tag is at the end
	return tags[-1]


def get_manifest(registry_url: str, image_name: str, tag: str, auth: tuple) -> dict:
	url = f"{registry_url}/{image_name}/manifests/{tag}"
	headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
	response = requests.get(url, headers=headers, auth=auth, verify=False)
	response.raise_for_status()
	
	return response.json()


def download_blob(registry_url: str, image_name: str, digest: str, auth: tuple) -> str:
	url = f"{registry_url}/{image_name}/blobs/{digest}"
	response = requests.get(url, auth=auth, stream=True, verify=False)
	response.raise_for_status()

	# Extracting filename from digest and preparing to save it locally
	filename = digest.replace("sha256:", "")[:12] + ".tar.gz"
	filepath = os.path.join('downloaded_blobs', filename)

	# Ensure directory exists
	os.makedirs('downloaded_blobs', exist_ok=True)

	# Writing the blob to a file
	with open(filepath, 'wb') as f:
		for chunk in response.iter_content(chunk_size=8192):
			f.write(chunk)

	print(f"[+] Downloaded and saved blob {digest} as {filename}")
	return filepath


def download_all_blobs(registry_url: str, image_name: str, manifest: dict, auth: tuple) -> list:
	blobs = []
	for layer in manifest['layers']:
		digest = layer['digest']
		blob = download_blob(registry_url, image_name, digest, auth)
		blobs.append(blob)
	
	return blobs


def main():
	parser = argparse.ArgumentParser(description='Tries to download all blobs from a docker image via docker registry.')
	parser.add_argument('--registry_url', type=str, required=True, help='The FULL URL for the docker registry')
	parser.add_argument('--image', type=str, required=True, help='Image name')
	parser.add_argument('--tag', type=str, help='Image tag')
	parser.add_argument('--username', type=str, default='admin', help='Username to authenticate as')
	parser.add_argument('--password', type=str, default='admin', help='User password')
	args = parser.parse_args()

	auth = (args.username, args.password)

	try:
		if args.tag:
			latest_tag = args.tag
		else:
			latest_tag = get_latest_tag(args.registry_url, args.image, auth)
			print(f"[~] Latest tag: {latest_tag}")

		manifest = get_manifest(args.registry_url, args.image, latest_tag, auth)
		print(f"[~] Got manifest for tag {latest_tag}")

		blobs = download_all_blobs(args.registry_url, args.image, manifest, auth)
		print(f"[~] Downloaded {len(blobs)} blobs for the image {args.image} with tag {latest_tag}")

	except requests.HTTPError as e:
		print(f"[!] HTTP error occurred: {e}")
	except Exception as e:
		print(f"[!] An error occurred: {e}")


if __name__ == "__main__":
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	main()

