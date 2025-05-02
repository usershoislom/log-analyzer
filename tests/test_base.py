import pytest

from reports import BaseReport, register_report, REPORT_TYPES


class DummyReport(BaseReport):
    def process(self):
        self.counter["/api/test"]["INFO"] = 2
        self.counter["/admin/page"]["ERROR"] = 1
        self.total_requests = 3

    def generate(self):
        self.report_content = "Отчёт готов."


@pytest.mark.parametrize("filename", ["file1.log", "test.log", "access.log"])
def test_validate_files_valid(tmp_path, filename):
    file_path = tmp_path / filename
    file_path.write_text("some log info")

    report = DummyReport([str(file_path)])
    assert report.files == [str(file_path)]


@pytest.mark.parametrize("filename", ["nofile1.log", "missing.txt", "404.log"])
def test_validate_files_invalid(tmp_path, filename):
    file_path = tmp_path / filename

    with pytest.raises(SystemExit) as exc:
        DummyReport([str(file_path)])
    assert exc.value.code == 1


@pytest.mark.parametrize(
    "line, expected",
    [
        ("INFO Something happened", "INFO"),
        ("ERROR: critical failure", "ERROR"),
        ("no log level here", None),
    ],
)
def test_extract_log_level(line, expected):
    assert BaseReport.extract_log_level(line) == expected


@pytest.mark.parametrize(
    "line, expected",
    [
        ("[django.request] GET /api/test/", "/api/test/"),
        ("[django.request] POST /admin/login", "/admin/login"),
        ("Unrelated log line", None),
    ],
)
def test_extract_endpoint(line, expected):
    assert BaseReport.extract_endpoint(line) == expected


def test_print_summary_output(capsys):
    report = DummyReport([__file__])
    report.process()
    report.print_summary()

    captured = capsys.readouterr()
    assert "Total requests: 3" in captured.out
    assert "/api/test" in captured.out
    assert "/admin/page" in captured.out
    assert "INFO" in captured.out
    assert "ERROR" in captured.out


def test_run_calls_process_and_generate():
    report = DummyReport([__file__])
    report.run()
    assert report.report_content == "Отчёт готов."


def test_register_report_decorator():
    @register_report("test_report")
    class MyTestReport(BaseReport):
        def process(self):
            pass

        def generate(self):
            pass

    assert "test_report" in REPORT_TYPES
    assert REPORT_TYPES["test_report"] is MyTestReport
