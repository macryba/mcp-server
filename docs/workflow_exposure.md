# Exposing Workflow Guidance to MCP Clients

This document explains how this MCP server exposes workflow guidance and best practices to AI agents that connect to it.

## Multi-Layer Approach

The server uses a **4-layer approach** to expose workflow guidance:

### 1. Tool Descriptions (Primary Interface)
Every tool description includes "RECOMMENDED WORKFLOW" guidance that explains when and how to use that tool in the context of the overall workflow.

**Example from `search_wikipedia`:**
```
RECOMMENDED WORKFLOW: Use this tool first for quick lookups. If you need more specialized
or comprehensive information, call list_domains to learn about available domains, then use
search_polish_history with specific domains.
```

**Why this works:**
- Tool descriptions are always visible to AI agents
- Provides context-specific guidance for each tool
- No extra API calls needed

### 2. Server Info Tool (Overview)
The `server_info()` tool provides a high-level overview including the recommended workflow.

**Usage:** Agents should call this when first connecting to understand the server's capabilities and workflow.

```python
info = await server_info()
# Returns workflow summary, capabilities, domain information
```

**Returns:**
- Server metadata (name, version, description)
- 3-step workflow summary with examples
- Tool capabilities
- Domain information

### 3. Usage Guide Tool (Detailed Guidance)
The `usage_guide()` tool provides comprehensive workflow documentation with examples and best practices.

**Usage:** Agents should call this after `server_info()` for detailed guidance.

```python
guide = await usage_guide()
# Returns detailed workflow with examples, domain specializations, best practices
```

**Returns:**
- Detailed 4-step workflow with examples
- Domain specialization reference
- Query optimization tips
- Best practices
- Example research scenarios

### 4. Documentation (Reference Material)
This document and `docs/search_tools.md` provide comprehensive reference material for developers and advanced users.

## Recommended Agent Connection Pattern

When an AI agent connects to this MCP server, it should follow this pattern:

```
1. Connect to MCP server
2. Call server_info() → Get overview and workflow summary
3. Call usage_guide() → Get detailed workflow guidance (optional)
4. Start using tools following the recommended workflow
```

### Example Agent Connection Flow

```python
# Agent connects to MCP server
tools = get_mcp_tools("polish-history")

# Step 1: Get server overview
info = await server_info()
print(info['recommended_workflow'])
# → Learn about 3-step progressive research workflow

# Step 2: Get detailed usage guide (optional)
guide = await usage_guide()
print(guide['core_workflow'])
# → Learn detailed workflow with examples

# Step 3: Start using tools
# User asks: "Tell me about the Warsaw Uprising"
result = await search_wikipedia("Powstanie warszawskie")

# User wants primary sources
domains = await list_domains()
# → Learn IPN and Polona specialize in this

result = await search_polish_history(
    "Powstanie warszawskie dokumenty",
    domains=["ipn", "polona"]
)
```

## Why This Multi-Layer Approach Works

### 1. **Progressive Disclosure**
- **Quick:** Tool descriptions provide immediate context
- **Overview:** server_info gives workflow summary
- **Deep:** usage_guide provides comprehensive guidance

### 2. **No Forced Reading**
- Agents can start using tools immediately (tool descriptions guide them)
- Detailed guidance available on-demand (server_info, usage_guide)
- No upfront documentation reading required

### 3. **Contextual Guidance**
- Each tool description explains its role in the workflow
- Examples show how tools work together
- Best practices embedded in tool context

### 4. **Scalable**
- Works for simple queries (just read tool descriptions)
- Works for complex research (call server_info, usage_guide)
- Works for learning and reference (documentation)

## Tool Description Best Practices

Based on this server's approach, here are best practices for MCP tool descriptions:

### DO:
- ✅ Include "RECOMMENDED WORKFLOW" section
- ✅ Explain when to use this tool in the overall workflow
- ✅ Mention related tools and when to use them
- ✅ Provide usage examples
- ✅ Keep descriptions concise but informative

### DON'T:
- ❌ Write generic descriptions that could apply to any tool
- ❌ Assume the agent knows the overall workflow
- ❌ Hide important workflow information
- ❌ Make descriptions too long or verbose

## Example Tool Description Template

```python
@mcp.tool()
async def my_tool(param: str) -> str:
    """
    Brief description of what this tool does

    RECOMMENDED WORKFLOW: Use this tool when [specific condition].
    After getting results, consider using [related_tool] for [next_step].

    Args:
        param: Parameter description

    Returns:
        Return value description
    """
```

## Server Metadata vs Runtime Guidance

### Server Metadata (Connection Time)
- Server name, version, description
- Tool list and signatures
- **Best for:** Discovery, connection establishment

### Runtime Guidance (During Operation)
- Tool descriptions with workflow context
- server_info with workflow summary
- usage_guide with detailed examples
- **Best for:** Guiding agent behavior during actual use

This server emphasizes **runtime guidance** over extensive connection-time metadata,
because workflow guidance is most useful when the agent is actually using the tools.

## Evaluating Workflow Guidance Effectiveness

To determine if your workflow guidance is effective:

1. **Test with real agents:** Do agents follow the recommended workflow?
2. **Monitor tool usage:** Are tools used in the expected order?
3. **Check error rates:** Do agents misuse tools or call them in wrong contexts?
4. **User feedback:** Are users getting good results from agent interactions?

This server's approach can be evaluated by checking:
- Do agents call search_wikipedia first?
- Do they use list_domains before targeted searches?
- Do they specify domains in search_polish_history based on learned specializations?
- Are users satisfied with the relevance of search results?

## Conclusion

The most effective way to expose workflow guidance is a **multi-layer approach**:

1. **Tool descriptions** (always visible, context-specific)
2. **server_info** (overview and workflow summary)
3. **usage_guide** (detailed guidance and examples)
4. **Documentation** (reference material)

This approach provides **progressive disclosure** - agents can start working immediately
with basic guidance, and access more detailed guidance as needed.
