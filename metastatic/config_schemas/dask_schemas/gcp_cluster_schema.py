from omegaconf import SI, MISSING
from dataclasses import dataclass, field
from hydra.core.config_store import ConfigStore
from typing import Optional, Any


@dataclass
class DaskGCPClusterConfig:
	_target_: str = 'dask_cloudprovider.gcp.GCPCluster'
	projectid: str = SI("${oc.env:DATASET_GCP_PROJECT_ID}")
	zone: str = SI("${oc.env:ZONE}")
	network: str = SI("${oc.env:NETWORK}")
	network_projectid: Optional[str] = SI("${oc.env:DATASET_GCP_PROJECT_ID}")
	machine_type: str = "n1-standard-1"
	source_image: str = "projects/ubuntu-os-cloud/global/images/ubuntu-minimal-2004-focal-v20220203"
	docker_image: Optional[str] = 'daskdev/dask:latest'
	docker_args: str = ""
	extra_bootstrap: Optional[list[str]] = field(default_factory=lambda: ["gcloud auth configure-docker us-east1-docker.pkg.dev --quiet"])
	ngpus: Optional[int] = 0
	gpu_type: Optional[str] = None
	filesystem_size: int = 10
	disk_type: str = 'pd-standard'
	on_host_maintenance: str = "TERMINATE"

	n_workers: int = 0
	worker_class: str = "dask.distributed.Nanny"
	worker_options: dict[str, Any] = field(default_factory = lambda: {})
	env_vars: dict[str, str] = field(default_factory = lambda: {})
	scheduler_options: dict[str, str] = field(default_factory = lambda: {})
	silence_logs: Optional[bool] = None
	asynchronous: Optional[bool] = None
	security: bool = True
	preemptible: Optional[bool] = False
	debug: Optional[bool] = False
	instance_labels: Optional[dict[str, str]] = None


def setup_config():
	cs = ConfigStore.instance()
	cs.store(
		name="dask_gcp_cluster_schema",
		node=DaskGCPClusterConfig,
		group='dask_cluster'
	)