// API Configuration
const API_BASE = window.location.origin;

// State
let currentTask = null;
let environmentReady = false;

// DOM Elements
const taskButtons = document.querySelectorAll('.task-btn');
const actionButtons = document.querySelectorAll('.action-btn');
const baselineButtons = document.querySelectorAll('.baseline-btn');
const situationEl = document.getElementById('situation');
const goalEl = document.getElementById('goal');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const totalRewardEl = document.getElementById('total-reward');
const historyContainer = document.getElementById('history-container');
const stepInfoEl = document.getElementById('step-info');
const baselineResults = document.getElementById('baseline-results');
const apiStatus = document.getElementById('api-status');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('AI Life Decision Assistant initialized');
    checkAPIHealth();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Task selection
    taskButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const task = btn.dataset.task;
            resetEnvironment(task);
        });
    });
    
    // Actions
    actionButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            takeAction(action);
        });
    });
    
    // Baseline
    baselineButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const task = btn.dataset.task;
            runBaseline(task);
        });
    });
}

// API Functions
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            apiStatus.textContent = '● API Ready';
            apiStatus.style.color = '#10b981';
        } else {
            apiStatus.textContent = '● API Error';
            apiStatus.style.color = '#ef4444';
        }
    } catch (error) {
        console.error('Health check failed:', error);
        apiStatus.textContent = '● API Offline';
        apiStatus.style.color = '#ef4444';
    }
}

async function resetEnvironment(task) {
    try {
        console.log(`Resetting environment with task: ${task}`);
        
        const response = await fetch(`${API_BASE}/reset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task })
        });
        
        const data = await response.json();
        const observation = data.observation;
        
        // Update UI
        currentTask = task;
        environmentReady = true;
        
        situationEl.textContent = observation.situation;
        goalEl.textContent = observation.goal;
        updateProgress(observation.progress);
        totalRewardEl.textContent = '0.00';
        
        // Clear history
        historyContainer.innerHTML = '<p class="empty-message">No actions taken yet.</p>';
        
        // Reset action buttons
        actionButtons.forEach(btn => {
            btn.classList.remove('completed');
            btn.disabled = false;
        });
        
        // Clear step info
        stepInfoEl.innerHTML = '<p class="empty-message">Environment reset. Take an action to begin.</p>';
        
        // Highlight selected task
        taskButtons.forEach(btn => {
            if (btn.dataset.task === task) {
                btn.style.opacity = '1';
            } else {
                btn.style.opacity = '0.7';
            }
        });
        
        console.log('Environment reset successfully');
        
    } catch (error) {
        console.error('Reset failed:', error);
        alert('Failed to reset environment. Please try again.');
    }
}

async function takeAction(action) {
    if (!environmentReady) {
        alert('Please select a task first!');
        return;
    }
    
    try {
        console.log(`Taking action: ${action}`);
        
        const response = await fetch(`${API_BASE}/step`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action })
        });
        
        const data = await response.json();
        
        // Update observation
        updateObservation(data.observation);
        
        // Update reward
        updateReward(data.reward);
        
        // Add to history
        addToHistory(action, data.reward);
        
        // Update step info
        updateStepInfo(data);
        
        // Mark action as completed
        const actionBtn = document.querySelector(`[data-action="${action}"]`);
        if (actionBtn) {
            actionBtn.classList.add('completed');
        }
        
        // Check if done
        if (data.done) {
            handleEpisodeEnd(data);
        }
        
    } catch (error) {
        console.error('Action failed:', error);
        alert('Failed to execute action. Please try again.');
    }
}

async function runBaseline(task) {
    try {
        console.log(`Running baseline on ${task} task`);
        
        baselineResults.innerHTML = '<p>Running baseline agent...</p>';
        
        const response = await fetch(`${API_BASE}/baseline`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task })
        });
        
        const data = await response.json();
        
        // Display results
        displayBaselineResults(data);
        
    } catch (error) {
        console.error('Baseline failed:', error);
        baselineResults.innerHTML = '<p style="color: var(--danger-color);">Baseline execution failed.</p>';
    }
}

// UI Update Functions
function updateObservation(observation) {
    situationEl.textContent = observation.situation;
    goalEl.textContent = observation.goal;
    updateProgress(observation.progress);
}

function updateProgress(progress) {
    const percentage = Math.round(progress * 100);
    progressFill.style.width = `${percentage}%`;
    progressText.textContent = `${percentage}%`;
}

function updateReward(reward) {
    const currentReward = parseFloat(totalRewardEl.textContent);
    const newReward = currentReward + reward;
    totalRewardEl.textContent = newReward.toFixed(2);
    
    // Color coding
    if (newReward >= 0.8) {
        totalRewardEl.style.background = '#10b981';
    } else if (newReward >= 0.5) {
        totalRewardEl.style.background = '#f59e0b';
    } else {
        totalRewardEl.style.background = '#6366f1';
    }
}

function addToHistory(action, reward) {
    if (historyContainer.querySelector('.empty-message')) {
        historyContainer.innerHTML = '';
    }
    
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    
    const rewardClass = reward >= 0 ? '' : 'negative';
    
    historyItem.innerHTML = `
        <span class="history-action">${formatAction(action)}</span>
        <span class="history-reward ${rewardClass}">+${reward.toFixed(2)}</span>
    `;
    
    historyContainer.appendChild(historyItem);
    historyContainer.scrollTop = historyContainer.scrollHeight;
}

function updateStepInfo(data) {
    stepInfoEl.innerHTML = `
        <div class="info-item">
            <strong>Last Action:</strong>
            ${formatAction(data.observation.history[data.observation.history.length - 1])}
        </div>
        <div class="info-item">
            <strong>Reward:</strong>
            ${data.reward.toFixed(2)}
        </div>
        <div class="info-item">
            <strong>Done:</strong>
            ${data.done ? 'Yes ✅' : 'No'}
        </div>
        <div class="info-item">
            <strong>Steps Taken:</strong>
            ${data.info.step}
        </div>
        <div class="info-item">
            <strong>Total Reward:</strong>
            ${data.info.total_reward.toFixed(2)}
        </div>
    `;
}

function handleEpisodeEnd(data) {
    actionButtons.forEach(btn => btn.disabled = true);
    
    const totalReward = data.info.total_reward;
    let message = '';
    
    if (totalReward >= 0.9) {
        message = '🎉 Excellent! Perfect decision-making process!';
    } else if (totalReward >= 0.7) {
        message = '✅ Good job! Solid decision analysis.';
    } else if (totalReward >= 0.5) {
        message = '👍 Decent effort. Room for improvement.';
    } else {
        message = '📚 Keep learning! Try the complete process.';
    }
    
    stepInfoEl.innerHTML += `
        <div class="info-item" style="background: var(--primary-color); color: white; text-align: center; font-weight: bold; font-size: 1.1rem; margin-top: 1rem;">
            ${message}
        </div>
    `;
}

function displayBaselineResults(data) {
    let html = `
        <div style="margin-bottom: 1rem;">
            <h3 style="color: var(--primary-color); margin-bottom: 0.5rem;">Baseline Results: ${data.task.toUpperCase()} Task</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">Total Reward</div>
                    <div style="color: var(--success-color); font-size: 1.5rem; font-weight: bold;">${data.total_reward.toFixed(2)}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">Steps</div>
                    <div style="color: var(--primary-color); font-size: 1.5rem; font-weight: bold;">${data.steps}</div>
                </div>
            </div>
        </div>
        <div class="baseline-trajectory">
            <strong style="display: block; margin-bottom: 0.5rem; color: var(--text-primary);">Action Trajectory:</strong>
    `;
    
    data.trajectory.forEach(step => {
        html += `
            <div class="trajectory-step">
                <span>Step ${step.step}: ${formatAction(step.action)}</span>
                <span style="background: var(--success-color); color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.85rem;">
                    +${step.reward.toFixed(2)}
                </span>
            </div>
        `;
    });
    
    html += '</div>';
    
    baselineResults.innerHTML = html;
}

// Utility Functions
function formatAction(action) {
    return action
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

// Auto-refresh state
setInterval(async () => {
    if (environmentReady) {
        try {
            const response = await fetch(`${API_BASE}/state`);
            const data = await response.json();
            
            if (data.state && data.state.progress !== undefined) {
                updateProgress(data.state.progress);
            }
        } catch (error) {
            // Silently fail
        }
    }
}, 5000);