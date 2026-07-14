window.OKF_DATA = {
  "entities": {
    "ai-operations": {
      "type": "Category",
      "id": "ai-operations",
      "name": "AI Operations",
      "parent": null,
      "description": "AI-specific operations: generation, reasoning, orchestration, and knowledge retrieval. Encompasses the unique capabilities that make agentic systems powerful, from structured thinking to creative output.",
      "body": "",
      "_source": "data/categories/ai-operations.md"
    },
    "communication": {
      "type": "Category",
      "id": "communication",
      "name": "Communication",
      "parent": null,
      "description": "Team communication and collaboration. Covers messaging platforms, notification systems, and tools that facilitate coordination among distributed teams.",
      "body": "",
      "_source": "data/categories/communication.md"
    },
    "data": {
      "type": "Category",
      "id": "data",
      "name": "Data",
      "parent": null,
      "description": "Database, storage, and data management. Covers relational and NoSQL databases, caching systems, data migration, and structured data operations.",
      "body": "",
      "_source": "data/categories/data.md"
    },
    "development": {
      "type": "Category",
      "id": "development",
      "name": "Development",
      "parent": null,
      "description": "Tools and skills for software development. Encompasses code editing, version control, code review, debugging, and the full spectrum of activities involved in building software systems.",
      "body": "",
      "_source": "data/categories/development.md"
    },
    "infrastructure": {
      "type": "Category",
      "id": "infrastructure",
      "name": "Infrastructure",
      "parent": null,
      "description": "System infrastructure: time, error tracking, monitoring, and file system operations. Provides the foundational services that agents and applications depend on for reliable operation.",
      "body": "",
      "_source": "data/categories/infrastructure.md"
    },
    "web": {
      "type": "Category",
      "id": "web",
      "name": "Web",
      "parent": null,
      "description": "Web-related tools: browsing, search, mapping, and HTTP APIs. Includes both passive consumption (fetching, searching) and active interaction (browser automation, geolocation services).",
      "body": "",
      "_source": "data/categories/web.md"
    },
    "aws-kb-retrieval": {
      "type": "MCP-Server",
      "id": "aws-kb-retrieval",
      "name": "AWS Knowledge Base Retrieval",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-aws-kb-retrieval"
      },
      "capabilities": {
        "tools": [
          "retrieve_from_kb",
          "query_kb",
          "list_knowledge_bases"
        ],
        "resources": [
          "aws://knowledge-bases"
        ],
        "prompts": [
          "synthesize_knowledge"
        ]
      },
      "stars": 2400,
      "last_updated": "2025-04-04",
      "verified": true,
      "tier": "Official",
      "categories": [
        "ai-operations",
        "data"
      ],
      "skills_realized": [
        "knowledge-retrieval"
      ],
      "relations": {
        "exposes": [
          "aws://knowledge-bases"
        ],
        "belongs_to": [
          "ai-operations",
          "data"
        ],
        "commonly_composed_with": [
          "sequential-thinking",
          "fetch"
        ],
        "realizes_skills": [
          "knowledge-retrieval"
        ]
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-aws-kb-retrieval",
      "homepage": "https://github.com/modelcontextprotocol/server-aws-kb-retrieval",
      "description": "Official AWS Knowledge Base Retrieval MCP server for querying Amazon Bedrock Knowledge Bases with semantic search and RAG support.",
      "body": "The official AWS Knowledge Base Retrieval MCP server enables AI agents to query Amazon Bedrock Knowledge Bases through the Model Context Protocol. It supports retrieval-augmented generation (RAG) workflows.\n\n## Key Features\n\n- **Knowledge Retrieval**: Fetch relevant documents from Bedrock Knowledge Bases\n- **Semantic Search**: Natural language queries with vector similarity matching\n- **KB Management**: List and explore available knowledge bases\n- **Configurable Retrieval**: Control result count, relevance thresholds, and filters\n- **RAG Integration**: Built-in prompts for knowledge synthesis\n\n## Authentication\n\nRequires standard AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`) with permissions for `bedrock:Retrieve` and `bedrock-agent:ListKnowledgeBases`.\n\n## Use Cases\n\n- Enterprise knowledge base Q&A\n- Document-grounded response generation\n- Internal documentation search\n- Compliance and policy lookup",
      "_source": "data/mcp-servers/aws-kb-retrieval.md"
    },
    "brave-search": {
      "type": "MCP-Server",
      "id": "brave-search",
      "name": "Brave Search",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-brave-search"
      },
      "capabilities": {
        "tools": [
          "brave_web_search",
          "brave_local_search"
        ],
        "resources": null,
        "prompts": [
          "search_and_summarize"
        ]
      },
      "stars": 5800,
      "last_updated": "2025-04-14",
      "verified": true,
      "tier": "Official",
      "categories": [
        "web"
      ],
      "skills_realized": [
        "web-search"
      ],
      "relations": {
        "exposes": null,
        "belongs_to": [
          "web"
        ],
        "commonly_composed_with": [
          "fetch",
          "sequential-thinking"
        ],
        "realizes_skills": [
          "web-search"
        ]
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-brave-search",
      "homepage": "https://github.com/modelcontextprotocol/server-brave-search",
      "description": "Official Brave Search MCP server providing privacy-preserving web search and local business search capabilities.",
      "body": "The official Brave Search MCP server provides privacy-preserving web search capabilities for AI agents. It uses Brave's Search API to deliver high-quality search results without tracking user queries.\n\n## Key Features\n\n- **Web Search**: General search with pagination and configurable result counts\n- **Local Search**: Find local businesses and points of interest\n- **Privacy-First**: No user tracking or query profiling\n- **Result Filtering**: Offset and count controls for result pagination\n- **Search Prompts**: Built-in summarization and analysis prompts\n\n## Authentication\n\nRequires a `BRAVE_API_KEY` environment variable. Obtain a free or paid API key from the Brave Search API dashboard.\n\n## Use Cases\n\n- Research and information gathering\n- Documentation lookup and technical reference\n- Current event analysis and fact-checking\n- Local business and service discovery",
      "_source": "data/mcp-servers/brave-search.md"
    },
    "everart": {
      "type": "MCP-Server",
      "id": "everart",
      "name": "EverArt",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-everart"
      },
      "capabilities": {
        "tools": [
          "generate_image",
          "list_styles",
          "get_generation_status",
          "upscale_image",
          "vary_image"
        ],
        "resources": [
          "everart://generations",
          "everart://styles"
        ],
        "prompts": [
          "create_image_prompt",
          "refine_image_idea"
        ]
      },
      "stars": 1600,
      "last_updated": "2025-04-01",
      "verified": true,
      "tier": "Official",
      "categories": [
        "ai-operations"
      ],
      "skills_realized": null,
      "relations": {
        "exposes": [
          "everart://generations",
          "everart://styles"
        ],
        "belongs_to": [
          "ai-operations"
        ],
        "commonly_composed_with": [
          "filesystem",
          "fetch"
        ],
        "realizes_skills": null
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-everart",
      "homepage": "https://github.com/modelcontextprotocol/server-everart",
      "description": "Official EverArt MCP server enabling AI image generation with style controls, upscaling, and variation capabilities.",
      "body": "The official EverArt MCP server enables AI agents to generate and manipulate images through the Model Context Protocol. It provides access to AI image generation with style controls, upscaling, and variation capabilities.\n\n## Key Features\n\n- **Image Generation**: Create images from text prompts with parameter control\n- **Style Library**: Browse and apply predefined artistic styles\n- **Generation Tracking**: Monitor generation status and retrieve results\n- **Upscaling**: Increase resolution of generated images\n- **Variations**: Create alternative versions of existing images\n- **Prompt Engineering**: Built-in prompts for refining image ideas\n\n## Authentication\n\nRequires an `EVERART_API_KEY` environment variable. Sign up at EverArt to obtain API credentials.\n\n## Use Cases\n\n- Marketing asset and social media image generation\n- UI/UX mockup and wireframe creation\n- Concept art and illustration prototyping\n- Image variation exploration for creative workflows",
      "_source": "data/mcp-servers/everart.md"
    },
    "fetch": {
      "type": "MCP-Server",
      "id": "fetch",
      "name": "Fetch",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-fetch"
      },
      "capabilities": {
        "tools": [
          "fetch_url",
          "fetch_html",
          "fetch_json",
          "fetch_text"
        ],
        "resources": null,
        "prompts": null
      },
      "stars": 4800,
      "last_updated": "2025-04-09",
      "verified": true,
      "tier": "Official",
      "categories": [
        "web"
      ],
      "skills_realized": null,
      "relations": {
        "exposes": null,
        "belongs_to": [
          "web"
        ],
        "commonly_composed_with": [
          "brave-search",
          "puppeteer",
          "sequential-thinking"
        ],
        "realizes_skills": null
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-fetch",
      "homepage": "https://github.com/modelcontextprotocol/server-fetch",
      "description": "Official Fetch MCP server providing simple, reliable HTTP fetching with automatic HTML-to-Markdown conversion and JSON parsing.",
      "body": "The official Fetch MCP server provides simple, reliable HTTP fetching capabilities for AI agents. It handles HTML, JSON, and plain text content with automatic content-type detection and parsing.\n\n## Key Features\n\n- **HTTP Fetching**: GET, POST, and other HTTP methods with configurable headers\n- **HTML-to-Markdown**: Automatic conversion of HTML pages to clean Markdown\n- **JSON Parsing**: Automatic parsing and validation of JSON responses\n- **Text Extraction**: Plain text extraction from web pages\n- **Safety**: URL validation to prevent SSRF attacks\n\n## Use Cases\n\n- Quick data retrieval from REST APIs\n- Content fetching for analysis and summarization\n- Lightweight web scraping without browser overhead\n- Webhook integration and callback handling",
      "_source": "data/mcp-servers/fetch.md"
    },
    "filesystem": {
      "type": "MCP-Server",
      "id": "filesystem",
      "name": "Filesystem",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/dir"
      },
      "capabilities": {
        "tools": [
          "read_file",
          "write_file",
          "list_directory",
          "create_directory",
          "move_file",
          "search_files",
          "get_file_info",
          "list_allowed_directories"
        ],
        "resources": null,
        "prompts": null
      },
      "stars": 11000,
      "last_updated": "2025-04-12",
      "verified": true,
      "tier": "Official",
      "categories": [
        "development",
        "infrastructure"
      ],
      "skills_realized": [
        "file-operations"
      ],
      "relations": {
        "exposes": null,
        "belongs_to": [
          "development",
          "infrastructure"
        ],
        "commonly_composed_with": [
          "github",
          "postgres",
          "sqlite"
        ],
        "realizes_skills": [
          "file-operations"
        ]
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-filesystem",
      "homepage": "https://github.com/modelcontextprotocol/server-filesystem",
      "description": "Official Filesystem MCP server providing safe, sandboxed file system access with support for read, write, directory management, and file search operations.",
      "body": "The official Filesystem MCP server provides safe, sandboxed file system access for AI agents. All operations are restricted to explicitly allowed directories, preventing unauthorized access to sensitive system paths.\n\n## Key Features\n\n- **File Operations**: Read and write files with full text and binary support\n- **Directory Management**: List, create, and traverse directories\n- **File Search**: Pattern-based file search within allowed directories\n- **Metadata Inspection**: Get file info including size, permissions, and timestamps\n- **Sandboxed Access**: Multiple allowed directories with strict path validation\n\n## Security Model\n\nThe server requires explicit directory paths as command-line arguments. It will refuse to access any path outside these allowed directories, making it safe to use with untrusted agents.\n\n## Use Cases\n\n- Local file management and organization\n- Reading configuration files and logs\n- Writing generated code, reports, and documentation\n- Batch file processing and transformation",
      "_source": "data/mcp-servers/filesystem.md"
    },
    "github": {
      "type": "MCP-Server",
      "id": "github",
      "name": "GitHub",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-github"
      },
      "capabilities": {
        "tools": [
          "search_repositories",
          "get_file_contents",
          "create_issue",
          "create_pull_request",
          "list_commits",
          "get_issue",
          "update_issue",
          "list_pull_requests",
          "merge_pull_request",
          "fork_repository",
          "create_branch",
          "search_code",
          "list_issues",
          "add_issue_comment"
        ],
        "resources": [
          "repository://{owner}/{repo}",
          "issue://{owner}/{repo}/{number}",
          "pull-request://{owner}/{repo}/{number}"
        ],
        "prompts": [
          "review_pull_request",
          "analyze_repository",
          "summarize_issues"
        ]
      },
      "stars": 13000,
      "last_updated": "2025-04-15",
      "verified": true,
      "tier": "Official",
      "categories": [
        "development"
      ],
      "skills_realized": [
        "code-review"
      ],
      "relations": {
        "exposes": [
          "repository://{owner}/{repo}",
          "issue://{owner}/{repo}/{number}",
          "pull-request://{owner}/{repo}/{number}"
        ],
        "belongs_to": [
          "development"
        ],
        "commonly_composed_with": [
          "filesystem",
          "fetch"
        ],
        "realizes_skills": [
          "code-review"
        ]
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-github",
      "homepage": "https://github.com/modelcontextprotocol/server-github",
      "description": "Official GitHub MCP server providing comprehensive access to GitHub's API for repository management, issues, pull requests, and code review.",
      "body": "The official GitHub MCP server provides comprehensive access to GitHub's API through the Model Context Protocol. It enables agents to search repositories, read file contents, manage issues and pull requests, analyze commit history, and perform code review tasks.\n\n## Key Features\n\n- **Repository Operations**: Search, fork, and browse repositories across GitHub\n- **Issue Management**: Create, read, update, and comment on issues\n- **Pull Request Workflow**: Create, review, merge, and manage PRs\n- **Code Search**: Search code across all of GitHub with advanced queries\n- **Branch Management**: Create branches and manage repository structure\n\n## Authentication\n\nRequires a `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable with appropriate scopes. Recommended scopes: `repo`, `read:user`, and `read:org` for full functionality.\n\n## Use Cases\n\n- Automated code review and PR summarization\n- Repository analysis and documentation generation\n- Issue triage and bug tracking workflows\n- Contributor analytics and project insights",
      "_source": "data/mcp-servers/github.md"
    },
    "google-maps": {
      "type": "MCP-Server",
      "id": "google-maps",
      "name": "Google Maps",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-google-maps"
      },
      "capabilities": {
        "tools": [
          "maps_geocode",
          "maps_reverse_geocode",
          "maps_search_places",
          "maps_place_details",
          "maps_directions",
          "maps_distance_matrix",
          "maps_elevation"
        ],
        "resources": null,
        "prompts": [
          "plan_route",
          "find_nearby"
        ]
      },
      "stars": 3100,
      "last_updated": "2025-04-06",
      "verified": true,
      "tier": "Official",
      "categories": [
        "web"
      ],
      "skills_realized": null,
      "relations": {
        "exposes": null,
        "belongs_to": [
          "web"
        ],
        "commonly_composed_with": [
          "brave-search",
          "fetch"
        ],
        "realizes_skills": null
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-google-maps",
      "homepage": "https://github.com/modelcontextprotocol/server-google-maps",
      "description": "Official Google Maps MCP server providing geocoding, place search, directions, distance matrix, and elevation APIs.",
      "body": "The official Google Maps MCP server enables AI agents to access Google's geocoding, places, directions, and elevation APIs through the Model Context Protocol.\n\n## Key Features\n\n- **Geocoding**: Convert addresses to coordinates and vice versa\n- **Place Search**: Find businesses and points of interest with text queries\n- **Place Details**: Retrieve reviews, photos, and detailed place information\n- **Directions**: Get driving, walking, biking, and transit directions\n- **Distance Matrix**: Calculate travel times and distances for multiple points\n- **Elevation**: Query elevation data for coordinates and paths\n\n## Authentication\n\nRequires a `GOOGLE_MAPS_API_KEY` environment variable. Enable the relevant APIs (Geocoding, Places, Directions, Distance Matrix, Elevation) in the Google Cloud Console.\n\n## Use Cases\n\n- Location-based service recommendations\n- Route planning and logistics optimization\n- Address validation and standardization\n- Travel time analysis and planning",
      "_source": "data/mcp-servers/google-maps.md"
    },
    "postgres": {
      "type": "MCP-Server",
      "id": "postgres",
      "name": "PostgreSQL",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-postgres postgresql://localhost/mydb"
      },
      "capabilities": {
        "tools": [
          "query",
          "execute",
          "list_tables",
          "describe_table",
          "get_connections"
        ],
        "resources": [
          "database://schemas",
          "database://tables"
        ],
        "prompts": [
          "analyze_schema",
          "optimize_query"
        ]
      },
      "stars": 8500,
      "last_updated": "2025-04-10",
      "verified": true,
      "tier": "Official",
      "categories": [
        "data"
      ],
      "skills_realized": [
        "database-query"
      ],
      "relations": {
        "exposes": [
          "database://schemas",
          "database://tables"
        ],
        "belongs_to": [
          "data"
        ],
        "commonly_composed_with": [
          "filesystem",
          "redis"
        ],
        "realizes_skills": [
          "database-query"
        ]
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-postgres",
      "homepage": "https://github.com/modelcontextprotocol/server-postgres",
      "description": "Official PostgreSQL MCP server enabling SQL query execution, schema introspection, and database management with read-only and read-write modes.",
      "body": "The official PostgreSQL MCP server enables AI agents to interact with PostgreSQL databases through the Model Context Protocol. It supports both read-only and read-write operations with configurable permissions.\n\n## Key Features\n\n- **SQL Execution**: Run queries with parameterized safety against injection\n- **Schema Introspection**: List tables, describe columns, and analyze relationships\n- **Read-Only Mode**: Safe exploration mode for production databases\n- **Transaction Support**: Full ACID transaction support for write operations\n- **Connection Management**: Efficient connection pooling and multi-database support\n\n## Connection\n\nPass a PostgreSQL connection string as a command-line argument. Supports all standard PostgreSQL connection options including SSL and custom ports.\n\n## Use Cases\n\n- Database exploration and schema analysis\n- SQL query generation and optimization\n- Data migration and transformation scripts\n- Reporting and analytics workflows",
      "_source": "data/mcp-servers/postgres.md"
    },
    "puppeteer": {
      "type": "MCP-Server",
      "id": "puppeteer",
      "name": "Puppeteer",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-puppeteer"
      },
      "capabilities": {
        "tools": [
          "puppeteer_navigate",
          "puppeteer_screenshot",
          "puppeteer_click",
          "puppeteer_type",
          "puppeteer_evaluate",
          "puppeteer_get_content",
          "puppeteer_scroll"
        ],
        "resources": [
          "browser://console",
          "browser://network"
        ],
        "prompts": [
          "debug_webpage",
          "extract_data"
        ]
      },
      "stars": 7200,
      "last_updated": "2025-04-11",
      "verified": true,
      "tier": "Official",
      "categories": [
        "web"
      ],
      "skills_realized": [
        "browser-automation"
      ],
      "relations": {
        "exposes": [
          "browser://console",
          "browser://network"
        ],
        "belongs_to": [
          "web"
        ],
        "commonly_composed_with": [
          "fetch",
          "brave-search"
        ],
        "realizes_skills": [
          "browser-automation"
        ]
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-puppeteer",
      "homepage": "https://github.com/modelcontextprotocol/server-puppeteer",
      "description": "Official Puppeteer MCP server providing full browser automation via headless Chrome for navigation, interaction, screenshots, and JavaScript execution.",
      "body": "The official Puppeteer MCP server provides full browser automation capabilities for AI agents. Built on Google's Puppeteer, it enables navigation, interaction, screenshot capture, and JavaScript execution in headless Chrome.\n\n## Key Features\n\n- **Navigation**: Load URLs and wait for page stabilization\n- **Screenshots**: Capture full-page or element-specific screenshots\n- **Interaction**: Click elements, fill forms, and simulate user input\n- **JavaScript Execution**: Run JS in browser context for dynamic content extraction\n- **Content Extraction**: Retrieve structured data from rendered pages\n- **Scrolling**: Handle infinite scroll and dynamic content loading\n\n## Use Cases\n\n- Web scraping and data extraction from JavaScript-heavy sites\n- Visual regression testing and screenshot comparison\n- Automated form submission and workflow testing\n- PDF generation from web pages\n- SPA (Single Page Application) interaction and testing",
      "_source": "data/mcp-servers/puppeteer.md"
    },
    "redis": {
      "type": "MCP-Server",
      "id": "redis",
      "name": "Redis",
      "publisher": "community",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-redis"
      },
      "capabilities": {
        "tools": [
          "redis_get",
          "redis_set",
          "redis_delete",
          "redis_list_keys",
          "redis_expire",
          "redis_incr",
          "redis_decr",
          "redis_hget",
          "redis_hset",
          "redis_lpush",
          "redis_lrange",
          "redis_publish",
          "redis_subscribe"
        ],
        "resources": [
          "redis://keys",
          "redis://databases"
        ],
        "prompts": null
      },
      "stars": 2800,
      "last_updated": "2025-04-05",
      "verified": false,
      "tier": "Community",
      "categories": [
        "data",
        "infrastructure"
      ],
      "skills_realized": [
        "database-query"
      ],
      "relations": {
        "exposes": [
          "redis://keys",
          "redis://databases"
        ],
        "belongs_to": [
          "data",
          "infrastructure"
        ],
        "commonly_composed_with": [
          "postgres",
          "sqlite"
        ],
        "realizes_skills": [
          "database-query"
        ]
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-redis",
      "homepage": "https://github.com/modelcontextprotocol/server-redis",
      "description": "Redis MCP server providing high-performance key-value store operations including strings, hashes, lists, and pub/sub messaging.",
      "body": "The Redis MCP server provides high-performance key-value store operations for AI agents. It supports the full range of Redis data structures including strings, hashes, lists, sets, and pub/sub messaging.\n\n## Key Features\n\n- **String Operations**: get, set, delete, expire, increment/decrement\n- **Hash Operations**: Field-level get and set for structured data\n- **List Operations**: Push, pop, and range queries\n- **Key Management**: Pattern matching, scanning, and TTL management\n- **Pub/Sub**: Publish and subscribe to channels for real-time messaging\n- **Cache Strategies**: Built-in TTL and expiration management\n\n## Connection\n\nConfigure via `REDIS_HOST`, `REDIS_PORT`, and optionally `REDIS_PASSWORD` environment variables. Supports both standalone and clustered Redis deployments.\n\n## Use Cases\n\n- High-speed caching and session storage\n- Real-time leaderboards and counters\n- Message queuing and job scheduling\n- Rate limiting and throttling\n- Real-time analytics and event streaming",
      "_source": "data/mcp-servers/redis.md"
    },
    "sentry": {
      "type": "MCP-Server",
      "id": "sentry",
      "name": "Sentry",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-sentry"
      },
      "capabilities": {
        "tools": [
          "sentry_get_issue",
          "sentry_list_issues",
          "sentry_get_project",
          "sentry_list_projects",
          "sentry_get_event",
          "sentry_create_comment"
        ],
        "resources": [
          "sentry://projects",
          "sentry://issues"
        ],
        "prompts": [
          "analyze_error",
          "triage_issues"
        ]
      },
      "stars": 1900,
      "last_updated": "2025-04-02",
      "verified": true,
      "tier": "Official",
      "categories": [
        "infrastructure",
        "development"
      ],
      "skills_realized": null,
      "relations": {
        "exposes": [
          "sentry://projects",
          "sentry://issues"
        ],
        "belongs_to": [
          "infrastructure",
          "development"
        ],
        "commonly_composed_with": [
          "slack",
          "github"
        ],
        "realizes_skills": null
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-sentry",
      "homepage": "https://github.com/modelcontextprotocol/server-sentry",
      "description": "Official Sentry MCP server enabling agents to monitor application errors, inspect stack traces, retrieve issues, and assist with bug triage.",
      "body": "The official Sentry MCP server enables AI agents to monitor and analyze application errors through the Model Context Protocol. Agents can retrieve issues, inspect stack traces, and help triage bugs.\n\n## Key Features\n\n- **Issue Retrieval**: Get detailed issue information with full stack traces\n- **Issue Management**: List and filter issues by project, status, and priority\n- **Project Browsing**: Explore projects and organizations\n- **Event Inspection**: Deep-dive into individual error events with context\n- **Team Collaboration**: Add comments to issues for workflow coordination\n- **Analysis Prompts**: Built-in error analysis and triage assistance\n\n## Authentication\n\nRequires a `SENTRY_AUTH_TOKEN` environment variable with `org:read`, `project:read`, and `event:read` scopes.\n\n## Use Cases\n\n- Automated error triage and prioritization\n- Root cause analysis from stack traces\n- Bug report generation and ticket creation\n- Error trend monitoring and alerting",
      "_source": "data/mcp-servers/sentry.md"
    },
    "sequential-thinking": {
      "type": "MCP-Server",
      "id": "sequential-thinking",
      "name": "Sequential Thinking",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-sequential-thinking"
      },
      "capabilities": {
        "tools": [
          "sequentialthinking",
          "think",
          "revise_thought"
        ],
        "resources": null,
        "prompts": [
          "chain_of_thought",
          "step_by_step_analysis"
        ]
      },
      "stars": 9500,
      "last_updated": "2025-04-13",
      "verified": true,
      "tier": "Official",
      "categories": [
        "ai-operations"
      ],
      "skills_realized": [
        "reasoning"
      ],
      "relations": {
        "exposes": null,
        "belongs_to": [
          "ai-operations"
        ],
        "commonly_composed_with": [
          "brave-search",
          "fetch",
          "github"
        ],
        "realizes_skills": [
          "reasoning"
        ]
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-sequential-thinking",
      "homepage": "https://github.com/modelcontextprotocol/server-sequential-thinking",
      "description": "Official Sequential Thinking MCP server enabling structured, step-by-step reasoning with chain-of-thought patterns and thought revision capabilities.",
      "body": "The official Sequential Thinking MCP server enables structured, step-by-step reasoning for AI agents. It implements a chain-of-thought pattern where each reasoning step builds on previous ones, with support for revision and branching.\n\n## Key Features\n\n- **Step-by-Step Reasoning**: Progressive thought building with full memory of prior steps\n- **Thought Revision**: Ability to revisit and correct previous thoughts when new information arises\n- **Branching**: Explore multiple reasoning paths and hypotheses simultaneously\n- **Configurable Depth**: Control the complexity and depth of reasoning chains\n- **Integration Prompts**: Built-in chain-of-thought and analysis prompts\n\n## Philosophy\n\nRather than generating a single response, this server encourages agents to think through problems methodically, tracking their reasoning process and allowing course correction — mimicking human analytical thinking.\n\n## Use Cases\n\n- Complex problem decomposition and analysis\n- Multi-step planning and strategy formulation\n- Debugging and root cause analysis\n- Research synthesis from multiple sources\n- Decision-making with transparent reasoning",
      "_source": "data/mcp-servers/sequential-thinking.md"
    },
    "slack": {
      "type": "MCP-Server",
      "id": "slack",
      "name": "Slack",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-slack"
      },
      "capabilities": {
        "tools": [
          "slack_list_channels",
          "slack_post_message",
          "slack_reply_to_thread",
          "slack_add_reaction",
          "slack_get_channel_history",
          "slack_get_thread_replies",
          "slack_get_users",
          "slack_get_user_profile"
        ],
        "resources": [
          "slack://channels",
          "slack://users"
        ],
        "prompts": [
          "summarize_conversation",
          "draft_announcement"
        ]
      },
      "stars": 6200,
      "last_updated": "2025-04-08",
      "verified": true,
      "tier": "Official",
      "categories": [
        "communication"
      ],
      "skills_realized": null,
      "relations": {
        "exposes": [
          "slack://channels",
          "slack://users"
        ],
        "belongs_to": [
          "communication"
        ],
        "commonly_composed_with": [
          "github",
          "sentry"
        ],
        "realizes_skills": null
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-slack",
      "homepage": "https://github.com/modelcontextprotocol/server-slack",
      "description": "Official Slack MCP server enabling agents to read channel history, post messages, reply to threads, and manage reactions in Slack workspaces.",
      "body": "The official Slack MCP server allows AI agents to interact with Slack workspaces. Agents can read channel history, post messages, reply to threads, and manage reactions — enabling rich team collaboration workflows.\n\n## Key Features\n\n- **Channel Operations**: List channels and retrieve message history\n- **Messaging**: Post messages to channels and reply in threads\n- **Reactions**: Add emoji reactions to messages for lightweight interactions\n- **Thread Context**: Retrieve full thread replies for contextual conversations\n- **User Directory**: List workspace users and view profiles\n\n## Authentication\n\nRequires a `SLACK_BOT_TOKEN` environment variable. The bot needs appropriate scopes including `chat:write`, `channels:read`, `channels:history`, and `users:read`.\n\n## Use Cases\n\n- Automated status updates and announcements\n- Conversation summarization and action item extraction\n- Interactive team assistance and Q&A\n- Incident response coordination",
      "_source": "data/mcp-servers/slack.md"
    },
    "sqlite": {
      "type": "MCP-Server",
      "id": "sqlite",
      "name": "SQLite",
      "publisher": "community",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-sqlite /path/to/database.db"
      },
      "capabilities": {
        "tools": [
          "query",
          "execute",
          "list_tables",
          "describe_table",
          "create_table",
          "insert_data"
        ],
        "resources": [
          "sqlite://tables",
          "sqlite://schema"
        ],
        "prompts": [
          "schema_analysis",
          "query_optimization"
        ]
      },
      "stars": 4200,
      "last_updated": "2025-04-07",
      "verified": false,
      "tier": "Community",
      "categories": [
        "data"
      ],
      "skills_realized": [
        "database-query"
      ],
      "relations": {
        "exposes": [
          "sqlite://tables",
          "sqlite://schema"
        ],
        "belongs_to": [
          "data"
        ],
        "commonly_composed_with": [
          "filesystem",
          "postgres"
        ],
        "realizes_skills": [
          "database-query"
        ]
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-sqlite",
      "homepage": "https://github.com/modelcontextprotocol/server-sqlite",
      "description": "SQLite MCP server providing local file-based database operations with full SQL support, schema introspection, and zero external dependencies.",
      "body": "The SQLite MCP server provides local, file-based database operations for AI agents. Unlike the PostgreSQL server, it requires no separate database process — just a path to a `.db` file.\n\n## Key Features\n\n- **SQL Operations**: Execute queries with full DDL and DML support\n- **Schema Management**: Create, alter, and inspect tables and indexes\n- **Data Manipulation**: Insert, update, delete with parameterized queries\n- **Schema Introspection**: Automatic analysis of database structure\n- **Zero Configuration**: No server setup — works directly with `.db` files\n\n## Use Cases\n\n- Local application data storage\n- Prototyping and development databases\n- Embedded analytics and reporting\n- Data transformation pipelines\n- Cache and session management",
      "_source": "data/mcp-servers/sqlite.md"
    },
    "time": {
      "type": "MCP-Server",
      "id": "time",
      "name": "Time",
      "publisher": "modelcontextprotocol",
      "transport": "stdio",
      "install": {
        "type": "npm",
        "command": "npx -y @modelcontextprotocol/server-time"
      },
      "capabilities": {
        "tools": [
          "get_current_time",
          "convert_timezone",
          "list_timezones",
          "parse_natural_time"
        ],
        "resources": null,
        "prompts": null
      },
      "stars": 2100,
      "last_updated": "2025-04-03",
      "verified": true,
      "tier": "Official",
      "categories": [
        "infrastructure"
      ],
      "skills_realized": null,
      "relations": {
        "exposes": null,
        "belongs_to": [
          "infrastructure"
        ],
        "commonly_composed_with": [
          "slack",
          "sentry"
        ],
        "realizes_skills": null
      },
      "license": "MIT",
      "source_url": "https://github.com/modelcontextprotocol/server-time",
      "homepage": "https://github.com/modelcontextprotocol/server-time",
      "description": "Official Time MCP server providing time and timezone operations including current time, timezone conversion, and natural language time parsing.",
      "body": "The official Time MCP server provides time and timezone operations for AI agents. It enables getting current time, converting between timezones, and parsing natural language time expressions.\n\n## Key Features\n\n- **Current Time**: Get precise current time in any IANA timezone\n- **Timezone Conversion**: Convert timestamps between timezones\n- **Timezone Listing**: Browse all available IANA timezone identifiers\n- **Natural Language Parsing**: Understand expressions like \"3pm tomorrow in Tokyo\"\n- **ISO 8601 Output**: Machine-readable timestamp formatting\n\n## Use Cases\n\n- Multi-timezone scheduling and coordination\n- Deadline tracking and countdown calculations\n- Timestamp normalization across data sources\n- Meeting time finding across time zones",
      "_source": "data/mcp-servers/time.md"
    },
    "context-amplification": {
      "type": "Agentic-Pattern",
      "id": "context-amplification",
      "name": "Context Amplification",
      "description": "Using retrieval tools to augment agent context beyond training data. This pattern describes how agents overcome their inherent knowledge limitations by dynamically retrieving current, relevant information from external sources during task execution. The agent's effective context is amplified by the tools it can access.",
      "examples": [
        "brave-search",
        "aws-kb-retrieval",
        "fetch",
        "sequential-thinking"
      ],
      "relations": {
        "exemplified_by": [
          "brave-search",
          "aws-kb-retrieval",
          "fetch",
          "sequential-thinking"
        ],
        "related_to": [
          "tool-composition",
          "skill-realization"
        ]
      },
      "body": "",
      "_source": "data/patterns/context-amplification.md"
    },
    "skill-realization": {
      "type": "Agentic-Pattern",
      "id": "skill-realization",
      "name": "Skill Realization",
      "description": "Abstract skills mapped to concrete tool implementations. This pattern describes how high-level capabilities (skills) are grounded in specific MCP server implementations. A single skill like 'database-query' can be realized by multiple servers (PostgreSQL, SQLite, Redis), each optimized for different scenarios.",
      "examples": [
        "postgres",
        "sqlite",
        "redis",
        "brave-search",
        "puppeteer"
      ],
      "relations": {
        "exemplified_by": [
          "postgres",
          "sqlite",
          "redis",
          "brave-search",
          "puppeteer"
        ],
        "related_to": [
          "tool-composition",
          "context-amplification"
        ]
      },
      "body": "",
      "_source": "data/patterns/skill-realization.md"
    },
    "tool-composition": {
      "type": "Agentic-Pattern",
      "id": "tool-composition",
      "name": "Tool Composition",
      "description": "Multiple MCP servers composed to accomplish complex tasks. This pattern describes how agents break down complex objectives into sub-tasks, each delegated to the most appropriate MCP server. The outputs of one tool become inputs to another, creating a pipeline of capabilities that exceeds what any single server could achieve alone.",
      "examples": [
        "filesystem",
        "postgres",
        "github",
        "slack"
      ],
      "relations": {
        "exemplified_by": [
          "filesystem",
          "postgres",
          "github",
          "slack"
        ],
        "related_to": [
          "skill-realization",
          "context-amplification"
        ]
      },
      "body": "",
      "_source": "data/patterns/tool-composition.md"
    },
    "anthropic": {
      "type": "Publisher",
      "id": "anthropic",
      "name": "Anthropic",
      "type_org": "Official",
      "links": {
        "github": "https://github.com/anthropics",
        "website": "https://www.anthropic.com"
      },
      "relations": {
        "publishes": null,
        "maintains": [
          "sequential-thinking"
        ]
      },
      "body": "",
      "_source": "data/publishers/anthropic.md"
    },
    "community": {
      "type": "Publisher",
      "id": "community",
      "name": "Community Contributors",
      "type_org": "Community",
      "links": {
        "github": "https://github.com/modelcontextprotocol",
        "website": "https://github.com/modelcontextprotocol"
      },
      "relations": {
        "publishes": [
          "sqlite",
          "redis"
        ],
        "maintains": [
          "sqlite",
          "redis"
        ]
      },
      "body": "",
      "_source": "data/publishers/community.md"
    },
    "docker": {
      "type": "Publisher",
      "id": "docker",
      "name": "Docker",
      "type_org": "Official",
      "links": {
        "github": "https://github.com/docker",
        "website": "https://www.docker.com"
      },
      "relations": {
        "publishes": null,
        "maintains": null
      },
      "body": "",
      "_source": "data/publishers/docker.md"
    },
    "individual": {
      "type": "Publisher",
      "id": "individual",
      "name": "Individual Maintainers",
      "type_org": "Individual",
      "links": {
        "github": null,
        "website": null
      },
      "relations": {
        "publishes": null,
        "maintains": null
      },
      "body": "",
      "_source": "data/publishers/individual.md"
    },
    "jetbrains": {
      "type": "Publisher",
      "id": "jetbrains",
      "name": "JetBrains",
      "type_org": "Official",
      "links": {
        "github": "https://github.com/JetBrains",
        "website": "https://www.jetbrains.com"
      },
      "relations": {
        "publishes": null,
        "maintains": null
      },
      "body": "",
      "_source": "data/publishers/jetbrains.md"
    },
    "modelcontextprotocol": {
      "type": "Publisher",
      "id": "modelcontextprotocol",
      "name": "Model Context Protocol",
      "type_org": "Official",
      "links": {
        "github": "https://github.com/modelcontextprotocol",
        "website": "https://modelcontextprotocol.io"
      },
      "relations": {
        "publishes": [
          "github",
          "filesystem",
          "postgres",
          "slack",
          "brave-search",
          "puppeteer",
          "fetch",
          "sequential-thinking",
          "google-maps",
          "aws-kb-retrieval",
          "time",
          "sentry",
          "everart"
        ],
        "maintains": [
          "github",
          "filesystem",
          "postgres",
          "slack",
          "brave-search",
          "puppeteer",
          "fetch",
          "sequential-thinking",
          "google-maps",
          "aws-kb-retrieval",
          "time",
          "sentry",
          "everart"
        ]
      },
      "body": "",
      "_source": "data/publishers/modelcontextprotocol.md"
    },
    "pulsarity-labs": {
      "type": "Publisher",
      "id": "pulsarity-labs",
      "name": "Pulsarity Labs",
      "type_org": "Community",
      "links": {
        "github": "https://github.com/pulsarity-labs",
        "website": "https://pulsarity.io"
      },
      "relations": {
        "publishes": null,
        "maintains": null
      },
      "body": "",
      "_source": "data/publishers/pulsarity-labs.md"
    },
    "smithery": {
      "type": "Publisher",
      "id": "smithery",
      "name": "Smithery",
      "type_org": "Community",
      "links": {
        "github": "https://github.com/smithery-ai",
        "website": "https://smithery.ai"
      },
      "relations": {
        "publishes": null,
        "maintains": null
      },
      "body": "",
      "_source": "data/publishers/smithery.md"
    },
    "browser-automation": {
      "type": "Skill",
      "id": "browser-automation",
      "name": "Browser Automation",
      "taxonomy": "al-dente-core",
      "level": 3,
      "parent": null,
      "categories": [
        "web"
      ],
      "relations": {
        "realized_by": [
          "puppeteer"
        ],
        "belongs_to": [
          "web"
        ],
        "related_to": [
          "web-search"
        ]
      },
      "description": "Control web browsers for testing, scraping, and interaction with dynamic web applications. This skill encompasses navigation, form interaction, screenshot capture, and JavaScript execution. It sits at level 3 as a more specific technique within the web domain, requiring deeper integration with browser internals.",
      "body": "",
      "_source": "data/skills/browser-automation.md"
    },
    "code-generation": {
      "type": "Skill",
      "id": "code-generation",
      "name": "Code Generation",
      "taxonomy": "al-dente-core",
      "level": 2,
      "parent": null,
      "categories": [
        "development"
      ],
      "relations": {
        "realized_by": null,
        "belongs_to": [
          "development"
        ],
        "related_to": [
          "code-review"
        ]
      },
      "description": "Generate, modify, and refactor source code across programming languages. This skill enables agents to write new functions, transform existing code, adapt code between languages, and apply architectural patterns. It sits at level 2 in the taxonomy as a broad but well-defined capability within the software development domain.",
      "body": "",
      "_source": "data/skills/code-generation.md"
    },
    "code-review": {
      "type": "Skill",
      "id": "code-review",
      "name": "Code Review",
      "taxonomy": "al-dente-core",
      "level": 2,
      "parent": null,
      "categories": [
        "development"
      ],
      "relations": {
        "realized_by": [
          "github"
        ],
        "belongs_to": [
          "development"
        ],
        "related_to": [
          "code-generation"
        ]
      },
      "description": "Analyze code for bugs, security vulnerabilities, style issues, and improvement opportunities. This skill encompasses static analysis, pattern detection, and constructive feedback generation. It enables agents to act as automated code reviewers, catching issues before they reach production.",
      "body": "",
      "_source": "data/skills/code-review.md"
    },
    "database-query": {
      "type": "Skill",
      "id": "database-query",
      "name": "Database Query",
      "taxonomy": "al-dente-core",
      "level": 2,
      "parent": null,
      "categories": [
        "data"
      ],
      "relations": {
        "realized_by": [
          "postgres",
          "sqlite",
          "redis"
        ],
        "belongs_to": [
          "data"
        ],
        "related_to": [
          "knowledge-retrieval"
        ]
      },
      "description": "Read, write, and manage structured data in databases. This skill covers SQL and NoSQL query formulation, schema design, data migration, and transaction management. It enables agents to interact with persistent storage systems to retrieve, analyze, and modify structured information.",
      "body": "",
      "_source": "data/skills/database-query.md"
    },
    "file-operations": {
      "type": "Skill",
      "id": "file-operations",
      "name": "File Operations",
      "taxonomy": "al-dente-core",
      "level": 2,
      "parent": null,
      "categories": [
        "development",
        "infrastructure"
      ],
      "relations": {
        "realized_by": [
          "filesystem"
        ],
        "belongs_to": [
          "development",
          "infrastructure"
        ],
        "related_to": [
          "database-query"
        ]
      },
      "description": "Read, write, and manage files and directories. This skill enables agents to interact with the local file system for code editing, log analysis, configuration management, and document processing. It forms the foundation for many development and system administration workflows.",
      "body": "",
      "_source": "data/skills/file-operations.md"
    },
    "knowledge-retrieval": {
      "type": "Skill",
      "id": "knowledge-retrieval",
      "name": "Knowledge Retrieval",
      "taxonomy": "al-dente-core",
      "level": 2,
      "parent": null,
      "categories": [
        "ai-operations",
        "data"
      ],
      "relations": {
        "realized_by": [
          "aws-kb-retrieval"
        ],
        "belongs_to": [
          "ai-operations",
          "data"
        ],
        "related_to": [
          "web-search",
          "reasoning"
        ]
      },
      "description": "Access and query structured knowledge bases and documentation. This skill enables agents to retrieve relevant information from curated knowledge stores, supporting retrieval-augmented generation (RAG) workflows. It includes semantic search, relevance ranking, and knowledge synthesis.",
      "body": "",
      "_source": "data/skills/knowledge-retrieval.md"
    },
    "reasoning": {
      "type": "Skill",
      "id": "reasoning",
      "name": "Reasoning",
      "taxonomy": "al-dente-core",
      "level": 1,
      "parent": null,
      "categories": [
        "ai-operations"
      ],
      "relations": {
        "realized_by": [
          "sequential-thinking"
        ],
        "belongs_to": [
          "ai-operations"
        ],
        "related_to": [
          "knowledge-retrieval"
        ]
      },
      "description": "Apply structured thinking, planning, and step-by-step problem solving. This is a broad domain-level skill (level 1) that underpins complex agent workflows. It encompasses decomposition, hypothesis generation, evidence evaluation, and conclusion drawing — forming the cognitive backbone of agentic systems.",
      "body": "",
      "_source": "data/skills/reasoning.md"
    },
    "web-search": {
      "type": "Skill",
      "id": "web-search",
      "name": "Web Search",
      "taxonomy": "al-dente-core",
      "level": 2,
      "parent": null,
      "categories": [
        "web"
      ],
      "relations": {
        "realized_by": [
          "brave-search"
        ],
        "belongs_to": [
          "web"
        ],
        "related_to": [
          "knowledge-retrieval"
        ]
      },
      "description": "Search the internet for current information, documentation, and real-time data. This skill enables agents to overcome the knowledge cutoff of their training data by retrieving up-to-date information from the web. It includes query formulation, result evaluation, and source credibility assessment.",
      "body": "",
      "_source": "data/skills/web-search.md"
    }
  },
  "byType": {
    "MCP-Server": [
      "aws-kb-retrieval",
      "brave-search",
      "everart",
      "fetch",
      "filesystem",
      "github",
      "google-maps",
      "postgres",
      "puppeteer",
      "redis",
      "sentry",
      "sequential-thinking",
      "slack",
      "sqlite",
      "time"
    ],
    "Skill": [
      "browser-automation",
      "code-generation",
      "code-review",
      "database-query",
      "file-operations",
      "knowledge-retrieval",
      "reasoning",
      "web-search"
    ],
    "Category": [
      "ai-operations",
      "communication",
      "data",
      "development",
      "infrastructure",
      "web"
    ],
    "Agentic-Pattern": [
      "context-amplification",
      "skill-realization",
      "tool-composition"
    ],
    "Publisher": [
      "anthropic",
      "community",
      "docker",
      "individual",
      "jetbrains",
      "modelcontextprotocol",
      "pulsarity-labs",
      "smithery"
    ]
  },
  "byCategory": {
    "ai-operations": [
      "aws-kb-retrieval",
      "everart",
      "knowledge-retrieval",
      "reasoning",
      "sequential-thinking"
    ],
    "data": [
      "aws-kb-retrieval",
      "database-query",
      "knowledge-retrieval",
      "postgres",
      "redis",
      "sqlite"
    ],
    "web": [
      "brave-search",
      "browser-automation",
      "fetch",
      "google-maps",
      "puppeteer",
      "web-search"
    ],
    "development": [
      "code-generation",
      "code-review",
      "file-operations",
      "filesystem",
      "github",
      "sentry"
    ],
    "infrastructure": [
      "file-operations",
      "filesystem",
      "redis",
      "sentry",
      "time"
    ],
    "communication": [
      "slack"
    ]
  },
  "metadata": {
    "generated": "2026-07-14T10:52:10.531956+00:00",
    "version": "0.1.0",
    "entityCount": 40,
    "countsByType": {
      "MCP-Server": 15,
      "Skill": 8,
      "Category": 6,
      "Agentic-Pattern": 3,
      "Publisher": 8
    }
  }
};
