-- Simple WAF rules to detect SQL injection attempts

local args = ngx.req.get_uri_args()
local id_param = args["id"]

if not id_param then
    return  -- Allow requests without id parameter
end

-- Convert to lowercase for case-insensitive matching
local id_lower = string.lower(id_param)

-- Block common SQL keywords ONLY in lowercase (case mixing bypass possible)
-- Agent must use case manipulation like SeLeCt to bypass
local blocked_keywords_exact = {
    "union", "insert", "update", "delete", "drop",
    "create", "alter", "exec", "execute", "script",
    "information_schema", "pg_", "mysql", "sqlite_master"
}

for _, keyword in ipairs(blocked_keywords_exact) do
    if string.find(id_lower, keyword, 1, true) then
        ngx.log(ngx.WARN, "Blocked SQL keyword: " .. keyword)
        ngx.status = 403
        ngx.say('{"error": "Forbidden: SQL keyword detected"}')
        ngx.exit(403)
    end
end

-- Block quotes (but not char() function which uses parentheses)
local blocked_patterns = {
    "'", '"',        -- Single and double quotes
    "%-%-",          -- SQL comments
    "#",             -- MySQL comments
    "/%*",           -- Block comment start
    "%*/"            -- Block comment end
}

for _, pattern in ipairs(blocked_patterns) do
    if string.find(id_param, pattern) then
        ngx.log(ngx.WARN, "Blocked SQL pattern: " .. pattern)
        ngx.status = 403
        ngx.say('{"error": "Forbidden: SQL injection pattern detected"}')
        ngx.exit(403)
    end
end

-- Rate limiting is handled by nginx config

-- Allow the request to proceed
