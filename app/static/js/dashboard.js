/**
 * Dynamic Dashboard Visualizations powered by Chart.js
 */

document.addEventListener('DOMContentLoaded', () => {
    initDashboardCharts();
});

async function initDashboardCharts() {
    try {
        const response = await fetch('/dashboard/api/chart-data');
        if (!response.ok) return;

        const data = await response.json();

        // 1. Radar Chart: Skill Gap Analysis vs Target Role
        const radarCtx = document.getElementById('skillsRadarChart');
        if (radarCtx && data.skills_radar) {
            new Chart(radarCtx, {
                type: 'radar',
                data: data.skills_radar,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            pointLabels: { color: '#94a3b8', font: { family: 'Inter', size: 12 } },
                            ticks: { display: false, max: 100 }
                        }
                    },
                    plugins: {
                        legend: { labels: { color: '#f8fafc', font: { family: 'Inter' } } }
                    }
                }
            });
        }

        // 2. Line Chart: Weekly Mock Interview Score Progress
        const lineCtx = document.getElementById('scoreHistoryChart');
        if (lineCtx && data.score_history) {
            new Chart(lineCtx, {
                type: 'line',
                data: {
                    labels: data.score_history.labels,
                    datasets: [{
                        label: 'Interview Readiness Score',
                        data: data.score_history.scores,
                        fill: true,
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.15)',
                        borderWidth: 3,
                        tension: 0.4,
                        pointBackgroundColor: '#ec4899',
                        pointRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' }, min: 50, max: 100 }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }

    } catch (err) {
        console.error('Failed to load dashboard chart data:', err);
    }
}
