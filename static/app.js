let currentInput = '0';
let operator = null;
let previousValue = null;
let waitingForOperand = false;

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
    }
});
