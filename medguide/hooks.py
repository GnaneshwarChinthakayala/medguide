import sys
import time

from strands.hooks import (BeforeInvocationEvent, BeforeToolCallEvent,
                           HookProvider, HookRegistry)


class RateLimiterHook(HookProvider):
    """Caps each tool at max_calls per request (same pattern as workshop Module 2)."""

    def __init__(self, max_calls: int = 6):
        self.max_calls = max_calls
        self.counts: dict[str, int] = {}

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeInvocationEvent, self.reset)
        registry.add_callback(BeforeToolCallEvent, self.check)

    def reset(self, event: BeforeInvocationEvent) -> None:
        self.counts = {}

    def check(self, event: BeforeToolCallEvent) -> None:
        name = event.tool_use["name"]
        self.counts[name] = self.counts.get(name, 0) + 1
        if self.counts[name] > self.max_calls:
            event.cancel_tool = (f"'{name}' hit the {self.max_calls}-call limit. "
                                 "Do NOT call this tool again.")


class AuditLogHook(HookProvider):
    """Prints and stores a line for every tool call, so behaviour is visible."""

    def __init__(self, path: str | None = "audit.log"):
        self.path = path
        self.lines: list[str] = []

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolCallEvent, self.log)

    def log(self, event: BeforeToolCallEvent) -> None:
        line = f"{time.strftime('%H:%M:%S')} tool={event.tool_use['name']} input={event.tool_use.get('input')}"
        self.lines.append(line)
        print(f"\n[audit] {line}", file=sys.stderr)
        if self.path:
            try:
                with open(self.path, "a") as f:
                    f.write(line + "\n")
            except OSError:
                pass
