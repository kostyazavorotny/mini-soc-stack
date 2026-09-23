import requests
import time
import re

OPENSEARCH_URL = "http://opensearch:9200/_search"

ATTACK_PATTERNS = {
    "SQL Injection": r"(?i)(union.*select|select.*from|exec\(|drop.*table|'OR'1'='1)",
    "Path Traversal / LFI": r"(\.\./\.\./|\.\.\\\.\.\\|/etc/passwd)",
    "Web Scanner (Nikto/Nmap)": r"(?i)(nikto|nmap|sqlmap|masscan)"
}

def log_msg(msg):
    print(msg, flush=True)

def extract_ip(log_text):
    ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log_text)
    return ip_match.group(0) if ip_match else "Unknown"

def query_logs():
    query = {
        "size": 50,
        "query": {
            "match_all": {}
        }
    }
    
    try:
        response = requests.post(OPENSEARCH_URL, json=query, timeout=5)
        if response.status_code == 200:
            hits = response.json().get('hits', {}).get('hits', [])
            if not hits:
                log_msg("[*] логи пока не дошли")
                return
            
            log_msg(f"[*] Найдено логов: {len(hits)} шт.")
            
            for hit in hits:
                source_dict = hit.get('_source', {})
                log_text = source_dict.get('message', str(source_dict))
                
                for attack_type, pattern in ATTACK_PATTERNS.items():
                    if re.search(pattern, log_text):
                        source_ip = extract_ip(log_text)
                        
                        log_msg(f"\n[!!!!SECURITY ALERT] {attack_type} Detected!")
                        log_msg(f"  ├─ Source IP: {source_ip}")
                        log_msg(f"  └─ Payload: {log_text[:200]}")
                        break 
        else:
            log_msg(f"[!] Ошибка БД (код {response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        log_msg(f"[!] Ошибка подключения к базе: {e}")

if __name__ == "__main__":
    log_msg("[*] SOC Detector запущен. Начинаем мониторинг")
    time.sleep(5)
    while True:
        query_logs()
        time.sleep(5)
