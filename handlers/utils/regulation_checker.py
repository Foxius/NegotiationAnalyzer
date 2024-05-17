import json
import re

class RegulationChecker:
    def __init__(self, regulation_file):
        with open(regulation_file, 'r') as file:
            self.regulations = json.load(file)

    def check_compliance(self, text):
        results = []
        for reg in self.regulations:
            pattern = self._create_regex_pattern(reg['pattern'])
            if re.search(pattern, text):
                results.append((True, reg['description']))
            else:
                results.append((False, reg['description']))
        return results

    def _create_regex_pattern(self, template):
        template = re.escape(template)
        template = template.replace(r'\%station\_name\%', r'[\w\s]+')
        template = template.replace(r'\%train\_number\%', r'\d+')
        return re.compile(template)
