"""
this module contains logic to manage script file
"""
import json
import urllib.parse
from benchmark.config import Config
from benchmark.shared.singleton import SingletonMeta
from benchmark.shared.testing import Request, RequestFactory
from benchmark.services.drive import DriveService
from benchmark.services.contract import ContractService
from benchmark.shared.exceptions import InvalidURI

class ScriptService(metaclass=SingletonMeta):
    """this class represent the service responsible to operations with the script configuration
    """

    def __init__(self) -> None:
        self._config = Config()
        self._contract_service = ContractService()        
        self._drive_service = DriveService()        

    def read_testing_request_from_script(self, script_name: str) -> Request:
        """reads the script file and convert it into a Request class
        """
        with open(script_name + ".json", encoding="utf-8") as file:
            script_content = json.load(file)
            uri = script_content["uri"]
            parsed_uri = urllib.parse.urlparse(uri)
            contracts = []
            if parsed_uri.scheme == "file":
                contracts = self._contract_service.list_contracts_from_folder(parsed_uri.path)
                path = parsed_uri.path
            elif parsed_uri.scheme == "http" or parsed_uri.scheme == "https":
                self._drive_service.download_contracts(uri)
                contracts = self._contract_service.list_contracts_from_contract_list()
                path = self._config.contracts_download_folder + "/" + "contracts"
            else:
                raise InvalidURI("an invalid UIR was provided")
            
            request = RequestFactory.from_script(script_content, contracts, path)
        return request
