"""
this module contains the service that peforms operations in the benchmark
"""
import multiprocessing
import docker
import os

from datetime import datetime
from time import sleep
from docker import APIClient
from docker.models.containers import Container
from benchmark.services.contract import ContractService
from benchmark.services.dogefuzz import DogefuzzService
from benchmark.services.progress import ProgressService
from benchmark.services.queue import QueueService
from benchmark.services.server import ServerService
from benchmark.shared.dogefuzz.api import TaskReport
from benchmark.shared.exceptions import ContractNotFoundException
from benchmark.shared.singleton import SingletonMeta
from benchmark.shared.testing import Request


class BenchmarkService(metaclass=SingletonMeta):
    """this class represents the service that peforms operations in the benchmark
    """

    def __init__(self) -> None:
        self._server_service = ServerService()
        self._progress_service = ProgressService()
        self._queue_service = QueueService()
        self._dogefuzz_service = DogefuzzService()
        self._contract_service = ContractService()
        self._docker_client = docker.from_env()         

    def get_health(self, container: Container):
        api_client = APIClient()
        inspect_results = api_client.inspect_container(container.name)
        return inspect_results['State']['Health']['Status']

    def run(self, request: Request, stop: multiprocessing.Event) -> list:
        "runs the benchmark following the testing request class"
        self._server_service.start()
        self._progress_service.start()

        executions = {}
        for entry in request.entries:
            if stop.is_set():
                break

            executions[entry.file] = {}
            for fuzzing_type in entry.fuzzing_types:
                contract_executions = []
                for _ in range(entry.times):
                    result = {
                        "startTime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    }

                    contract_source = None
                    try:
                        contract_source = self._contract_service.read_contract(
                            entry)
                    except ContractNotFoundException as ex:
                        result["status"] = "error"
                        result["error"] = str(ex)
                        result["execution"] = None
                        result["endTime"] = datetime.now().strftime(
                            "%d/%m/%Y %H:%M:%S")
                        contract_executions.append(result)
                        step = 100/(len(request.entries) *
                                    len(entry.fuzzing_types)*entry.times)
                        self._progress_service.update_progress_bar(step)
                        continue

                    task_id = None
                    try:
                        task_id = self._dogefuzz_service.start_task(
                            entry, contract_source, fuzzing_type)
                    except Exception as ex:
                        result["status"] = "error"
                        result["error"] = str(ex)
                        result["execution"] = None
                        result["endTime"] = datetime.now().strftime(
                            "%d/%m/%Y %H:%M:%S")
                        contract_executions.append(result)
                        step = 100/(len(request.entries) *
                                    len(entry.fuzzing_types)*entry.times)
                        self._progress_service.update_progress_bar(step)
                        continue

                    timeout = int(entry.duration[:-1])
                    request_result = self._wait_dogefuzz_respond(
                        task_id, timeout, stop)
                    if request_result is None or request_result.task_status == "error":
                        result["status"] = "timeout"
                        result["error"] = f"timeout after {timeout} + 5 minutes or error"
                        result["execution"] = None
                        result["endTime"] = datetime.now().strftime(
                            "%d/%m/%Y %H:%M:%S")
                        contract_executions.append(result)
                        self._restart_containers()
                    else:
                        result["status"] = "success"
                        result["error"] = None
                        result["endTime"] = datetime.now().strftime(
                            "%d/%m/%Y %H:%M:%S")
                        result["execution"] = request_result.to_dict()
                        contract_executions.append(result)
                        
                    step = 100/(len(request.entries) *
                                len(entry.fuzzing_types)*entry.times)
                    self._progress_service.update_progress_bar(step)
                executions[entry.file][fuzzing_type] = contract_executions

        if (int(entry.duration[:-1]) >= 10):
            self._restart_containers()
                        
        self._progress_service.stop()
        self._server_service.stop()

        return executions


    def _restart_containers(self):
        # Restart dogefuzz and geth for the next test, 
        dogefuzz_id = os.environ.get("DOGEFUZZ")
        geth_id = os.environ.get("GETH")                        
        container = self._docker_client.containers.get(geth_id)
        container.restart()
        while self.get_health(container) != 'healthy':
            sleep(1)                        
        container = self._docker_client.containers.get(dogefuzz_id)
        container.restart()
        while self.get_health(container) != 'healthy':
            sleep(1)
    
    def _wait_dogefuzz_respond(self, task_id: str, timeout: int, stop: multiprocessing.Event) -> TaskReport:
        report = None
        limit = (timeout + 5) * 60  # duration + 5 minutes
        time = 0
        while True:
            if stop.is_set():
                break

            report = self._queue_service.get()
            if report is not None and report.task_id == task_id:
                break
            sleep(5)
            time = time + 5
            if time > limit:
                return None
        return report
