"""CLI moodule
"""
import json
import multiprocessing
import signal
import os
import urllib.parse

from datetime import datetime
from benchmark.services.contract import ContractService
from benchmark.services.benchmark import BenchmarkService
from benchmark.services.progress import ProgressService
from benchmark.services.drive import DriveService
from benchmark.services.script import ScriptService
from benchmark.shared.testing import RequestFactory
from benchmark.config import Config

stop_threads = multiprocessing.Event()


def signal_handler(sig, frame):
    print('You pressed Ctrl+C! shuting down benchmark...')
    stop_threads.set()


signal.signal(signal.SIGINT, signal_handler)


class Benchmark():
    """the CLI options for benchmarking the Dogefuzz project
    """

    def __init__(self) -> None:
        self._benchmark_service = BenchmarkService()
        self._progress_service = ProgressService()
        self._drive_service = DriveService()
        self._contract_service = ContractService()
        self._script_service = ScriptService()
        self._config = Config()        

    def script(self, script_name: str):
        """benchmarks based on a script file
        """
        request = self._script_service.read_testing_request_from_script(script_name)
        result = self._benchmark_service.run(request, stop_threads)
        self._write_result(result, None)

    def all(self, uri: str, duration: str, fuzzing_types: str, times: str, result_prefix: str):
        """benchmarks all available contracts
        """
        parsed_uri = urllib.parse.urlparse(uri)
        if parsed_uri.scheme:
            self._drive_service.download_contracts(uri)
            path = self._config.contracts_download_folder + "/" + "contracts"        
            contracts = self._contract_service.list_contracts_from_contract_list()
        else: 
            path = uri
            contracts_csv = os.path.join(path, "contracts.csv")
            if not os.path.exists(contracts_csv):
                contracts = self._contract_service.list_contracts_from_folder(path)
            else:
                contracts = self._contract_service.list_contracts_from_contract_list_folder(path)
        
        fuzzing_types_list = str(fuzzing_types).split(";")        
        request = RequestFactory.from_contracts_list(
            contracts, duration, fuzzing_types_list, times, path)

        result = self._benchmark_service.run(request, stop_threads)
        self._write_result(result, result_prefix)
        print("SUCCESS")

    def generate_results(self, timestamp: str):
        """generates the results
        """
        self._progress_service.generate_results()

    def download_contracts(self):
        """downloads contracts from cloud
        """
        self._drive_service.download_contracts()

    def _write_result(self, result: list, result_prefix: str):
        """writes the result to a file
        """
        timestamp = datetime.now().timestamp()
        
        dt = datetime.fromtimestamp(timestamp)
        formatted_timestamp = dt.strftime('%Y%m%d%H%M%S')
        if result_prefix:
            folder_path = os.path.join("results", result_prefix, formatted_timestamp)
        else:
            folder_path = os.path.join("results", formatted_timestamp)
            
        os.makedirs(folder_path, exist_ok=True)

        with open(f"{folder_path}/result.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(result, indent=4))
