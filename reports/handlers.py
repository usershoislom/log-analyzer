from reports.base import BaseReport, register_report


@register_report("handlers")
class HandlersReport(BaseReport):
    def process(self):
        for path in self.files:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if "django.request" not in line:
                        continue
                    endpoint = self.extract_endpoint(line)
                    level = self.extract_log_level(line)

                    if endpoint and level:
                        self.counter[endpoint][level] += 1
                        self.total_requests += 1

    def generate(self):
        self.print_summary()
