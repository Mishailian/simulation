import json

class Functions_json:
    @staticmethod
    def load_results(results_file):
        try:
            with open(results_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    @staticmethod
    def save_results(results, results_file):
        with open(results_file, "w") as file:
            json.dump(results, file)

    def save_result(self, duration):
        results = self.load_results()
        results.append(duration)
        results.sort(reverse=True)
        results = results[:10]
        self.save_results(results)