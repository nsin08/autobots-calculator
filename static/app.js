let currentInput = '0';
let operator = null;
let previousValue = null;
let waitingForOperand = false;
let isScientificMode = false;
let angleMode = 'DEG'; // 'DEG' or 'RAD'
let isHistoryVisible = false;
let calculationHistory = [];
const MAX_HISTORY = 20;
let previousDisplay = '';

const display = document.getElementById('display');
const previousDisplayElement = document.getElementById('previousDisplay');
const errorDisplay = document.getElementById('error');

function updateDisplay() {
    display.textContent = currentInput;
    previousDisplayElement.textContent = previousDisplay;
    errorDisplay.textContent = '';
}

function clearDisplay() {
    currentInput = '0';
    operator = null;
    previousValue = null;
    waitingForOperand = false;
    previousDisplay = '';
    updateDisplay();
}

function deleteChar() {
    if (currentInput.length > 1) {
        currentInput = currentInput.slice(0, -1);
    } else {
        currentInput = '0';
    }
    updateDisplay();
}

function appendNumber(num) {
    if (waitingForOperand) {
        currentInput = num;
        waitingForOperand = false;
    } else {
        currentInput = currentInput === '0' ? num : currentInput + num;
    }
    updateDisplay();
}

function appendDecimal() {
    if (waitingForOperand) {
        currentInput = '0.';
        waitingForOperand = false;
    } else if (!currentInput.includes('.')) {
        currentInput += '.';
    }
    updateDisplay();
}

function appendOperator(op) {
    const inputValue = parseFloat(currentInput);
    
    if (previousValue === null) {
        previousValue = inputValue;
        previousDisplay = `${inputValue} ${op}`;
    } else if (operator) {
        // If there's a pending operation, calculate it first
        performCalculation();
        previousDisplay = `${currentInput} ${op}`;
    } else {
        previousValue = inputValue;
        previousDisplay = `${inputValue} ${op}`;
    }
    
    waitingForOperand = true;
    operator = op;
    updateDisplay();
}

function performCalculation() {
    const inputValue = parseFloat(currentInput);
    
    if (previousValue === null || operator === null) {
        return;
    }
    
    // Map display operators to API operators
    const operatorMap = {
        '+': 'add',
        '-': 'subtract',
        '*': 'multiply',
        '/': 'divide'
    };
    
    const apiOperator = operatorMap[operator];
    
    // Save expression for history
    const expression = `${previousValue} ${operator} ${inputValue}`;
    
    // Call backend API
    fetch('/api/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            operation: apiOperator,
            a: previousValue,
            b: inputValue
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            errorDisplay.textContent = `Error: ${data.error}`;
            currentInput = '0';
            previousValue = null;
            operator = null;
        } else {
            currentInput = String(data.result);
            previousValue = data.result;
            // Add to history
            addToHistory(expression, data.result);
        }
        updateDisplay();
    })
    .catch(error => {
        errorDisplay.textContent = 'Network error. Please try again.';
        console.error('Error:', error);
    });
}

function calculate() {
    if (operator === null || previousValue === null) {
        return;
    }
    
    const inputValue = parseFloat(currentInput);
    const expression = `${previousValue} ${operator} ${inputValue}`;
    previousDisplay = `${expression} =`;
    
    performCalculation();
    operator = null;
    previousValue = null;
    waitingForOperand = true;
}

// Keyboard support
document.addEventListener('keydown', (event) => {
    const key = event.key;
    
    if (key >= '0' && key <= '9') {
        appendNumber(key);
    } else if (key === '.') {
        appendDecimal();
    } else if (key === '+' || key === '-' || key === '*' || key === '/') {
        appendOperator(key);
    } else if (key === 'Enter' || key === '=') {
        event.preventDefault();
        calculate();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        clearDisplay();
    } else if (key === 'Backspace') {
        deleteChar();
    } else if (key === 's') {
        calculateScientific('sin');
    } else if (key === 'o') {
        calculateScientific('cos');
    } else if (key === 't') {
        calculateScientific('tan');
    } else if (key === 'q') {
        calculateScientific('sqrt');
    } else if (key === 'l') {
        calculateScientific('log');
    }
});

// Toggle scientific mode
function toggleScientificMode() {
    isScientificMode = !isScientificMode;
    const panel = document.getElementById('scientificPanel');
    const toggle = document.getElementById('modeToggle');
    
    if (isScientificMode) {
        panel.style.display = 'grid';
        toggle.textContent = 'Basic';
        toggle.classList.add('active');
    } else {
        panel.style.display = 'none';
        toggle.textContent = 'Scientific';
        toggle.classList.remove('active');
    }
}

// Toggle angle mode (degrees/radians)
function toggleAngleMode() {
    angleMode = angleMode === 'DEG' ? 'RAD' : 'DEG';
    const toggle = document.getElementById('angleToggle');
    toggle.textContent = angleMode;
}

// Convert degrees to radians
function toRadians(degrees) {
    return degrees * (Math.PI / 180);
}

// Convert radians to degrees
function toDegrees(radians) {
    return radians * (180 / Math.PI);
}

// Calculate scientific functions
function calculateScientific(func) {
    const inputValue = parseFloat(currentInput);
    
    if (isNaN(inputValue)) {
        errorDisplay.textContent = 'Invalid input';
        return;
    }
    
    let result;
    
    try {
        switch(func) {
            case 'sin':
                result = angleMode === 'DEG' ? Math.sin(toRadians(inputValue)) : Math.sin(inputValue);
                break;
            case 'cos':
                result = angleMode === 'DEG' ? Math.cos(toRadians(inputValue)) : Math.cos(inputValue);
                break;
            case 'tan':
                result = angleMode === 'DEG' ? Math.tan(toRadians(inputValue)) : Math.tan(inputValue);
                break;
            case 'sqrt':
                if (inputValue < 0) {
                    errorDisplay.textContent = 'Cannot take square root of negative number';
                    return;
                }
                result = Math.sqrt(inputValue);
                break;
            case 'log':
                if (inputValue <= 0) {
                    errorDisplay.textContent = 'Logarithm requires positive number';
                    return;
                }
                result = Math.log10(inputValue);
                break;
            case 'ln':
                if (inputValue <= 0) {
                    errorDisplay.textContent = 'Natural log requires positive number';
                    return;
                }
                result = Math.log(inputValue);
                break;
            case 'exp':
                result = Math.exp(inputValue);
                break;
            case 'pi':
                result = Math.PI;
                break;
            default:
                errorDisplay.textContent = 'Unknown function';
                return;
        }
        
        // Round to avoid floating point precision issues
        result = Math.round(result * 1e10) / 1e10;
        currentInput = String(result);
        waitingForOperand = true;
        updateDisplay();
        
    } catch (error) {
        errorDisplay.textContent = 'Calculation error';
        console.error('Scientific calculation error:', error);
    }
}

// History Management
function loadHistory() {
    try {
        const stored = sessionStorage.getItem('calculatorHistory');
        if (stored) {
            calculationHistory = JSON.parse(stored);
            renderHistory();
        }
    } catch (error) {
        console.error('Error loading history:', error);
        calculationHistory = [];
    }
}

function saveHistory() {
    try {
        sessionStorage.setItem('calculatorHistory', JSON.stringify(calculationHistory));
    } catch (error) {
        console.error('Error saving history:', error);
    }
}

function addToHistory(expression, result) {
    const entry = {
        expression: expression,
        result: result,
        timestamp: new Date().toISOString()
    };
    
    calculationHistory.unshift(entry); // Add to beginning
    
    // Keep only last 20 entries
    if (calculationHistory.length > MAX_HISTORY) {
        calculationHistory = calculationHistory.slice(0, MAX_HISTORY);
    }
    
    saveHistory();
    renderHistory();
}

function renderHistory() {
    const historyList = document.getElementById('historyList');
    
    if (calculationHistory.length === 0) {
        historyList.innerHTML = '<p class="no-history">No history</p>';
        return;
    }
    
    historyList.innerHTML = '';
    
    calculationHistory.forEach((entry, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.onclick = () => loadFromHistory(entry);
        
        const expressionDiv = document.createElement('div');
        expressionDiv.className = 'history-expression';
        expressionDiv.textContent = entry.expression;
        
        const resultDiv = document.createElement('div');
        resultDiv.className = 'history-result';
        resultDiv.textContent = `= ${entry.result}`;
        
        historyItem.appendChild(expressionDiv);
        historyItem.appendChild(resultDiv);
        historyList.appendChild(historyItem);
    });
}

function loadFromHistory(entry) {
    currentInput = String(entry.result);
    previousDisplay = entry.expression;
    operator = null;
    previousValue = null;
    waitingForOperand = true;
    updateDisplay();
}

function clearHistory() {
    calculationHistory = [];
    saveHistory();
    renderHistory();
}

function toggleHistory() {
    isHistoryVisible = !isHistoryVisible;
    const panel = document.getElementById('historyPanel');
    const toggle = document.getElementById('historyToggle');
    
    if (isHistoryVisible) {
        panel.style.display = 'block';
        toggle.classList.add('active');
    } else {
        panel.style.display = 'none';
        toggle.classList.remove('active');
    }
}

// Load history on page load
window.addEventListener('load', loadHistory);

// ============== AUTH FUNCTIONS ==============

// Check auth status on page load
window.addEventListener('load', checkAuthStatus);

async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/status');
        const data = await response.json();
        
        if (data.authenticated) {
            // Store user info in sessionStorage
            sessionStorage.setItem('userId', data.user_id);
            sessionStorage.setItem('username', data.username);
            sessionStorage.setItem('isAuthenticated', 'true');
            
            // Update UI if on calculator page
            if (document.getElementById('display')) {
                showUserInfo(data.username);
            }
        } else {
            // Clear session storage
            sessionStorage.removeItem('userId');
            sessionStorage.removeItem('username');
            sessionStorage.removeItem('isAuthenticated');
            
            // Redirect to login if on protected pages (future use)
            // For now, allow guest access to calculator
        }
    } catch (error) {
        console.error('Auth status check failed:', error);
    }
}

function showUserInfo(username) {
    // Add user info to calculator UI
    const modeToggle = document.querySelector('.mode-toggle');
    if (modeToggle && !document.getElementById('userInfo')) {
        const userInfo = document.createElement('div');
        userInfo.id = 'userInfo';
        userInfo.className = 'user-info';
        userInfo.innerHTML = `
            <span>Welcome, ${username}</span>
            <button class="btn-toggle" onclick="handleLogout()">Logout</button>
        `;
        modeToggle.appendChild(userInfo);
    }
}

// Registration handler
async function handleRegister(event) {
    event.preventDefault();
    
    // Clear previous errors
    clearFormErrors();
    
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // Client-side validation
    let hasError = false;
    
    if (username.length < 3 || username.length > 50) {
        showFieldError('username', 'Username must be 3-50 characters');
        hasError = true;
    }
    
    if (!isValidEmail(email)) {
        showFieldError('email', 'Please enter a valid email address');
        hasError = true;
    }
    
    if (password.length < 8) {
        showFieldError('password', 'Password must be at least 8 characters');
        hasError = true;
    }
    
    if (password !== confirmPassword) {
        showFieldError('confirmPassword', 'Passwords do not match');
        hasError = true;
    }
    
    if (hasError) {
        return;
    }
    
    // Disable submit button
    const registerBtn = document.getElementById('registerBtn');
    registerBtn.disabled = true;
    registerBtn.textContent = 'Creating account...';
    
    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Registration successful - auto login
            sessionStorage.setItem('userId', data.user_id);
            sessionStorage.setItem('username', data.username);
            sessionStorage.setItem('isAuthenticated', 'true');
            
            // Redirect to calculator
            window.location.href = '/static/index.html';
        } else {
            // Show error from server
            showFormError(data.error || 'Registration failed');
            registerBtn.disabled = false;
            registerBtn.textContent = 'Register';
        }
    } catch (error) {
        showFormError('Network error. Please try again.');
        registerBtn.disabled = false;
        registerBtn.textContent = 'Register';
    }
}

// Login handler
async function handleLogin(event) {
    event.preventDefault();
    
    // Clear previous errors
    clearFormErrors();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    
    // Client-side validation
    if (!username) {
        showFieldError('username', 'Username is required');
        return;
    }
    
    if (!password) {
        showFieldError('password', 'Password is required');
        return;
    }
    
    // Disable submit button
    const loginBtn = document.getElementById('loginBtn');
    loginBtn.disabled = true;
    loginBtn.textContent = 'Logging in...';
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Login successful
            sessionStorage.setItem('userId', data.user_id);
            sessionStorage.setItem('username', data.username);
            sessionStorage.setItem('isAuthenticated', 'true');
            
            // Redirect to calculator
            window.location.href = '/static/index.html';
        } else {
            // Show error from server
            showFormError(data.error || 'Login failed');
            loginBtn.disabled = false;
            loginBtn.textContent = 'Login';
        }
    } catch (error) {
        showFormError('Network error. Please try again.');
        loginBtn.disabled = false;
        loginBtn.textContent = 'Login';
    }
}

// Logout handler
async function handleLogout() {
    try {
        await fetch('/api/auth/logout');
        
        // Clear session storage
        sessionStorage.removeItem('userId');
        sessionStorage.removeItem('username');
        sessionStorage.removeItem('isAuthenticated');
        
        // Redirect to login page
        window.location.href = '/static/login.html';
    } catch (error) {
        console.error('Logout failed:', error);
        // Still clear local session and redirect
        sessionStorage.clear();
        window.location.href = '/static/login.html';
    }
}

// Form validation helpers
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showFieldError(fieldId, message) {
    const errorElement = document.getElementById(`${fieldId}Error`);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
    
    const inputElement = document.getElementById(fieldId);
    if (inputElement) {
        inputElement.classList.add('error');
    }
}

function showFormError(message) {
    const formError = document.getElementById('formError');
    if (formError) {
        formError.textContent = message;
        formError.style.display = 'block';
    }
}

function clearFormErrors() {
    // Clear field errors
    const errorElements = document.querySelectorAll('.form-error');
    errorElements.forEach(el => {
        el.textContent = '';
        el.style.display = 'none';
    });
    
    // Clear form error
    const formError = document.getElementById('formError');
    if (formError) {
        formError.textContent = '';
        formError.style.display = 'none';
    }
    
    // Remove error class from inputs
    const inputs = document.querySelectorAll('input.error');
    inputs.forEach(input => input.classList.remove('error'));
}
