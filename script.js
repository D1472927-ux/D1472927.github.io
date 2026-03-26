/* ========================================
   運勢占卜網站 - 主程式
   ========================================

   📌 修改指南
   -----------
   如需自訂占卜主題，只需修改下方 FORTUNE_DATA 陣列。
   每筆資料包含：
     - name     : 運勢類型名稱
     - emoji    : 代表 Emoji
     - stars    : 星等 (1~5)
     - description : 簡短運勢說明
     - work     : 工作面分析
     - study    : 學業面分析
     - love     : 愛情面分析
     - money    : 金錢面分析
     - quote    : 結語（一句有趣或鼓勵性名言）
   
   ※ 至少保留 1 筆資料即可運作。
   ======================================== */

// ─── 占卜結果資料（集中管理，方便修改）───
const FORTUNE_DATA = [
  {
    name: "大吉",
    emoji: "🌟",
    stars: 5,
    description: "萬事如意！今天宇宙為你開了外掛，所有星星都在為你閃爍。",
    work: "貴人運爆棚，主管對你讚賞有加，適合提出新企劃或爭取加薪！",
    study: "腦袋特別清晰，讀什麼都能快速吸收，考試一定穩穩過關。",
    love: "桃花朵朵開～單身者今天出門特別有魅力，有伴的感情更加甜蜜。",
    money: "偏財運旺盛，可能會有意外驚喜收入，但別因此亂花錢喔！",
    quote: "你就是自己的幸運星，今天什麼都擋不住你！🚀"
  },
  {
    name: "中吉",
    emoji: "☀️",
    stars: 4,
    description: "整體運勢不錯，只要稍加努力就能收穫滿滿。",
    work: "工作效率很高，團隊合作順暢，但注意細節別馬虎。",
    study: "適合複習重點，整理筆記會有意想不到的新理解。",
    love: "與另一半或心儀對象聊天會特別投緣，把握說甜話的機會。",
    money: "正財穩定，適合規劃未來理財計畫，今天先別衝動消費。",
    quote: "穩扎穩打的人，運氣從來不會太差。🌈"
  },
  {
    name: "小吉",
    emoji: "🌤️",
    stars: 3,
    description: "平穩中帶點小驚喜，保持好心情就對了。",
    work: "日常事務順利進行，可能會接到一個有趣的新任務。",
    study: "學習狀態OK，建議找同學一起討論，效率更高。",
    love: "感情平順，一個溫暖的小舉動就能讓關係更親近。",
    money: "收支平衡，適合記帳理財，留意有沒有忘記繳費的帳單。",
    quote: "小確幸也是人生中美好的風景。☁️"
  },
  {
    name: "吉",
    emoji: "✨",
    stars: 3,
    description: "運勢平順安穩，像一杯溫暖的拿鐵，舒服自在。",
    work: "沒有大風大浪，適合處理文書和整理工作流程。",
    study: "專注力尚可，建議用番茄鐘工作法來保持節奏。",
    love: "感情穩定，兩人可以一起做些日常的小事，增進默契。",
    money: "財務狀況穩定，適合做長期規劃，不宜大額投資。",
    quote: "安穩本身就是一種幸福，享受平靜吧。🍵"
  },
  {
    name: "末吉",
    emoji: "🌙",
    stars: 2,
    description: "運勢稍弱，但只要保持正面心態，一切都能化險為夷。",
    work: "可能會遇到小阻礙，請耐心處理，別急躁。",
    study: "注意力容易分散，試試換個環境或聽白噪音。",
    love: "溝通上可能有些小誤會，多一點耐心傾聽對方。",
    money: "不宜大筆支出，今天請把錢包守緊一點。",
    quote: "烏雲的背後，太陽一直都在。🌅"
  },
  {
    name: "半吉半凶",
    emoji: "⚖️",
    stars: 3,
    description: "今天的運勢如同蹺蹺板，好壞參半，關鍵在你的選擇。",
    work: "可能有機會也有挑戰並存，謹慎判斷再做決定。",
    study: "效率忽高忽低，見好就收，累了就休息。",
    love: "可能會有浪漫邂逅，但也容易因小事起爭執。",
    money: "有進帳但也有支出，記得做好收支平衡。",
    quote: "人生就像巧克力，你永遠不知道下一顆是什麼口味。🍫"
  },
  {
    name: "小凶",
    emoji: "🌧️",
    stars: 2,
    description: "今天運勢略顯低迷，但不要灰心，低潮總會過去的。",
    work: "工作上可能被挑剔，深呼吸，把被批評當作成長的養分。",
    study: "讀書效率較低，建議先做簡單的複習暖身。",
    love: "跟另一半可能有些冷戰氣氛，主動破冰是好策略。",
    money: "小心衝動消費！今天看到特價先存入收藏，改天再買。",
    quote: "每一次低谷，都是在為下一次高峰做準備。💪"
  },
  {
    name: "凶",
    emoji: "⛈️",
    stars: 1,
    description: "暴風雨前的寧靜？今天挑戰較多，但你比你想的更強大。",
    work: "注意溝通方式，今天容易踩到地雷，謹言慎行。",
    study: "腦袋像漿糊？不急，先散步再回來念書效果更好。",
    love: "感情上容易鑽牛角尖，試著換位思考會好很多。",
    money: "漏財注意！仔細檢查帳單和交易紀錄。",
    quote: "就算今天不順，明天的太陽會更燦爛。🌻"
  },
  {
    name: "大凶",
    emoji: "💫",
    stars: 1,
    description: "看起來很可怕？放心，大凶其實是轉運的前兆！物極必反。",
    work: "可能被交辦棘手任務，但完成後會獲得極大成就感！",
    study: "今天考試可能有點慘烈，但記住：失敗是成功之母。",
    love: "感情上可能有波折，但真正的感情經得起考驗。",
    money: "可能會有一筆意外支出，記得預留一些緊急備用金。",
    quote: "最深的夜要來了，這代表天亮也不遠了。🌄"
  },
  {
    name: "超級幸運日",
    emoji: "🎆",
    stars: 5,
    description: "恭喜！你抽中了隱藏版超級幸運日！今天做什麼都順風順水。",
    work: "你就是職場最亮的星，升職加薪都有機會！",
    study: "過目不忘模式啟動！現在翻開課本，效率 MAX。",
    love: "今天你散發的魅力值破表，出門前記得照照鏡子欣賞自己。",
    money: "財神爺今天特別眷顧你，可以買張刮刮樂試手氣！",
    quote: "今天就是你的 LUCKY DAY，勇敢去做想做的事吧！🎉"
  },
  {
    name: "佛系好運",
    emoji: "🧘",
    stars: 4,
    description: "心靜自然涼～今天不用太努力，好運會自己找上門。",
    work: "不爭不搶，反而會被看見你的實力與穩重。",
    study: "輕鬆學習效果最好，今天適合看科普影片或課外讀物。",
    love: "順其自然的感情最甜蜜，不刻意反而更有吸引力。",
    money: "隨緣消費，你會發現今天買到的都是物超所值的好東西。",
    quote: "有時候放慢腳步，反而能走得更遠。🐢💨"
  },
  {
    name: "冒險運",
    emoji: "🗺️",
    stars: 3,
    description: "今天適合嘗試新事物！跳出舒適圈可能會有驚喜發現。",
    work: "可以主動嘗試不同的工作方式，說不定有突破。",
    study: "嘗試新的學習方法或工具，也許會發現更適合自己的方式。",
    love: "勇敢表白或規劃約會吧！冒險精神今天會獲得回報。",
    money: "適合小額嘗試新的理財方式，但不宜押大注。",
    quote: "冒險不一定會成功，但不冒險一定不會。🏔️"
  }
];

// ─── 幸運色資料 ───
const LUCKY_COLORS = [
  "薰衣草紫 💜", "玫瑰金 🌹", "星空藍 💙", "翡翠綠 💚",
  "暖陽橘 🧡", "櫻花粉 🌸", "月光銀 🤍", "琥珀金 ✨",
  "珊瑚紅 ❤️", "薄荷綠 🍃", "深海藍 🌊", "蜜桃色 🍑"
];

// ─── DOM 元素 ───
const divineBtn     = document.getElementById('divine-btn');
const retryBtn      = document.getElementById('retry-btn');
const homeSection   = document.getElementById('home-section');
const resultSection = document.getElementById('result-section');
const diviningAnim  = document.getElementById('divining-animation');

const resultEmoji   = document.getElementById('result-emoji');
const resultName    = document.getElementById('result-name');
const resultStars   = document.getElementById('result-stars');
const resultDesc    = document.getElementById('result-description');
const detailWork    = document.getElementById('detail-work');
const detailStudy   = document.getElementById('detail-study');
const detailLove    = document.getElementById('detail-love');
const detailMoney   = document.getElementById('detail-money');
const quoteText     = document.getElementById('result-quote-text');
const luckyColor    = document.getElementById('lucky-color');
const luckyNumber   = document.getElementById('lucky-number');

// ─── 工具函數 ───
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function generateStars(count) {
  return '⭐'.repeat(count) + '☆'.repeat(5 - count);
}

// ─── 占卜邏輯 ───
function performDivination() {
  // 1. 隱藏按鈕，顯示動畫
  divineBtn.classList.add('hidden');
  diviningAnim.classList.remove('hidden');

  // 2. 等待動畫後顯示結果
  setTimeout(() => {
    const fortune = pickRandom(FORTUNE_DATA);

    // 填入結果
    resultEmoji.textContent   = fortune.emoji;
    resultName.textContent    = fortune.name;
    resultStars.textContent   = generateStars(fortune.stars);
    resultDesc.textContent    = fortune.description;
    detailWork.textContent    = fortune.work;
    detailStudy.textContent   = fortune.study;
    detailLove.textContent    = fortune.love;
    detailMoney.textContent   = fortune.money;
    quoteText.textContent     = fortune.quote;
    luckyColor.textContent    = pickRandom(LUCKY_COLORS);
    luckyNumber.textContent   = randomInt(1, 99);

    // 切換顯示
    homeSection.classList.add('hidden');
    diviningAnim.classList.add('hidden');
    resultSection.classList.remove('hidden');

    // 滾到結果頂部
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, 2200);
}

function resetDivination() {
  resultSection.classList.add('hidden');
  homeSection.classList.remove('hidden');
  divineBtn.classList.remove('hidden');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── 事件綁定 ───
divineBtn.addEventListener('click', performDivination);
retryBtn.addEventListener('click', resetDivination);

// ─── Canvas 星空背景 ───
(function initStars() {
  const canvas = document.getElementById('starsCanvas');
  const ctx = canvas.getContext('2d');
  let stars = [];
  const STAR_COUNT = 120;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function createStars() {
    stars = [];
    for (let i = 0; i < STAR_COUNT; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.8 + 0.3,
        alpha: Math.random(),
        dAlpha: (Math.random() - 0.5) * 0.015,
        speed: Math.random() * 0.15 + 0.02
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    stars.forEach(s => {
      s.alpha += s.dAlpha;
      if (s.alpha <= 0.1 || s.alpha >= 1) s.dAlpha *= -1;
      s.alpha = Math.max(0.1, Math.min(1, s.alpha));

      s.y += s.speed;
      if (s.y > canvas.height + 5) {
        s.y = -5;
        s.x = Math.random() * canvas.width;
      }

      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(200, 190, 255, ${s.alpha})`;
      ctx.fill();
    });

    requestAnimationFrame(draw);
  }

  resize();
  createStars();
  draw();

  window.addEventListener('resize', () => {
    resize();
    createStars();
  });
})();
