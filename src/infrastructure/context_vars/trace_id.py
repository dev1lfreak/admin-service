from contextvars import ContextVar


trace_id_var: ContextVar[str] = ContextVar('trace_id', default='N/A')
