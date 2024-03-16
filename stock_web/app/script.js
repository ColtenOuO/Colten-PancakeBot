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

    // 獲取模態框元素
  var modal = document.getElementById('buyModal');

  // 獲取打開模態框的按鈕元素
  var btns = document.querySelectorAll('.buy');

  // 獲取模態框中的 <span> 元素，用於關閉模態框
  var span = document.getElementsByClassName('close')[0];

  // 當用戶點擊按鈕時打開模態框
  btns.forEach(button => {
    button.onclick = function() {
      modal.style.display = 'block';
    }
  });

  // 當用戶點擊 <span> (x), 關閉模態框
  span.onclick = function() {
    modal.style.display = 'none';
  }

  // 當用戶點擊模態框之外的區域，也可以關閉它
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = 'none';
    }
  }

});
