import dns.resolver
import dns.reversename
import time

# Mapping from known IPs to PTR record and organization
IP_TO_ORG = {
    "8.8.8.8": ("dns.google.", "Google DNS"),
    "1.1.1.1": ("one.one.one.one.", "Cloudflare"),
    "9.9.9.9": ("dns9.quad9.net.", "Quad9 DNS"),
    "142.250.64.110": ("lga34s31-in-f14.1e100.net.", "Google"),
    "151.101.1.69": ("151.101.1.69", "Fastly CDN"),
    "172.217.16.195": ("maa03s23-in-f3.1e100.net.", "Google"),
    "185.199.108.153": ("185.199.108.153", "GitHub Pages"),
    "142.250.72.14": ("", "Google"),
    "142.250.191.78": ("", "Google"),
    "157.240.229.35": ("", "Facebook / Meta"),
    "142.250.189.14": ("", "YouTube / Google"),
    "104.16.133.229": ("", "Cloudflare"),
    "104.16.132.229": ("", "Cloudflare"),
    "104.22.9.190": ("", "OpenAI / Cloudflare"),
    "104.22.8.190": ("", "OpenAI / Cloudflare"),
    "140.82.121.4": ("", "GitHub"),
    "52.45.61.146": ("", "Netflix / AWS"),
    "3.226.71.26": ("", "Epic Games / AWS"),
    "34.195.126.236": ("", "Epic Games / AWS"),
    "3.235.105.133": ("", "Amazon AWS"),
    "40.90.189.241": ("", "Microsoft / Outlook"),
    "151.101.0.81": ("", "Fastly"),
    "185.60.216.35": ("", "Facebook"),
    "172.217.160.78": ("", "Google"),
    "204.79.197.200": ("", "Microsoft / Bing"),
    "151.101.192.223": ("", "Reddit / Fastly"),
    "151.101.129.140": ("", "Stack Overflow / Fastly"),
    "104.244.42.1": ("", "Twitter / X Corp"),
    "13.107.246.10": ("", "Microsoft"),
    "192.30.255.112": ("", "GitHub"),
}

def get_organization_from_ip(ip_address):
    """Return known PTR and org name from IP, if available."""
    return IP_TO_ORG.get(ip_address, (None, None))

def get_organization_from_hostname(hostname):
    """Guess organization from PTR hostname (reverse lookup)."""
    hostname = hostname.lower()
    if "google" in hostname or "1e100" in hostname:
        return "Google"
    elif "cloudflare" in hostname or "one.one.one" in hostname:
        return "Cloudflare"
    elif "quad9" in hostname:
        return "Quad9"
    elif "fastly" in hostname:
        return "Fastly"
    elif "github" in hostname:
        return "GitHub"
    elif "amazonaws" in hostname:
        return "Amazon AWS"
    elif "microsoft" in hostname or "azure" in hostname:
        return "Microsoft / Azure"
    elif "akamai" in hostname:
        return "Akamai"
    elif "netflix" in hostname:
        return "Netflix"
    elif "facebook" in hostname or "meta" in hostname:
        return "Facebook / Meta"
    elif "openai" in hostname:
        return "OpenAI"
    elif "twitter" in hostname or "x.com" in hostname:
        return "Twitter / X"
    elif "reddit" in hostname:
        return "Reddit"
    elif "bing" in hostname:
        return "Microsoft / Bing"
    elif "epicgames" in hostname:
        return "Epic Games"
    else:
        return "Unknown"

def resolve_dns(domain, record_type, dns_server, reverse=False):
    """Resolves a domain or IP (for reverse lookup) using specified DNS server."""
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]

        start_time = time.time()

        if reverse:
            rev_name = dns.reversename.from_address(domain)
            answers = resolver.resolve(rev_name, 'PTR')
            record_type = "PTR"
            hostname = answers[0].to_text().strip('.')

            # Known IP match
            _, organization = get_organization_from_ip(domain)
            if not organization:
                # Try guessing from PTR hostname
                organization = get_organization_from_hostname(hostname)

            return {
                "domain": domain,
                "record_type": record_type,
                "results": [hostname],
                "organization": organization,
                "hex_dump": answers.response.to_wire().hex(),
                "dns_server": dns_server,
                "response_time": round((time.time() - start_time) * 1000, 2),
                "total_records": len(answers)
            }

        # Normal forward lookup
        answers = resolver.resolve(domain, record_type)
        records = [rdata.to_text() for rdata in answers]
        hex_dump = answers.response.to_wire().hex()

        return {
            "domain": domain,
            "record_type": record_type,
            "results": records,
            "organization": None,
            "hex_dump": hex_dump,
            "dns_server": dns_server,
            "response_time": round((time.time() - start_time) * 1000, 2),
            "total_records": len(records)
        }

    except Exception as e:
        return {"error": str(e)}
