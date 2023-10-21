"""this module contains class that will describe the testing process
"""
import urllib.parse
from benchmark.shared.utils import validate_duration, validate_fuzzing_types

class Entry():
    """represents a single testing entry, which is a single execution of the dogefuzz
    """

    def __init__(self, file: str, contract: str, args: list, duration: str, fuzzing_types: list, times: int, path: str) -> None:
        self.file = file
        self.contract = contract
        self.args = args
        self.duration = duration
        self.fuzzing_types = fuzzing_types
        self.times = times
        self.path = path


class Request():
    """represents the testing request containing the set of tests to be made
    """

    def __init__(self, entries: list) -> None:
        self.entries: list = entries


class RequestFactory():
    """
    represents the factory pattern to create the Request instance
    """

    @classmethod
    def from_contracts_list(cls, contracts: list, duration: str, fuzzing_types: list, times: int, path: str) -> Request:
        """creates the Request class from a list of contracts
        """
        validate_duration(duration)
        validate_fuzzing_types(fuzzing_types)

        testing_entries = []
        for contract in contracts:
            entry = Entry(contract["file"], contract["name"], [], duration, fuzzing_types, times, path)
            testing_entries.append(entry)
        return Request(testing_entries)

    @classmethod
    def from_script(cls, script_content: map, contracts: list, path: str) -> Request:
        """creates the Request class from the script.json content
        """
        duration = script_content["duration"]
        fuzzing_types = script_content["fuzzingTypes"]
        times = script_content["times"]
        
        validate_duration(duration)
        validate_fuzzing_types(fuzzing_types)  
                          
        testing_entries = []
        if script_content.get("contracts") is None:
            for entry in contracts:
                entry = Entry(
                    entry["file"],
                    entry["name"],
                    [],
                    duration,
                    fuzzing_types,
                    times,
                    path
                )
                testing_entries.append(entry)
                 
        else:
            for entry in script_content["contracts"]:
                entry = Entry(
                    entry["file"],
                    entry["name"],
                    entry["arguments"],
                    duration,
                    fuzzing_types,
                    times,
                    path
                )
                testing_entries.append(entry)

        return Request(testing_entries)
