"""
S0NAR — static configuration.

Everything that doesn't change at runtime lives here: port lists,
the built-in DNS wordlist, resolver pool, the takeover fingerprint
database, and the paths used by built-in vulnerability checks.

Author: LordXapose
Repo:   https://github.com/LordXapose/s0nar
"""

from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────
# Global metadata
# ─────────────────────────────────────────────────────────────────────

VERSION = "1.0.0"
AUTHOR  = "LordXapose"
REPO    = "github.com/LordXapose/s0nar"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"

# ─────────────────────────────────────────────────────────────────────
# DNS
# ─────────────────────────────────────────────────────────────────────

# Public resolvers — rotated round-robin per query
DNS_RESOLVERS = [
    "8.8.8.8",        # Google
    "8.8.4.4",        # Google
    "1.1.1.1",        # Cloudflare
    "1.0.0.1",        # Cloudflare
    "9.9.9.9",        # Quad9
    "208.67.222.222", # OpenDNS
]

DNS_TIMEOUT   = 5      # seconds per query
DNS_LIFETIME  = 5      # total resolution lifetime

# ─────────────────────────────────────────────────────────────────────
# Ports
# ─────────────────────────────────────────────────────────────────────

# Top ~120 ports — common services + non-HTTP services worth flagging
DEFAULT_PORTS = ",".join(str(p) for p in [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 161, 389, 443,
    445, 465, 587, 636, 993, 995, 1080, 1433, 1521, 1723, 1883, 2049,
    2082, 2083, 2086, 2087, 2095, 2096, 2181, 2222, 2375, 2376, 2480,
    3000, 3128, 3260, 3306, 3389, 4000, 4443, 4444, 5000, 5432, 5555,
    5601, 5672, 5900, 5901, 5984, 6379, 6443, 7001, 7070, 7443, 8000,
    8008, 8009, 8080, 8081, 8088, 8443, 8888, 8983, 9000, 9001, 9042,
    9090, 9091, 9200, 9300, 9418, 9443, 10000, 10250, 11211, 15672,
    27017, 27018, 50000, 50070, 61616,
])

# Ports that speak HTTP or HTTPS — used by the prober
HTTP_PORTS  = {80, 3000, 5000, 5601, 7001, 7070, 8000, 8008, 8080,
               8081, 8088, 8888, 8983, 9000, 9001, 9090, 9200, 10000,
               15672, 50070}
HTTPS_PORTS = {443, 4443, 6443, 7443, 8443, 9443, 10250}

# Friendly names for non-HTTP services — used in the ports table
NON_HTTP_SERVICES = {
    21:    "FTP",         22:    "SSH",        23:    "Telnet",
    25:    "SMTP",        53:    "DNS",        110:   "POP3",
    111:   "rpcbind",     135:   "MSRPC",      139:   "NetBIOS",
    143:   "IMAP",        161:   "SNMP",       389:   "LDAP",
    445:   "SMB",         465:   "SMTPS",      587:   "SMTP",
    636:   "LDAPS",       993:   "IMAPS",      995:   "POP3S",
    1080:  "SOCKS",       1433:  "MSSQL",      1521:  "Oracle",
    1723:  "PPTP",        1883:  "MQTT",       2049:  "NFS",
    2181:  "Zookeeper",   2222:  "SSH-alt",    2375:  "Docker",
    2376:  "Docker-TLS",  3260:  "iSCSI",      3306:  "MySQL",
    3389:  "RDP",         5432:  "PostgreSQL", 5555:  "ADB",
    5672:  "RabbitMQ",    5900:  "VNC",        5901:  "VNC",
    5984:  "CouchDB",     6379:  "Redis",      9042:  "Cassandra",
    9091:  "Prometheus",  9300:  "Elasticsearch", 9418: "Git",
    11211: "Memcached",   15672: "RabbitMQ-UI",
    27017: "MongoDB",     27018: "MongoDB",    61616: "ActiveMQ",
}

# ─────────────────────────────────────────────────────────────────────
# Built-in DNS brute-force wordlist (~200 common subdomains)
# ─────────────────────────────────────────────────────────────────────

BUILTIN_WORDLIST = [
    # Common services
    "www", "mail", "smtp", "pop", "pop3", "imap", "webmail", "mx",
    "mx1", "mx2", "mail1", "mail2", "email", "owa", "exchange",
    "autodiscover", "autoconfig", "webdisk", "cpanel", "whm", "plesk",
    "direct", "directadmin",

    # DNS / infrastructure
    "ns", "ns1", "ns2", "ns3", "ns4", "dns", "dns1", "dns2",
    "ftp", "sftp", "ssh", "vpn", "remote", "gateway", "router",
    "firewall", "proxy", "squid", "cache", "cdn", "static", "assets",

    # Dev / staging
    "dev", "development", "stage", "staging", "stg", "test", "testing",
    "qa", "uat", "preprod", "sandbox", "demo", "beta", "alpha", "canary",
    "preview", "old", "legacy", "new", "next", "v2", "v3",

    # Apps / APIs
    "api", "api-v1", "api-v2", "rest", "graphql", "grpc", "ws", "wss",
    "web", "app", "apps", "mobile", "m", "portal", "dashboard", "panel",
    "console", "admin", "administrator", "manage", "manager",

    # Business / comms
    "blog", "news", "forum", "bbs", "shop", "store", "ecommerce",
    "checkout", "cart", "payment", "pay", "billing", "invoice",
    "support", "help", "helpdesk", "ticket", "tickets", "crm", "erp",
    "hr", "intranet", "internal", "extranet", "partner", "partners",
    "client", "clients", "customer", "customers",

    # Content / media
    "media", "images", "img", "video", "videos", "files", "docs",
    "doc", "document", "documents", "download", "downloads", "upload",
    "uploads", "ftp2", "wiki", "kb", "knowledgebase", "faq",

    # Infra / ops
    "monitor", "monitoring", "status", "health", "metrics", "stats",
    "analytics", "log", "logs", "logging", "grafana", "kibana",
    "prometheus", "nagios", "zabbix", "sentry", "datadog",

    # CI/CD / devops
    "git", "gitlab", "github", "bitbucket", "jenkins", "travis",
    "circleci", "build", "ci", "cd", "deploy", "registry", "docker",
    "k8s", "kubernetes", "rancher", "openshift", "helm",

    # Databases / storage
    "db", "database", "mysql", "postgres", "postgresql", "mongo",
    "mongodb", "redis", "elastic", "elasticsearch", "cassandra",
    "backup", "backups", "archive", "s3", "storage", "blob",

    # Auth / security
    "sso", "auth", "login", "id", "identity", "oauth", "saml",
    "ldap", "ad", "vault", "kms", "keys",

    # Misc
    "meet", "chat", "im", "voip", "sip", "call", "conference",
    "zoom", "teams", "slack", "calendar", "calls", "video2",
    "training", "learn", "edu", "academy", "lms", "course", "courses",
    "community", "social", "events", "webinar", "press", "careers",
    "jobs", "recruiting", "investor", "ir", "legal", "privacy",
    "security", "trust", "compliance", "policy",
]

# ─────────────────────────────────────────────────────────────────────
# Subdomain takeover fingerprints
#
# key   = substring matched against the CNAME target (lowercase)
# value = (friendly service name, list of "unclaimed page" body strings)
# ─────────────────────────────────────────────────────────────────────

TAKEOVER_FINGERPRINTS: dict[str, tuple[str, list[str]]] = {
    "github.io":              ("GitHub Pages",
                                ["there isn't a github pages site here",
                                 "for root urls (like http://example.com) you must provide an index.html file"]),
    "herokuapp.com":          ("Heroku",
                                ["no such app",
                                 "heroku | no such app"]),
    "s3.amazonaws.com":       ("AWS S3",
                                ["nosuchbucket",
                                 "the specified bucket does not exist"]),
    "cloudfront.net":         ("AWS CloudFront",
                                ["bad request",
                                 "error: the request could not be satisfied"]),
    "elasticbeanstalk.com":   ("AWS Elastic Beanstalk",
                                ["404 not found"]),
    "azurewebsites.net":      ("Azure Web Apps",
                                ["404 web site not found",
                                 "error 404 - web app not found"]),
    "cloudapp.azure.com":     ("Azure",
                                ["404 web site not found"]),
    "trafficmanager.net":     ("Azure Traffic Manager",
                                ["page not found"]),
    "blob.core.windows.net":  ("Azure Blob Storage",
                                ["blobnotfound"]),
    "azurefd.net":            ("Azure Front Door",
                                ["404 not found"]),
    "shopify.com":            ("Shopify",
                                ["sorry, this shop is currently unavailable"]),
    "myshopify.com":          ("Shopify",
                                ["sorry, this shop is currently unavailable"]),
    "fastly.net":             ("Fastly",
                                ["fastly error: unknown domain"]),
    "pantheonsite.io":        ("Pantheon",
                                ["the gods are wise, but do not know of the site which you seek"]),
    "zendesk.com":            ("Zendesk",
                                ["help center closed"]),
    "readme.io":              ("ReadMe",
                                ["the creators of this project are still working on making this readme better"]),
    "surge.sh":               ("Surge",
                                ["project not found"]),
    "bitbucket.io":           ("Bitbucket",
                                ["repository not found"]),
    "ghost.io":               ("Ghost",
                                ["domain error"]),
    "statuspage.io":          ("Statuspage",
                                ["you are being redirected"]),
    "wordpress.com":          ("WordPress",
                                ["do you want to register"]),
    "teamwork.com":           ("Teamwork",
                                ["oops - we didn't find your customer portal"]),
    "helpscout.net":          ("HelpScout",
                                ["no settings were found for this company"]),
    "unbounce.com":           ("Unbounce",
                                ["the requested url was not found on this server"]),
    "tumblr.com":             ("Tumblr",
                                ["there's nothing here"]),
    "wpengine.com":           ("WPEngine",
                                ["the site you were looking for couldn't be found"]),
    "smugmug.com":            ("SmugMug",
                                ["page not found"]),
    "pingdom.com":            ("Pingdom",
                                ["sorry, couldn't find the status page"]),
    "campaignmonitor.com":    ("Campaign Monitor",
                                ["trying to access your account?"]),
    "cargocollective.com":    ("Cargo",
                                ["404 not found"]),
    "feedpress.me":           ("FeedPress",
                                ["the feed has not been found"]),
    "freshdesk.com":          ("Freshdesk",
                                ["may be this is still fresh!"]),
    "uservoice.com":          ("UserVoice",
                                ["this uservoice subdomain is currently available"]),
    "intercom.help":          ("Intercom",
                                ["this page is reserved for artistic purposes"]),
    "kajabi.com":             ("Kajabi",
                                ["the page you were looking for doesn't exist"]),
    "launchrock.com":         ("LaunchRock",
                                ["the page you were looking for doesn't exist"]),
    "ngrok.io":               ("Ngrok",
                                ["ngrok.io not found"]),
    "proposify.com":          ("Proposify",
                                ["if you need immediate assistance"]),
    "simplebooklet.com":      ("Simplebooklet",
                                ["we can't find this simplebooklet"]),
    "smartling.com":          ("Smartling",
                                ["domain is not configured"]),
    "strikingly.com":         ("Strikingly",
                                ["but if you're looking for a site you can build"]),
    "wishpond.com":           ("Wishpond",
                                ["https://www.wishpond.com/404?campaign=true"]),
    "aftership.com":          ("AfterShip",
                                ["oops."]),
    "aha.io":                 ("Aha",
                                ["could not find that idea"]),
    "bitly.com":              ("Bitly",
                                ["bitly is temporarily unavailable"]),
    "brightcove.com":         ("Brightcove",
                                ["oops, looks like you've found a broken link"]),
    "bigcartel.com":          ("Big Cartel",
                                ["oops, this shop is currently unavailable"]),
    "desk.com":               ("Desk",
                                ["sorry, we couldn't find that page"]),
    "hatenablog.com":         ("HatenaBlog",
                                ["404 blog not found"]),
    "uberflip.com":           ("Uberflip",
                                ["non-hub domain"]),
    "firebaseapp.com":        ("Firebase",
                                ["404"]),
    "webflow.io":             ("Webflow",
                                ["the page you are looking for doesn't exist"]),
    "netlify.app":            ("Netlify",
                                ["not found"]),
    "vercel.app":             ("Vercel",
                                ["the deployment could not be found"]),
    "squarespace.com":        ("Squarespace",
                                ["no site found"]),
    "readthedocs.io":         ("ReadTheDocs",
                                ["404"]),
    "fly.io":                 ("Fly.io",
                                ["404"]),
    "onrender.com":           ("Render",
                                ["not found"]),
    "glitch.me":              ("Glitch",
                                ["project not found"]),
    "stackpathdns.com":       ("StackPath",
                                ["not found"]),
    "convertkit.com":         ("ConvertKit",
                                ["404"]),
    "tictail.com":            ("Tictail",
                                ["this shop is not available"]),
    "tave.com":               ("Tave",
                                ["you're being redirected"]),
    "uberflip.com":           ("Uberflip",
                                ["non-hub domain"]),
    "vendhq.com":             ("Vend",
                                ["404 not found"]),
    "kajabi.com":             ("Kajabi",
                                ["the page you were looking for doesn't exist"]),
}

# ─────────────────────────────────────────────────────────────────────
# Built-in vulnerability checks
# ─────────────────────────────────────────────────────────────────────

# Security headers — if missing, reported as a finding
SECURITY_HEADERS = {
    "Strict-Transport-Security": "Missing HSTS header — HTTPS downgrade possible",
    "Content-Security-Policy":   "Missing CSP header — XSS risk increased",
    "X-Frame-Options":           "Missing X-Frame-Options — clickjacking risk",
    "X-Content-Type-Options":    "Missing X-Content-Type-Options — MIME sniffing risk",
    "Referrer-Policy":           "Missing Referrer-Policy — referrer leakage",
    "Permissions-Policy":        "Missing Permissions-Policy — feature abuse risk",
}

# Files that should never be publicly reachable
SENSITIVE_PATHS = [
    "/.git/config",
    "/.git/HEAD",
    "/.env",
    "/.env.local",
    "/.env.production",
    "/.htaccess",
    "/.DS_Store",
    "/config.php.bak",
    "/wp-config.php.bak",
    "/backup.zip",
    "/backup.tar.gz",
    "/db.sql",
    "/dump.sql",
    "/phpinfo.php",
    "/server-status",
    "/server-info",
    "/.well-known/security.txt",
    "/crossdomain.xml",
    "/sitemap.xml",
]

# HTTP methods to probe with OPTIONS
HTTP_METHODS_TO_CHECK = ["OPTIONS", "TRACE"]

# ─────────────────────────────────────────────────────────────────────
# Geolocation
# ─────────────────────────────────────────────────────────────────────

GEO_API_URL   = "http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,isp,org,as,query"
GEO_RATE_PER_MIN = 45      # free tier of ip-api.com

# ─────────────────────────────────────────────────────────────────────
# Concurrency defaults (overridable via CLI flags)
# ─────────────────────────────────────────────────────────────────────

DEFAULT_PROBE_CONCURRENCY    = 100
DEFAULT_TAKEOVER_CONCURRENCY = 50
DEFAULT_PORT_WORKERS         = 10
DEFAULT_HTTP_TIMEOUT         = 8