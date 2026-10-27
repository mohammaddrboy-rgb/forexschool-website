/* Live price ticker under the home-page menu.
   Prices come from TradingView's free "Ticker Tape" widget (real-time/delayed per exchange).
   Symbol titles: names on English pages, international codes on /fa/ (see note below). */
(function () {
  'use strict';
  var bar = document.querySelector('.tickerbar');
  if (!bar) return;
  var host = bar.querySelector('.tradingview-widget-container');
  var fa = document.documentElement.lang === 'fa';

  // [TradingView symbol, English-page title, Dari-page title]
  // The widget is a TradingView iframe, so our fonts cannot reach inside it: Persian text there falls
  // back to the visitor's default Arabic-script font. On /fa/ we therefore show the standard
  // international codes (XAU/USD, WTI, AAPL…) — no Persian letters inside the iframe; all Dari text
  // around the ticker uses the site's Vazirmatn font.
  var SYMBOLS = [
    ['FX_IDC:EURUSD', 'EUR/USD', 'EUR/USD'],
    ['FX_IDC:GBPUSD', 'GBP/USD', 'GBP/USD'],
    ['FX_IDC:USDJPY', 'USD/JPY', 'USD/JPY'],
    ['OANDA:XAUUSD', 'Gold', 'XAU/USD'],
    ['FOREXCOM:SPXUSD', 'S&P 500', 'S&P 500'],
    ['TVC:USOIL', 'Crude Oil (WTI)', 'WTI'],
    ['BITSTAMP:BTCUSD', 'Bitcoin', 'BTC/USD'],
    ['FX_IDC:USDCHF', 'USD/CHF', 'USD/CHF'],
    ['FX_IDC:AUDUSD', 'AUD/USD', 'AUD/USD'],
    ['FX_IDC:USDCAD', 'USD/CAD', 'USD/CAD'],
    ['FX_IDC:NZDUSD', 'NZD/USD', 'NZD/USD'],
    ['FX_IDC:EURJPY', 'EUR/JPY', 'EUR/JPY'],
    ['FX_IDC:GBPJPY', 'GBP/JPY', 'GBP/JPY'],
    ['OANDA:XAGUSD', 'Silver', 'XAG/USD'],
    ['OANDA:XPTUSD', 'Platinum', 'XPT/USD'],
    ['TVC:DXY', 'US Dollar Index', 'DXY'],
    ['FOREXCOM:NSXUSD', 'Nasdaq 100', 'NASDAQ 100'],
    ['FOREXCOM:DJI', 'Dow Jones', 'DOW 30'],
    ['TVC:UKOIL', 'Brent Oil', 'BRENT'],
    ['NASDAQ:AAPL', 'Apple', 'AAPL'],
    ['NASDAQ:NVDA', 'Nvidia', 'NVDA'],
    ['NASDAQ:MSFT', 'Microsoft', 'MSFT'],
    ['NASDAQ:TSLA', 'Tesla', 'TSLA'],
    ['NASDAQ:AMZN', 'Amazon', 'AMZN'],
    ['NASDAQ:GOOGL', 'Alphabet (Google)', 'GOOGL'],
    ['BITSTAMP:ETHUSD', 'Ethereum', 'ETH/USD']
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
