"""
工具文件
"""
from typing import (
    Union,
    List,
    Mapping
)
from elastic_transport import NodeConfig


TYPE_HOST = Union[str, List[Union[str, Mapping[str, Union[str, int]], NodeConfig]]]
