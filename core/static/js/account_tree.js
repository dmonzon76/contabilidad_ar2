document.addEventListener("DOMContentLoaded", () => {

    const toggles = document.querySelectorAll(".erp-tree-toggle");

    toggles.forEach(toggle => {
        toggle.addEventListener("click", () => {
            const nodeId = toggle.getAttribute("data-toggle");
            const children = document.querySelector(`ul[data-parent='${nodeId}']`);

            if (!children) return;

            const isHidden = children.style.display === "none";

            children.style.display = isHidden ? "block" : "none";
            toggle.textContent = isHidden ? "▼" : "▶";
        });
    });

});
