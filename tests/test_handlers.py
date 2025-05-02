import pytest
from reports.handlers import HandlersReport


def test_handlers_report_registration():
    from reports.base import REPORT_TYPES

    assert "handlers" in REPORT_TYPES
    assert REPORT_TYPES["handlers"] is HandlersReport


def test_process_valid_logs(tmp_path):
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "[django.request] GET /api/test/ INFO some log\n"
        "[django.request] POST /admin/login ERROR something went wrong\n"
        "[django.request] GET /api/test/ INFO another log\n"
    )

    report = HandlersReport([str(log_file)])
    report.process()

    assert report.total_requests == 3
    assert report.counter["/api/test/"]["INFO"] == 2
    assert report.counter["/admin/login"]["ERROR"] == 1


def test_generate_summary_output(tmp_path, capsys):
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "[django.request] GET /api/test/ INFO some log\n"
        "[django.request] POST /admin/login ERROR something went wrong\n"
        "[django.request] GET /api/test/ INFO another log\n"
    )

    report = HandlersReport([str(log_file)])
    report.process()
    report.generate()

    captured = capsys.readouterr()
    assert "Total requests: 3" in captured.out
    assert "/api/test" in captured.out
    assert "/admin/login" in captured.out
    assert "INFO" in captured.out
    assert "ERROR" in captured.out


@pytest.mark.parametrize(
    "log_content, expected_total_requests, expected_counter",
    [
        (
            "[django.request] GET /api/test/ INFO log 1\n"
            "[django.request] POST /admin/login ERROR log\n",
            2,
            {"/api/test/": {"INFO": 1}, "/admin/login": {"ERROR": 1}},
        ),
        (
            "[django.request] GET /api/test/ INFO log 1\n"
            "[django.request] GET /api/test/ INFO log 2\n",
            2,
            {"/api/test/": {"INFO": 2}},
        ),
        (
            "[django.request] POST /admin/login ERROR log"
            "\n[django.request] POST /admin/login ERROR log\n",
            2,
            {"/admin/login": {"ERROR": 2}},
        ),
    ],
)
def test_process_various_logs(
    tmp_path, log_content, expected_total_requests, expected_counter
):
    log_file = tmp_path / "log.txt"
    log_file.write_text(log_content)

    report = HandlersReport([str(log_file)])
    report.process()

    assert report.total_requests == expected_total_requests
    for endpoint, levels in expected_counter.items():
        for level, count in levels.items():
            assert report.counter[endpoint][level] == count


def test_process_empty_log(tmp_path):
    log_file = tmp_path / "empty_log.txt"
    log_file.write_text("")

    report = HandlersReport([str(log_file)])
    report.process()

    assert report.total_requests == 0
    assert not report.counter


def test_process_different_encoding(tmp_path):
    log_file = tmp_path / "log_windows1251.txt"
    log_content = "[django.request] GET /api/test/ INFO some log\n"
    log_file.write_text(log_content, encoding="windows-1251")

    report = HandlersReport([str(log_file)])
    report.process()

    assert report.total_requests == 1
    assert report.counter["/api/test/"]["INFO"] == 1
