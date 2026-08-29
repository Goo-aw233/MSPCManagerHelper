"""ScrollableFrame: CTkScrollableFrame subclass with WinUI-like smooth scrolling.

CRITICAL: COMPATIBILITY WITH OTHER PLATFORMS IS POSSIBLE, BUT TESTING HAS BEEN CONDUCTED EXCLUSIVELY ON WINDOWS.

This subclass keeps CustomTkinter's own event flow (the content-area handler
_mouse_wheel_all stays bound via CTk's bind_all) but replaces the discrete jump
with a smooth, eased animation that matches the WinUI feel:

  - Content area: _mouse_wheel_all is overridden to start the animation.
  - Scrollbar: its wheel event is re-bound to the same animation handler.
  - Every notch scrolls `scroll_pixel_step` pixels (default 48 px, matching
    WinUI's default of 3 lines x 16 px) with an exponential ease-out.
"""

import sys

import customtkinter


class ScrollableFrame(customtkinter.CTkScrollableFrame):
    # Windows mouse wheel delta for a single notch.
    _WHEEL_DELTA = 120

    # Smooth-scroll animation timing (~60 fps, exponential ease-out).
    _SMOOTH_ANIMATION_MS = 14
    _SMOOTH_FACTOR = 0.25

    def __init__(self, master, scroll_pixel_step: int = 48, **kwargs):
        # Smooth-scroll animation state (per instance).
        self._scroll_pixel_step = max(1, int(scroll_pixel_step))
        self._smooth_target = None
        self._smooth_horizontal = False
        self._smooth_running = False
        self._smooth_after_id = None

        super().__init__(master=master, **kwargs)
        self._accelerate_scrollbar_wheel()

        # Harden the base class' <Configure> binding. The base CTkScrollableFrame
        # registers `self.bind("<Configure>", lambda e: ...)`, but Tk can deliver a
        # <Configure> event with an empty/incomplete argument list when this frame
        # is destroyed or recreated inside its canvas (e.g. during a UI refresh /
        # language switch). tkinter's `_substitute` then short-circuits and the
        # lambda is called with no event, raising
        # "missing 1 required positional argument: 'e'". Replace it with a handler
        # that tolerates a missing event argument.
        self.unbind("<Configure>")
        self.bind("<Configure>", self._update_scrollregion)

    def _update_scrollregion(self, *_args):
        """Refresh the canvas scroll region; tolerates a missing event argument."""
        self._parent_canvas.configure(scrollregion=self._parent_canvas.bbox("all"))

    # ------------------------------------------------------------------ #
    # Wheel Event Handlers
    # ------------------------------------------------------------------ #
    def _mouse_wheel_all(self, event):
        """Content-area wheel handler (overrides CTk, adds smooth scrolling)."""
        if not self._check_if_valid_scroll(event.widget):
            # Not a valid scroll target for this frame (e.g. a nested
            # CTkTextbox). Intentionally do NOT return "break" here so the
            # focused widget keeps handling the wheel itself.
            return None
        self._start_smooth_scroll(self._wheel_delta_px(event),
                                  horizontal=self._shift_pressed)
        return "break"

    def _on_scrollbar_mouse_wheel(self, event=None):
        """Scrollbar wheel handler (overrides CTk, adds smooth scrolling)."""
        self._start_smooth_scroll(self._wheel_delta_px(event),
                                  horizontal=(self._orientation == "horizontal"))
        return "break"

    def _wheel_delta_px(self, event):
        """Signed pixel delta for a wheel event (positive = down/right)."""
        if sys.platform.startswith("win"):
            return round(-self._scroll_pixel_step * event.delta / self._WHEEL_DELTA)
        elif sys.platform == "darwin":
            return round(-self._scroll_pixel_step * event.delta)
        else:
            # X11: the wheel produces <Button-4> (up) / <Button-5> (down).
            if event.num == 4:
                return -self._scroll_pixel_step
            if event.num == 5:
                return self._scroll_pixel_step
            # Some Linux environments (e.g. Wayland / newer Tk) deliver a
            # <MouseWheel> event with a delta instead.
            delta = getattr(event, "delta", 0) or 0
            if delta:
                return round(-self._scroll_pixel_step * delta / self._WHEEL_DELTA)
            return 0

    # ------------------------------------------------------------------ #
    # Smooth Scroll Animation
    # ------------------------------------------------------------------ #
    def _start_smooth_scroll(self, step_px, horizontal=False):
        if step_px == 0:
            return
        total, _, max_px = self._scroll_metrics(horizontal)
        if total <= 0:
            return
        # Accumulate on the current target while an animation is running, so
        # rapid consecutive notches keep adding instead of being eaten by the
        # animation's in-flight position.
        if (self._smooth_running and self._smooth_target is not None
                and self._smooth_horizontal == horizontal):
            base = self._smooth_target
        else:
            base = self._current_scroll_px(horizontal)
        self._smooth_target = min(max(0.0, base + step_px), max_px)
        self._smooth_horizontal = horizontal
        if not self._smooth_running:
            self._smooth_running = True
            self._smooth_loop()

    def _smooth_loop(self):
        if self._smooth_target is None:
            self._smooth_running = False
            self._smooth_after_id = None
            return

        horizontal = self._smooth_horizontal
        current = self._current_scroll_px(horizontal)
        diff = self._smooth_target - current
        if abs(diff) <= 1.0:
            # Snap to the target and stop the animation.
            self._set_scroll_px(self._smooth_target, horizontal)
            self._smooth_target = None
            self._smooth_running = False
            self._smooth_after_id = None
            return

        self._set_scroll_px(current + diff * self._SMOOTH_FACTOR, horizontal)
        self._smooth_after_id = self.after(self._SMOOTH_ANIMATION_MS, self._smooth_loop)

    # ------------------------------------------------------------------ #
    # Scroll Position Helpers (Canvas Scroll Region is in Pixels)
    # ------------------------------------------------------------------ #
    def _scroll_metrics(self, horizontal):
        region = self._parent_canvas.cget("scrollregion")
        if not region:
            return 0.0, 0.0, 0.0
        coords = [float(v) for v in region.split()]
        if horizontal:
            total = coords[2] - coords[0]
            view = self._parent_canvas.winfo_width()
        else:
            total = coords[3] - coords[1]
            view = self._parent_canvas.winfo_height()
        return total, view, max(0.0, total - view)

    def _current_scroll_px(self, horizontal):
        total, _, _ = self._scroll_metrics(horizontal)
        if total <= 0:
            return 0.0
        start = (self._parent_canvas.xview()[0] if horizontal
                 else self._parent_canvas.yview()[0])
        return start * total

    def _set_scroll_px(self, px, horizontal):
        total, _, _ = self._scroll_metrics(horizontal)
        if total <= 0:
            return
        fraction = min(1.0, max(0.0, px / total))
        if horizontal:
            self._parent_canvas.xview_moveto(fraction)
        else:
            self._parent_canvas.yview_moveto(fraction)

    # ------------------------------------------------------------------ #
    # Scrollbar Re-binding
    # ------------------------------------------------------------------ #
    def _accelerate_scrollbar_wheel(self):
        """Re-bind the scrollbar wheel so it scrolls smoothly like the content.

        Also cancel any in-flight smooth-scroll animation while the user drags
        the scrollbar, otherwise the animation fights the drag and the page
        bounces back and forth.
        """
        scrollbar_canvas = self._scrollbar._canvas
        scrollbar_canvas.unbind("<MouseWheel>")
        scrollbar_canvas.bind("<MouseWheel>", self._on_scrollbar_mouse_wheel)
        scrollbar_canvas.bind("<Button-1>", self._cancel_smooth_scroll, add=True)
        scrollbar_canvas.bind("<B1-Motion>", self._cancel_smooth_scroll, add=True)
        if "linux" in sys.platform:
            scrollbar_canvas.unbind("<Button-4>")
            scrollbar_canvas.unbind("<Button-5>")
            scrollbar_canvas.bind("<Button-4>", self._on_scrollbar_mouse_wheel)
            scrollbar_canvas.bind("<Button-5>", self._on_scrollbar_mouse_wheel)

    def _cancel_smooth_scroll(self, *_args):
        """Stop any in-flight smooth-scroll animation.

        Called when the user starts dragging the scrollbar so the animation
        does not fight the drag and make the page bounce back and forth.
        The trailing event argument from the Tk binding is intentionally
        ignored.
        """
        if getattr(self, "_smooth_after_id", None) is not None:
            try:
                self.after_cancel(self._smooth_after_id)
            except Exception:
                pass
        self._smooth_after_id = None
        self._smooth_running = False
        self._smooth_target = None

    def destroy(self):
        self._cancel_smooth_scroll()
        super().destroy()
