import tkinter
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    """A page-level scrollable frame that exposes `.content_frame` for placing widgets.

    Usage:
        scrollable = ScrollableFrame(parent, bg=frame_bg)
        scrollable.pack(fill="both", expand=True)
        content = scrollable.content_frame
        # create widgets under `content`
    """

    def __init__(self, parent, bg=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Determine background color using ttk style fallback to widget's background.
        style = ttk.Style(self)
        frame_bg = bg if bg is not None else (style.lookup("TFrame", "background") or self.cget("background"))

        # Create scrollbar and canvas.
        self._page_scrollbar = ttk.Scrollbar(self, orient="vertical")
        self._page_scrollbar.pack(side="right", fill="y")

        self._canvas = tkinter.Canvas(self, borderwidth=0, highlightthickness=0, bg=frame_bg)
        self._canvas.pack(side="left", fill="both", expand=True)
        self._page_scrollbar.config(command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._page_scrollbar.set)

        # Inner frame that will hold page content.
        self.content_frame = ttk.Frame(self._canvas)
        self._window_id = self._canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Sync scrollregion with content size.
        def _on_content_configure(event):
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        self.content_frame.bind("<Configure>", _on_content_configure)

        # Keep inner window width match canvas width.
        def _on_canvas_configure(event):
            self._canvas.itemconfigure(self._window_id, width=event.width)
        self._canvas.bind("<Configure>", _on_canvas_configure)

        # Mouse wheel handling (Windows/macOS/Linux).
        def _on_mousewheel(event):
            try:
                # Windows / macOS
                delta = -int(event.delta / 120)
                self._canvas.yview_scroll(delta, "units")
            except Exception:
                # X11 Button-4 / Button-5
                if getattr(event, "num", None) == 4:
                    self._canvas.yview_scroll(-1, "units")
                elif getattr(event, "num", None) == 5:
                    self._canvas.yview_scroll(1, "units")

        def _bind_mousewheel(_):
            self._canvas.bind_all("<MouseWheel>", _on_mousewheel)
            self._canvas.bind_all("<Button-4>", _on_mousewheel)
            self._canvas.bind_all("<Button-5>", _on_mousewheel)

        def _unbind_mousewheel(_):
            self._canvas.unbind_all("<MouseWheel>")
            self._canvas.unbind_all("<Button-4>")
            self._canvas.unbind_all("<Button-5>")

        self.content_frame.bind("<Enter>", _bind_mousewheel)
        self.content_frame.bind("<Leave>", _unbind_mousewheel)

        # Ensure cleanup when destroyed.
        def _on_destroy(event):
            try:
                _unbind_mousewheel(None)
            except Exception:
                pass
        self.bind("<Destroy>", _on_destroy, add=True)
