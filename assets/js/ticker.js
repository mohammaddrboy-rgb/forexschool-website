/* Live price ticker under the home-page menu.
   Prices come from TradingView's free "Ticker Tape" widget (real-time/delayed per exchange).
   Symbol titles are bilingual: Dari on /fa/ pages, English elsewhere. */
(function () {
  'use strict';
  var bar = document.querySelector('.tickerbar');
  if (!bar) return;
  var host = bar.querySelector('.tradingview-widget-container');
  var fa = document.documentElement.lang === 'fa';

  // [TradingView symbol, English title, Dari title]
  var SYMBOLS = [
    ['FX_IDC:EURUSD', 'EUR/USD', 'یورو/دلار'],
    ['FX_IDC:GBPUSD', 'GBP/USD', 'پوند/دلار'],
    ['FX_IDC:USDJPY', 'USD/JPY', 'دلار/ین'],
    ['OANDA:XAUUSD', 'Gold', 'طلا'],
    ['FOREXCOM:SPXUSD', 'S&P 500', 'اس‌اندپی ۵۰۰'],
    ['TVC:USOIL', 'Crude Oil (WTI)', 'نفت خام WTI'],
    ['BITSTAMP:BTCUSD', 'Bitcoin', 'بیت‌کوین'],
    ['FX_IDC:USDCHF', 'USD/CHF', 'دلار/فرانک'],
    ['FX_IDC:AUDUSD', 'AUD/USD', 'دلار استرالیا/دلار'],
    ['FX_IDC:USDCAD', 'USD/CAD', 'دلار/دلار کانادا'],
    ['FX_IDC:NZDUSD', 'NZD/USD', 'دلار نیوزیلند/دلار'],
    ['FX_IDC:EURJPY', 'EUR/JPY', 'یورو/ین'],
    ['FX_IDC:GBPJPY', 'GBP/JPY', 'پوند/ین'],
    ['OANDA:XAGUSD', 'Silver', 'نقره'],
    ['OANDA:XPTUSD', 'Platinum', 'پلاتین'],
    ['TVC:DXY', 'US Dollar Index', 'شاخص دلار'],
    ['FOREXCOM:NSXUSD', 'Nasdaq 100', 'نزدک ۱۰۰'],
    ['FOREXCOM:DJI', 'Dow Jones', 'داوجونز'],
    ['TVC:UKOIL', 'Brent Oil', 'نفت برنت'],
    ['NASDAQ:AAPL', 'Apple', 'اپل'],
    ['NASDAQ:NVDA', 'Nvidia', 'انویدیا'],
    ['NASDAQ:MSFT', 'Microsoft', 'مایکروسافت'],
    ['NASDAQ:TSLA', 'Tesla', 'تسلا'],
    ['NASDAQ:AMZN', 'Amazon', 'آمازون'],
    ['NASDAQ:GOOGL', 'Alphabet (Google)', 'گوگل'],
    ['BITSTAMP:ETHUSD', 'Ethereum', 'اتریوم']
  ];

  var cfg = {
    symbols: SYMBOLS.map(function (s) { return { proName: s[0], title: fa ? s[2] : s[1] }; }),
    showSymbolLogo: true,
    isTransparent: true,
    displayMode: 'adaptive',
    colorTheme: 'dark',
    locale: 'en'
  };

  var s = document.createElement('script');
  s.type = 'text/javascript';
  s.async = true;
  s.src = 'https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js';
  s.text = JSON.stringify(cfg);
  s.onerror = function () { bar.classList.add('is-offline'); };
  host.appendChild(s);

  // Mark the bar ready once TradingView's iframe has loaded (fades the placeholder out).
  var tries = 0;
  var t = setInterval(function () {
    var f = host.querySelector('iframe');
    if (f) { f.addEventListener('load', function () { bar.classList.add('is-ready'); }); bar.classList.add('is-ready'); clearInterval(t); }
    else if (++tries > 40) { clearInterval(t); bar.classList.add('is-offline'); }
  }, 250);
})();
