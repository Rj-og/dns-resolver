document.addEventListener("DOMContentLoaded", function () {
    const resolveBtn = document.getElementById("resolve-btn");
    const domainInput = document.getElementById("domain-input");
    const recordTypeSelect = document.getElementById("record-type");
    const dnsServerSelect = document.getElementById("dns-server");
    const reverseToggle = document.getElementById("reverse-toggle");
    const resultContainer = document.getElementById("results");

    resolveBtn.addEventListener("click", function () {
        const domain = domainInput.value.trim();
        const recordType = recordTypeSelect.value;
        const dnsServer = dnsServerSelect.value;
        const isReverse = reverseToggle.checked;

        if (domain === "") {
            alert("Please enter a domain or IP.");
            return;
        }

        const url = `/resolve?domain=${domain}&record_type=${recordType}&dns_server=${dnsServer}&reverse=${isReverse}`;

        const startTime = performance.now();

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const endTime = performance.now();
                const actualTime = (endTime - startTime).toFixed(2);

                if (data.error) {
                    resultContainer.innerHTML = `<div class="result-box show">❌ ${data.error}</div>`;
                } else {
                    displayResults(data, actualTime);
                }
            })
            .catch(error => {
                console.error("Error fetching DNS data:", error);
                resultContainer.innerHTML = `<div class="result-box show">❌ Error resolving DNS.</div>`;
            });
    });

    function displayResults(data, actualTime) {
        resultContainer.innerHTML = "";

        addResult(`🌐 Domain: ${data.domain}`);
        addArrow();
        addResult(`🧾 Record Type: ${data.record_type}`);
        addArrow();

        if (data.results.length > 0) {
            data.results.forEach(record => {
                addResult(`📦 ${data.record_type} Record: ${record}`);
                addArrow();
            });
        } else {
            addResult(`❌ No records found for ${data.record_type}`);
            addArrow();
        }

        addResult(`📊 Total Records: ${data.total_records}`);
        addArrow();
        addResult(`⏱️ Response Time: ${data.response_time} ms`);
        addArrow();
        addResult(`🛰️ DNS Server Used: ${data.dns_server}`);
        addArrow();

        if (data.organization) {
            addResult(`🏢 Organization: ${data.organization}`);
            addArrow();
        }

        const hexDumpDiv = document.createElement("div");
        hexDumpDiv.classList.add("result-box", "hex-dump", "show");
        hexDumpDiv.textContent = `📜 Raw DNS Hex Dump:\n${data.hex_dump}`;
        resultContainer.appendChild(hexDumpDiv);
    }

    function addResult(text) {
        const div = document.createElement("div");
        div.classList.add("result-box", "show");
        div.textContent = text;

        div.addEventListener("click", () => {
            div.classList.toggle("collapsed");
            if (div.style.whiteSpace === "nowrap") {
                div.style.whiteSpace = "normal";
            } else {
                div.style.whiteSpace = "nowrap";
                div.style.overflow = "hidden";
                div.style.textOverflow = "ellipsis";
            }
        });

        resultContainer.appendChild(div);
    }

    function addArrow() {
        const arrow = document.createElement("div");
        arrow.classList.add("arrow", "show");
        arrow.textContent = "↓";
        resultContainer.appendChild(arrow);
    }

    // Theme toggle
    const themeToggle = document.querySelector(".theme-toggle");
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        themeToggle.textContent = document.body.classList.contains("dark") ? "🌙" : "🌞";
    });
});
