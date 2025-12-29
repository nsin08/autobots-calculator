let currentInput = '0';
let operator = null;
let previousValue = null;
let waitingForOperand = false;
let isScientificMode = false;
let angleMode = 'DEG'; // 'DEG' or 'RAD'

const display = document.getElementById('display');
const errorDisplay = document.getElementById('error');

function updateDisplay() {
    display.textContent = currentInput;
    errorDisplay.textContent = '';
}

function clearDisplay() {
    currentInput = '0';
    operator = null;
    previousValue = null;
    waitingForOperand = false;
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
    } else if (operator) {
        // If there's a pending operation, calculate it first
        performCalculation();
    }
    
    waitingForOperand = true;
    operator = op;
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
