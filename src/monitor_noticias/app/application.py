from __future__ import annotations

import logging
import sys

from .exceptions import install_global_exception_hooks
from .logging_setup import configure_logging
from .paths import AppPaths


class Application:
    def __init__(self, paths: AppPaths | None = None) -> None:
        self.paths = paths or AppPaths.discover()

    def run(self) -> int:
        self.paths.ensure_runtime_dirs()
        configure_logging(self.paths)
        install_global_exception_hooks()
        log = logging.getLogger("monitor_noticias.application")
        log.info("Inicializando Monitor de Notícias PySide6")

        from PySide6.QtCore import QTimer
        from PySide6.QtWidgets import QApplication
        from monitor_noticias.app.composition import AppContainer
        from monitor_noticias.ui.layout_refresh import apply_reference_layout
        from monitor_noticias.ui.main_window import MainWindow

        qt_app = QApplication.instance() or QApplication(sys.argv)
        qt_app.setApplicationName("Monitor de Notícias")
        container = AppContainer.build(self.paths)
        window = MainWindow(controller=container.controller, paths=self.paths)

        def polish() -> None:
            apply_reference_layout(window)

        polish()
        if hasattr(window, "stack"):
            window.stack.currentChanged.connect(lambda _index: QTimer.singleShot(0, polish))

        window.show()
        QTimer.singleShot(0, polish)
        QTimer.singleShot(120, polish)
        try:
            result = qt_app.exec()
        finally:
            container.close()
        log.info("Aplicação encerrada com código %s", result)
        return int(result)


def main() -> int:
    return Application().run()
