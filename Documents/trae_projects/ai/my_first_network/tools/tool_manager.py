# 工具调用抽象层
# 用于管理和调用各种工具

import mcp
from typing import Dict, List, Any, Optional, Callable
from pydantic import BaseModel

class Tool(BaseModel):
    """工具定义类"""
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    input_schema: Dict[str, Any]
    output_schema: Optional[Dict[str, Any]] = None
    implementation: Callable[..., Any]

class ToolManager:
    """工具管理器"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool) -> None:
        """注册工具"""
        self.tools[tool.name] = tool
    
    def register_function(self, name: str, title: Optional[str] = None, description: Optional[str] = None, input_schema: Optional[Dict[str, Any]] = None, output_schema: Optional[Dict[str, Any]] = None):
        """装饰器：注册函数为工具"""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            # 如果没有提供输入模式，从函数签名生成简单的输入模式
            func_input_schema = input_schema  # 创建局部变量
            if func_input_schema is None:
                from inspect import signature
                sig = signature(func)
                func_input_schema = {}
                for param_name, param in sig.parameters.items():
                    if param_name != "self" and param.annotation is not param.empty:
                        func_input_schema[param_name] = {
                            "type": "string" if param.annotation == str else "number" if param.annotation in [int, float] else "object"
                        }
            
            tool = Tool(
                name=name,
                title=title or name,
                description=description or func.__doc__ or "",
                input_schema=func_input_schema,
                output_schema=output_schema,
                implementation=func
            )
            self.register_tool(tool)
            return func
        return decorator
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """获取工具"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """列出所有工具名称"""
        return list(self.tools.keys())
    
    def call_tool(self, name: str, **kwargs) -> Any:
        """调用工具"""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"工具 '{name}' 未找到")
        
        try:
            return tool.implementation(**kwargs)
        except Exception as e:
            raise Exception(f"调用工具 '{name}' 时出错: {str(e)}") from e
    
    def to_mcp_tools(self) -> List[mcp.Tool]:
        """转换为mcp工具列表"""
        mcp_tools = []
        for tool in self.tools.values():
            mcp_tool = mcp.Tool(
                name=tool.name,
                title=tool.title,
                description=tool.description,
                inputSchema=tool.input_schema,
                outputSchema=tool.output_schema
            )
            mcp_tools.append(mcp_tool)
        return mcp_tools

# 创建全局工具管理器实例
tool_manager = ToolManager()
