from sklearn.externals import joblib


class PerformancePredictor(object):
    """Main Class"""
    def __init__(self, processor, nbr_ip_cores, nbr_orig_cores):
        # type: (str, int, int) -> None
        self.processor = processor

        self.nbr_ip_cores = nbr_ip_cores

        self.nbr_orig_cores = nbr_orig_cores

    def get_results(self):
        preditor = joblib.load(self.processor + '.pkl')

        scalator = joblib.load('Scaler_' + self.processor + '.pkl')

        total_nbr_cores = self.nbr_orig_cores + self.nbr_ip_cores

        constraints = [[self.nbr_orig_cores, self.nbr_ip_cores, total_nbr_cores]]

        steps = scalator.transform(constraints)

        print("\nCasos de Teste: ", steps)

        resp = preditor.predict(steps)

        print("\nresp: ", resp)
