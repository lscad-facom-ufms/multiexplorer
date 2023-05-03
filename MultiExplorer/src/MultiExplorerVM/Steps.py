from MultiExplorer.src.Infrastructure.Events import Event
from MultiExplorer.src.Infrastructure.ExecutionFlow import Step
from Adapters import CloudsimAdapter

class CloudSimStep(Step):

    def get_results(self):
        return self.adapter.get_results()
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                CloudSimStep,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(CloudSimStep, self).__init__()

        self.adapter = CloudsimAdapter() #mudar para o adapter do cloudsim (nsga2main)

    @staticmethod
    def get_label():
        return 'Simulation' #Ver com o Danillo  qual seria o nome mais adequado

    @staticmethod
    def has_user_input():
        return True

    def get_user_inputs(self):
        return self.adapter.get_user_inputs()

    def __execute__(self):
        self.execution_exception = None

        try:
            self.adapter.execute()
        except BaseException as exception:
            self.execution_exception = exception

    def __finish__(self):
        if self.execution_exception is None:
            self.fire(Event.STEP_EXECUTION_ENDED)
        else:
            self.fire(Event.STEP_EXECUTION_FAILED, self)

    def get_presenter(self):
        return CloudsimPresenter() # Mudar para o CloudSim