import tkinter

import customtkinter

from core.set_font_family import FLUENT_ICONS_FONT_FAMILY


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
