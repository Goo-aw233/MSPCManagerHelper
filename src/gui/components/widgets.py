import tkinter

import customtkinter

from core.set_font_family import FLUENT_ICONS_FONT_FAMILY
from .scrollable_frame import ScrollableFrame
from .task_coordinator import task_coordinator


# =============== Page-Specific Widget Layouts ===============

class BaseWidgets:
    scroll_frame: ScrollableFrame
    font_family: str

    def _create_section_label(self, text):
        label = customtkinter.CTkLabel(
            self.scroll_frame,
            text=text,
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x", padx=25, pady=(20, 10))

    def _create_group_frame(self):
        frame = customtkinter.CTkFrame(
            self.scroll_frame,
            fg_color=("gray95", "#202020"),
            corner_radius=4,
            border_width=1,
            border_color=("gray90", "#2b2b2b")
        )
        frame.pack(fill="x", padx=20, pady=0)
        return frame

    @staticmethod
    def _create_separator(parent):
        separator = customtkinter.CTkFrame(parent, height=2, fg_color=("gray90", "#2b2b2b"))
        separator.pack(fill="x", padx=10)
        return separator

    def _create_actions_card(self, parent, title, description, widget_constructor=None, **widget_kwargs):
        container = customtkinter.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=10, pady=8)

        # Text Column
        text_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=5)

        title_label = customtkinter.CTkLabel(
            text_frame,
            text=title,
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            anchor="w"
        )
        title_label.pack(fill="x")

        if description:
            desc_label = customtkinter.CTkLabel(
                text_frame,
                text=description,
                font=customtkinter.CTkFont(family=self.font_family, size=12),
                text_color=("gray50", "gray70"),
                anchor="w"
            )
            desc_label.pack(fill="x")

        # Widget Column
        if widget_constructor:
            # Inject font family if not present and if the widget supports it (most CTk widgets do).
            if "font" not in widget_kwargs:
                widget_kwargs["font"] = customtkinter.CTkFont(family=self.font_family)

            # Fail-safe: default new action widgets to disable. Section-end refresh
            # functions immediately override this with the correct state.
            widget_kwargs.setdefault("state", "disabled")

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None

    @staticmethod
    def _set_card_state(card, state):
        # While an operation is running, no action card may be enabled.
        if task_coordinator.is_busy():
            state = "disabled"
        card.configure(state=state)

    def _set_entry_group_state(self, enabled, entry, button=None):
        if button is not None:
            button.configure(state="normal" if enabled else "disabled")
        entry.unbind("<Button-1>")
        entry.configure(state="normal")
        if not enabled:
            entry.bind("<Button-1>", self._block_entry_event)

    @staticmethod
    def _set_entry_text(entry, text):
        entry.delete(0, tkinter.END)
        entry.insert(0, text)

    @staticmethod
    def _block_entry_event(_):
        return "break"


class AboutPageWidgets(BaseWidgets):
    def _create_info_card(self, parent, title, description, widget_constructor=None, description_command=None,
                              **widget_kwargs):
        container = customtkinter.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=10, pady=8)

        # Text Column
        text_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=5)

        title_label = customtkinter.CTkLabel(
            text_frame,
            text=title,
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            anchor="w"
        )
        title_label.pack(fill="x")

        if description:
            desc_label = customtkinter.CTkLabel(
                text_frame,
                text=description,
                font=customtkinter.CTkFont(family=self.font_family, size=12),
                text_color=("#1f6aa5", "#3a7ebf") if description_command else ("gray50", "gray70"),
                anchor="w",
                cursor="hand2" if description_command else "arrow"
            )
            desc_label.pack(fill="x")

            if description_command:
                desc_label.bind("<Button-1>", lambda _: description_command())

        # Widget Column
        if widget_constructor:
            # Inject font family if not present and if the widget supports it (most CTk widgets do).
            if "font" not in widget_kwargs:
                widget_kwargs["font"] = customtkinter.CTkFont(family=self.font_family)

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None


class HomePageWidgets(BaseWidgets):
    def _create_section_label_with_button(self, text, button_text, command, icon_char="", icon_size=14):
        container = customtkinter.CTkFrame(self.scroll_frame, fg_color="transparent")
        container.pack(fill="x", padx=25, pady=(20, 10))

        label = customtkinter.CTkLabel(
            container,
            text=text,
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold"),
            anchor="w"
        )
        label.pack(side="left")

        button = CTkIconButton(
            container,
            text=button_text,
            icon_char=icon_char,
            icon_size=icon_size,
            font=customtkinter.CTkFont(family=self.font_family, size=12),
            command=command
        )
        button.pack(side="right")
        return button

    def _create_info_textbox_card(self, parent, title, description, widget_constructor=None,
                                  enable_text_selection=False, activate_scrollbars=False, min_height=50,
                                  max_height=130, **widget_kwargs):
        container = customtkinter.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=10, pady=8)

        # Text Column
        text_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=5)

        title_label = customtkinter.CTkLabel(
            text_frame,
            text=title,
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            anchor="w"
        )
        title_label.pack(fill="x")

        if description:
            # Auto-adjust height based on newlines (approx 22px per line + padding).
            line_count = description.count("\n") + 1
            content_height = line_count * 22 + 10
            textbox_height = min(max(min_height, content_height), max_height)
            show_scrollbars = activate_scrollbars and content_height > max_height

            desc_textbox = customtkinter.CTkTextbox(
                text_frame,
                font=customtkinter.CTkFont(family=self.font_family, size=12),
                text_color="gray50",    # CTkTextbox does not support dual-mode text_color ("gray50", "gray70").
                fg_color="transparent",
                wrap="word",
                height=textbox_height,
                activate_scrollbars=show_scrollbars,
                border_width=0
            )
            desc_textbox.pack(fill="x", pady=(0, 5))
            desc_textbox.insert("1.0", description)
            desc_textbox.configure(state="disabled")
            # Disable Text Selection
            if not enable_text_selection:
                desc_textbox.bind("<Button-1>", lambda _: "break")  # Disable Single Click
                desc_textbox.bind("<B1-Motion>", lambda _: "break")  # Disable Click & Drag
                desc_textbox.bind("<Double-Button-1>", lambda _: "break")  # Disable Double Click
                desc_textbox.bind("<Triple-Button-1>", lambda _: "break")  # Disable Triple Click
                # Keep Arrow Instead of Cursor
                desc_textbox.bind("<Enter>", lambda _: desc_textbox.configure(cursor="arrow"))
                desc_textbox.bind("<Leave>", lambda _: desc_textbox.configure(cursor="arrow"))

        # Widget Column
        if widget_constructor:
            # Inject font family if not present and if the widget supports it (most CTk widgets do).
            if "font" not in widget_kwargs:
                widget_kwargs["font"] = customtkinter.CTkFont(family=self.font_family)

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None


class SettingsPageWidgets(BaseWidgets):
    def _create_settings_card(self, parent, title, description, widget_constructor=None, **widget_kwargs):
        container = customtkinter.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=10, pady=8)

        # Text Column
        text_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=5)

        title_label = customtkinter.CTkLabel(
            text_frame,
            text=title,
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            anchor="w"
        )
        title_label.pack(fill="x")

        if description:
            desc_label = customtkinter.CTkLabel(
                text_frame,
                text=description,
                font=customtkinter.CTkFont(family=self.font_family, size=12),
                text_color=("gray50", "gray70"),
                anchor="w"
            )
            desc_label.pack(fill="x")

        # Widget Column
        if widget_constructor:
            # Inject font family if not present and if the widget supports it (most CTk widgets do).
            if "font" not in widget_kwargs:
                widget_kwargs["font"] = customtkinter.CTkFont(family=self.font_family)

            # For OptionMenu, also set the dropdown font.
            if widget_constructor == customtkinter.CTkOptionMenu and "dropdown_font" not in widget_kwargs:
                widget_kwargs["dropdown_font"] = customtkinter.CTkFont(family=self.font_family)

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None


# =============== Custom CTk-like Widgets ===============

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


class CTkIconButton(customtkinter.CTkButton):
    """CTkButton that also renders a FluentSystemIcons glyph next to the text.

    A single label cannot mix two fonts, so the icon glyph (FluentSystemIcons)
    and the text (application font family) are rendered as two separate labels.
    The icon occupies the same slot as the CTkButton image (left of the text by
    default), so every CTkButton feature (state, hover, command, colors, corner
    radius, border, anchor, compound, ...) behaves exactly like the base button.
    """

    def __init__(self, master, icon_char="", icon_size=18, focus_border_width=2,
                 focus_border_color=("gray50", "gray70"), **kwargs):
        # These attributes must exist before CTkButton.__init__() runs self._draw().
        self._icon_char = icon_char
        self._icon_size = icon_size
        self._icon_font = customtkinter.CTkFont(family=FLUENT_ICONS_FONT_FAMILY, size=icon_size)
        self._icon_label = None
        self._focused = False
        self._focus_from_mouse = False
        super().__init__(master, **kwargs)

        self._normal_border_width = self._border_width
        self._normal_border_color = self._border_color
        self._focus_border_width = focus_border_width
        self._focus_border_color = focus_border_color

        # Keyboard Accessibility
        tkinter.Frame.configure(self, takefocus=1)  # Tab-focusable
        tkinter.Frame.bind(self, "<FocusIn>", self._on_focus_in)  # Highlight on Focus
        tkinter.Frame.bind(self, "<FocusOut>", self._on_focus_out)  # Remove Highlight on Focus Out
        tkinter.Frame.bind(self, "<KeyPress-Return>", self._on_key_activate)  # Activate on Enter Key
        tkinter.Frame.bind(self, "<KeyPress-space>", self._on_key_activate)  # Activate on Space Key

        # Mouse clicks must not show the keyboard focus ring.
        self.bind("<ButtonPress-1>", self._on_mouse_press)

    def _update_icon_label(self, no_color_updates=False):
        if self._icon_char:
            if self._icon_label is None:
                self._icon_label = tkinter.Label(master=self,
                                                 font=self._apply_font_scaling(self._icon_font),
                                                 text=self._icon_char,
                                                 anchor="center",
                                                 padx=0,
                                                 pady=0,
                                                 borderwidth=0)
                self._create_grid()

                self._icon_label.bind("<Enter>", self._on_enter)
                self._icon_label.bind("<Leave>", self._on_leave)
                self._icon_label.bind("<ButtonPress-1>", self._on_mouse_press)
                self._icon_label.bind("<ButtonRelease-1>", self._on_release)

            if not no_color_updates:
                if self._state == tkinter.DISABLED:
                    self._icon_label.configure(fg=self._apply_appearance_mode(self._text_color_disabled))
                else:
                    self._icon_label.configure(fg=self._apply_appearance_mode(self._text_color))

                if self._apply_appearance_mode(self._fg_color) == "transparent":
                    self._icon_label.configure(bg=self._apply_appearance_mode(self._bg_color))
                else:
                    self._icon_label.configure(bg=self._apply_appearance_mode(self._fg_color))
        else:
            if self._icon_label is not None:
                self._icon_label.destroy()
                self._icon_label = None
                self._create_grid()

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)
        self._update_icon_label(no_color_updates)

    def _on_enter(self, event=None):
        del event  # Parameter Name Match CTkButton._on_enter
        self._mouse_inside = True
        self._apply_inner_color()

    def _on_leave(self, event=None):
        del event  # Parameter Name Match CTkButton._on_leave
        self._mouse_inside = False
        self._apply_inner_color()

    def _on_mouse_press(self, _):
        self._focus_from_mouse = True

    def _on_focus_in(self, _):
        # Only keyboard focus (Tab) shows the focus ring; mouse clicks set
        # _focus_from_mouse on press and must not get the ring.
        self._focused = not self._focus_from_mouse
        self._focus_from_mouse = False
        # Apply the border first: changing border_width triggers a redraw that
        # would reset the hover background, so reapply it last.
        self._apply_focus_border()
        self._apply_inner_color()

    def _on_focus_out(self, _):
        self._focused = False
        self._focus_from_mouse = False
        self._apply_focus_border()
        self._apply_inner_color()

    def _apply_focus_border(self):
        if self._focused:
            self.configure(border_width=self._focus_border_width, border_color=self._focus_border_color)
        else:
            self.configure(border_width=self._normal_border_width, border_color=self._normal_border_color)

    def _on_key_activate(self, _):
        if self._state != tkinter.DISABLED and self._command is not None:
            self._command()

    def _apply_inner_color(self):
        """Recolor the canvas and all labels (text/image/icon) for mouse hover.

        Keyboard focus is indicated by the focus ring only (_apply_focus_border),
        so the background only follows the mouse hover state.
        """
        if self._mouse_inside and self._hover and self._state == tkinter.NORMAL:
            inner_parts_color = self._hover_color if self._hover_color is not None else self._fg_color
        else:
            inner_parts_color = self._bg_color if self._fg_color == "transparent" else self._fg_color

        inner_parts_color = self._apply_appearance_mode(inner_parts_color)
        self._canvas.itemconfig("inner_parts", outline=inner_parts_color, fill=inner_parts_color)

        if self._text_label is not None:
            self._text_label.configure(bg=inner_parts_color)
        if self._image_label is not None:
            self._image_label.configure(bg=inner_parts_color)
        if self._icon_label is not None:
            self._icon_label.configure(bg=inner_parts_color)

    def _create_grid(self):
        super()._create_grid()

        if self._icon_label is not None:
            if self._compound in ("right", "left"):
                # Reserve the same spacing the base button uses between image and text.
                self.grid_columnconfigure(2, weight=0, minsize=self._apply_widget_scaling(self._image_label_spacing))

            if self._compound == "right":
                self._icon_label.grid(row=2, column=3, sticky="w")
            elif self._compound == "top":
                self._icon_label.grid(row=1, column=2, sticky="s")
            elif self._compound == "bottom":
                self._icon_label.grid(row=3, column=2, sticky="n")
            else:  # "left" (default) & "center"
                self._icon_label.grid(row=2, column=1, sticky="e")

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)
        if self._icon_label is not None:
            self._icon_label.configure(font=self._apply_font_scaling(self._icon_font))

    def _update_font(self):
        super()._update_font()
        if self._icon_label is not None:
            self._icon_label.configure(font=self._apply_font_scaling(self._icon_font))

    def configure(self, require_redraw=False, **kwargs):
        if "icon_char" in kwargs:
            self._icon_char = kwargs.pop("icon_char")
            if self._icon_label is not None:
                self._icon_label.configure(text=self._icon_char)
            else:
                require_redraw = True  # the label will be created in _draw().
        if "icon_size" in kwargs:
            self._icon_size = kwargs.pop("icon_size")
            self._icon_font = customtkinter.CTkFont(family=FLUENT_ICONS_FONT_FAMILY, size=self._icon_size)
            if self._icon_label is not None:
                self._icon_label.configure(font=self._apply_font_scaling(self._icon_font))
        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name):
        if attribute_name == "icon_char":
            return self._icon_char
        return super().cget(attribute_name)

    def focus_set(self):
        # Base CTkButton.focus_set() delegates to the text label, which may not
        # exist for icon-only buttons; focus the underlying frame instead so
        # that keyboard events reach the button.
        return tkinter.Frame.focus_set(self)
