import ctypes
import sys
import tkinter

import customtkinter


class ContentMenu(tkinter.Menu):
    """Right-click menu for a text widget, with built-in copy, clear and refresh actions.

    The menu owns the menu-related behavior: rendering, theming, binding, and the
    implementations of the available actions.

    Parameters:
        parent: Tk widget that owns the menu.
        textbox: Text widget the actions operate on.
        app_translator: AppTranslator used to translate menu labels.
        font_family: Font family applied to the menu items.
        actions: Action names in display order. Use ``None`` to insert a separator.
            See the action constants defined below for the supported values.
        content_provider: Callable returning the current text (or ``None`` when it
            cannot be read). Required when ``REFRESH`` is used; it is the only
            data-source specific part left to the caller.

    USAGE EXAMPLE:

        self.content_menu = ContentMenu(
            parent=self,
            textbox=self.content_textbox,
            app_translator=self.app_translator,
            font_family=self.font_family,
            actions=[
                ContentMenu.REFRESH,
                None,   # Separator
                ContentMenu.COPY,
                ContentMenu.CLEAR,
                None,   # Separator
                ContentMenu.SELECT_ALL,
            ],
            content_provider=self._read_content,
        )
        self.content_menu.load_content(initial_content)
    """

    CLEAR = "clear"
    COPY = "copy"
    REFRESH = "refresh"
    SELECT_ALL = "select_all"

    _LABEL_KEYS = {
        COPY: "pages.common.copy",
        CLEAR: "pages.common.clear",
        REFRESH: "pages.common.refresh",
        SELECT_ALL: "pages.common.select_all",
    }

    # Operations disabled on an empty text box.
    _CONTENT_DEPENDENT_ACTIONS = (CLEAR, COPY, SELECT_ALL)

    # Design size in points; scaled to the real display DPI in _menu_font_size().
    _FONT_SIZE = 10

    # Text color for actions that are unavailable on an empty text box. It is applied per entry
    # rather than through the menu's "-disabledforeground" option; see _update_action_states().
    _DISABLED_FG = ("#737373", "#9a9a9a")

    _COLORS = {
        "bg": ("#fafafa", "#2b2b2b"),
        "fg": ("#1a1a1a", "#f0f0f0"),
        "activebackground": ("#e6e6e6", "#3d3d3d"),
        "activeforeground": ("#111111", "#ffffff"),
    }

    def __init__(self, parent, textbox, app_translator, font_family, actions, content_provider=None):
        super().__init__(parent, tearoff=0)
        self.textbox = textbox
        self.font_family = font_family
        self.content_provider = content_provider
        self._action_indexes = {}
        self._font_size_by_dpi = {}
        self._bound = False

        position = 0
        for action in actions:
            if action is None:
                self.add_separator()
                position += 1
                continue
            if action not in self._LABEL_KEYS:
                raise ValueError(f"Unsupported Content Menu Action: {action!r}")
            if action == self.REFRESH and content_provider is None:
                raise ValueError("A content_provider is required for the refresh action.")
            self.add_command(
                label=app_translator.translate(self._LABEL_KEYS[action]),
                command=getattr(self, f"{action}_content"),
            )
            self._action_indexes[action] = position
            position += 1

    def bind_to(self):
        if self._bound:
            return

        self._bound = True
        self.textbox.bind("<Button-3>", self._show)

        # Bind to the top-level window. Multiple pages may share the same top-level window,
        # so each handler checks whether its own text box is currently visible.
        toplevel = self.textbox.winfo_toplevel()
        toplevel.bind("<Shift-F10>", self._show_from_keyboard, add="+")
        # Windows reports the context-menu key as the "Menu" keysym.
        toplevel.bind("<Menu>", self._show_from_keyboard, add="+")

    def select_all_content(self):
        """Select the whole content."""
        if not self._has_content():
            return

        self.textbox.tag_add(tkinter.SEL, "1.0", "end-1c")
        self.textbox.mark_set(tkinter.INSERT, "1.0")
        self.textbox.focus_set()

    def copy_content(self):
        """Copy the selection, or the whole content when nothing is selected."""
        if not self._has_content():
            return

        try:
            selected_text = self.textbox.get("sel.first", "sel.last")
        except tkinter.TclError:
            selected_text = self.textbox.get("1.0", "end-1c")

        if selected_text:
            self.textbox.clipboard_clear()
            self.textbox.clipboard_append(selected_text)

    def clear_content(self):
        """Remove all content while preserving the widget state."""
        if not self._has_content():
            return

        self.load_content("")

    def refresh_content(self):
        """Reload the content from the provider, keeping the scroll position."""
        if self.content_provider is None:
            return

        content = self.content_provider()
        if content is None:
            # Keep the current content when the source cannot be read.
            return

        # Restore by line number, not by fraction.
        # As log files grow, and a fraction would drift down the file.
        top_line = self.textbox.index("@0,0")
        was_at_bottom = self.textbox.yview()[1] >= 0.999
        horizontal_position = self.textbox.xview()[0]

        self.load_content(content)

        if was_at_bottom:
            self.textbox.see("end")
        else:
            self.textbox.yview(top_line)
        self.textbox.xview_moveto(horizontal_position)

    def load_content(self, content):
        """Replace the whole content while preserving the widget state."""
        state = self.textbox.cget("state")
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", content)
        self.textbox.configure(state=state)

    def _show(self, event):
        self._popup(event.x_root, event.y_root, event.widget)

    def _show_from_keyboard(self, _):
        """Open the menu at the insertion cursor, for the keyboard shortcuts."""
        # Hidden pages and unselected tabs stay unmapped, only the visible textbox reacts.
        if not self.textbox.winfo_viewable():
            return

        # CTkTextbox wraps a plain Text widget; bbox() and the root coordinates belong to it.
        widget = getattr(self.textbox, "_textbox", self.textbox)

        try:
            bbox = widget.bbox(tkinter.INSERT)
        except tkinter.TclError:
            bbox = None

        if bbox:
            x_root = widget.winfo_rootx() + bbox[0]
            y_root = widget.winfo_rooty() + bbox[1] + bbox[3]
        else:
            # When the insertion cursor is not visible, place it at the top left corner of the widget.
            x_root = widget.winfo_rootx()
            y_root = widget.winfo_rooty()

        self._popup(x_root, y_root, widget)
        return "break"

    def _popup(self, x_root, y_root, widget):
        colors = {
            option: self._resolve_color(modes)
            for option, modes in self._COLORS.items()
        }
        self.configure(**colors, font=(self.font_family, self._menu_font_size(widget)))
        self._update_action_states(colors, self._resolve_color(self._DISABLED_FG))
        self.tk_popup(x_root, y_root)

    def _menu_font_size(self, widget):
        # Use real DPI compensation to fix the problem where text appears blurry and too small on high-DPI screens.
        # CustomTkinter only sets the process to be DPI-aware after Tk has started, causing Tk's font
        # scaling to remain at 96 DPI, while native menus are rendered according to the monitor's real DPI.
        if not sys.platform.startswith("win"):
            return self._FONT_SIZE

        try:
            # Using the window that received the event, the font size will follow the multi-monitor settings.
            real_dpi = ctypes.windll.user32.GetDpiForWindow(widget.winfo_toplevel().winfo_id())
            tk_dpi = self.winfo_fpixels("1i")
        except (AttributeError, OSError, tkinter.TclError):
            return self._FONT_SIZE

        if not real_dpi or not tk_dpi:
            return self._FONT_SIZE

        font_size = self._font_size_by_dpi.get(real_dpi)
        if font_size is None:
            font_size = max(1, round(self._FONT_SIZE * real_dpi / tk_dpi))
            self._font_size_by_dpi[real_dpi] = font_size
        return font_size

    def _update_action_states(self, colors, disabled_fg):
        has_content = self._has_content()

        if has_content:
            entry_colors = {
                "foreground": colors["fg"],
                "activeforeground": colors["activeforeground"],
                "activebackground": colors["activebackground"],
            }
        else:
            # Custom-draw the effect of disabled context menus
            # to avoid using Tk's default disabled effect in dark mode.
            entry_colors = {
                "foreground": disabled_fg,
                "activeforeground": disabled_fg,
                "activebackground": colors["bg"],
            }

        for action in self._CONTENT_DEPENDENT_ACTIONS:
            index = self._action_indexes.get(action)
            if index is not None:
                self.entryconfigure(index, state="normal", **entry_colors)

    def _has_content(self):
        # index("end-1c") is "1.0" exactly when the textbox is empty; avoids reading the whole content.
        return self.textbox.index("end-1c") != "1.0"

    @staticmethod
    def _resolve_color(modes):
        light, dark = modes
        return light if customtkinter.get_appearance_mode() == "Light" else dark
