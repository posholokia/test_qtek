from typing import (
    Any,
    Type,
    TypeVar,
    Union,
)


T = TypeVar("T")


class Mapper:
    @classmethod
    def dataclass_to_schema(cls, schema: Type[T], obj: Any) -> T:
        """
        Функция конвертирует объекты dataclass в pydantic схему
        """
        attrs = {}
        for field in schema.__fields__.keys():
            value = getattr(obj, field)
            sub_schema = schema.__fields__[field]
            field_type = cls._extract_field_type(sub_schema)
            if (
                isinstance(value, list)
                and len(value) > 0
                and hasattr(value[0], "__dataclass_fields__")
            ):
                attrs[field] = [
                    cls.dataclass_to_schema(field_type, item) for item in value
                ]
            elif hasattr(value, "__dataclass_fields__"):
                attrs[field] = cls.dataclass_to_schema(field_type, value)
            else:
                attrs[field] = value
        return schema(**attrs)

    @staticmethod
    def _extract_field_type(field_type: Any) -> Any:
        if isinstance(field_type, list):
            field_type = field_type[0]
        if hasattr(field_type, "__origin__"):
            if field_type.__origin__ is Union:
                return next(
                    t for t in field_type.__args__ if t is not type(None)
                )
            elif field_type.__origin__ is list:
                return field_type.__args__[0]
        return field_type
