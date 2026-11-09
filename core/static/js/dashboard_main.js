document.addEventListener("DOMContentLoaded", function () {
    initKpiCountUp();
    initCharts();
    initRangeControls();
});

/* ============================
   KPI COUNT-UP ANIMATION
   ============================ */
function initKpiCountUp() {
    const kpiElements = document.querySelectorAll(".kpi-value");

    kpiElements.forEach(el => {
        const target = parseFloat(el.dataset.target || "0");
        const duration = 800;
        const start = performance.now();

        function animate(now) {
            const progress = Math.min((now - start) / duration, 1);
            const value = target * progress;
            el.textContent = value.toLocaleString("en-US");
            if (progress < 1) requestAnimationFrame(animate);
        }

        requestAnimationFrame(animate);
    });
}

/* ============================
   CHARTS INITIALIZATION
   ============================ */
function initCharts() {
    if (!window.dashboardData) {
        console.warn("dashboardData missing");
        return;
    }

    const salesPurchases = window.dashboardData.salesPurchases || null;
    const cashFlow = window.dashboardData.cashFlow || null;

    if (!salesPurchases || !salesPurchases.labels) {
        console.warn("salesPurchases data missing or invalid");
        return;
    }

    const salesCtx = document.getElementById("chartSalesPurchases");
    if (salesCtx) {
        const salesChartConfig = buildSalesChartConfig(salesPurchases, "month");
        window.salesChart = new Chart(salesCtx, salesChartConfig);
    }

    if (!cashFlow || !cashFlow.labels) {
        console.warn("cashFlow data missing or invalid");
        return;
    }

    const cashCtx = document.getElementById("chartCashFlow");
    if (cashCtx) {
        const cashChartConfig = buildCashChartConfig(cashFlow, "month");
        window.cashChart = new Chart(cashCtx, cashChartConfig);
    }
}

function initRangeControls() {
    const selects = document.querySelectorAll(".chart-range-select");

    selects.forEach(select => {
        select.addEventListener("change", function () {
            const range = this.value || "month";
            const chartId = this.id;

            if (chartId === "range-sales-purchases") {
                if (window.salesChart) {
                    window.salesChart.destroy();
                }
                const config = buildSalesChartConfig(window.dashboardData.salesPurchases, range);
                window.salesChart = new Chart(document.getElementById("chartSalesPurchases"), config);
            }

            if (chartId === "range-cash-flow") {
                if (window.cashChart) {
                    window.cashChart.destroy();
                }
                const config = buildCashChartConfig(window.dashboardData.cashFlow, range);
                window.cashChart = new Chart(document.getElementById("chartCashFlow"), config);
            }
        });
    });
}

function buildSalesChartConfig(data, range) {
    const labels = [...(data.labels || [])];
    const sliceSize = range === "quarter" ? 3 : range === "year" ? labels.length : Math.min(6, labels.length);
    const slicedLabels = labels.slice(-sliceSize);

    return {
        type: "line",
        data: {
            labels: slicedLabels,
            datasets: [
                {
                    label: "Sales",
                    data: (data.sales || []).slice(-sliceSize),
                    borderColor: "#2563eb",
                    backgroundColor: "rgba(37, 99, 235, 0.08)",
                    tension: 0.3,
                    fill: true
                },
                {
                    label: "Purchases",
                    data: (data.purchases || []).slice(-sliceSize),
                    borderColor: "#f97316",
                    backgroundColor: "rgba(249, 115, 22, 0.06)",
                    tension: 0.3,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true }
            }
        }
    };
}

function buildCashChartConfig(data, range) {
    const labels = [...(data.labels || [])];
    const sliceSize = range === "quarter" ? 3 : range === "year" ? labels.length : Math.min(6, labels.length);
    const slicedLabels = labels.slice(-sliceSize);
    const values = (data.values || []).slice(-sliceSize);

    return {
        type: "bar",
        data: {
            labels: slicedLabels,
            datasets: [
                {
                    label: "Cash Flow",
                    data: values,
                    backgroundColor: values.map(value => value >= 0 ? "#16a34a" : "#dc2626"),
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    };
}
