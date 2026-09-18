from abc import ABC,abstractmethod
from decimal import Decimal

from src.application.domain.entities.order import OrderEntity


class IOrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self,order_id: str) -> OrderEntity | None:
        raise NotImplementedError


    @abstractmethod
    async def list_by_user_id(self,*,user_id: str,limit: int,offset: int) -> list[OrderEntity]:
        raise NotImplementedError

    
    @abstractmethod
    async def list_all(self,*,limit: int,offset: int, search: str | None = None) -> list[OrderEntity]:
        raise NotImplementedError

    
    @abstractmethod
    async def list_by_date(self,*,year: int,month: int,limit: int,offset: int) -> list[OrderEntity]:
        raise NotImplementedError
    

    @abstractmethod
    async def sum_by_month(self,*,year: int,month: int, search: str | None = None) -> Decimal:
        raise NotImplementedError
    

    @abstractmethod
    async def sum_by_day(self,*,year: int,month: int,day: int, search: str | None = None) -> Decimal:
        raise NotImplementedError
    

    @abstractmethod
    async def count_all(self,*,search: str | None = None) -> int:
        raise NotImplementedError
    

    @abstractmethod
    async def count_by_month(self,*,year: int,month: int | None = None, search: str | None = None) -> int:
        raise NotImplementedError
    
    
    @abstractmethod
    async def count_by_day(self,*,year: int,month: int,day: int, search: str | None = None) -> int:
        raise NotImplementedError
