import tkinter

import customtkinter

from core.set_font_family import FLUENT_ICONS_FONT_FAMILY


class CTkNavButton(customtkinter.CTkFrame):
    """Navigation button that renders the Fluent icon and the text separately.

    A single label cannot mix two fonts, so the icon glyph (FluentSystemIcons)
    and the localized text (application font family) are drawn as two side-by-side
    labels with a small gap between them. The overall look (height, corner radius,
    transparent background, hover highlight, selected color and spacing) matches
    the previous emoji-based navigation buttons.
    """

    # Cached ordered list of sibling nav buttons; set in __init__ and invalidated
    # whenever a new CTkNavButton joins the same master.
    _ordered_nav_cache: list["CTkNavButton"] | None = None

    def __init__(self, master, icon_char="", text="", command=None,
                 font_family=None, corner_radius=4, height=40, border_spacing=10,
                 fg_color="transparent", hover_color=("gray70", "gray30"),
                 text_color=("gray10", "gray90"), icon_size=18,
                 focus_border_width=2, focus_border_color=("gray50", "gray70")):
        super().__init__(master, corner_radius=corner_radius, fg_color=fg_color,
                         width=0, height=height)

        self._command = command
        self._normal_color = fg_color
        self._selected_color = None
        self._hover_color = hover_color
        self._text_color = text_color
        self._border_spacing = border_spacing
        self._is_selected = False
        self._hovering = False
        self._focused = False
        self._focus_from_mouse = False
        self._ordered_nav_cache = None
        self._normal_border_width = self._border_width
        self._normal_border_color = self._border_color
        self._focus_border_width = focus_border_width
        self._focus_border_color = focus_border_color

        # Leave room around the labels so the focus ring (border) wraps around
        # the whole button instead of being hidden behind the labels.
        ring_margin = self._focus_border_width
        label_height = max(1, height - 2 * ring_margin)

        # Icon label rendered with the bundled FluentSystemIcons font.
        self._icon_label = customtkinter.CTkLabel(
            self,
            text=icon_char,
            height=label_height,
            font=customtkinter.CTkFont(family=FLUENT_ICONS_FONT_FAMILY, size=icon_size),
            text_color=text_color,
            cursor="hand2"
        )
        self._icon_label.pack(side="left", padx=(border_spacing, 4), pady=(ring_margin, ring_margin))

        # Text label rendered with the application font family.
        self._text_label = customtkinter.CTkLabel(
            self,
            text=text,
            height=label_height,
            anchor="w",
            font=customtkinter.CTkFont(family=font_family),
            text_color=text_color,
            cursor="hand2"
        )
        self._text_label.pack(
            side="left", fill="x", expand=True,
            padx=(4, border_spacing), pady=(ring_margin, ring_margin)
        )

        # Interaction: hover highlight and click command across the whole button area.
        for widget in (self, self._icon_label, self._text_label):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)

        # Set the cursor directly on the underlying frame (the CTkNavButton
        # cursor is a tkinter.Frame attribute; no override dispatch needed).
        tkinter.Frame.configure(self, cursor="hand2")

        # Keyboard Accessibility
        tkinter.Frame.configure(self, takefocus=1)  # Tab-focusable
        tkinter.Frame.bind(self, "<FocusIn>", self._on_focus_in)  # Highlight on Focus
        tkinter.Frame.bind(self, "<FocusOut>", self._on_focus_out)  # Remove Highlight on Focus Out
        tkinter.Frame.bind(self, "<KeyPress-Return>", self._on_key_activate)  # Activate on Enter Key
        tkinter.Frame.bind(self, "<KeyPress-space>", self._on_key_activate)  # Activate on Space Key
        tkinter.Frame.bind(self, "<KeyPress-Up>", self._on_arrow_up)  # Previous Nav Button
        tkinter.Frame.bind(self, "<KeyPress-Down>", self._on_arrow_down)  # Next Nav Button
        tkinter.Frame.bind(self, "<KeyPress-Home>", self._on_home)  # Jump to First Nav Button
        tkinter.Frame.bind(self, "<KeyPress-End>", self._on_end)  # Jump to Last Nav Button

        # Invalidate cached sibling ordering when a new nav button joins the group,
        # so the arrow-key navigation stays correct even for dynamic additions.
        has_sibling = False
        for sibling in self.master.winfo_children():
            if isinstance(sibling, CTkNavButton) and sibling is not self:
                sibling._ordered_nav_cache = None
                has_sibling = True
        # Roving tabindex: only one nav button is in the Tab order at a time.
        # The first-created button is the initial Tab stop; every later button
        # starts excluded and is promoted when it receives focus.
        if has_sibling:
            tkinter.Frame.configure(self, takefocus=0)

    def _apply_state(self):
        # Background follows the mouse hover / selection state only; keyboard
        # focus is indicated exclusively by the focus ring (border). Both are
        # applied in a single configure call so the canvas redraws only once.
        if self._hovering:
            color = self._hover_color
        elif self._is_selected:
            color = self._selected_color or self._normal_color
        else:
            color = self._normal_color

        if self._focused:
            border_width, border_color = self._focus_border_width, self._focus_border_color
        else:
            border_width, border_color = self._normal_border_width, self._normal_border_color

        super().configure(fg_color=color, border_width=border_width, border_color=border_color)

    def _activate(self):
        if self._command is not None:
            self._command()

    def _on_enter(self, _):
        self._hovering = True
        self._apply_state()

    def _on_leave(self, _):
        self._hovering = False
        self._apply_state()

    def _on_click(self, _):
        self._focus_from_mouse = True
        self._activate()

    def _on_focus_in(self, _):
        # Only keyboard focus (Tab) shows the focus ring; mouse clicks set
        # _focus_from_mouse on press and must not get the ring.
        self._focused = not self._focus_from_mouse
        self._focus_from_mouse = False
        self._promote_tab_stop()
        self._apply_state()

    def _on_focus_out(self, _):
        self._focused = False
        self._focus_from_mouse = False
        self._apply_state()

    def _on_key_activate(self, _):
        self._activate()

    def _on_arrow_up(self, _):
        self._focus_adjacent(-1)

    def _on_arrow_down(self, _):
        self._focus_adjacent(1)

    def _on_home(self, _):
        self._focus_first()

    def _on_end(self, _):
        self._focus_last()

    def _focus_first(self):
        """Move focus to the first nav button in the group."""
        buttons = self._ordered_nav_buttons()
        if buttons:
            buttons[0].focus_set()

    def _focus_last(self):
        """Move focus to the last nav button in the group."""
        buttons = self._ordered_nav_buttons()
        if buttons:
            buttons[-1].focus_set()

    def _promote_tab_stop(self):
        """Keep only this button in the Tab order (roving tabindex).

        The nav sidebar behaves as a single composite control: Tab enters the
        group and lands on the current item, Arrow / Home / End move focus within
        the group, and Tab pressed again leaves the whole group. For this to
        work, only the button that currently holds focus stays reachable via Tab
        (takefocus=1); every sibling is removed from the Tab order (takefocus=0)
        so Tab does not step through each nav button one by one.
        """
        for sibling in self._ordered_nav_buttons():
            if sibling is not self and sibling.winfo_exists():
                tkinter.Frame.configure(sibling, takefocus=0)
        tkinter.Frame.configure(self, takefocus=1)

    def _ordered_nav_buttons(self) -> list["CTkNavButton"]:
        """All sibling CTkNavButtons in the same master (including self), ordered by grid row.

        The result is cached to avoid re-traversing and re-sorting on every arrow
        key press. The cache is invalidated whenever a new CTkNavButton is created
        in the same master and revalidated against destroyed widgets on use.
        """
        cache = self._ordered_nav_cache
        if cache is not None and all(btn.winfo_exists() for btn in cache):
            return cache

        buttons = []
        for child in self.master.winfo_children():
            if isinstance(child, CTkNavButton):
                try:
                    row = int(child.grid_info().get("row", 0))
                except (TypeError, ValueError):
                    row = 0
                buttons.append((row, child))
        buttons.sort(key=lambda item: item[0])
        ordered = [button for _, button in buttons]
        self._ordered_nav_cache = ordered
        return ordered

    def _focus_adjacent(self, step):
        """Move focus to the previous (-1) or next (+1) nav button in the group."""
        buttons = self._ordered_nav_buttons()
        if len(buttons) < 2:
            return
        index = buttons.index(self)
        target = buttons[(index + step) % len(buttons)]
        target.focus_set()

    def configure(self, require_redraw=False, **kwargs):
        if "height" in kwargs:
            height = kwargs["height"]
            if height is not None:
                # Recompute the label inset so the focus ring (border) keeps
                # wrapping the whole button if the height changes after creation.
                ring_margin = self._focus_border_width
                label_height = max(1, height - 2 * ring_margin)
                self._icon_label.configure(height=label_height)
                self._text_label.configure(height=label_height)
                self._icon_label.pack(
                    side="left", padx=(self._border_spacing, 4),
                    pady=(ring_margin, ring_margin)
                )
                self._text_label.pack(
                    side="left", fill="x", expand=True,
                    padx=(4, self._border_spacing), pady=(ring_margin, ring_margin)
                )
        if "fg_color" in kwargs:
            color = kwargs.pop("fg_color")
            self._is_selected = color != "transparent"
            self._selected_color = color if self._is_selected else None
            self._apply_state()
        if "font" in kwargs:
            self._text_label.configure(font=kwargs.pop("font"))
        if "text" in kwargs:
            self._text_label.configure(text=kwargs.pop("text"))
        if "icon_char" in kwargs:
            self._icon_label.configure(text=kwargs.pop("icon_char"))
        if "icon_size" in kwargs:
            self._icon_label.configure(font=customtkinter.CTkFont(
                family=FLUENT_ICONS_FONT_FAMILY, size=kwargs.pop("icon_size")))
        if "text_color" in kwargs:
            self._text_color = kwargs.pop("text_color")
            self._icon_label.configure(text_color=self._text_color)
            self._text_label.configure(text_color=self._text_color)
        if "hover_color" in kwargs:
            self._hover_color = kwargs.pop("hover_color")
            self._apply_state()
        if "command" in kwargs:
            self._command = kwargs.pop("command")
        if kwargs or require_redraw:
            super().configure(require_redraw=require_redraw, **kwargs)
