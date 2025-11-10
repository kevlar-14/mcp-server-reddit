import os

from starlette.applications import Starlette
from starlette.routing import Mount

from mcp.server.fastmcp import FastMCP

from .server import RedditServer, RedditTools


# Create FastMCP server
mcp = FastMCP("mcp-reddit")

# Expose MCP over Streamable HTTP at the root path "/"
# Ref: modelcontextprotocol/python-sdk "Streamable HTTP Transport" & "Basic mounting" examples
# (mcp.settings.streamable_http_path = "/")
mcp.settings.streamable_http_path = "/"


# Underlying Reddit logic from the existing server
reddit = RedditServer()


@mcp.tool()
def get_frontpage_posts(limit: int = 10):
    """Get hot posts from Reddit frontpage."""
    return [p.model_dump() for p in reddit.get_frontpage_posts(limit)]


@mcp.tool()
def get_subreddit_info(subreddit_name: str):
    """Get information about a subreddit."""
    return reddit.get_subreddit_info(subreddit_name).model_dump()


@mcp.tool()
def get_subreddit_hot_posts(subreddit_name: str, limit: int = 10):
    """Get hot posts from a specific subreddit."""
    return [p.model_dump() for p in reddit.get_subreddit_hot_posts(subreddit_name, limit)]


@mcp.tool()
def get_subreddit_new_posts(subreddit_name: str, limit: int = 10):
    """Get new posts from a specific subreddit."""
    return [p.model_dump() for p in reddit.get_subreddit_new_posts(subreddit_name, limit)]


@mcp.tool()
def get_subreddit_top_posts(
    subreddit_name: str,
    limit: int = 10,
    time: str = "",
):
    """Get top posts from a specific subreddit."""
    return [
        p.model_dump()
        for p in reddit.get_subreddit_top_posts(subreddit_name, limit, time)
    ]


@mcp.tool()
def get_subreddit_rising_posts(subreddit_name: str, limit: int = 10):
    """Get rising posts from a specific subreddit."""
    return [
        p.model_dump()
        for p in reddit.get_subreddit_rising_posts(subreddit_name, limit)
    ]


@mcp.tool()
def get_post_content(
    post_id: str,
    comment_limit: int = 10,
    comment_depth: int = 3,
):
    """Get detailed content of a specific post, including comments."""
    detail = reddit.get_post_content(post_id, comment_limit, comment_depth)
    return detail.model_dump()


@mcp.tool()
def get_post_comments(post_id: str, limit: int = 10):
    """Get comments from a post."""
    return [
        c.model_dump()
        for c in reddit.get_post_comments(post_id, limit)
    ]


# Build ASGI app that serves MCP over HTTP
# Pattern based on python-sdk docs "StreamableHTTP servers / Basic mounting":
# app = Starlette(routes=[Mount("/", app=mcp.streamable_http_app())])
app = Starlette(
    routes=[
        Mount("/", app=mcp.streamable_http_app()),
    ]
)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
