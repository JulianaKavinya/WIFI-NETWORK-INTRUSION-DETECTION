const quizData = [
    {
        question: "What is the capital of France?",
        options: ["Paris", "London", "Berlin", "Madrid"],
        answer: "Paris"
    },
    {
        question: "What is 2 + 2?",
        options: ["3", "4", "5", "6"],
        answer: "4"
    },
    {
        question: "What is the color of the sky?",
        options: ["Blue", "Red", "Green", "Yellow"],
        answer: "Blue"
    }
];

let currentQuestionIndex = 0;
let score = 0;

function loadQuestion() {
    const questionEl = document.getElementById('question');
    const optionsEl = document.getElementById('options');
    optionsEl.innerHTML = '';

    const currentQuestion = quizData[currentQuestionIndex];
    questionEl.textContent = currentQuestion.question;

    currentQuestion.options.forEach(option => {
        const button = document.createElement('button');
        button.textContent = option;
        button.addEventListener('click', () => checkAnswer(option));
        optionsEl.appendChild(button);
    });
}

function checkAnswer(selectedAnswer) {
    if (selectedAnswer === quizData[currentQuestionIndex].answer) {
        score++;
    }

    currentQuestionIndex++;
    if (currentQuestionIndex < quizData.length) {
        loadQuestion();
    } else {
        displayScore();
    }
}

function displayScore() {
    document.getElementById('question').style.display = 'none';
    document.getElementById('options').style.display = 'none';
    document.getElementById('next-button').style.display = 'none';

    const scoreEl = document.getElementById('score');
    scoreEl.textContent = `Your score: ${score}/${quizData.length}`;
    scoreEl.style.display = 'block';
}

document.getElementById('next-button').addEventListener('click', loadQuestion);

loadQuestion();
