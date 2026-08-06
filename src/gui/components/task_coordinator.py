import threading


class TaskCoordinator:
    """Global operation lock ensuring only one operation runs at a time.

    The coordinator is a process-wide singleton. Functional pages register
    their executable action cards (along with the state-refresh callback that
    recomputes the card's enabled/disabled state) via ``register``.

    While an operation is running:
      - every registered card is disabled via ``disable_all`` so no second
        operation can be started from the UI;
      - any refresh callback (e.g. triggered by an option change) is forced to
        keep cards disabled, because ``BaseWidgets._set_card_state`` short-
        circuits to ``"disabled"`` while the coordinator is busy.

    When the operation finishes, ``restore_all`` re-runs every registered
    refresh callback so each card recomputes its correct state.

    USAGE EXAMPLE:

    Functional pages normally do not touch this class directly. They register
    their lockable cards (usually at the end of ``__init__``) and then run
    operations through ``BaseFuncPageFrame._run_operation``:

    # 1. Register the action cards that must be locked.
    self._operation_cards = [
        (self.sample1_card, self._refresh_sample1_state),
        (self.sample2_card, self._refresh_sample2_state),
    ]
    self._register_operation_cards()

    # 2. Run an operation; the coordinator acquires the lock, disables every
    #    registered card, and restores them when the operation completes.
    self._run_operation(
        worker.execute,
        "pages.common.sample1",
        on_completion=lambda: self._refresh_sample1_state(),
    )

    The low-level API (``try_acquire`` / ``release`` / ``restore_all`` / ...)
    is used internally by ``_run_operation``. Pages must NOT manage the lock
    manually — always go through ``_run_operation`` so the lock is acquired,
    released and every card restored in one consistent flow.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Guard so repeated TaskCoordinator() calls (which the singleton always
        # resolves to the same instance) do not reset the coordinator state.
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self._lock = threading.Lock()
        self._busy = False
        self._current_operation = None
        self._registry = []  # (page, card, refresh)

    def is_busy(self):
        with self._lock:
            return self._busy

    def current_operation(self):
        with self._lock:
            return self._current_operation

    def try_acquire(self, operation_name):
        with self._lock:
            if self._busy:
                return False
            self._busy = True
            self._current_operation = operation_name
            return True

    def release(self):
        with self._lock:
            self._busy = False
            self._current_operation = None

    def register(self, page, card, refresh):
        with self._lock:
            self._registry.append((page, card, refresh))

    def disable_all(self):
        with self._lock:
            registry = list(self._registry)
        for _page, card, _refresh in registry:
            try:
                card.configure(state="disabled")
            except Exception:
                pass

    def restore_all(self):
        with self._lock:
            registry = list(self._registry)
        for _page, _card, refresh in registry:
            try:
                refresh()
            except Exception:
                pass


task_coordinator = TaskCoordinator()
