import json

class Functions_json:
    def load_results(self):
        try:
            with open(self.results_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_results(self, results):
        with open(self.results_file, "w") as file:
            json.dump(results, file)

    def save_result(self, duration):
        results = self.load_results()
        results.append(duration)
        results.sort(reverse=True)
        results = results[:10]
        self.save_results(results)