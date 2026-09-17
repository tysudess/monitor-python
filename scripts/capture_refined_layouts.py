from pathlib import Path
import os
import sys
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("MONITOR_DISABLE_WEATHER", "1")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from PySide6.QtWidgets import QApplication
from monitor_noticias.automation.models import LiveSearchProgress
from monitor_noticias.models import News
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


def seed_news_reference(window: MainWindow) -> None:
    """Insere somente dados efêmeros para a captura visual da aba Notícias."""
    now = int(time.time() * 1000)
    templates = [
        ("sapo.pt", "Diana Azevedo comanda a Capitania do Porto da Nazaré - sapo.pt", "Diana Azevedo comanda a Capitania do Porto da Nazaré, reforçando a segurança marítima na região.", "CAPITANIA DOS PORTOS"),
        ("Grupo Pilau", "SALTO DO JACUÍ: Polícia Civil e Brigada Militar prendem dois e apreendem menor - Grupo Pilau", "Polícia Civil e Brigada Militar realizam operação no Salto do Jacuí e prendem dois suspeitos.", "MILITAR"),
        ("R7", "Polícias Civil e Militar realizam prisões e apreensões em Santa Maria, em Campos - R7", "Operação integrada resulta na prisão de suspeitos e na apreensão de materiais ilícitos em Campos.", "MILITAR"),
        ("Estado de Minas", "Thales apresenta o HexaForce: sistema de comando e controle soberano, impulsionado por IA, para a OTAN e nações aliadas", "Empresa brasileira apresenta inovação em defesa com tecnologia de IA para comando e controle.", "FORÇAS ARMADAS"),
        ("Tribuna de Petrópolis", "Líbano, França e Jordânia se reúnem para angariar apoio ao exército libanês - Tribuna de Petrópolis", "Encontro discute apoio internacional às forças armadas do Líbano em meio à escalada de tensões.", "EXÉRCITO"),
    ]
    news = []
    for index in range(25):
        source, title, snippet, term = templates[index % len(templates)]
        news.append(
            News(
                id=index + 1,
                title=title,
                source=source,
                date=now - index * 180_000,
                link=f"https://example.test/noticia/{index + 1}",
                snippet=snippet,
                matchedTerm=term,
                capturedAt=now - index * 180_000,
            )
        )
    state = window.controller.state
    state.news = news
    state.new_news_links = {item.link for item in news}
    state.news_progress = LiveSearchProgress(
        active=False,
        kind="news",
        startedAt=now - 20_000,
        finishedAt=now,
        completed=31,
        total=31,
        currentSource="",
        currentQuery="",
        found=106,
        newCount=106,
        errors=0,
    )
    state.news_busy = False
    state.status = "Busca concluída com sucesso"
    state.last_news_duration_ms = 20_000


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
        if section == Section.NEWS:
            seed_news_reference(window)
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
