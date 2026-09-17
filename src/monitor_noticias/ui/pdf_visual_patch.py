from __future__ import annotations

from types import MethodType

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


def apply_pdf_visual_patch(window: QWidget) -> None:
    """Mostra estado vazio claro no preview sem alterar o motor PDF/crop."""
    pages = getattr(window, "pages", {})
    if not isinstance(pages, dict):
        return

    page = next((p for p in pages.values() if p.__class__.__name__ == "RefinedPdfEditorPage"), None)
    if page is None:
        return

    preview = getattr(page, "preview", None)
    if preview is None:
        return

    overlay = getattr(preview, "_reference_empty_overlay", None)
    if overlay is None:
        overlay = QLabel(
            "▱\n\nArraste e solte seus arquivos aqui\n"
            "Suporte a PDFs e imagens (JPG, PNG, etc.)",
            preview,
        )
        overlay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay.setWordWrap(True)
        overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        overlay.setStyleSheet(
            "QLabel{background:#FBFDFF;color:#667DA2;"
            "border:1px dashed #BCD5F0;border-radius:10px;"
            "font-size:13px;font-weight:600;padding:24px;}"
        )

        layout = preview.layout()
        if layout is None:
            layout = QVBoxLayout(preview)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
        layout.addWidget(overlay)
        preview._reference_empty_overlay = overlay

        original_set_image = preview.set_image

        def set_image_with_overlay(self, image, zoom, existing_crop=None):
            original_set_image(image, zoom, existing_crop)
            empty = image is None or image.isNull()
            self._reference_empty_overlay.setVisible(empty)
            if empty:
                self._reference_empty_overlay.raise_()

        preview.set_image = MethodType(set_image_with_overlay, preview)

    image = getattr(preview, "_image", None)
    empty = image is None or image.isNull()
    overlay.setVisible(empty)
    if empty:
        overlay.raise_()
