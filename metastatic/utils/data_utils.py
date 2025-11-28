import subprocess
from shutil import rmtree
from metastatic.utils.utils import run_shell_command
from metastatic.utils.gcp_utils import access_secret_version
import pandas as pd
import dvc.api


def get_cmd_to_get_raw_data(version: str,
							data_local_save_dir: str,
							dvc_remote_repo: str,
							dvc_data_folder: str,
							github_user_name: str,
							github_access_token: str) -> str:
	'''
	Get shell command to download raw data from dvc stor
	https://github.com/amir2520/metastasis-data-versioning.git
	https://username:token@github.com/amir2520/metastasis-data-versioning.git
	'''
	without_https = dvc_remote_repo.replace('https://', '')
	dvc_remote_repo = f'https://{github_user_name}:{github_access_token}@{without_https}'
	command = f"dvc get {dvc_remote_repo} {dvc_data_folder} --rev {version} -o {data_local_save_dir}"
	return command

def get_raw_data_with_version(version: str,
								data_local_save_dir: str,
								dvc_remote_repo: str,
								dvc_data_folder: str,
								github_user_name: str,
								github_access_token: str) -> None:
	rmtree(data_local_save_dir, ignore_errors = True)
	
	command = get_cmd_to_get_raw_data(version, data_local_save_dir, dvc_remote_repo,
									  dvc_data_folder, github_user_name, github_access_token)
	run_shell_command(command)

	
def get_data_url_with_version(version: str,
							  dvc_remote_repo: str,
							  dvc_data_folder: str,
							  dataset_name: str,
							  github_user_name: str,
							  github_access_token: str) -> str:
	dataset_full_path = dvc_data_folder + '/' + dataset_name
	without_https = dvc_remote_repo.replace('https://', '')
	dvc_remote_repo = f'https://{github_user_name}:{github_access_token}@{without_https}'
	url = dvc.api.get_url(dataset_full_path, dvc_remote_repo, rev=version)
	return url


def get_repo_address_with_access_token(gcp_project_id: str, gcp_secret_id: str, repo_address: str, user_name: str) -> str:
	access_token = access_secret_version(gcp_project_id, gcp_secret_id)
	repo_address = repo_address.replace('https://', '')
	return f'https://{user_name}:{access_token}@{repo_address}'


def filter_based_on_minimum_number_of_words(df: pd.DataFrame, min_nrof_words: int):
	return df[df['cleaned_text'].str.split().apply(len) >= min_nrof_words]