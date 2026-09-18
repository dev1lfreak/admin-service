from enum import Enum


class OrderStatus(str, Enum):
    PENDING = 'pending'
    REJECTED = 'rejected'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    ERROR = 'error'