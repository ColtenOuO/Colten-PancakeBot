document.addEventListener('DOMContentLoaded', function() {
  // 顯示當前時間的函數
  function updateTime() {
    const now = new Date();
    const currentTime = now.toLocaleTimeString();
    document.getElementById('current-time').textContent = currentTime;
  }
  
  setInterval(updateTime, 1000); // 每秒更新時間

  document.getElementById('login-message').addEventListener('click', function() {
    window.location.href = 'https://discord.com/oauth2/authorize?client_id=1233320856772673536&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A5500%2Fstock_web%2Fapp%2Fmain.html&scope=identify+email';
  });

  document.querySelectorAll('.buy').forEach(button => {
    button.addEventListener('click', function() {
        // 找到該按鈕的股票資訊
        const stockContainer = this.closest('.stock');
        const span = stockContainer.querySelector('span');
        const text = span.textContent;
        const parts = text.split(':');
        const stockCode = parts[1].trim();
        const stockName = parts[0].trim();
        const currentPrice = stockContainer.parentNode.querySelector('.current-price span').textContent;
        const user_id = document.getElementById('discord_id').value;
        const buyPageUrl = `buy_stock.html?stock_code=${encodeURIComponent(stockCode)}&stock_price=${encodeURIComponent(currentPrice)}&stock_name=${encodeURIComponent(stockName)}&discord_id=${encodeURIComponent(user_id)}`;
        window.open(buyPageUrl, '_blank'); // 在新標籤頁中開啟buy_stock.html，並帶上股票代碼和價格作為URL參數
    });
  });
document.querySelectorAll('.sell').forEach(button => {
    button.addEventListener('click', function() {
      const stockContainer = this.closest('.stock');
        const span = stockContainer.querySelector('span');
        const text = span.textContent;
        const parts = text.split(':');
        const stockCode = parts[1].trim();
        const stockName = parts[0].trim();
        const currentPrice = stockContainer.parentNode.querySelector('.current-price span').textContent;
        const user_id = document.getElementById('discord_id').value;

        const sellPageUrl = `sell_stock.html?stock_code=${encodeURIComponent(stockCode)}&stock_price=${encodeURIComponent(currentPrice)}&stock_name=${encodeURIComponent(stockName)}
        &discord_id=${encodeURIComponent(user_id)}`;
        window.open(sellPageUrl, '_blank'); // 在新標籤頁中開啟buy_stock.html，並帶上股票代碼和價格作為URL參數
    });
  });
});

window.onload = function() {
  const params = new URLSearchParams(window.location.search);
  const code = params.get('code');
  if (code) {
    fetch(`http://127.0.0.1:8000/auth/callback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `code=${encodeURIComponent(code)}`
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok: ' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
      if( data.username ) {
        document.getElementById('login-message').textContent = `Welcome aborad，${data.username}！`;
        document.getElementById('discord_id').value = `${data.id}`
      }
      else {
        document.getElementById('login-message').textContent = `登入後繼續`;
      }
    })
    .catch(error => {
      console.error('Error:', error);
      document.getElementById('login-message').textContent = 'Error';
    });
  }
};

function fetchPrice() {
  for (let i = 1; i <= 6; i++) {
    fetch(`http://localhost:8000/price/${1000 + i}`)
      .then(response => response.json())
      .then(data => {
          document.querySelector(`#current-price${i} span`).innerText = data.price;
      })
      .catch(error => console.error('Error fetching data:', error));
  }
}

// 定期更新價格，每5秒一次
setInterval(fetchPrice, 5000);