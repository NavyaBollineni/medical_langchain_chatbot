
const form = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const messages = document.getElementById("messages");
const statusText = document.getElementById("status");
const sendButton = document.getElementById("send-button");
const suggestionList = document.getElementById("suggestion-list");

const API_URL = "http://127.0.0.1:5000/chat";

// Pool of questions to choose from
const questionPool = [
    "Which doctors specialize in cardiology?",
    "Which hospitals are available?",
    "How can I book an appointment?",
    "Which specialties are available?",
    "Show me available doctors.",
    "What are the appointment booking rules?",
    "Which doctors work at a particular hospital?",
    "How can I find a specialist?",
    "What appointment slots are available?",
    "Can you help me find a hospital?"
];

// Shuffle questions and select three different ones
function generateSuggestions() {
    const shuffled = [...questionPool];

    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));

        [shuffled[i], shuffled[j]] =
            [shuffled[j], shuffled[i]];
    }

    const selectedQuestions = shuffled.slice(0, 3);

    suggestionList.replaceChildren();

    selectedQuestions.forEach(function(question) {
        const button = document.createElement("button");

        button.type = "button";
        button.className = "suggestion-button";
        button.textContent = question;

        button.addEventListener("click", function() {
            askQuestion(question);
        });

        suggestionList.appendChild(button);
    });
}

function addMessage(text, className) {
    const message = document.createElement("div");

    message.className = "message " + className;
    message.textContent = text;

    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}

async function askQuestion(question) {
    if (!question.trim() || sendButton.disabled) {
        return;
    }

    addMessage(question, "user-message");

    questionInput.value = "";
    sendButton.disabled = true;
    statusText.textContent = "Getting your answer...";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to get an answer."
            );
        }

        addMessage(data.answer, "bot-message");
        statusText.textContent = "";

    } catch (error) {
        addMessage(
            "Unable to connect to the backend. Please check that your server is running.",
            "error-message"
        );

        statusText.textContent = "";

    } finally {
        sendButton.disabled = false;
        questionInput.focus();
    }
}

form.addEventListener("submit", function(event) {
    event.preventDefault();
    askQuestion(questionInput.value);
});

// Generate new suggestions whenever the page loads
generateSuggestions();
