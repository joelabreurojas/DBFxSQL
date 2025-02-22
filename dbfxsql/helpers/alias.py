from typing import Iterable, TypeAlias

from ..models import Condition, SyncTable

# Independent aliases
ChangeDict: TypeAlias = dict[str, SyncTable | list[SyncTable]]

ChangesList: TypeAlias = list[list[str]]

ConditionsList: TypeAlias = list[Condition]

FieldsIterable: TypeAlias = Iterable[tuple[str, str]]

FieldsTuple: TypeAlias = tuple[list[str], list[str]]

FilesDict: TypeAlias = dict[str, list[str]]

IndexesList: TypeAlias = list[list[int]]

OperationsList: TypeAlias = list[dict[str, list[dict]]]

RowIndexesTuple: TypeAlias = tuple[dict, list[int]]

RowsIndexesTuple: TypeAlias = tuple[list[dict], list[int]]

SQLParameters: TypeAlias = dict[str, str] | list[dict[str, str]] | None

SyncTableDict: TypeAlias = dict[str, dict[str, str | list[str] | None]]

TablesDict: TypeAlias = dict[str, list[str]]

TablesTuple: TypeAlias = tuple[list[dict], list[dict]]

TypesList: TypeAlias = list[dict[str, str]]

VariableFieldsTuple: TypeAlias = tuple[tuple[str, str], ...]
