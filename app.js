document.addEventListener('DOMContentLoaded', function () {
    const translations = {
        en: {
            title: "Medical QA System",
            description: "Ask your medical questions below:",
            placeholder: "Enter your question here",
            askButton: "Ask",
            answerTitle: "Answer:",
            langToggle: "English",
            historyTitle: "History:",
            popularQuestionsTitle: "Popular Questions:"
        },
        zh: {
            title: "医疗问答系统",
            description: "请在下方输入您的问题：",
            placeholder: "请输入您的问题",
            askButton: "提问",
            answerTitle: "答案：",
            langToggle: "中文",
            historyTitle: "历史提问：",
            popularQuestionsTitle: "热门问题："
        },
        ms: {
            title: "Sistem Soal Jawab Perubatan",
            description: "Ajukan soalan perubatan anda di bawah:",
            placeholder: "Masukkan soalan anda di sini",
            askButton: "Tanya",
            answerTitle: "Jawapan:",
            langToggle: "Bahasa Melayu",
            historyTitle: "Sejarah:",
            popularQuestionsTitle: "Soalan Popular:"
        }
    };

    let currentLang = "en";

    applyTranslations();

    // 切换语言菜单
    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', function () {
            const selectedLang = this.getAttribute('data-lang');
            if (selectedLang) {
                currentLang = selectedLang;
                applyTranslations();
                document.getElementById("langToggle").innerText = translations[currentLang].langToggle;
            }
        });
    });

    const askButton = document.getElementById('askButton');
    askButton.addEventListener('click', async function () {
        const question = document.getElementById('question').value.trim();
        const mode = document.querySelector('input[name="outputMode"]:checked').value; // 获取选中的模式

        if (!question) {
            alert(translations[currentLang].placeholder);
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5001/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, language: currentLang, mode: parseInt(mode) })
            });

            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();

            const answerBox = document.getElementById('answerBox');
            const answerParagraph = document.getElementById('answer');
            answerParagraph.innerText = data.answer;

            answerBox.classList.remove('animate-visible');
            void answerBox.offsetWidth;
            answerBox.classList.add('animate-visible');

            updateHistory(question); // 更新历史提问
        } catch (error) {
            console.error("Error during fetch:", error);
        }
    });

    // 点击热门问题，更新输入框
    document.querySelectorAll('.popular-item').forEach(item => {
        item.addEventListener('click', function () {
            const questionInput = document.getElementById('question');
            questionInput.value = this.innerText; // 填充热门问题到输入框
            questionInput.focus(); // 聚焦输入框
        });
    });

    // 更新历史提问
    function updateHistory(question) {
        const historyList = document.getElementById('historyList');

        // 检查重复项，避免重复记录
        const existingItems = Array.from(historyList.children).map(item => item.innerText);
        if (!existingItems.includes(question)) {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.innerText = question;

            // 点击历史记录提问时填充到输入框
            li.addEventListener('click', function () {
                const questionInput = document.getElementById('question');
                questionInput.value = this.innerText;
                questionInput.focus();
            });

            historyList.appendChild(li); // 添加到历史提问列表
        }
    }

    // 应用翻译更新
    function applyTranslations() {
        const lang = translations[currentLang];
        document.getElementById("title").innerText = lang.title;
        document.getElementById("description").innerText = lang.description;
        document.getElementById("question").placeholder = lang.placeholder;
        document.getElementById("askButton").innerText = lang.askButton;
        document.getElementById("answerTitle").innerText = lang.answerTitle;
        document.getElementById("historyTitle").innerText = lang.historyTitle;
        document.getElementById("popularQuestionsTitle").innerText = lang.popularQuestionsTitle;
    }
});
