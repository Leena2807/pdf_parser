const form = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const errorBox = document.getElementById("error");
const table = document.getElementById("resultTable");
const tbody = document.getElementById("resultBody");
const searchInput = document.getElementById("searchInput");
const toppersBtn = document.getElementById("loadToppers");
const toppersBox = document.getElementById("toppersBox");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.style.display = "none";
    tbody.innerHTML = "";
    table.style.display = "none";
    toppersBox.innerHTML = "";

    const files = fileInput.files;
    if (!files.length) return;

    const formData = new FormData();
    for (const file of files) formData.append("file", file);

    try {
        const res = await fetch("http://localhost:5000/add_pdf", { method: "POST", body: formData });
        // const data = await res.json();
        const raw = await res.text();
        console.log("RAW RESPONSE:", raw);
        const data = JSON.parse(raw);
        if (!res.ok) throw new Error(data.message || "Upload failed");
        if (!data.students || data.students.length === 0) throw new Error("No students extracted");

        data.students.forEach((s, index) => addRow(s, index));
        table.style.display = "table";
    } catch (err) {
        errorBox.textContent = err.message;
        errorBox.style.display = "block";
    }
});

function addRow(s, index) {
    const tr = document.createElement("tr");
    tr.style.animationDelay = `${index * 0.05}s`;
    tr.innerHTML = `
        <td style="font-weight: 700; color: #818cf8;">${s.seat_number}</td>
        <td style="color: #f8fafc; font-weight: 500;">${s.name}</td>
        <td><span style="font-family: monospace;">${s.sgpa_sem1 ?? "--"}</span></td>
        <td><span style="font-family: monospace;">${s.sgpa_sem2 ?? "--"}</span></td>
        <td><span class="${s.result === 'PASS' ? 'pass' : 'fail'}">${s.result}</span></td>
        <td style="color: var(--text-muted); font-size: 0.8rem;">${s.source_file}</td>
    `;
    tbody.appendChild(tr);
}

searchInput.addEventListener("input", async () => {
    const q = searchInput.value.trim();
    if (q.length === 0) return;
    try {
        const res = await fetch(`http://localhost:5000/search/${q}`);
        const data = await res.json();
        tbody.innerHTML = "";
        if (data.length > 0) {
            data.forEach((s, i) => addRow(s, i));
            table.style.display = "table";
        } else {
            table.style.display = "none";
        }
    } catch (e) { console.error(e); }
});

toppersBtn.addEventListener("click", async () => {
    try {
        const res = await fetch("http://localhost:5000/toppers");
        const data = await res.json();
        toppersBox.innerHTML = "";
        data.forEach((s, i) => {
            const score = s.sgpa_sem2 || s.sgpa_sem1 || "0.00";
            toppersBox.innerHTML += `
                <div class="topper-card" style="animation-delay: ${i * 0.1}s">
                    <div class="rank-indicator rank-${i + 1}">${i + 1}</div>
                    <div class="topper-info">
                        <h4>${s.name}</h4>
                        <p>Seat: ${s.seat_number}</p>
                    </div>
                    <div class="topper-score">
                        <span class="score-label">SGPA</span>
                        <span class="score-value">${score}</span>
                    </div>
                </div>
            `;
        });
    } catch (e) { console.error("Could not load toppers"); }
});