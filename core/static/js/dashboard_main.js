document.addEventListener("DOMContentLoaded", function () {
    initKpiCountUp();
    initCharts();
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

    /* -----------------------------
       SALES VS PURCHASES
       ----------------------------- */
    const salesPurchases = window.dashboardData.salesPurchases || null;

    if (!salesPurchases || !salesPurchases.labels) {
        console.warn("salesPurchases data missing or invalid");
        return;
    }

    const salesPurchasesCtx = document.getElementById("chartSalesPurchases");

    if (salesPurchasesCtx) {
        new Chart(salesPurchasesCtx, {
            type: "line",
            data: {
                labels: salesPurchases.labels,
                datasets: [
                    {
                        label: "Sales",
                        data: salesPurchases.sales,
                        borderColor: "#2563eb",
                        tension: 0.3
                    },
                    {
                        label: "Purchases",
                        data: salesPurchases.purchases,
                        borderColor: "#f97316",
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    /* -----------------------------
       CASH FLOW
       ----------------------------- */
    const cashFlow = window.dashboardData.cashFlow || null;

    if (!cashFlow || !cashFlow.labels) {
        console.warn("cashFlow data missing or invalid");
        return;
    }

    const cashFlowCtx = document.getElementById("chartCashFlow");

    if (cashFlowCtx) {
        new Chart(cashFlowCtx, {
            type: "bar",
            data: {
                labels: cashFlow.labels,
                datasets: [
                    {
                        label: "Cash Flow",
                        data: cashFlow.values,
                        backgroundColor: ctx => ctx.raw >= 0 ? "green" : "red"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}
