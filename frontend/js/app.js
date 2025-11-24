// ========== CONFIGURATION ==========
const API_BASE_URL = 'http://localhost:8000/api';

// ========== STATE MANAGEMENT ==========
const appState = {
    currentCity: '',
    currentPage: 'dashboard',
    prices: [],
    recommendations: [],
    predictions: [],
    vegetables: [],
    savings: 0
};
// chart instances container
appState.charts = {};

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    loadInitialData();
}

// ========== EVENT LISTENERS ==========
function setupEventListeners() {
    // City selector
    const cityDropdown = document.getElementById('city-dropdown');
    cityDropdown.addEventListener('change', (e) => {
        appState.currentCity = e.target.value;
        if (appState.currentCity) {
            loadDashboardData();
        }
    });

    // Refresh button
    const refreshBtn = document.getElementById('refresh-btn');
    refreshBtn.addEventListener('click', () => {
        if (appState.currentCity) {
            loadDashboardData();
        }
    });

    // Global vegetable filter
    document.getElementById('global-veg-select')?.addEventListener('change', (e) => {
        const veg = e.target.value;
        appState.selectedVegetable = veg || '';
        // sync other selects
        const itemSelect = document.getElementById('item-select');
        if (itemSelect) itemSelect.value = veg || '';
        const predictionItem = document.getElementById('prediction-item');
        if (predictionItem) predictionItem.value = veg || '';

        // refresh currently visible page
        if (appState.currentCity) {
            switch (appState.currentPage) {
                case 'dashboard':
                    loadDashboardData();
                    break;
                case 'compare':
                    if (veg) loadComparisonData(veg);
                    break;
                case 'predictions':
                    if (veg) loadPredictionData(veg);
                    break;
                case 'insights':
                    loadInsightsData(document.getElementById('insight-month')?.value || 'January');
                    break;
            }
        }
    });

    // Navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = e.target.getAttribute('data-page');
            switchPage(page);
        });
    });

    // Page-specific selectors
    // item-select change will not auto-trigger comparison; user must click Apply
    document.getElementById('item-select')?.addEventListener('change', (e) => {
        // placeholder: selection changed
    });

    document.getElementById('prediction-item')?.addEventListener('change', (e) => {
        if (e.target.value && appState.currentCity) {
            loadPredictionData(e.target.value);
        }
    });

    document.getElementById('prediction-days')?.addEventListener('change', (e) => {
        const itemSelect = document.getElementById('prediction-item');
        if (itemSelect.value && appState.currentCity) {
            loadPredictionData(itemSelect.value);
        }
    });

    document.getElementById('insight-month')?.addEventListener('change', (e) => {
        if (appState.currentCity) {
            loadInsightsData(e.target.value);
        }
    });

    // Compare Apply button
    document.getElementById('compare-apply-btn')?.addEventListener('click', () => {
        const item = document.getElementById('item-select')?.value;
        if (!item) {
            showError('Please select an item to compare');
            return;
        }
        loadComparisonData(item);
    });

    // Report Price button (open modal)
    document.getElementById('report-price-btn')?.addEventListener('click', (ev) => {
        console.log('Report Price button clicked', ev);
        openSubmitModal();
    });

    // Modal cancel/close handlers
    document.getElementById('modal-cancel')?.addEventListener('click', () => {
        closeSubmitModal();
    });
    document.getElementById('modal-close')?.addEventListener('click', () => {
        closeSubmitModal();
    });
    document.getElementById('modal-overlay')?.addEventListener('click', () => {
        closeSubmitModal();
    });

    // Submit-price form
    document.getElementById('submit-price-form')?.addEventListener('submit', (e) => {
        e.preventDefault();
        submitPrice();
    });
}

// ========== PAGE SWITCHING ==========
function switchPage(pageName) {
    // Update active page
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    document.getElementById(pageName)?.classList.add('active');

    // Update active nav link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    document.querySelector(`[data-page="${pageName}"]`)?.classList.add('active');

    appState.currentPage = pageName;

    // Load page-specific data
    if (appState.currentCity) {
        switch (pageName) {
            case 'dashboard':
                loadDashboardData();
                break;
            case 'compare':
                loadComparePageData();
                break;
            case 'predictions':
                loadPredictionPageData();
                break;
            case 'insights':
                loadInsightsPageData();
                break;
        }
    }
}

// ========== DATA LOADING FUNCTIONS ==========
async function loadInitialData() {
    try {
        // Load vegetables list for dropdowns
        const response = await fetch(`${API_BASE_URL}/vegetables`);
        let vegetables = await response.json();
        // Handle paginated response from DRF
        if (vegetables.results) {
            vegetables = vegetables.results;
        }
        appState.vegetables = vegetables;
        populateVegetableSelects(vegetables);
        
        // Load cities for dropdowns
        try {
            const citiesResp = await fetch(`${API_BASE_URL}/cities`);
            let cities = await citiesResp.json();
            if (cities.results) cities = cities.results;
            appState.cities = cities;
            populateCityDropdown(cities);
            populateStateSelect(cities);
        } catch (err) {
            console.warn('Could not load cities:', err);
        }
    } catch (error) {
        console.error('Error loading vegetables:', error);
    }
}

async function loadDashboardData() {
    try {
        // Load current prices
        const pricesResponse = await fetch(
            `${API_BASE_URL}/current-prices?city=${appState.currentCity}`
        );
        const prices = await pricesResponse.json();
        // if API returns paginated DRF object, extract results
        let priceList = prices.results ? prices.results : prices;
        // apply vegetable filter client-side if set
        if (appState.selectedVegetable) {
            priceList = priceList.filter(p => p.vegetable_name === appState.selectedVegetable);
        }
        appState.prices = priceList;
        renderPrices(priceList);

        // Load recommendations
        const recsResponse = await fetch(
            `${API_BASE_URL}/recommendation?city=${appState.currentCity}`
        );
        let recommendations = await recsResponse.json();
        if (recommendations.results) recommendations = recommendations.results;
        if (appState.selectedVegetable) {
            recommendations = recommendations.filter(r => r.vegetable_name === appState.selectedVegetable);
        }
        appState.recommendations = recommendations;
        renderRecommendations(recommendations);

        // Load savings summary (insights requires city parameter)
        const savingsResponse = await fetch(
            `${API_BASE_URL}/insights?city=${appState.currentCity}&month=${new Date().toLocaleString('default', { month: 'long' })}`
        );
        const savings = await savingsResponse.json();
        renderSavings(savings);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showError('Failed to load dashboard data');
    }
}

async function loadComparePageData() {
    // Populate item select for comparison
    const itemSelect = document.getElementById('item-select');
    if (itemSelect && appState.vegetables.length > 0) {
        populateSelect(itemSelect, appState.vegetables);
    }
}

async function loadComparisonData(vegetableName) {
    try {
        // Build query parameters from filters
        const params = new URLSearchParams();
        params.append('item', vegetableName);
        const city = appState.currentCity;
        const state = document.getElementById('state-select')?.value;
        const startDate = document.getElementById('start-date')?.value;
        const endDate = document.getElementById('end-date')?.value;
        const sort = document.getElementById('sort-select')?.value;

        if (city) params.append('city', city);
        if (state) params.append('state', state);
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        if (sort) params.append('sort', sort);

        const url = `${API_BASE_URL}/comparison?${params.toString()}`;
        const response = await fetch(url);
        const comparisons = await response.json();
        renderComparison(comparisons);
    } catch (error) {
        console.error('Error loading comparison data:', error);
    }
}

async function loadPredictionPageData() {
    // Populate item select for predictions
    const itemSelect = document.getElementById('prediction-item');
    if (itemSelect && appState.vegetables.length > 0) {
        populateSelect(itemSelect, appState.vegetables);
    }
}

async function loadPredictionData(vegetableName) {
    try {
        const days = document.getElementById('prediction-days')?.value || 7;
        const response = await fetch(
            `${API_BASE_URL}/prediction?city=${appState.currentCity}&item=${vegetableName}&days=${days}`
        );
        let predictions = await response.json();
        // Handle paginated response from DRF
        if (predictions.results) {
            predictions = predictions.results;
        }
        appState.predictions = predictions;
        renderPredictionChart(predictions);
    } catch (error) {
        console.error('Error loading prediction data:', error);
    }
}

async function loadInsightsPageData() {
    const month = document.getElementById('insight-month')?.value || 'January';
    loadInsightsData(month);
}

async function loadInsightsData(month) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/insights?month=${month}&city=${appState.currentCity}`
        );
        const insights = await response.json();
        renderInsights(insights);
    } catch (error) {
        console.error('Error loading insights:', error);
    }
}

// ========== RENDER FUNCTIONS ==========
function renderPrices(prices) {
    const container = document.getElementById('prices-grid');
    container.innerHTML = '';

    if (!prices || prices.length === 0) {
        container.innerHTML = '<p class="text-center">No price data available</p>';
        return;
    }

    prices.forEach(price => {
        const card = createPriceCard(price);
        container.appendChild(card);
    });
}

function createPriceCard(price) {
    const card = document.createElement('div');
    card.className = 'price-card';
    
    const priceChange = price.price_change || 0;
    const changeIcon = priceChange > 0 ? '📈' : priceChange < 0 ? '📉' : '➡️';
    const changeColor = priceChange > 0 ? 'danger' : priceChange < 0 ? 'warning' : '';

    card.innerHTML = `
        <div class="card-header">
            <div>
                <div class="card-title">${price.vegetable_name}</div>
                <div class="card-meta">${price.source} • ${price.city}</div>
            </div>
            <div class="card-badge ${changeColor}">
                ${changeIcon} ${Math.abs(priceChange).toFixed(1)}%
            </div>
        </div>
        <div class="price-display">₹${price.price_per_kg.toFixed(2)}/kg</div>
        <div class="card-meta">
            Last updated: ${new Date(price.timestamp).toLocaleString()}
        </div>
    `;

    return card;
}

function renderRecommendations(recommendations) {
    const container = document.getElementById('recommendations-grid');
    container.innerHTML = '';

    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<p class="text-center">No recommendations available</p>';
        return;
    }

    recommendations.forEach(rec => {
        const card = createRecommendationCard(rec);
        container.appendChild(card);
    });
}

function createRecommendationCard(rec) {
    const card = document.createElement('div');
    const recClass = rec.action.toLowerCase() === 'wait' ? 'wait' : 'buy';
    card.className = `recommendation-card ${recClass}`;

    card.innerHTML = `
        <div class="rec-title">${rec.vegetable_name}</div>
        <div class="rec-advice">
            Current: ₹${rec.current_price.toFixed(2)}/kg<br>
            Predicted: ₹${rec.predicted_price.toFixed(2)}/kg
        </div>
        <div class="rec-advice">${rec.reason}</div>
        <div class="rec-action ${recClass}">
            ${rec.action.toUpperCase()} - Save ₹${rec.potential_savings.toFixed(2)}
        </div>
    `;

    return card;
}

function renderSavings(savings) {
    const container = document.getElementById('savings-summary');
    
    const totalSavings = savings.total_savings || 0;
    const itemsSaved = savings.items_saved || 0;

    container.innerHTML = `
        <div class="summary-amount">₹${totalSavings.toFixed(2)}</div>
        <div class="summary-text">Total savings this week</div>
        <div class="summary-text">By following recommendations on ${itemsSaved} items</div>
    `;
}

function renderComparison(comparisons) {
    const container = document.getElementById('comparison-grid');
    container.innerHTML = '';

    if (!comparisons || comparisons.length === 0) {
        container.innerHTML = '<p class="text-center">No comparison data available</p>';
        return;
    }

    let bestPrice = Math.min(...comparisons.map(c => c.price));

    comparisons.forEach(comp => {
        const isBest = comp.price === bestPrice;
        const card = document.createElement('div');
        card.className = `comparison-card ${isBest ? 'best' : ''}`;

        card.innerHTML = `
            <div class="comp-header">
                <div>
                    <div class="comp-source">${comp.source}</div>
                    <div class="comp-meta">${comp.location} • ${comp.city} • ${comp.date}</div>
                </div>
                ${isBest ? '<span class="best-tag">BEST</span>' : ''}
            </div>
            <div class="comp-price">₹${comp.price.toFixed(2)}</div>
            <div class="comp-meta">
                Difference: ${isBest ? '—' : '+₹' + (comp.price - bestPrice).toFixed(2)} • Quality: ${comp.quality_rating}
            </div>
        `;

        container.appendChild(card);
    });
}

function renderPredictionChart(predictions) {
    const container = document.getElementById('prediction-chart');
    container.innerHTML = '';

    if (!predictions || predictions.length === 0) {
        container.innerHTML = '<p class="text-center">No prediction data available</p>';
        return;
    }

    // Create a canvas for Chart.js
    const canvas = document.createElement('canvas');
    canvas.id = 'prediction-chart-canvas';
    container.appendChild(canvas);

    // Prepare data
    const labels = predictions.map(p => p.date);
    const data = predictions.map(p => p.predicted_price);

    // Destroy existing chart if present
    if (appState.charts.prediction) {
        try { appState.charts.prediction.destroy(); } catch (e) { /* ignore */ }
    }

    const ctx = canvas.getContext('2d');
    appState.charts.prediction = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Predicted Price (₹/kg)',
                data: data,
                borderColor: 'rgba(14,165,164,0.9)',
                backgroundColor: 'rgba(14,165,164,0.15)',
                tension: 0.25,
                fill: true,
                pointRadius: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true }
            },
            scales: {
                x: { display: true, title: { display: false } },
                y: { display: true, title: { display: { display: false } }, beginAtZero: false }
            }
        }
    });
}

function renderInsights(insights) {
    const container = document.getElementById('insights-container');
    container.innerHTML = '';

    if (!insights || insights.length === 0) {
        container.innerHTML = '<p class="text-center">No insights available</p>';
        return;
    }

    insights.forEach((insight, idx) => {
        const card = document.createElement('div');
        card.className = 'insight-card';

        // create a small canvas for min/avg/max bar chart
        const chartId = `insight-chart-${idx}`;
        card.innerHTML = `
            <div class="insight-title">${insight.item_name}</div>
            <div style="height:120px; margin-top:8px;"><canvas id="${chartId}"></canvas></div>
            <div class="insight-text mt-2">Min: ₹${insight.min_price.toFixed(2)} | Avg: ₹${insight.avg_price.toFixed(2)} | Max: ₹${insight.max_price.toFixed(2)}</div>
            <div class="insight-text mt-2">Trend: ${insight.trend > 0 ? '📈 Rising' : insight.trend < 0 ? '📉 Falling' : '➡️ Stable'}</div>
        `;

        container.appendChild(card);

        // render bar chart
        try {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Min', 'Avg', 'Max'],
                    datasets: [{
                        label: '₹/kg',
                        data: [insight.min_price, insight.avg_price, insight.max_price],
                        backgroundColor: ['#f87171', '#60a5fa', '#34d399']
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
            });
        } catch (e) {
            console.warn('Chart render failed for insight', e);
        }
    });
}

// ========== UTILITY FUNCTIONS ==========
function populateVegetableSelects(vegetables) {
    const selects = [
        document.getElementById('item-select'),
        document.getElementById('prediction-item'),
        document.getElementById('item-submit'),
        document.getElementById('global-veg-select')
    ];

    selects.forEach(select => {
        if (select) {
            populateSelect(select, vegetables);
        }
    });
}

function populateSelect(select, items) {
    const currentValue = select.value;
    select.innerHTML = '<option value="">Select Item</option>';

    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item.name;
        option.textContent = item.name;
        select.appendChild(option);
    });

    select.value = currentValue;
}

function populateCityDropdown(cities) {
    const cityDropdown = document.getElementById('city-dropdown');
    if (!cityDropdown) return;
    const current = cityDropdown.value;
    cityDropdown.innerHTML = '<option value="">Select City</option>';
    cities.forEach(c => {
        const option = document.createElement('option');
        option.value = c.name;
        option.textContent = c.name;
        cityDropdown.appendChild(option);
    });
    cityDropdown.value = current;

    // Also populate modal city selector if present
    const citySubmit = document.getElementById('city-submit');
    if (citySubmit) {
        const cur = citySubmit.value;
        citySubmit.innerHTML = '<option value="">Select City</option>';
        cities.forEach(c => {
            const option = document.createElement('option');
            option.value = c.name;
            option.textContent = c.name;
            citySubmit.appendChild(option);
        });
        citySubmit.value = cur;
    }
}

// ========== SUBMIT PRICE MODAL & ACTIONS ==========
function openSubmitModal() {
    const modal = document.getElementById('submit-price-modal');
    if (!modal) return;
    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden', 'false');
    // If vegetables already loaded, ensure modal select is populated
    const vegSelect = document.getElementById('item-submit');
    if (vegSelect && appState.vegetables && appState.vegetables.length > 0) {
        populateSelect(vegSelect, appState.vegetables);
    }
    // If cities are loaded, ensure city select populated
    const citySelect = document.getElementById('city-submit');
    if (citySelect && appState.cities && appState.cities.length > 0) {
        populateCityDropdown(appState.cities);
    }
    // Pre-select current city in modal if available
    try {
        const curCity = appState.currentCity || '';
        if (curCity) {
            const citySubmit = document.getElementById('city-submit');
            if (citySubmit) citySubmit.value = curCity;
        }
        // Pre-select global vegetable if set
        const curVeg = appState.selectedVegetable || '';
        if (curVeg) {
            const vegSubmit = document.getElementById('item-submit');
            if (vegSubmit) vegSubmit.value = curVeg;
            const globalSel = document.getElementById('global-veg-select');
            if (globalSel) globalSel.value = curVeg;
        }
    } catch (e) {
        console.warn('Could not preselect modal fields', e);
    }
}

function closeSubmitModal() {
    const modal = document.getElementById('submit-price-modal');
    if (!modal) return;
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
    // clear form
    const form = document.getElementById('submit-price-form');
    if (form) form.reset();
}

async function submitPrice() {
    const veg = document.getElementById('item-submit')?.value;
    const priceStr = document.getElementById('price-input')?.value;
    const city = document.getElementById('city-submit')?.value;
    const source = document.getElementById('source-input')?.value || 'User';
    const quality = parseInt(document.getElementById('quality-select')?.value || '3', 10);

    if (!veg) {
        showError('Please select an item');
        return;
    }
    if (!city) {
        showError('Please select a city');
        return;
    }
    const price_per_kg = parseFloat(priceStr);
    if (isNaN(price_per_kg) || price_per_kg <= 0) {
        showError('Please enter a valid price');
        return;
    }

    const payload = {
        vegetable_name: veg,
        city_name: city,
        price_per_kg: price_per_kg,
        source: source,
        quality_rating: quality
    };

    try {
        const resp = await fetch(`${API_BASE_URL}/submit-price/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!resp.ok) {
            const txt = await resp.text();
            let errMsg = 'Failed to submit price';
            try {
                const json = JSON.parse(txt);
                if (json.detail) errMsg = json.detail;
                else if (json.error) errMsg = json.error;
            } catch (e) {
                // ignore
            }
            showError(errMsg);
            return;
        }

        showSuccess('Price submitted — thank you!');
        closeSubmitModal();
        // Refresh dashboard if visible
        if (appState.currentCity) {
            loadDashboardData();
        }
    } catch (err) {
        console.error('Submit price error', err);
        showError('Network error submitting price');
    }
}

function populateStateSelect(cities) {
    const stateSelect = document.getElementById('state-select');
    if (!stateSelect) return;
    const states = Array.from(new Set(cities.map(c => c.state))).sort();
    stateSelect.innerHTML = '<option value="">Select State</option>';
    states.forEach(s => {
        const option = document.createElement('option');
        option.value = s;
        option.textContent = s;
        stateSelect.appendChild(option);
    });
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    
    const container = document.querySelector('.main-content');
    if (container.firstChild) {
        container.insertBefore(errorDiv, container.firstChild);
    } else {
        container.appendChild(errorDiv);
    }

    setTimeout(() => errorDiv.remove(), 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success';
    successDiv.textContent = message;
    
    const container = document.querySelector('.main-content');
    if (container.firstChild) {
        container.insertBefore(successDiv, container.firstChild);
    } else {
        container.appendChild(successDiv);
    }

    setTimeout(() => successDiv.remove(), 5000);
}

// ========== EXPORT FUNCTIONS FOR TESTING ==========
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadDashboardData,
        loadComparisonData,
        loadPredictionData,
        loadInsightsData,
        switchPage
    };
}
