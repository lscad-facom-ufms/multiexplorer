import json
import os


class DbSelector(object):
    """ This class makes the selection of json file
        concerning the database.
    """

    def __init__(self):
        pass

    @staticmethod
    def get_db_id(model_name, tech):
        return model_name + "_" + tech

    @staticmethod
    def get_performance_in_db(model_name, bench, app, tech):
        # type: (str, str, str, str) -> float
        id_input = DbSelector.get_db_id(model_name, tech)

        list_itens_bd = json.loads(
            open(os.path.dirname(os.path.realpath(__file__)) + '/db/Experimentos/all/' + tech + '.json').read()
        )

        for item_bd in list_itens_bd["ipcores"]:
            if item_bd["id"] == id_input:
                return float(item_bd["perf"])

        raise NotImplementedError(
            "Performance not predicted for parameters specified ->"
            + " model_name: " + model_name
            + "; bench: " + bench
            + "; app: " + app
            + "; tech: " + tech + "."
        )

    @staticmethod
    def get_core_in_db(model_name, tech):
        # type: (str, str) -> dict
        id_input = DbSelector.get_db_id(model_name, tech)

        db_dict = json.loads(
            open(os.path.dirname(os.path.realpath(__file__)) + '/db/Experimentos/all/' + tech + '.json').read()
        )

        for item_bd in db_dict["ipcores"]:
            if item_bd["id"] == id_input:
                return item_bd

    # This method return a string with the full path of database choosen
    @staticmethod
    def select_db(bench, app, tech):
        # type: (str, str, str) -> str
        database_path = os.path.dirname(os.path.realpath(__file__)) + '/db/Experimentos/all/' + tech + '.json'

        return database_path

    @staticmethod
    def all_cores_path():
        return os.path.dirname(os.path.realpath(__file__)) + '/db/Experimentos/all/all.json'
