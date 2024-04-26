document.addEventListener('DOMContentLoaded', function() {
  // 顯示當前時間的函數
  function updateTime() {
    const now = new Date();
    const currentTime = now.toLocaleTimeString();
    document.getElementById('current-time').textContent = currentTime;
  }
  
  setInterval(updateTime, 1000); // 每秒更新時間

  // 買進按鈕事件綁定
  document.querySelectorAll('.buy').forEach(button => {
    button.addEventListener('click', function() {

        var span = document.getElementById('companyInfo');
        var text = span.textContent;
        var parts = text.split(':')

        const stockContainer = this.closest('.stock');
        const stockCode = parts[1].trim();
        const stockName = parts[0].trim();
        const currentPrice = stockContainer.parentNode.querySelector('.current-price span').textContent;
        
        const buyPageUrl = `buy_stock.html?stock_code=${encodeURIComponent(stockCode)}&stock_price=${encodeURIComponent(currentPrice)}&stock_name=${encodeURIComponent(stockName)}`;
        window.open(buyPageUrl, '_blank'); // 在新標籤頁中開啟buy_stock.html，並帶上股票代碼和價格作為URL參數
    });
  });

  // 賣出按鈕事件綁定（保持原有功能，無需更改）
  document.querySelectorAll('.sell').forEach(button => {
    button.addEventListener('click', function() {
      alert('賣出操作');
    });
  });
});
