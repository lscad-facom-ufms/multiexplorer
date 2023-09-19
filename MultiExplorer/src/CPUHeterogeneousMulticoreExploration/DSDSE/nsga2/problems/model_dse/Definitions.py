# coding=utf-8

class Definitions:
    def __init__(self, performance_predictor):
        self.performance_predictor = performance_predictor

        self.contador = 0

    # para
    # features[0] é "amount_original_cores"
    # features[1] é "area_orig"
    # features[2] é "power_orig"
    # features[3] é "performance_orig"
    # features[4] é "amount_ip_cores"
    # features[5] é o ipcore, um dicionário {"id","pow","area","perf"}

    # objective
    @staticmethod
    def power_density(individual):
        total_power = (
                individual.features[0] * individual.features[2]
                + individual.features[4] * individual.features[5]["pow"]
        )

        total_area = (
                individual.features[0] * individual.features[1]
                + individual.features[4] * individual.features[5]["area"]
        )

        try:
            return total_power / total_area
        except ZeroDivisionError:
            raise Exception("Individual with missing or invalid parameters: " + str(individual.features))

    def performance(self, individual):  # performance com preditor
        self.contador = self.contador + 1

        if self.contador % 10000 == 0:
            print("SVR Counter Performance: { " + str(self.contador) + " }\n")

        self.performance_predictor.set_imported_processor(individual.features[5]["id"])

        performance_pred = float(self.performance_predictor.get_results_l(
            individual.features[4],
            individual.features[0]
        ))

        return int(performance_pred)

    def performance_old(self, individual):  # performance ingenua
        self.contador = self.contador + 1

        if self.contador % 1000000 == 0:
            print("Counter Performance: { " + str(self.contador) + " }\n")
        # print "Gerou indivíduo com parâmetros" + str(individual.features)
        return (
                individual.features[3] * individual.features[0]
                + individual.features[5]["perf"] * individual.features[4]
        )

    # restriction
    @staticmethod
    def total_area(individual):
        return individual.features[0] * individual.features[1] + individual.features[4] * individual.features[5]["area"]

    @staticmethod
    def total_power(individual):
        t_power = (
                individual.features[0] * individual.features[2]
                + individual.features[4] * individual.features[5]["pow"]
        )

        t_area = (
                individual.features[0] * individual.features[1]
                + individual.features[4] * individual.features[5]["area"]
        )

        return t_power / t_area
