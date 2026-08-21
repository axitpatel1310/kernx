/**
 * KernxTech Dashboard Interactivity
 */

// Filter system architectures in real-time
function filterArchitectures() {
    const input = document.getElementById('arch-search').value.toLowerCase();
    const cards = document.querySelectorAll('.arch-card');

    cards.forEach(card => {
        const name = card.getAttribute('data-name');
        if (name && name.includes(input)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

// Open Delete Confirmation Modal
function openDeleteModal(deleteUrl, archName) {
    const modal = document.getElementById('deleteModal');
    const targetName = document.getElementById('deleteTargetName');
    const confirmBtn = document.getElementById('confirmDeleteBtn');

    if (targetName) {
        targetName.textContent = archName;
    }
    if (confirmBtn) {
        confirmBtn.setAttribute('href', deleteUrl);
    }
    if (modal) {
        modal.classList.add('active');
    }
}

// Close Delete Confirmation Modal
function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking outside the card
window.addEventListener('click', (e) => {
    const modal = document.getElementById('deleteModal');
    if (e.target === modal) {
        closeDeleteModal();
    }
});

// Close modal with Escape key
window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeDeleteModal();
    }
});


const activityData =
    JSON.parse(
        document.getElementById("activity-data").textContent
    );

const svg = document.getElementById("activityGraph");

const CELL_SIZE = 14;
const GAP = 4;

const DAYS = 7;
const WEEKS = 53;

const width =
    WEEKS * (CELL_SIZE + GAP);

const height =
    DAYS * (CELL_SIZE + GAP);

svg.setAttribute("viewBox", `0 0 ${width} ${height}`);

function getLevel(count) {

    if (count === 0) {
        return 0;
    }

    if (count <= 2) {
        return 1;
    }

    if (count <= 5) {
        return 2;
    }

    if (count <= 9) {
        return 3;
    }

    return 4;
}


function createCell(x, y, count, date) {

    const rect =
        document.createElementNS(
            "http://www.w3.org/2000/svg",
            "rect"
        );

    rect.setAttribute(
        "x",
        x * (CELL_SIZE + GAP)
    );

    rect.setAttribute(
        "y",
        y * (CELL_SIZE + GAP)
    );

    rect.setAttribute(
        "width",
        CELL_SIZE
    );

    rect.setAttribute(
        "height",
        CELL_SIZE
    );

    rect.setAttribute(
        "rx",
        3
    );

    rect.dataset.level =
        getLevel(count);

    rect.dataset.date =
        date;

    rect.dataset.count =
        count;

    svg.appendChild(rect);
}


const today = new Date();

for (let week = 0; week < WEEKS; week++) {

    for (let day = 0; day < DAYS; day++) {

        const date =
            new Date(today);

        date.setDate(
            today.getDate()
            - ((WEEKS - 1 - week) * 7)
            - today.getDay()
            + day
        );

        const dateString =
            date.toISOString().split("T")[0];

        const count =
            activityData[dateString] || 0;

        createCell(
            week,
            day,
            count,
            dateString
        );
    }
}
