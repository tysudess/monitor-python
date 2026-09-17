from pathlib import Path
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("MONITOR_DISABLE_WEATHER", "1")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from PySide6.QtWidgets import QApplication
from monitor_noticias.ui.density_tuning import apply_density_tuning
from monitor_noticias.ui.layout_refresh import apply_reference_layout
from monitor_noticias.ui.main_window import MainWindow
from monitor_noticias.ui.pdf_visual_patch import apply_pdf_visual_patch
from monitor_noticias.ui.sections import Section


def polish(window: MainWindow) -> None:
    """Replica o acabamento executado por Application.run()."""
    apply_reference_layout(window)
    apply_density_tuning(window)
    apply_pdf_visual_patch(window)


def main() -> int:
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window._timer.stop()
    polish(window)

    # Gate funcional: trocar de seção não pode derrubar o estado maximizado.
    window.showMaximized()
    app.processEvents()
    window.navigate(Section.NEWS)
    polish(window)
    app.processEvents()
    app.processEvents()
    if not window.isMaximized():
        raise RuntimeError("Troca de aba removeu o estado maximizado da janela principal.")

    window.showNormal()
    window.resize(1721, 914)
    window.show()
    polish(window)
    app.processEvents()

    out_dir = ROOT / "artifacts" / "refined-ui"
    out_dir.mkdir(parents=True, exist_ok=True)
    targets = [
        (Section.HOME, "inicio"),
        (Section.NEWS, "noticias"),
        (Section.VIDEOS, "videos"),
        (Section.DEMANDS, "demandas"),
        (Section.SOURCES, "fontes"),
        (Section.HISTORY, "historico"),
        (Section.TERMS, "termos"),
        (Section.SETTINGS, "configuracoes"),
        (Section.PDF_EDITOR, "editor-pdf"),
        (Section.EXTRACTOR, "extrator-videos"),
        (Section.VIDEO_EDITOR, "editor-video"),
    ]
    for section, name in targets:
        window.navigate(section)
        window.pages[section].refresh(window.controller.state)
        window._tick()
        polish(window)
        app.processEvents()
        app.processEvents()
        polish(window)
        app.processEvents()
        if section == Section.VIDEO_EDITOR:
            video_page = window.pages[section]
            if video_page.editor.isWindow():
                raise RuntimeError("Editor de Vídeo voltou a abrir como janela top-level.")
            if video_page.editor.parentWidget() is not video_page:
                raise RuntimeError("Editor de Vídeo não está incorporado à página do Monitor.")
        path = out_dir / f"{name}-1721x914.png"
        if not window.grab().save(str(path), "PNG"):
            raise RuntimeError(f"Falha ao salvar {path}")
        print(f"SCREENSHOT={section.name}:{path}")

    print(f"WINDOW={window.width()}x{window.height()}")
    print(f"SIDEBAR={window.sidebar.width()}")
    window.exit_application()
    app.processEvents()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
