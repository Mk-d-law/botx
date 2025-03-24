document.addEventListener('DOMContentLoaded', function() {
    simulateDataLoading();

    document.querySelector('.create-bot-btn').addEventListener('click', function() {
        document.querySelector('.create-bot-modal').classList.remove('hidden');
    });

    document.querySelector('.submit-bot-btn').addEventListener('click', function() {
        const botName = document.querySelector('.bot-input').value;
        if (botName) {
            const botList = document.querySelector('.bot-list');
            const botItem = document.createElement('div');
            const now = new Date();
            botItem.innerHTML = `<p>${botName} - Created on ${now.toLocaleDateString()} at ${now.toLocaleTimeString()}</p>`;
            botList.appendChild(botItem);

            const currentBots = parseInt(document.getElementById('bots').textContent);
            document.getElementById('bots').textContent = currentBots + 1;

            document.querySelector('.bot-created-message').classList.remove('hidden');
            setTimeout(() => {
                document.querySelector('.create-bot-modal').classList.add('hidden');
                document.querySelector('.bot-created-message').classList.add('hidden');
                document.querySelector('.bot-input').value = '';
            }, 1500);
        }
    });

    document.addEventListener('click', function(event) {
        const modal = document.querySelector('.create-bot-modal');
        const createBotBtn = document.querySelector('.create-bot-btn');
        
        if (!modal.classList.contains('hidden') && 
            !modal.contains(event.target) && 
            !createBotBtn.contains(event.target)) {
            
            modal.classList.add('hidden');
        }
    });
});

function simulateDataLoading() {
    let botCount = 0;
    let userCount = 0;
    let messageCount = 0;
    
    const botInterval = setInterval(() => {
        if (botCount < 5) {
            botCount++;
            document.getElementById('bots').textContent = botCount;
        } else {
            clearInterval(botInterval);
        }
    }, 200);
    
    const userInterval = setInterval(() => {
        if (userCount < 250) {
            userCount += Math.floor(Math.random() * 50) + 10;
            if (userCount > 250) userCount = 250;
            document.getElementById('users').textContent = userCount;
        } else {
            clearInterval(userInterval);
        }
    }, 100);
    
    const messageInterval = setInterval(() => {
        if (messageCount < 1500) {
            messageCount += Math.floor(Math.random() * 300) + 50;
            if (messageCount > 1500) messageCount = 1500;
            document.getElementById('messages').textContent = messageCount;
        } else {
            clearInterval(messageInterval);
        }
    }, 80);
}
