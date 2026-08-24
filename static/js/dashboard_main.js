document.addEventListener("DOMContentLoaded", function () {
    initKpiCountUp();
    initCharts();
});

function initKpiCountUp() {
    const kpiElements = document.querySelectorAll(".kpi-value");

    kpiElements.forEach(el => {
        const target = parseFloat(el.dataset.target || "0");
        const duration = 800; // ms
        const start = performance.now();

        function animate(now) {
            const progress = Math.min((now - start) / duration, 1);
            const value = target * progress;
            el.textContent = formatNumber(value);
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }

        requestAnimationFrame(animate);
    });
}

function formatNumber(value) {
    return value.toLocaleString("en-US", {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });
}

function initCharts() {
    const salesPurchasesCtx = document.getElementById("chartSalesPurchases");
    const cashFlowCtx = document.getElementById("chartCashFlow");

    if (salesPurchasesCtx) {
        new Chart(salesPurchasesCtx, {
            type: "line",
            data: {
                labels: window.dashboardData?.salesPurchases?.labels || [],
                datasets: [
                    {
                        label: "Sales",
                        data: window.dashboardData?.salesPurchases?.sales || [],
                        borderColor: "#2563eb",
                        backgroundColor: "rgba(37, 99, 235, 0.1)",
                        tension: 0.3
                    },
                    {
                        label: "Purchases",
                        data: window.dashboardData?.salesPurchases?.purchases || [],
                        borderColor: "#f97316",
                        backgroundColor: "rgba(249, 115, 22, 0.1)",
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                },
                scales: {
                    x: {
                        grid: { display: false }
                    },
                    y: {
                        grid: { color: "#e5e7eb" }
                    }
                }
            }
        });
    }

    if (cashFlowCtx) {
        new Chart(cashFlowCtx, {
            type: "bar",
            data: {
                labels: window.dashboardData?.cashFlow?.labels || [],
                datasets: [
                    {
                        label: "Cash Flow",
                        data: window.dashboardData?.cashFlow?.values || [],
                        backgroundColor: (ctx) => {
                            const value = ctx.raw || 0;
                            return value >= 0 ? "rgba(34, 197, 94, 0.7)" : "rgba(239, 68, 68, 0.7)";
                        }
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { display: false }
                    },
                    y: {
                        grid: { color: "#e5e7eb" }
                    }
                }
            }
        });
    }
}
