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
      window.open('buy_stock.html', '_blank'); // 在新標籤頁中開啟buy_stock.html
    });
  });

  // 賣出按鈕事件綁定
  document.querySelectorAll('.sell').forEach(button => {
    button.addEventListener('click', function() {
      alert('賣出操作');
    });
  });
});
